"""
Video Creator - Generate videos from scripts using AI and stock footage
"""

import os
import requests
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip, 
    concatenate_videoclips, AudioFileClip, ColorClip
)
import numpy as np
from pathlib import Path

class VideoCreator:
    def __init__(self):
        self.output_dir = "generated_videos"
        os.makedirs(self.output_dir, exist_ok=True)
        self.video_width = 1080
        self.video_height = 1920
        self.fps = 30
    
    def get_stock_image(self, keyword):
        """Get free stock image from Pexels or create colored background"""
        try:
            # Using free API to get images
            images_dir = "stock_images"
            os.makedirs(images_dir, exist_ok=True)
            
            # Create a colorful gradient background for now
            return self.create_gradient_background()
        except Exception as e:
            print(f"Error getting stock image: {e}")
            return self.create_gradient_background()
    
    def create_gradient_background(self):
        """Create a beautiful gradient background"""
        img = Image.new('RGB', (self.video_width, self.video_height))
        pixels = img.load()
        
        # Create gradient from top to bottom
        colors = [
            (255, 107, 107),  # Red
            (255, 180, 100),  # Orange
            (255, 218, 185),  # Peach
        ]
        
        for y in range(self.video_height):
            ratio = y / self.video_height
            if ratio < 0.5:
                r = int(colors[0][0] * (1 - ratio*2) + colors[1][0] * (ratio*2))
                g = int(colors[0][1] * (1 - ratio*2) + colors[1][1] * (ratio*2))
                b = int(colors[0][2] * (1 - ratio*2) + colors[1][2] * (ratio*2))
            else:
                ratio = (ratio - 0.5) * 2
                r = int(colors[1][0] * (1 - ratio) + colors[2][0] * ratio)
                g = int(colors[1][1] * (1 - ratio) + colors[2][1] * ratio)
                b = int(colors[1][2] * (1 - ratio) + colors[2][2] * ratio)
            
            for x in range(self.video_width):
                pixels[x, y] = (r, g, b)
        
        bg_path = "temp_bg.png"
        img.save(bg_path)
        return bg_path
    
    def add_text_overlay(self, image_path, text, output_path):
        """Add text overlay to image"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to use a better font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        except:
            font = ImageFont.load_default()
        
        # Add text with background for better readability
        text_width = len(text) * 30
        text_height = 100
        
        x = (self.video_width - text_width) // 2
        y = (self.video_height - text_height) // 2
        
        # Draw background rectangle
        draw.rectangle(
            [x-20, y-20, x+text_width+20, y+text_height+20],
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        img.save(output_path)
        return output_path
    
    def create_video_from_script(self, script, content_type, video_id):
        """Create a complete video from script"""
        print(f"\n🎬 Creating video for {content_type}...")
        
        try:
            # Get background image
            bg_image = self.get_stock_image(script[:50])
            
            # Create clips
            clip = ImageClip(bg_image).set_duration(4)
            
            # Add text
            txt_clip = TextClip(
                script,
                fontsize=50,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(1000, 1800),
                align='center'
            ).set_duration(4).set_position('center')
            
            # Composite video
            final_clip = CompositeVideoClip([
                clip,
                txt_clip.set_opacity(0.9)
            ]).set_size((self.video_width, self.video_height))
            
            # Output path
            output_path = os.path.join(self.output_dir, f"short_{video_id}.mp4")
            
            # Write video file
            final_clip.write_videofile(
                output_path,
                fps=self.fps,
                verbose=False,
                logger=None,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return None
    
    def create_simple_video(self, text, video_id):
        """Create a simple text-based video (faster method)"""
        print(f"📹 Creating simple video #{video_id}...")
        
        try:
            # Create colored background
            background = ColorClip(
                size=(self.video_width, self.video_height),
                color=(40, 40, 60)
            ).set_duration(4)
            
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(1000, 1800),
                align='center'
            ).set_duration(4).set_position('center')
            
            # Composite
            video = CompositeVideoClip([background, txt_clip])
            
            # Output
            output_path = os.path.join(self.output_dir, f"short_{video_id}.mp4")
            
            video.write_videofile(
                output_path,
                fps=24,
                verbose=False,
                logger=None
            )
            
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

if __name__ == "__main__":
    creator = VideoCreator()
    
    # Test video creation
    test_script = "यह एक मजेदार वीडियो है! हंसो और शेयर करो 😂"
    video_path = creator.create_simple_video(test_script, "test_001")
    print(f"\nVideo saved at: {video_path}")