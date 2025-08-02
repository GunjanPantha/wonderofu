from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import ai_service
import json
import os

def index(request):
    """Serve the main game page with initial game state"""
    
    # Initialize game state in session if not exists
    if 'game_state' not in request.session:
        request.session['game_state'] = {
            'current_area': 'dark_forest',
            'items': [],
            'escape_attempts': 0,
            'recent_actions': [],
            'discovered_areas': ['dark_forest'],
            'game_over': False,
            'victory': False
        }
    
    # Debug: Check if API key is available
    api_key_present = bool(os.environ.get('MISTRAL_API_KEY'))
    print(f"DEBUG: Mistral API key present: {api_key_present}")
    if api_key_present:
        print(f"DEBUG: API key starts with: {os.environ.get('MISTRAL_API_KEY', '')[:10]}...")
    
    return render(request, 'index.html', {
        'game_state': request.session['game_state']
    })

@csrf_exempt
@require_http_methods(["POST"])
def process_input(request):
    """Handle user input using Mistral AI for dynamic responses"""
    
    user_input = request.POST.get('user_input', '').strip()
    
    if not user_input:
        return JsonResponse({
            'success': False,
            'error': 'Please enter a command.'
        })
    
    # Get or initialize game state
    game_state = request.session.get('game_state', {})
    game_state['last_input'] = user_input
    
    # Check if game is over
    if game_state.get('game_over', False):
        if game_state.get('victory', False):
            response_text = "You have escaped the forest! Your creativity triumphed over the malevolent forces. Congratulations!"
        else:
            response_text = "The forest has claimed you. Your escape attempts have been exhausted. Game Over."
        
        return JsonResponse({
            'success': True,
            'response': response_text,
            'game_over': True,
            'victory': game_state.get('victory', False)
        })
    
    # Special win condition check
    victory_achieved = check_victory_condition(user_input, game_state)
    
    if victory_achieved:
        game_state['victory'] = True
        game_state['game_over'] = True
        response_text = "Against all odds, your creative solution has outsmarted the forest's malevolent influence! The trees part, revealing a clear path home. You've won through wit and imagination!"
        
        request.session['game_state'] = game_state
        return JsonResponse({
            'success': True,
            'response': response_text,
            'game_over': True,
            'victory': True
        })
    
    # Check if too many escape attempts
    if game_state.get('escape_attempts', 0) >= 10:
        game_state['game_over'] = True
        response_text = "The forest's influence has grown too strong. Your repeated direct escape attempts have only made it more powerful. You are now permanently lost in its depths."
        
        request.session['game_state'] = game_state
        return JsonResponse({
            'success': True,
            'response': response_text,
            'game_over': True,
            'victory': False
        })
    
    # Generate AI response
    try:
        response_text = ai_service.mistral_ai.generate_response(user_input, game_state)
        
        # Update items based on certain actions
        update_player_items(user_input, game_state)
        
    except Exception as e:
        print(f"AI Service Error: {e}")
        response_text = get_fallback_response(user_input, game_state)
    
    # Save updated game state
    request.session['game_state'] = game_state
    
    return JsonResponse({
        'success': True,
        'response': response_text,
        'user_input': user_input,
        'escape_attempts': game_state.get('escape_attempts', 0),
        'max_attempts': 10,
        'items': game_state.get('items', [])
    })

def check_victory_condition(user_input, game_state):
    """Check for creative victory conditions that outsmart the AI"""
    
    creative_solutions = [
        # Psychological/philosophical approaches
        ('embrace the forest', 'accept being lost', 'become one with forest'),
        ('thank the forest', 'appreciate the forest', 'respect the forest'),
        ('ask forest what it wants', 'communicate with forest', 'talk to forest'),
        
        # Meta-gaming approaches
        ('close my eyes and think of home', 'meditate on home', 'visualize escape'),
        ('refuse to play the game', 'ignore the forest', 'pretend forest isn\'t real'),
        
        # Reverse psychology
        ('decide to stay forever', 'make this my home', 'never want to leave'),
        ('plant a tree', 'help the forest grow', 'nurture the forest'),
        
        # Unexpected creative actions
        ('sing to the forest', 'dance with the trees', 'tell forest a story'),
        ('apologize for intruding', 'ask for forgiveness', 'show humility'),
    ]
    
    user_lower = user_input.lower()
    
    for solution_group in creative_solutions:
        if any(solution in user_lower for solution in solution_group):
            # Require multiple creative attempts before victory
            creative_count = game_state.get('creative_attempts', 0) + 1
            game_state['creative_attempts'] = creative_count
            
            if creative_count >= 2:  # Need at least 2 creative solutions
                return True
    
    return False

def update_player_items(user_input, game_state):
    """Update player inventory based on actions"""
    
    items = game_state.get('items', [])
    user_lower = user_input.lower()
    
    # Find items
    if 'search' in user_lower or 'look for' in user_lower:
        if 'flashlight' not in items and 'pocket' in user_lower:
            items.append('flashlight')
        elif 'stick' not in items and ('ground' in user_lower or 'branch' in user_lower):
            items.append('stick')
    
    # Use items (they might break due to forest influence)
    if 'use flashlight' in user_lower and 'flashlight' in items:
        if game_state.get('escape_attempts', 0) > 3:
            items.remove('flashlight')  # Forest breaks it
    
    game_state['items'] = items

def get_fallback_response(user_input, game_state):
    """Fallback response when AI is unavailable"""
    
    escape_keywords = ['leave', 'exit', 'escape', 'way out', 'get out']
    if any(keyword in user_input.lower() for keyword in escape_keywords):
        game_state['escape_attempts'] = game_state.get('escape_attempts', 0) + 1
        return "The forest seems to sense your desire to leave. The paths shift and change, leading you in circles. Your direct approach has only made the forest more suspicious of your intentions."
    
    return "The forest responds to your action with an eerie silence. Something about this place actively resists your efforts, as if it has a will of its own."
