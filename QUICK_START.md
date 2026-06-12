# Quick Start Guide - YouTube Shorts Bot

## 5 Minutes Setup! ⚡

### Step 1: Get API Keys (5 min)

**Groq API (FREE AI):**
1. https://console.groq.com/keys
2. Sign up
3. Copy API Key
4. Save it

**YouTube API:**
1. https://console.cloud.google.com/
2. Create new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 Desktop credentials
5. Download as JSON (save as `client_secrets.json`)

### Step 2: Setup Bot (5 min)

```bash
# Clone repo
git clone https://github.com/jata4565-byte/YouTube-Shorts-Bot-.git
cd YouTube-Shorts-Bot-

# Create Python environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install libraries
pip install -r requirements.txt
```

### Step 3: Configure (2 min)

Create `.env` file with:
```
GROQ_API_KEY=your_key_here
ENABLE_YOUTUBE=true
ENABLE_FACEBOOK=false
UPLOAD_TIME=09:00
```

Put `client_secrets.json` in project folder

### Step 4: Test (1 min)

```bash
python main_improved.py --once
```

### Step 5: Daily Automatic

```bash
python main_improved.py
```

OR use GitHub Actions (see SETUP_GUIDE_HINDI.md)

---

**Done! Your bot is ready!** 🚀

Check logs in: `bot_logs/`
Generated videos in: `generated_videos/`

For detailed guide, see: **SETUP_GUIDE_HINDI.md**