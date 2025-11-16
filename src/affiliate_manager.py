"""
Affiliate Link Manager - Automatically insert affiliate links into content
"""
import os
import re
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

class AffiliateLinkManager:
    def __init__(self):
        self.affiliate_links = self.load_affiliate_links()
        
    def load_affiliate_links(self):
        """Load affiliate links from environment"""
        links_str = os.getenv('AFFILIATE_LINKS', '')
        if not links_str:
            return []
        return [link.strip() for link in links_str.split(',')]
    
    def insert_affiliate_links(self, content, num_links=3):
        """Insert affiliate links naturally into the content"""
        if not self.affiliate_links:
            print("⚠ No affiliate links configured")
            return content
        
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('p')
        
        if len(paragraphs) < num_links:
            num_links = len(paragraphs)
        
        # Select random paragraphs to add affiliate links
        selected_paragraphs = random.sample(paragraphs, num_links)
        
        for i, p in enumerate(selected_paragraphs):
            link = random.choice(self.affiliate_links)
            cta_text = self.get_cta_text()
            
            # Create affiliate box
            affiliate_box = soup.new_tag('div', **{'class': 'affiliate-box'})
            affiliate_link = soup.new_tag('a', href=link, **{
                'class': 'cta-button',
                'target': '_blank',
                'rel': 'nofollow noopener'
            })
            affiliate_link.string = cta_text
            
            disclosure = soup.new_tag('p')
            disclosure.string = "💡 "
            strong = soup.new_tag('strong')
            strong.string = "Recommended Product"
            disclosure.append(strong)
            disclosure.append(" - Check out this highly-rated option:")
            
            affiliate_box.append(disclosure)
            affiliate_box.append(affiliate_link)
            
            # Insert after the paragraph
            p.insert_after(affiliate_box)
        
        return str(soup)
    
    def get_cta_text(self):
        """Get random call-to-action text"""
        cta_options = [
            "Check Price on Amazon",
            "View on Amazon",
            "See Current Price",
            "Check Latest Price",
            "View Product Details",
            "See Best Deal",
            "Compare Prices",
            "Shop Now"
        ]
        return random.choice(cta_options)
    
    def add_disclosure(self, content):
        """Add affiliate disclosure at the beginning"""
        disclosure = """
        <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 5px;">
            <p style="margin: 0; font-size: 0.9em;"><strong>📢 Disclosure:</strong> This post contains affiliate links. 
            If you make a purchase through these links, we may earn a commission at no additional cost to you. 
            We only recommend products we genuinely believe in.</p>
        </div>
        """
        return disclosure + content

if __name__ == "__main__":
    manager = AffiliateLinkManager()
    
    # Test content
    test_content = """
    <p>This is a sample paragraph about products.</p>
    <p>Another paragraph with more information.</p>
    <p>Yet another paragraph discussing features.</p>
    <p>Final paragraph with conclusions.</p>
    """
    
    result = manager.insert_affiliate_links(test_content, num_links=2)
    result = manager.add_disclosure(result)
    
    print("✓ Affiliate links inserted")
    print(f"  Links configured: {len(manager.affiliate_links)}")
