const textElement = document.getElementById('typewriter-text');
const textToType = "You wake up in a dark forest.";
let i = 0;

function typeWriter() {
  if (i < textToType.length) {
    textElement.innerHTML += textToType.charAt(i);
    i++;
    setTimeout(typeWriter, 100); 
  }
}

// Django form handling with game state
document.addEventListener('DOMContentLoaded', () => {
  console.log('JavaScript loaded successfully');
  setTimeout(typeWriter, 1000);
  
  const form = document.getElementById('game-form');
  const userInput = document.getElementById('user-input');
  const gameResponse = document.getElementById('game-response');
  
  console.log('Form found:', form);
  console.log('Input found:', userInput);
  
  // Create game UI elements
  createGameUI();
  
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); // Prevent default form submission
      console.log('Form submitted');
      
      const inputValue = userInput.value.trim();
      console.log('Input value:', inputValue);
      
      if (!inputValue) {
        console.log('Empty input, returning');
        return;
      }
      
      // Disable input during processing
      userInput.disabled = true;
      
      try {
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const formData = new FormData();
        formData.append('user_input', inputValue);
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        console.log('Sending request to /process-input/');
        
        const response = await fetch('/process-input/', {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          }
        });
        
        console.log('Response received:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('Response data:', data);
          
          // Display the response
          displayGameResponse(data.response, inputValue);
          
          // Update game state UI
          updateGameStateUI(data);
          
          // Check for game over
          if (data.game_over) {
            handleGameOver(data.victory);
          }
          
          // Clear input
          userInput.value = '';
          
        } else {
          console.error('Server error:', response.status);
          displayGameResponse('Error connecting to the game server. Try again.', inputValue);
        }
      } catch (error) {
        console.error('Request failed:', error);
        displayGameResponse('Connection error. The forest\'s influence may be interfering...', inputValue);
      } finally {
        userInput.disabled = false;
        userInput.focus();
      }
    });
  }
  
  // Handle Enter key directly without form submission event
  if (userInput) {
    userInput.addEventListener('keypress', async (e) => {
      if (e.key === 'Enter' && !userInput.disabled) {
        e.preventDefault();
        
        // Manually trigger the same logic as form submit
        const inputValue = userInput.value.trim();
        console.log('Enter pressed, input value:', inputValue);
        
        if (!inputValue) {
          console.log('Empty input, returning');
          return;
        }
        
        // Disable input during processing
        userInput.disabled = true;
        
        try {
          // Get CSRF token
          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
          
          const formData = new FormData();
          formData.append('user_input', inputValue);
          formData.append('csrfmiddlewaretoken', csrfToken);
          
          console.log('Sending request to /process-input/ (from Enter key)');
          
          const response = await fetch('/process-input/', {
            method: 'POST',
            body: formData,
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
            }
          });
          
          console.log('Response received:', response.status);
          
          if (response.ok) {
            const data = await response.json();
            console.log('Response data:', data);
            
            // Display the response
            displayGameResponse(data.response, inputValue);
            
            // Update game state UI
            updateGameStateUI(data);
            
            // Check for game over
            if (data.game_over) {
              handleGameOver(data.victory);
            }
            
            // Clear input
            userInput.value = '';
            
          } else {
            console.error('Server error:', response.status);
            displayGameResponse('Error connecting to the game server. Try again.', inputValue);
          }
        } catch (error) {
          console.error('Request failed:', error);
          displayGameResponse('Connection error. The forest\'s influence may be interfering...', inputValue);
        } finally {
          userInput.disabled = false;
          userInput.focus();
        }
      }
    });
  }
});

function createGameUI() {
  // Create game status container
  const gameStatus = document.createElement('div');
  gameStatus.id = 'game-status';
  gameStatus.className = 'mb-4 p-3 border border-green-400 text-sm';
  gameStatus.innerHTML = `
    <div class="flex justify-between items-center">
      <span>Escape Attempts: <span id="escape-count">0</span>/10</span>
      <span>Items: <span id="item-list">None</span></span>
    </div>
  `;
  
  // Insert before the input form
  const inputContainer = document.querySelector('.mt-8');
  inputContainer.parentNode.insertBefore(gameStatus, inputContainer);
  
  // Create game history container
  const gameHistory = document.createElement('div');
  gameHistory.id = 'game-history';
  gameHistory.className = 'mt-6 max-h-96 overflow-y-auto';
  
  // Insert after the input form
  inputContainer.parentNode.insertBefore(gameHistory, inputContainer.nextSibling);
}

function displayGameResponse(response, userCommand) {
  const gameHistory = document.getElementById('game-history');
  
  // Create command entry
  const commandEntry = document.createElement('div');
  commandEntry.className = 'mb-4 p-3 border-l-2 border-green-400';
  commandEntry.innerHTML = `
    <div class="text-green-300 text-sm mb-1">→ ${userCommand}</div>
    <div class="text-green-400">${response}</div>
  `;
  
  gameHistory.appendChild(commandEntry);
  
  // Scroll to bottom
  gameHistory.scrollTop = gameHistory.scrollHeight;
  
  // Limit history entries
  const entries = gameHistory.children;
  if (entries.length > 20) {
    gameHistory.removeChild(entries[0]);
  }
}

function updateGameStateUI(data) {
  // Update escape attempts
  const escapeCount = document.getElementById('escape-count');
  if (escapeCount && data.escape_attempts !== undefined) {
    escapeCount.textContent = data.escape_attempts;
    
    // Change color based on attempts
    const statusContainer = document.getElementById('game-status');
    if (data.escape_attempts >= 8) {
      statusContainer.className = statusContainer.className.replace('border-green-400', 'border-red-400');
    } else if (data.escape_attempts >= 5) {
      statusContainer.className = statusContainer.className.replace('border-green-400', 'border-yellow-400');
    }
  }
  
  // Update items
  const itemList = document.getElementById('item-list');
  if (itemList && data.items) {
    itemList.textContent = data.items.length > 0 ? data.items.join(', ') : 'None';
  }
}

function handleGameOver(victory) {
  const userInput = document.getElementById('user-input');
  userInput.disabled = true;
  userInput.placeholder = victory ? "You have escaped! Congratulations!" : "Game Over - The forest has claimed you.";
  
  // Create restart button
  const restartButton = document.createElement('button');
  restartButton.textContent = 'Start New Game';
  restartButton.className = 'mt-4 px-4 py-2 bg-green-600 text-white border border-green-400 hover:bg-green-700';
  restartButton.onclick = () => window.location.reload();
  
  userInput.parentNode.appendChild(restartButton);
}
