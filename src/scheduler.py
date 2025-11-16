"""
Scheduler - Automate content generation on a schedule
"""
import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from main import AutomationPipeline

load_dotenv()

def scheduled_job():
    """Job to run on schedule"""
    print(f"\n⏰ Scheduled job triggered at {datetime.now()}")
    pipeline = AutomationPipeline()
    pipeline.generate_single_article()

def main():
    """Run the scheduler"""
    posts_per_day = int(os.getenv('ARTICLES_PER_DAY', 3))
    
    print("="*60)
    print("🤖 PASSIVE INCOME AUTOMATION SCHEDULER")
    print("="*60)
    print(f"\n📅 Configured to generate {posts_per_day} articles per day")
    print(f"⏰ Schedule: 9:00 AM, 2:00 PM, 7:00 PM")
    print("\n🔄 Scheduler is running... (Press Ctrl+C to stop)")
    print("="*60 + "\n")
    
    # Schedule jobs at specific times
    schedule.every().day.at("09:00").do(scheduled_job)
    schedule.every().day.at("14:00").do(scheduled_job)
    schedule.every().day.at("19:00").do(scheduled_job)
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped by user")

if __name__ == "__main__":
    main()
