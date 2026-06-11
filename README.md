# 🎬 YouTube Shorts + Facebook Auto Uploader Bot

A complete automation system that generates **Comedy + Motivational** YouTube Shorts and Facebook videos daily using **FREE AI models**.

## 🎯 Features

✅ **AI-Powered Content Generation** - Uses free Groq API (Mixtral 8x7b)  
✅ **Comedy + Motivational Mix** - Randomly generates engaging content  
✅ **Automatic Video Creation** - Creates 15-60 second shorts  
✅ **YouTube Auto-Upload** - Uploads to your YouTube channel  
✅ **Facebook Auto-Upload** - Posts to your Facebook page  
✅ **Daily Scheduling** - Runs automatically at set times  
✅ **100% FREE** - No premium tools needed!

---

## 📋 Requirements

- Python 3.8+
- YouTube Channel
- Facebook Page
- GitHub Account (for deployment)

---

## 🚀 Quick Start

### Step 1: Get Free API Keys

#### A. Groq API (For AI Content)
1. Go to https://console.groq.com/keys
2. Sign up (free)
3. Create an API key
4. Copy the key

#### B. YouTube API
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as JSON (save as `client_secrets.json`)

#### C. Facebook API
1. Go to https://developers.facebook.com/
2. Create an app
3. Get Page Access Token
4. Copy your Page ID

---

### Step 2: Setup Your Repository

```bash
# Clone the repo
git clone https://github.com/jata4565-byte/YouTube-Shorts-Bot-.git
cd YouTube-Shorts-Bot-

# Create Python environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3: Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```
GROQ_API_KEY=your_groq_key_here
FACEBOOK_ACCESS_TOKEN=your_fb_token
FACEBOOK_PAGE_ID=your_fb_page_id
ENABLE_YOUTUBE=true
ENABLE_FACEBOOK=true
```

3. Place `client_secrets.json` in the project root

---

### Step 4: Run the Bot

**Test Run (Generate 1 video):**
```bash
python main.py --once
```

**Auto-Scheduled (Runs daily at 9 AM):**
```bash
python main.py
```

---

## 📁 Project Structure

```
YouTube-Shorts-Bot-/
├── main.py                      # Main bot orchestrator
├── ai_content_generator.py      # AI content creation
├── video_creator.py             # Video generation
├── youtube_uploader.py          # YouTube API integration
├── facebook_uploader.py         # Facebook API integration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── client_secrets.json          # YouTube API credentials (add this)
├── token.pickle                 # Auto-generated YouTube token
└── generated_videos/            # Output videos folder
```

---

## 🔧 How It Works

### Content Generation Process

1. **AI Content Creation**
   - Groq API generates comedy script
   - OR generates motivational content
   - Randomly alternates between both

2. **Video Creation**
   - Creates 4-second video with text overlay
   - Beautiful gradient background
   - White text on dark background

3. **Automatic Uploads**
   - YouTube: Posts with hashtags and description
   - Facebook: Posts with description and links

4. **Scheduling**
   - Runs automatically every day at 9 AM
   - Can be customized in `.env` file

---

## 📊 Example Content Generated

### Comedy Script:
```
Scene: Office desk
Employee 1: "Bhai, meeting mein laptop on kar?"
Employee 2: "Haan, but camera off hai!"
[Everyone laughs]
```

### Motivational Script:
```
Scene: Person climbing mountain
Voiceover: "Har mushkil se sikhne ka mauka hai"
Message: "Apne aap par vishwas rakho, safalta zaroor aayegi"
```

---

## 🎮 Commands

```bash
# Run once (for testing)
python main.py --once

# Run with auto-scheduler
python main.py

# Test content generation only
python ai_content_generator.py

# Test video creation only
python video_creator.py

# Test YouTube setup
python youtube_uploader.py

# Test Facebook setup
python facebook_uploader.py
```

---

## 🌐 Deployment (Optional)

### Deploy on GitHub Actions (FREE!)

1. Push code to GitHub
2. Go to your repo → Settings → Secrets
3. Add your API keys as secrets
4. Create `.github/workflows/bot.yml`:

```yaml
name: Daily Video Upload

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run bot
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          FACEBOOK_ACCESS_TOKEN: ${{ secrets.FACEBOOK_ACCESS_TOKEN }}
          FACEBOOK_PAGE_ID: ${{ secrets.FACEBOOK_PAGE_ID }}
        run: python main.py --once
```

---

## ⚠️ Troubleshooting

### "API Key not found"
- Make sure `.env` file exists and has correct keys
- Check spelling of variable names

### "Video upload failed"
- Check YouTube/Facebook credentials
- Ensure channel/page exists
- Try uploading manually first to test credentials

### "Video creation slow"
- First run downloads libraries
- Subsequent runs are faster
- Use `--once` to test before scheduling

### MoviePy errors
- Install FFmpeg: `choco install ffmpeg` (Windows) or `brew install ffmpeg` (Mac)
- Ubuntu: `sudo apt-get install ffmpeg`

---

## 🎨 Customization

### Change Upload Time
Edit `.env`:
```
UPLOAD_SCHEDULE=0 18 * * *  # 6 PM instead
```

### Change Video Duration
Edit `video_creator.py`:
```python
txt_clip = TextClip(...).set_duration(6)  # 6 seconds instead of 4
```

### Add Custom Content Types
Edit `ai_content_generator.py` and add new methods:
```python
def generate_trending_script(self):
    prompt = "Your custom prompt here"
    # ... generate content
```

---

## 📈 Performance Tips

1. **Use Free Tier Limits:**
   - Groq: 14K requests/day (free)
   - YouTube: 10k units/day (free)
   - Facebook: Check rate limits

2. **Optimize Video Creation:**
   - Use simple backgrounds (faster)
   - Reduce video length
   - Use lower resolution if needed

3. **Monitor Usage:**
   - Check API dashboards weekly
   - Set up alerts for quota warnings

---

## 📞 Support

If you face issues:

1. Check error messages carefully
2. Review `.env` configuration
3. Test APIs individually
4. Check API quotas/limits
5. See Troubleshooting section above

---

## 📝 License

Free to use and modify for personal projects.

---

## 🎯 Next Steps

1. ✅ Get API keys (Groq, YouTube, Facebook)
2. ✅ Clone this repository
3. ✅ Setup `.env` file
4. ✅ Run `python main.py --once`
5. ✅ Check generated video
6. ✅ Schedule daily uploads!

---

## 🌟 Show Your Support

If this bot helps you grow your channel:
- ⭐ Star this repo
- 📢 Share with friends
- 💬 Leave feedback
- 🔗 Follow on YouTube: Anil Jaat

---

**Happy Uploading! 🚀**

_Last updated: 2024_  
_Bot by: Anil Jaat (@jata4565-byte)_