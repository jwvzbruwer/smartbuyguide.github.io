"""
Content Generator - AI-powered article creation with SEO optimization
"""
import os
import yaml
import random
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.load_config()
        
    def load_config(self):
        """Load configuration files"""
        with open('config/topics.yaml', 'r') as f:
            self.topics_config = yaml.safe_load(f)
        with open('config/settings.yaml', 'r') as f:
            self.settings = yaml.safe_load(f)
    
    def get_random_topic(self, niche=None):
        """Get a random topic from the configured niche"""
        if niche is None:
            niche = os.getenv('NICHE', 'technology')
        
        topics = self.topics_config['topics'].get(niche, [])
        if not topics:
            topics = self.topics_config['topics']['technology']
        
        return random.choice(topics)
    
    def generate_article(self, topic=None):
        """Generate a complete article using AI"""
        if topic is None:
            topic = self.get_random_topic()
        
        print(f"Generating article: {topic}")
        
        # Create the prompt for article generation
        prompt = f"""Write a comprehensive, SEO-optimized blog article about "{topic}".

Requirements:
- Length: {self.settings['content']['min_words']}-{self.settings['content']['max_words']} words
- Tone: {self.settings['content']['tone']}
- Include sections: Introduction, detailed main content with subheadings, conclusion, and call-to-action
- Focus on providing value and practical information
- Include specific product recommendations where appropriate
- Write in a natural, engaging style
- Use HTML formatting with <h2> for main sections and <p> for paragraphs

Format the content as HTML (body content only, no <!DOCTYPE> or <html> tags).
Include clear section breaks and natural places for affiliate links."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert content writer specializing in product reviews and buying guides. You write engaging, informative content that helps readers make informed purchasing decisions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Generate SEO metadata
            seo_data = self.generate_seo_metadata(topic, content)
            
            return {
                'title': topic,
                'content': content,
                'seo': seo_data,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating article: {e}")
            return None
    
    def generate_seo_metadata(self, topic, content):
        """Generate SEO metadata for the article"""
        try:
            prompt = f"""Based on this article topic "{topic}", generate:
1. A compelling meta description (max 160 characters)
2. 5 relevant SEO keywords (comma-separated)
3. A short excerpt (2-3 sentences)

Format your response as:
META: [meta description]
KEYWORDS: [keyword1, keyword2, keyword3, keyword4, keyword5]
EXCERPT: [excerpt text]"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an SEO expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            result = response.choices[0].message.content
            
            # Parse the response
            lines = result.strip().split('\n')
            meta_desc = ""
            keywords = ""
            excerpt = ""
            
            for line in lines:
                if line.startswith('META:'):
                    meta_desc = line.replace('META:', '').strip()
                elif line.startswith('KEYWORDS:'):
                    keywords = line.replace('KEYWORDS:', '').strip()
                elif line.startswith('EXCERPT:'):
                    excerpt = line.replace('EXCERPT:', '').strip()
            
            return {
                'meta_description': meta_desc,
                'keywords': keywords,
                'excerpt': excerpt
            }
            
        except Exception as e:
            print(f"Error generating SEO metadata: {e}")
            return {
                'meta_description': topic,
                'keywords': topic,
                'excerpt': f"Read our comprehensive guide about {topic}."
            }

if __name__ == "__main__":
    generator = ContentGenerator()
    article = generator.generate_article()
    if article:
        print(f"\n✓ Generated: {article['title']}")
        print(f"  SEO Keywords: {article['seo']['keywords']}")
        print(f"  Word count: ~{len(article['content'].split())} words")
