"""
AI Content Generator using Groq API (Free)
Generates Comedy + Motivational content for shorts
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "mixtral-8x7b-32768"
    
    def generate_comedy_script(self):
        """Generate a short comedy script (15-60 seconds)"""
        prompt = """
        Create a SHORT, FUNNY, and RELATABLE comedy script for a 30-second YouTube Short.
        The script should be in HINDI and make people laugh.
        
        Requirements:
        - Make it relatable (about daily life, relationships, work, college, etc.)
        - Keep it family-friendly and clean
        - Add funny observations or jokes
        - Make it engaging and quick
        - Format: [Scene description] [Dialogue] [Action]
        
        Example format:
        Scene: Office desk
        Character 1: [Says something funny]
        Character 2: [Responds with humor]
        Action: [What happens]
        
        Now create a NEW original comedy script:
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    def generate_motivational_script(self):
        """Generate a motivational short script"""
        prompt = """
        Create a SHORT, INSPIRING, and MOTIVATIONAL script for a 30-second YouTube Short.
        The script should be in HINDI and inspire viewers.
        
        Requirements:
        - Make it motivational but not preachy
        - Include a real-life scenario
        - Add an inspiring message
        - Make it relatable and powerful
        - Format: [Scene] [Voiceover/Dialogue] [Message]
        
        Example format:
        Scene: Person facing a challenge
        Voiceover: [Motivational message]
        Message: [Call to action or life lesson]
        
        Now create a NEW original motivational script:
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    def generate_mixed_content(self):
        """Generate either comedy or motivational content"""
        import random
        
        content_type = random.choice(["comedy", "motivational"])
        
        if content_type == "comedy":
            script = self.generate_comedy_script()
            content_type_label = "🎭 COMEDY"
        else:
            script = self.generate_motivational_script()
            content_type_label = "💪 MOTIVATIONAL"
        
        return {
            "type": content_type_label,
            "script": script,
            "category": content_type
        }
    
    def generate_captions(self, script):
        """Generate engaging captions for the video"""
        prompt = f"""
        Create 2-3 SHORT, ENGAGING captions for this YouTube Short script:
        
        Script: {script}
        
        Requirements:
        - Use relevant hashtags
        - Make it catchy and clickable
        - Include emojis
        - Keep it in HINDI or Hinglish
        - Format: Caption 1, Caption 2, Caption 3
        """
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Test content generation
    print("🎬 Generating AI Content...\n")
    
    content = generator.generate_mixed_content()
    print(f"Content Type: {content['type']}")
    print(f"\nScript:\n{content['script']}\n")
    
    captions = generator.generate_captions(content['script'])
    print(f"Captions:\n{captions}")