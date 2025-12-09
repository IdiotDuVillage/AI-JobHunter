import os
import time
import random
from src.scraper import fetch_jobs_jobspy
from src.llm_parser import filter_jobs_with_gemini
from src.storage import JobDataBase
from src.reporter import generate_report
from src.notifier import send_notification

#Configuration
KEYWORD_FILE = "data/keyword.txt"

def run_bot():
    print("🤖 Launching Job-Hunter agent (multi-site + location) ...")

    TARGET_LOCATION = "France"
    TARGET_SITES = ["linkedin", "glassdoor", "indeed"]

    #Loading keywords : 
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]

    db = JobDataBase()
    total_new = 0

    for keyword in keywords : 
        print(f" 🔎 Fetching with : {keyword}")
        
        for site in TARGET_SITES:
            raw_jobs = fetch_jobs_jobspy(keyword, site=site, location=TARGET_LOCATION, num_results=15)
            if not raw_jobs:
                time.sleep(5)
                continue

            #2 Filtering with Gemini
            validated_jobs = filter_jobs_with_gemini(raw_jobs, keyword)
            print(f"    ✨ {len(validated_jobs)} relevant offers extracted")

            #Storage
            if validated_jobs:
                count = db.save_jobs(validated_jobs, source=f"{site.capitalize()}/{keyword}")
                total_new += count
                print(f"   💾{count} saved offers for {site}.")

            time.sleep(random.uniform(3, 7))
        print("   ⏸️ Changing keyword...")
        time.sleep(random.uniform(10,20))
    
    db.close()

    print(f"\n🏁 Finished. {total_new} new offers.")
    
    if total_new > 0:
        generate_report(open_browser=False)

    #Retrieving some offers 

    send_notification(total_new)

if __name__ == "__main__":
    run_bot()
