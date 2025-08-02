# 🎮 Quick Start Guide - Wonder of U

## ✅ Setup Complete!

I've set up your AI-powered text adventure game. Here's how to run it:

### � First Time Setup (Database)
**IMPORTANT**: Run this once before playing:
1. **Double-click** `setup_database.bat` in your Wonder of U folder
2. This creates the necessary database tables
3. You only need to do this once!

### �🚀 Method 1: Using the Batch File
1. **Double-click** `start_game.bat` in your Wonder of U folder
2. This will automatically start the Django server
3. Open your browser to: `http://127.0.0.1:8000/`

### 🚀 Method 2: Using PowerShell
1. **Right-click** `start_game.ps1` and select "Run with PowerShell"
2. Open your browser to: `http://127.0.0.1:8000/`

### 🚀 Method 3: Manual Command
1. Open **Command Prompt** or **PowerShell**
2. Navigate to your game folder:
   ```
   cd "C:\Users\gunja\Documents\Wonder of U"
   ```
3. Run database setup (first time only):
   ```
   ".venv\Scripts\python.exe" manage.py migrate
   ```
4. Run the server:
   ```
   ".venv\Scripts\python.exe" manage.py runserver
   ```
5. Open your browser to: `http://127.0.0.1:8000/`

## 🔧 Your Setup Details

### ✅ Installed Packages:
- ✅ Django 4.2+ (Web framework)
- ✅ Mistral AI SDK (AI integration)
- ✅ Python-dotenv (Environment variables)
- ✅ Requests (HTTP requests)

### ✅ Your Mistral API Key:
- ✅ Configured in `.env` file
- ✅ Ready for AI-powered responses

### ✅ Game Features:
- 🧠 **AI-Powered Responses**: Mistral-7B creates dynamic challenges
- 🎯 **Wonder of U Mechanics**: Forest actively opposes direct escape attempts
- 🎨 **Creative Victory System**: Win through unexpected solutions
- 📊 **Game State Tracking**: Inventory, escape attempts, progress
- 🎭 **Multiple Endings**: Victory through creativity or defeat through persistence

## 🎮 How to Play

### Starting Commands (to get familiar):
- `look around`
- `check pockets` 
- `search for something`

### ❌ DON'T Try These (AI will oppose them):
- `escape the forest`
- `find the exit`
- `go home`
- `call for rescue`

### ✅ DO Try Creative Approaches:
- `thank the forest for its beauty`
- `ask the forest what it wants`
- `embrace being lost`
- `sing to the trees`
- `apologize for intruding`
- `plant a seed`

## 🏆 Victory Tips
1. **Think Outside the Box**: Direct approaches will fail
2. **Be Respectful**: The forest responds to humility
3. **Use Philosophy**: Emotional and philosophical approaches work
4. **Accept Paradox**: Sometimes giving up is winning
5. **Be Creative**: The AI rewards unexpected solutions

## 🆘 Troubleshooting

### If the server won't start:
1. Make sure you're in the correct directory
2. Check that Python 3.8+ is installed
3. Try running: `".venv\Scripts\python.exe" -m django --version`

### If AI responses aren't working:
1. Check your Mistral API key in `.env`
2. Verify internet connection
3. The game will use fallback responses if AI fails

---

**Ready to escape the malevolent forest? Your creativity is your only weapon! 🌲✨**
