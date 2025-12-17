import os
import time
import random
from src.scraper import fetch_jobs_jobspy
from src.llm_parser import filter_jobs_with_LM
from src.storage import JobDataBase
from src.reporter import generate_report
from src.notifier import send_notification

#Configuration
KEYWORD_FILE = "data/keyword.txt"
COUNTRIES_FILE = "data/countries.txt"

def run_bot():
    print("🤖 Launching Job-Hunter agent (multi-site + location) ...")


    TARGET_SITES = ["linkedin", "glassdoor", "indeed"]

    #Loading keywords : 
    with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]

    #Loading countries : 
    if os.path.exists(COUNTRIES_FILE):
        with open(COUNTRIES_FILE, 'r', encoding='utf-8') as f:
            countries = [line.strip() for line in f if line.strip()]
    else : 
        print("⚠️ No data/countries.txt detected, using default country : France")
        countries = ["France"]     
    db = JobDataBase()
    total_new = 0

    for country in countries:
        print(f"\n🌍 --- DESTINATION : {country.upper()} ---")
        for keyword in keywords : 
            print(f" 🔎 Fetching with : {keyword}")
            for site in TARGET_SITES:
                raw_jobs = fetch_jobs_jobspy(keyword, site=site, country=country, num_results=15)
                if not raw_jobs:
                    time.sleep(5)
                    continue

                #2 Filtering with Gemini
                validated_jobs = filter_jobs_with_LM(raw_jobs, keyword)
                print(f"    ✨ {len(validated_jobs)} relevant offers extracted")

            #Storage
                if validated_jobs:
                    source_tag = f"{site.capitalize()}/{country}/{keyword}"

                    #Saving in BDD
                    count = db.save_jobs(validated_jobs, source=source_tag)
                    total_new += count

                    if count > 0 :
                        New_jobs.append(validated_jobs)
                    print(f"   💾{count} saved offers for {site}.")

            time.sleep(random.uniform(3, 7))
            print("   ⏸️ Changing keyword...")
            time.sleep(random.uniform(5,10))
        print("   ✈️  Changing countries...")
        time.sleep(random.uniform(10, 20))
    db.close()

    print(f"\n🏁 Finished. {total_new} new offers.")
    
    if total_new > 0:
        generate_report(open_browser=False)

    #Retrieving some offers 

    send_notification(total_new, top_jobs=validated_jobs)

if __name__ == "__main__":
    run_bot()
