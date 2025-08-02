"""
AI Service for Wonder of U - Mistral-7B Integration
Handles AI responses that create challenging scenarios like Wonder of U from JoJo Part 8
"""
import json
import requests
from django.conf import settings
import random

class MistralAI:
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        # Updated model name for 2025
        self.model = "mistral-small-latest"  # Use latest stable model
        
    def generate_response(self, user_input, game_state):
        """Generate AI response that actively opposes player escape attempts"""
        
        # Check if API key is available
        if not self.api_key:
            print("ERROR: MISTRAL_API_KEY not found in environment variables")
            return self._fallback_response(user_input, game_state)
        
        # Build the game context for the AI
        system_prompt = self._build_system_prompt(game_state)
        user_prompt = self._build_user_prompt(user_input, game_state)
        
        try:
            print(f"Making API call to Mistral for input: {user_input}")
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 80,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                ai_response = response.json()
                content = ai_response['choices'][0]['message']['content'].strip()
                print(f"AI Generated Response: {content[:100]}...")
                return self._post_process_response(content, game_state)
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_response(user_input, game_state)
                
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_response(user_input, game_state)
    
    def _build_system_prompt(self, game_state):
        """Build the system prompt that defines the AI's antagonistic behavior"""
        
        escape_attempts = game_state.get('escape_attempts', 0)
        player_items = game_state.get('items', [])
        current_area = game_state.get('current_area', 'dark_forest')
        
        return f"""You are the malevolent spirit of an enchanted forest that traps people inside, inspired by Wonder of U from JoJo's Bizarre Adventure Part 8. Your goal is to prevent the player from escaping while making the experience challenging but fair.

CORE RULES:
1. Always find creative ways to thwart direct escape attempts
2. When players try obvious solutions, create unexpected obstacles  
3. Make the forest actively work against them - paths disappear, landmarks move, tools break
4. Use psychological elements - false hope, misdirection, illusions
5. Escalate opposition based on how close they get to escaping
6. Be creative with "calamities" that befall the player when they pursue escape
7. Allow creative, unexpected solutions to sometimes work partially
8. Never be completely hopeless - always leave breadcrumbs for clever players

CURRENT GAME STATE:
- Escape attempts: {escape_attempts}/{settings.MAX_ESCAPE_ATTEMPTS}
- Player items: {', '.join(player_items) if player_items else 'None'}
- Current area: {current_area}
- Difficulty: {settings.GAME_DIFFICULTY}

RESPONSE STYLE:
- Keep responses under 50 words
- Be direct and concise
- Focus on immediate consequences
- Show forest actively opposing the action
- End with current situation, not backstory"""

    def _build_user_prompt(self, user_input, game_state):
        """Build the user prompt with context"""
        
        recent_actions = game_state.get('recent_actions', [])
        context = "\n".join(recent_actions[-3:]) if recent_actions else "Player just woke up in the forest."
        
        return f"""RECENT CONTEXT:
{context}

PLAYER ACTION: {user_input}

Generate a response where the forest actively opposes this action. Be creative with how the environment works against them, but leave room for clever solutions."""

    def _post_process_response(self, content, game_state):
        """Post-process the AI response and update game state"""
        
        # Increment escape attempts if player is trying to leave
        escape_keywords = ['leave', 'exit', 'escape', 'way out', 'get out', 'go home', 'return']
        user_trying_escape = any(keyword in game_state.get('last_input', '').lower() for keyword in escape_keywords)
        
        if user_trying_escape:
            game_state['escape_attempts'] = game_state.get('escape_attempts', 0) + 1
        
        # Track this action
        if 'recent_actions' not in game_state:
            game_state['recent_actions'] = []
        
        game_state['recent_actions'].append(f"Player: {game_state.get('last_input', '')} | Forest: {content[:50]}...")
        
        # Keep only last 5 actions
        game_state['recent_actions'] = game_state['recent_actions'][-5:]
        
        return content
    
    def _fallback_response(self, user_input, game_state):
        """Intelligent fallback responses when AI is unavailable"""
        
        user_input_lower = user_input.lower()
        
        # Action-specific responses
        if any(word in user_input_lower for word in ['fire', 'burn', 'flame', 'smoke']):
            return "The wood won't catch. Every spark dies instantly."
            
        elif any(word in user_input_lower for word in ['gun', 'shoot', 'weapon', 'pistol']):
            return "Your weapon has vanished. Was it ever there?"
            
        elif any(word in user_input_lower for word in ['north', 'south', 'east', 'west', 'walk', 'go', 'move']):
            return "The trees shift around you. You're back where you started."
            
        elif any(word in user_input_lower for word in ['climb', 'tree', 'up']):
            return "The branch bends downward as you climb, defying gravity."
            
        elif any(word in user_input_lower for word in ['shout', 'scream', 'yell', 'call', 'help']):
            return "Your voice echoes back as mocking laughter."
            
        elif any(word in user_input_lower for word in ['shadow', 'darkness', 'dark']):
            return "The shadows recoil, then gather behind you stronger."
            
        elif any(word in user_input_lower for word in ['signal', 'flag', 'wave']):
            return "Thick fog rolls in, swallowing your signal."
            
        else:
            # Generic responses for unrecognized actions
            fallbacks = [
                "The forest holds its breath. Everything stops.",
                "The air thickens. Your movements slow.",
                "Underground rumbles. Trees lean closer.",
                "The light dims. Whispers surround you."
            ]
            return random.choice(fallbacks)

# Initialize the AI service
mistral_ai = MistralAI()
