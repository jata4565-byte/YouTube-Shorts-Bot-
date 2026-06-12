"""
Main Bot - Improved Version
Generates and uploads Comedy + Motivational shorts daily
"""

import os
import sys
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from ai_content_generator import ContentGenerator
from video_creator import VideoCreator
from youtube_uploader_fixed import YouTubeUploader

load_dotenv()

class YouTubeShortsBot:
    def __init__(self):
        print("\n" + "="*60)
        print("🎬 YouTube Shorts Bot Initialized")
        print("="*60)
        
        self.content_generator = ContentGenerator()
        self.video_creator = VideoCreator()
        self.youtube_uploader = YouTubeUploader()
        self.videos_dir = "generated_videos"
        self.logs_dir = "bot_logs"
        
        # Create directories
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Setup logging
        self.log_file = os.path.join(self.logs_dir, f"bot_{datetime.now().strftime('%Y%m%d')}.log")
        self._log("Bot initialized successfully")
        
        # Authenticate
        self._setup_authentication()
    
    def _log(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Error writing to log: {e}")
    
    def _setup_authentication(self):
        """Setup authentication for all platforms"""
        self._log("\n🔐 Setting up authentication...\n")
        
        # YouTube
        if os.getenv("ENABLE_YOUTUBE", "true").lower() == "true":
            if self.youtube_uploader.authenticate():
                channel = self.youtube_uploader.get_channel_info()
                if channel:
                    self._log(f"✅ YouTube: {channel['snippet']['title']}")
                else:
                    self._log("⚠️ Could not fetch YouTube channel info")
            else:
                self._log("⚠️ YouTube authentication failed")
        else:
            self._log("⏭️ YouTube upload disabled")
    
    def generate_and_upload_video(self):
        """Main workflow: Generate -> Create -> Upload"""
        self._log("\n" + "="*60)
        self._log(f"🚀 Starting Video Generation at {datetime.now()}")
        self._log("="*60)
        
        try:
            # Step 1: Generate AI Content
            self._log("\n📝 Step 1: Generating AI Content...")
            
            try:
                content = self.content_generator.generate_mixed_content()
                self._log(f"✨ Type: {content['type']}")
                
                # Truncate script for logging
                script_preview = content['script'][:100].replace("\n", " ")
                self._log(f"📄 Script: {script_preview}...")
                
            except Exception as e:
                self._log(f"❌ Content generation failed: {e}")
                return False
            
            # Generate captions
            try:
                captions = self.content_generator.generate_captions(content['script'])
                captions_preview = captions[:100].replace("\n", " ")
                self._log(f"📢 Captions: {captions_preview}...")
            except Exception as e:
                self._log(f"⚠️ Caption generation failed: {e}")
                captions = "Check out this amazing content! 🎉"
            
            # Step 2: Create Video
            self._log("\n🎬 Step 2: Creating Video...")
            
            try:
                video_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_path = self.video_creator.create_simple_video(
                    content['script'],
                    video_id
                )
                
                if not video_path or not os.path.exists(video_path):
                    self._log("❌ Video creation failed!")
                    return False
                
                file_size = os.path.getsize(video_path) / (1024*1024)
                self._log(f"✅ Video created: {video_path} ({file_size:.2f} MB)")
                
            except Exception as e:
                self._log(f"❌ Video creation error: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # Step 3: Upload to YouTube
            self._log("\n📤 Step 3: Uploading to Platforms...")
            
            try:
                # Prepare metadata
                title = f"{content['type']} - Anil Jaat {datetime.now().strftime('%d.%m.%Y')}"
                description = f"{content['script']}\n\n{captions}\n\n#Shorts #Comedy #Motivation #Hindi #Viral"
                tags = ["shorts", "comedy", "motivation", "hindi", "viral", "funny"]
                
                # Upload to YouTube
                if os.getenv("ENABLE_YOUTUBE", "true").lower() == "true":
                    self._log("\n📺 Uploading to YouTube...")
                    
                    if self.youtube_uploader.upload_video(
                        video_path,
                        title=title,
                        description=description,
                        tags=tags,
                        category="24"  # Shorts category
                    ):
                        self._log("✅ YouTube upload successful!")
                    else:
                        self._log("❌ YouTube upload failed")
                        return False
                
            except Exception as e:
                self._log(f"❌ Upload error: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            self._log("\n" + "="*60)
            self._log("✅ Video Processing Complete!")
            self._log("="*60)
            return True
        
        except Exception as e:
            self._log(f"\n❌ Unexpected error in workflow: {e}")
            import traceback
            self._log(traceback.format_exc())
            return False
    
    def schedule_uploads(self):
        """Schedule automatic uploads"""
        upload_time = os.getenv("UPLOAD_TIME", "09:00")
        
        self._log(f"\n⏰ Scheduler started!")
        self._log(f"📅 Videos will upload at: {upload_time} IST")
        self._log("📌 Bot is running... (Press Ctrl+C to stop)\n")
        
        # Schedule at specific time
        schedule.every().day.at(upload_time).do(self.generate_and_upload_video)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self._log("\n\n🛑 Bot stopped by user!")
    
    def run_once(self):
        """Run the bot once (for testing)"""
        return self.generate_and_upload_video()

def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   🎬 YOUTUBE SHORTS AUTO UPLOADER BOT 🎬              ║
    ║           Comedy + Motivational Content               ║
    ║                By Anil Jaat (@jata4565)               ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Initialize bot
    bot = YouTubeShortsBot()
    
    # Run once or schedule
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        print("\n🎯 Running bot once...\n")
        success = bot.run_once()
        if success:
            print("\n✅ Bot run completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Bot run failed!")
            sys.exit(1)
    else:
        print("\n⏰ Running bot with scheduler...\n")
        bot.schedule_uploads()

if __name__ == "__main__":
    main()