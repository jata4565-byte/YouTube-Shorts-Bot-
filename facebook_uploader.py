"""
Facebook Uploader - Upload videos to Facebook
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FacebookUploader:
    def __init__(self):
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def upload_video(self, video_file_path, description, title=""):
        """Upload video to Facebook page"""
        try:
            if not self.access_token or not self.page_id:
                print("❌ Facebook credentials missing!")
                print("📝 Set FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID in .env")
                return False
            
            print(f"\n📤 Uploading to Facebook: {title or description[:50]}")
            
            # Prepare the file
            with open(video_file_path, 'rb') as video_file:
                files = {
                    'upload_session': (os.path.basename(video_file_path), video_file, 'video/mp4')
                }
                
                data = {
                    'description': description,
                    'title': title,
                    'access_token': self.access_token
                }
                
                # Upload endpoint
                url = f"{self.base_url}/{self.page_id}/videos"
                
                response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Video uploaded to Facebook!")
                print(f"📊 Video ID: {result.get('id', 'N/A')}")
                return True
            else:
                print(f"❌ Facebook upload failed: {response.status_code}")
                print(f"Response: {response.json()}")
                return False
        
        except Exception as e:
            print(f"❌ Error uploading to Facebook: {e}")
            return False
    
    def get_page_info(self):
        """Get Facebook page information"""
        try:
            if not self.access_token or not self.page_id:
                return None
            
            url = f"{self.base_url}/{self.page_id}"
            params = {
                'fields': 'name,fan_count,engagement',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    uploader = FacebookUploader()
    
    # Test page info
    page_info = uploader.get_page_info()
    if page_info:
        print(f"\n📱 Page: {page_info.get('name', 'N/A')}")
        print(f"👥 Followers: {page_info.get('fan_count', 'N/A')}")