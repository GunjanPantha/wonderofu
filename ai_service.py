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
        self.model = "mistral-7b-instruct-v0.3"
        
    def generate_response(self, user_input, game_state):
        """Generate AI response that actively opposes player escape attempts"""
        
        # Build the game context for the AI
        system_prompt = self._build_system_prompt(game_state)
        user_prompt = self._build_user_prompt(user_input, game_state)
        
        try:
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
                    "temperature": 0.8,
                    "max_tokens": 200,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            if response.status_code == 200:
                ai_response = response.json()
                content = ai_response['choices'][0]['message']['content'].strip()
                return self._post_process_response(content, game_state)
            else:
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
- Keep responses under 150 words
- Be atmospheric and slightly ominous
- Show the forest actively responding to player actions
- Include sensory details (sounds, smells, textures)
- End with the current situation, not obvious next steps"""

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
        """Fallback responses when AI is unavailable"""
        
        fallbacks = [
            "The forest whispers something unintelligible as your action seems to trigger an unexpected reaction. The trees lean closer, blocking more light.",
            "A strange mist rolls in as you attempt your action. Everything becomes disorienting and you find yourself back where you started.",
            "The ground beneath you shifts subtly. When you look around, the landmarks you remembered are no longer where they should be.",
            "An eerie silence falls over the forest. Your action seems to have awakened something that watches you from the shadows.",
            "The wind picks up, carrying with it the scent of something ancient and powerful. Your path forward becomes unclear."
        ]
        
        return random.choice(fallbacks)

# Initialize the AI service
mistral_ai = MistralAI()
