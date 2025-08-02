# 🌐 Deploy Wonder of U - AI Text Adventure Game

This guide will help you deploy your AI-powered text adventure game online so everyone can play!

## 🚀 Hosting Options (Ranked by Ease)

### 1. **Railway** ⭐ (Recommended for Beginners)
- **Free Tier**: $5 credit monthly (enough for small games)
- **Setup Time**: 5 minutes
- **Auto-deploys** from GitHub

**Steps:**
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub account
3. Upload your game folder to a GitHub repository
4. Click "Deploy from GitHub" on Railway
5. Add environment variables:
   - `SECRET_KEY`: Generate at [djecrety.ir](https://djecrety.ir)
   - `MISTRAL_API_KEY`: Your Mistral API key
   - `DEBUG`: False
6. Deploy! 🎉

### 2. **Render** 
- **Free Tier**: 750 hours/month
- **Setup Time**: 10 minutes
- **Good performance**

**Steps:**
1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Choose "Web Service"
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn wsgi:application`
6. Add environment variables (same as Railway)

### 3. **Heroku**
- **Free Tier**: Ended (paid plans start at $7/month)
- **Setup Time**: 15 minutes
- **Very reliable**

**Steps:**
1. Create account at [heroku.com](https://heroku.com)
2. Install Heroku CLI
3. Run commands:
   ```bash
   heroku create your-game-name
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set MISTRAL_API_KEY=your-api-key
   heroku config:set DEBUG=False
   git push heroku main
   ```

## 📋 Pre-Deployment Checklist

✅ **Files Ready:**
- `requirements.txt` (updated with gunicorn, whitenoise)
- `Procfile` (for Heroku)
- `railway.json` (for Railway)
- `.env.example` (environment variables template)

✅ **Environment Variables:**
- `SECRET_KEY`: Generate a new one for production
- `MISTRAL_API_KEY`: Your Mistral AI API key
- `DEBUG`: Set to False for production

✅ **Settings Updated:**
- Production-ready `settings.py`
- Static files configuration
- Allowed hosts for deployment

## 🔑 Getting Your Mistral API Key

1. Go to [console.mistral.ai](https://console.mistral.ai)
2. Create account or sign in
3. Navigate to "API Keys"
4. Create new API key
5. Copy the key (starts with `sk-`)

## 🔒 Security Notes

⚠️ **Important:**
- Never commit your `.env` file to GitHub
- Always use environment variables in production
- Generate a new SECRET_KEY for production
- Set DEBUG=False in production

## 🌍 Custom Domain (Optional)

Once deployed, you can add a custom domain:
- **Railway**: Project Settings → Domains
- **Render**: Settings → Custom Domains  
- **Heroku**: Settings → Domains

## 🎮 Testing Your Deployment

After deployment:
1. Visit your game URL
2. Test basic functionality:
   - Page loads correctly
   - Input form works
   - AI responses appear
   - No console errors
3. Share with friends! 🎉

## 🔧 Troubleshooting

**Common Issues:**

1. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT settings

2. **AI not responding:**
   - Verify MISTRAL_API_KEY is set correctly
   - Check API quota/billing

3. **Database errors:**
   - Run migrations: `python manage.py migrate`

4. **ALLOWED_HOSTS error:**
   - Add your domain to ALLOWED_HOSTS in settings.py

5. **WSGI Application error (Railway/Nixpacks):**
   - Ensure `wsgi.py` file exists
   - Check WSGI_APPLICATION setting in settings.py
   - Use `gunicorn wsgi:application` in start command

## 🆘 Need Help?

If you encounter issues:
1. Check deployment logs in your hosting platform
2. Verify all environment variables are set
3. Test locally first with `DEBUG=False`

---

## 🎯 Quick Start with Railway (Easiest)

1. **Create GitHub repo** with your game files
2. **Sign up at railway.app**
3. **Click "Deploy from GitHub"**
4. **Add environment variables:**
   ```
   SECRET_KEY=your-generated-secret-key
   MISTRAL_API_KEY=your-mistral-api-key  
   DEBUG=False
   ```
5. **Deploy and share your game URL!** 🚀

Your game will be live at: `https://your-app-name.up.railway.app`
