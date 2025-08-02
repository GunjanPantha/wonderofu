# Wonder of U - AI-Powered Text Adventure Setup

## 🌲 About the Game
An AI-powered text adventure where you wake up in a malevolent forest that actively works against your escape attempts, inspired by Wonder of U from JoJo's Bizarre Adventure Part 8. The Mistral-7B-Instruct AI creates dynamic, challenging scenarios that adapt to your actions.

## 🎯 Game Mechanics
- **Escape Attempts**: Limited to 10 direct escape attempts before game over
- **Creative Solutions**: Think outside the box to outsmart the AI
- **Dynamic AI**: Mistral-7B creates unique responses that actively oppose you
- **Wonder of U Style**: The forest will create "calamities" when you try obvious solutions
- **Victory Condition**: Use creativity and unexpected approaches to escape

## 🚀 Setup Instructions

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Get Mistral AI API Key
1. Go to [https://console.mistral.ai/](https://console.mistral.ai/)
2. Create an account and get your API key
3. Add it to your `.env` file:
```
MISTRAL_API_KEY=your_actual_api_key_here
```

### 3. Run the Game
```powershell
python manage.py runserver
```

### 4. Open in Browser
Go to: `http://127.0.0.1:8000/`

## 🎮 How to Play

### Starting the Game
- You wake up in a dark forest
- Type commands to interact with the environment
- Be creative - obvious escape attempts will be thwarted!

### Example Commands
**DON'T try these (the AI will oppose them):**
- "find the exit"
- "escape the forest" 
- "walk home"
- "call for rescue"

**DO try creative approaches:**
- "thank the forest for its beauty"
- "ask the forest what it wants"
- "embrace being lost"
- "sing to the trees"
- "plant a seed"
- "apologize for intruding"

### Game Features
- **Dynamic AI Responses**: Every playthrough is unique
- **Inventory System**: Find and use items (but they may break!)
- **Escalating Difficulty**: The more you resist, the stronger the forest becomes
- **Multiple Endings**: Victory through creativity or defeat through stubbornness

### Victory Tips
1. **Avoid Direct Approaches**: The forest expects you to try to escape
2. **Be Unexpected**: Try philosophical, emotional, or meta approaches
3. **Show Respect**: The forest may respond to humility and appreciation
4. **Think Laterally**: Sometimes the best way out is through acceptance
5. **Use Multiple Creative Attempts**: One creative solution may not be enough

## 🔧 Troubleshooting

### AI Not Working
- Check your Mistral API key in `.env`
- Verify internet connection
- The game will use fallback responses if AI fails

### Django Issues
- Make sure you have Python 3.8+
- Try: `python manage.py migrate` (if needed)
- Check that all dependencies are installed

## 🎨 Game Philosophy
This game is about lateral thinking and creativity over brute force. The AI will actively work against obvious solutions, forcing you to think like the protagonist in a psychological thriller. Victory comes through wit, not persistence.

**Remember**: The forest has a will of its own, and it doesn't want you to leave. Your creativity is your only weapon against its malevolent influence.

Good luck, and may your imagination set you free! 🌲✨
