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
                    "temperature": 0.8,
                    "max_tokens": 200,
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
        """Intelligent fallback responses when AI is unavailable"""
        
        user_input_lower = user_input.lower()
        
        # Action-specific responses
        if any(word in user_input_lower for word in ['fire', 'burn', 'flame', 'smoke']):
            return "You try to start a fire, but the wood refuses to catch. Every spark dies as soon as it forms, as if the forest itself is snuffing out your attempts. The dampness seems to follow you wherever you go."
            
        elif any(word in user_input_lower for word in ['gun', 'shoot', 'weapon', 'pistol']):
            return "You reach for your weapon, but your hand passes through empty air. Looking down, you realize your gun has vanished - or perhaps it was never there at all. The forest plays tricks on memory and reality."
            
        elif any(word in user_input_lower for word in ['north', 'south', 'east', 'west', 'walk', 'go', 'move']):
            return "You start walking in that direction, but the trees seem to shift around you. After what feels like progress, you notice the same gnarled oak you passed minutes ago. The forest has quietly rearranged itself."
            
        elif any(word in user_input_lower for word in ['climb', 'tree', 'up']):
            return "The tree branch creaks ominously under your weight. As you climb higher, the branch begins to bend back toward the ground, as if gravity itself is working against your escape."
            
        elif any(word in user_input_lower for word in ['shout', 'scream', 'yell', 'call', 'help']):
            return "Your voice echoes through the trees, but instead of your cry for help, you hear only mocking laughter that seems to come from the forest itself. The sound grows louder until it's all around you."
            
        elif any(word in user_input_lower for word in ['shadow', 'darkness', 'dark']):
            return "The shadows seem to recoil from your attention, but they quickly gather behind you. You can feel their presence growing stronger, as if confronting them has only made them bolder."
            
        elif any(word in user_input_lower for word in ['signal', 'flag', 'wave']):
            return "You create your signal, but as you do, a thick fog rolls in from nowhere, obscuring everything beyond arm's reach. Your signal disappears into the mist as if it never existed."
            
        else:
            # Generic responses for unrecognized actions
            fallbacks = [
                "The forest responds to your action with unnatural stillness. Even the wind stops, as if the woods are holding their breath and waiting for something.",
                "As you attempt this, the very air seems to thicken around you. Your movements become sluggish, as if you're moving through invisible molasses.",
                "The moment you try this, a low rumble emanates from deep underground. The trees lean inward slightly, their branches reaching toward you like grasping fingers.",
                "Your action triggers a subtle shift in the forest's mood. The light filtering through the canopy dims noticeably, and you swear you can hear whispered conversations in a language you don't recognize."
            ]
            return random.choice(fallbacks)

# Initialize the AI service
mistral_ai = MistralAI()
