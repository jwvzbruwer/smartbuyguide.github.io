"""
Main Automation Script - Orchestrates the entire content generation pipeline
"""
import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from content_generator import ContentGenerator
from affiliate_manager import AffiliateLinkManager
from site_builder import SiteBuilder

load_dotenv()

class AutomationPipeline:
    def __init__(self):
        self.content_dir = Path('generated_content')
        self.content_dir.mkdir(exist_ok=True)
        
        self.generator = ContentGenerator()
        self.affiliate_manager = AffiliateLinkManager()
        self.site_builder = SiteBuilder()
        
        # Load settings
        with open('config/settings.yaml', 'r') as f:
            self.settings = yaml.safe_load(f)
    
    def generate_single_article(self, topic=None):
        """Generate a single complete article"""
        print("\n" + "="*60)
        print("🚀 STARTING ARTICLE GENERATION")
        print("="*60)
        
        # Step 1: Generate content with AI
        print("\n[1/4] Generating article content with AI...")
        article = self.generator.generate_article(topic)
        
        if not article:
            print("❌ Failed to generate article")
            return None
        
        print(f"✓ Article generated: {article['title']}")
        
        # Step 2: Insert affiliate links
        print("\n[2/4] Inserting affiliate links...")
        article['content'] = self.affiliate_manager.add_disclosure(article['content'])
        article['content'] = self.affiliate_manager.insert_affiliate_links(
            article['content'], 
            num_links=3
        )
        print("✓ Affiliate links inserted")
        
        # Step 3: Save article data
        print("\n[3/4] Saving article...")
        filename = self.create_filename(article['title'])
        filepath = self.content_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Article saved: {filepath}")
        
        # Step 4: Build/update website
        print("\n[4/4] Building website...")
        self.site_builder.build_site()
        
        print("\n" + "="*60)
        print("✅ ARTICLE GENERATION COMPLETE!")
        print("="*60)
        print(f"\n📄 Title: {article['title']}")
        print(f"📊 Word count: ~{len(article['content'].split())} words")
        print(f"🔗 Affiliate links: Added")
        print(f"📅 Date: {article['date']}")
        
        return article
    
    def generate_batch(self, count=None):
        """Generate multiple articles"""
        if count is None:
            count = int(os.getenv('ARTICLES_PER_DAY', 3))
        
        print(f"\n🔄 Generating batch of {count} articles...\n")
        
        articles = []
        for i in range(count):
            print(f"\n--- Article {i+1}/{count} ---")
            article = self.generate_single_article()
            if article:
                articles.append(article)
        
        print(f"\n✅ Batch complete! Generated {len(articles)} articles.")
        return articles
    
    def create_filename(self, title):
        """Create a URL-friendly filename from title"""
        # Convert to lowercase and replace spaces with hyphens
        filename = title.lower()
        filename = filename.replace(' ', '-')
        # Remove special characters
        filename = ''.join(c for c in filename if c.isalnum() or c == '-')
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        return f"{timestamp}-{filename}"

def main():
    """Main entry point"""
    pipeline = AutomationPipeline()
    
    # Check if OpenAI API key is configured
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print("\n❌ ERROR: OpenAI API key not configured!")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Configure your affiliate links")
        print("\nRun: copy .env.example .env")
        return
    
    # Generate a single article
    pipeline.generate_single_article()

if __name__ == "__main__":
    main()
