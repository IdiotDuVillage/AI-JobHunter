import pandas as pd
import random
import os
from jobspy import scrape_jobs
#Proxies list
PROXY_file = "data/Webshare_10_proxies.txt"

def load_proxies():
    """
    Load proxies list from list
    Adapt key to JobSpy
    - user:pass@ip:port (Standard)
    - ip:port:user:pass (Webshare/Raw)
    """
    if not os.path.exists(PROXY_file):
        try:
            with open(PROXY_file, "w", encoding="utf-8") as f:
                f.write("# Add your proxies her (1 by ligne)\n")
                f.write("# Format: http://user:password@ip:port\n")
                f.write("# Example: http://bob:12345@45.67.89.10:8888\n")
            print(f"ℹ️ {PROXY_file} created. Add your proxies to avoid IP ban.")
        except Exception:
            pass
        return []
    
    if not os.path.exists(PROXY_file): return []
    formatted_proxies = []

    with open(PROXY_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            #Cleaning prefix "http;//" to analyze properly
            clean_line = line.replace("http://", "").replace("https://", "")
            parts = clean_line.split(':')
            #Case 1 = format IP:PORT:USER:PASS 
            if len(parts) == 4:
                ip, port, user, password = parts
                #Standardization 
                new_proxy = f"http://{user}:{password}@{ip}:{port}"
                formatted_proxies.append(new_proxy)
            #Cas2 : Format USER:PASS@IP:PORT 
            elif '@' in clean_line:
                formatted_proxies.append(f"http://{clean_line}")
            #Case 3 : Format IP:PORT 
            elif len(parts) == 2:
                formatted_proxies.append(f"http://(clean_line)") 
            else :
                formatted_proxies.append(line)
    return [p for p in formatted_proxies if p and len(p) > 5]

def fetch_jobs_jobspy(keyword, site, country, num_results=15):
    """
    Get offers with JobSpy with proxy rotation
    """

    print(f"🕵️ JobSpy Search with : '{keyword}' located in '{country}' on {site}")

    #Proxy management
    proxies_list = load_proxies()

    country_indeed_param = country 
    country_indeed = 'France' if site == 'indeed' else None
    if proxies_list :
        formatted_proxies = proxies_list
        print(f"   🛡️  {len(formatted_proxies)} loaded proxies, Rotation activated")
    else : 
        print(f"   ⚠️   No proxy found. Using user IP (might be banned)")
    
    try :
        #Calling JobSpy
        #Possibility of adding Indeed, Glassdoor, etc
        Jobs = scrape_jobs(
            site_name = [site],
            search_term=keyword,
            #LOCALISATION
            locations=country,
            country_indeed=country,
            results_wanted=num_results,
            hours_old=24, #Filterlast 24hrs
            proxies = formatted_proxies,

            #Ant-ban option
            linkedin_fetch_description=True #Usefull for LLM interpreter
        )

        if Jobs.empty:
            print(f"   ❌ No jobs found in {country} (might be blocked).")
            return[]
        
        print(f"   ✅ {len(Jobs)} job offers retrieved.")
        jobs_dict = Jobs.to_dict('records')
        for job in jobs_dict:
            if 'site' not in job or not job['site']:
                job['site']=site
        #Converting Dataframe to dictionary
            job['country_search'] = country
        return Jobs.to_dict('records')
    
    except Exception as e:
        print(f"   💀 JobSpy Fatal Error for {site.upper()} ({country}): {e}")
        return []
        