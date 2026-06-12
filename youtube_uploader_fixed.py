"""
YouTube Uploader - Upload videos to YouTube (Fixed Version)
"""

import os
import pickle
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

class YouTubeUploader:
    def __init__(self):
        self.youtube_api_service_name = "youtube"
        self.youtube_api_version = "v3"
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.credentials = None
    
    def authenticate(self, credentials_file="client_secrets.json"):
        """Authenticate with YouTube API"""
        print("🔐 Authenticating with YouTube...")
        
        try:
            # Check if token already exists
            if os.path.exists("token.pickle"):
                with open("token.pickle", "rb") as token:
                    self.credentials = pickle.load(token)
                    print("✅ Using existing token")
            
            # If no valid credentials, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    print("🔄 Refreshing token...")
                    self.credentials.refresh(Request())
                else:
                    if not os.path.exists(credentials_file):
                        print(f"⚠️ {credentials_file} not found!")
                        print("📝 Please download it from Google Cloud Console")
                        return False
                    
                    print(f"📂 Loading credentials from {credentials_file}")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, self.scopes
                    )
                    self.credentials = flow.run_local_server(port=0)
                
                # Save token for future use
                with open("token.pickle", "wb") as token:
                    pickle.dump(self.credentials, token)
                    print("💾 Token saved for future use")
            
            print("✅ YouTube authentication successful!")
            return True
        
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def upload_video(self, video_file_path, title, description, tags, category="24"):
        """
        Upload video to YouTube
        category: 23 = Comedy, 24 = Shorts, 22 = Shorts
        """
        try:
            if not self.credentials:
                print("❌ Not authenticated!")
                return False
            
            if not os.path.exists(video_file_path):
                print(f"❌ Video file not found: {video_file_path}")
                return False
            
            youtube = build(
                self.youtube_api_service_name,
                self.youtube_api_version,
                credentials=self.credentials
            )
            
            print(f"\n📤 Uploading video: {title}")
            print(f"📁 File size: {os.path.getsize(video_file_path) / (1024*1024):.2f} MB")
            
            # Create media upload
            media = MediaFileUpload(
                video_file_path,
                mimetype="video/mp4",
                resumable=True
            )
            
            # Prepare request
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "categoryId": category,
                        "description": description,
                        "tags": tags,
                        "title": title,
                        "defaultLanguage": "hi",
                        "defaultAudioLanguage": "hi"
                    },
                    "status": {
                        "privacyStatus": "public",
                        "madeForKids": False
                    }
                },
                media_body=media
            )
            
            # Execute request
            print("⏳ Uploading to YouTube...")
            response = request.execute()
            video_id = response["id"]
            
            print(f"\n✅ Video uploaded successfully!")
            print(f"🎬 Video ID: {video_id}")
            print(f"🔗 Link: https://youtu.be/{video_id}")
            
            return True
        
        except Exception as e:
            print(f"❌ Upload error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_channel_info(self):
        """Get channel information"""
        try:
            if not self.credentials:
                print("❌ Not authenticated for channel info")
                return None
            
            youtube = build(
                self.youtube_api_service_name,
                self.youtube_api_version,
                credentials=self.credentials
            )
            
            request = youtube.channels().list(
                part="snippet,statistics",
                mine=True
            )
            
            response = request.execute()
            if response["items"]:
                return response["items"][0]
            return None
        
        except Exception as e:
            print(f"❌ Error getting channel info: {e}")
            return None

if __name__ == "__main__":
    uploader = YouTubeUploader()
    
    # Test authentication
    if uploader.authenticate():
        channel_info = uploader.get_channel_info()
        if channel_info:
            print(f"\n📺 Channel: {channel_info['snippet']['title']}")
            print(f"📊 Subscribers: {channel_info['statistics'].get('subscriberCount', 'Hidden')}")