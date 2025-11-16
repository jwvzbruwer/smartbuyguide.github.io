"""
Site Builder - Generate static HTML site from articles
"""
import os
import json
from datetime import datetime
from jinja2 import Template
from pathlib import Path

class SiteBuilder:
    def __init__(self):
        self.output_dir = Path('output/site')
        self.content_dir = Path('generated_content')
        self.templates_dir = Path('templates')
        
    def build_site(self):
        """Build the complete static site"""
        print("Building static site...")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load all articles
        articles = self.load_articles()
        
        if not articles:
            print("⚠ No articles found. Generate some content first.")
            return
        
        # Generate article pages
        for article in articles:
            self.generate_article_page(article)
        
        # Generate index page
        self.generate_index_page(articles)
        
        print(f"✓ Site built successfully!")
        print(f"  Location: {self.output_dir.absolute()}")
        print(f"  Articles: {len(articles)}")
        print(f"\n  Open: {self.output_dir.absolute()}/index.html")
    
    def load_articles(self):
        """Load all generated articles"""
        articles = []
        
        if not self.content_dir.exists():
            return articles
        
        for json_file in self.content_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    article = json.load(f)
                    article['filename'] = json_file.stem
                    articles.append(article)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        # Sort by date (newest first)
        articles.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return articles
    
    def generate_article_page(self, article):
        """Generate HTML page for an article"""
        # Load template
        with open(self.templates_dir / 'article_template.html', 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        # Render HTML
        html = template.render(
            title=article['title'],
            content=article['content'],
            meta_description=article['seo']['meta_description'],
            keywords=article['seo']['keywords'],
            date=article['date'],
            author=os.getenv('AUTHOR_NAME', 'Admin'),
            site_name=os.getenv('SITE_NAME', 'My Blog')
        )
        
        # Save file
        output_file = self.output_dir / f"{article['filename']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✓ Generated: {article['filename']}.html")
    
    def generate_index_page(self, articles):
        """Generate the homepage with article listing"""
        # Load template
        with open(self.templates_dir / 'index_template.html', 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        # Prepare posts data
        posts = []
        for article in articles:
            posts.append({
                'title': article['title'],
                'excerpt': article['seo']['excerpt'],
                'date': article['date'],
                'url': f"{article['filename']}.html"
            })
        
        # Render HTML
        html = template.render(
            site_name=os.getenv('SITE_NAME', 'My Passive Income Blog'),
            posts=posts
        )
        
        # Save file
        output_file = self.output_dir / 'index.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✓ Generated: index.html")

if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build_site()
