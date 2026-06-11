"""
Main Bot - Orchestrate the entire workflow
Generates and uploads Comedy + Motivational shorts daily
"""

import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from ai_content_generator import ContentGenerator
from video_creator import VideoCreator
from youtube_uploader import YouTubeUploader
from facebook_uploader import FacebookUploader

load_dotenv()

class YouTubeShortsBot:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.video_creator = VideoCreator()
        self.youtube_uploader = YouTubeUploader()
        self.facebook_uploader = FacebookUploader()
        self.videos_dir = "generated_videos"
        
        # Create directories
        os.makedirs(self.videos_dir, exist_ok=True)
        
        # Authenticate
        self._setup_authentication()
    
    def _setup_authentication(self):
        """Setup authentication for all platforms"""
        print("\n🔐 Setting up authentication...\n")
        
        # YouTube
        if os.getenv("ENABLE_YOUTUBE", "true").lower() == "true":
            if self.youtube_uploader.authenticate():
                channel = self.youtube_uploader.get_channel_info()
                if channel:
                    print(f"✅ YouTube: {channel['snippet']['title']}")
        
        # Facebook
        if os.getenv("ENABLE_FACEBOOK", "true").lower() == "true":
            page = self.facebook_uploader.get_page_info()
            if page:
                print(f"✅ Facebook: {page.get('name', 'Connected')}")
    
    def generate_and_upload_video(self):
        """Main workflow: Generate -> Create -> Upload"""
        print("\n" + "="*60)
        print(f"🚀 Starting Video Generation at {datetime.now()}")
        print("="*60)
        
        try:
            # Step 1: Generate AI Content
            print("\n📝 Step 1: Generating AI Content...")
            content = self.content_generator.generate_mixed_content()
            print(f"✨ Type: {content['type']}")
            print(f"📄 Script: {content['script'][:100]}...")
            
            # Generate captions
            captions = self.content_generator.generate_captions(content['script'])
            print(f"📢 Captions: {captions[:100]}...")
            
            # Step 2: Create Video
            print("\n🎬 Step 2: Creating Video...")
            video_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = self.video_creator.create_simple_video(
                content['script'],
                video_id
            )
            
            if not video_path or not os.path.exists(video_path):
                print("❌ Video creation failed!")
                return False
            
            # Step 3: Upload to Platforms
            print("\n📤 Step 3: Uploading to Platforms...")
            
            # Prepare metadata
            title = f"{content['type']} - Anil Jaat"
            description = f"{content['script']}\n\n{captions}\n\n#Shorts #Comedy #Motivation"
            tags = ["shorts", "comedy", "motivation", "hindi", "viral"]
            
            # Upload to YouTube
            if os.getenv("ENABLE_YOUTUBE", "true").lower() == "true":
                print("\n📺 Uploading to YouTube...")
                try:
                    self.youtube_uploader.upload_video(
                        video_path,
                        title=title,
                        description=description,
                        tags=tags,
                        category="24"  # Shorts category
                    )
                except Exception as e:
                    print(f"⚠️ YouTube upload issue: {e}")
            
            # Upload to Facebook
            if os.getenv("ENABLE_FACEBOOK", "true").lower() == "true":
                print("\n📱 Uploading to Facebook...")
                try:
                    self.facebook_uploader.upload_video(
                        video_path,
                        description=description,
                        title=title
                    )
                except Exception as e:
                    print(f"⚠️ Facebook upload issue: {e}")
            
            print("\n✅ Video Processing Complete!")
            return True
        
        except Exception as e:
            print(f"\n❌ Error in workflow: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def schedule_uploads(self):
        """Schedule automatic uploads"""
        schedule_time = os.getenv("UPLOAD_SCHEDULE", "0 9 * * *")
        
        # Parse schedule time (using simple format: HH:MM)
        # For cron jobs, this would be handled by your system
        
        print(f"\n⏰ Scheduler started!")
        print(f"📅 Next upload scheduled")
        print("📌 Bot is running... (Press Ctrl+C to stop)\n")
        
        # For local testing, schedule at specific time
        schedule.every().day.at("09:00").do(self.generate_and_upload_video)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped!")
    
    def run_once(self):
        """Run the bot once (for testing)"""
        return self.generate_and_upload_video()

def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   🎬 YOUTUBE SHORTS + FACEBOOK AUTO UPLOADER BOT 🎬   ║
    ║           Comedy + Motivational Content               ║
    ║                By Anil Jaat (@jata4565)               ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Initialize bot
    bot = YouTubeShortsBot()
    
    # Run once or schedule
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        print("\n🎯 Running bot once...\n")
        bot.run_once()
    else:
        print("\n⏰ Running bot with scheduler...\n")
        bot.schedule_uploads()

if __name__ == "__main__":
    main()