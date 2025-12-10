import os
import time
import json
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

##Loading API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#Configuration 
PROMPT_FILE = "data/prompt.txt"
#Organizing Models fallback
MODEL_FALLBACK_LIST = [
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-2-0-flash-lite",
    "models/gemini-flash-latest",
    "models/gemlini-flash-lite-latest"
]

def get_gemini_response(prompt, model_name):
    """Calling specific models"""
    generation_config = {
        "temperature":0.1,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json"
        }
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )
    return model.generate_content(prompt)

def filter_jobs_with_gemini(jobs_list, search_keyword):
    """
    Take an already structured by JobSpy and filter it using AI.
    Use description if available to validate pertinence
    """
    if not jobs_list :
        return []
    
    print(f"🧠 Gemini's analyzing {len(jobs_list)} offers...")

    #generating a light sum-up to not overuse tokens if list if long
    #Send ID to retrieve original objects
    jobs_to_check = []
    for idx, job in enumerate(jobs_list):
        desc = job.get('description', '')
        #We cut description to 800 words
        short_desc = desc[:800] + "..." if desc else "No description"

        jobs_to_check.append({
            "id": idx,
            "title": job.get('title'),
            "company": job.get('company'),
            "summary": short_desc
        })

        try:
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                raw_prompt = f.read()
        except FileNotFoundError:
            print(f"⚠️  Error : {PROMPT_FILE} not found.")

        pormpt = raw_prompt.replace("{{keyword}}", search_keyword)
        prompt = prompt.replace("{{json_data}}", json.dumps(jobs_to_check, indent=2))
    # --- FALLBACK LOOP ---
    for model_name in MODEL_FALLBACK_LIST:
        try :
            print(f"   👉 Using {model_name}...")
            response = get_gemini_response(prompt, model_name)
            valid_ids = json.loads(response.text)

            #Constructing final list with all datas
            final_jobs = []
            for idx in valid_ids:
                if isinstance(idx, int) and 0 <= idx < len(jobs_list):
                    original_job = jobs_list[idx]

                    #Normalization for or DB
                    final_jobs.append({
                        "title": original_job.get('title'),
                        "company": original_job.get('company'),
                        "location": original_job.get('location'),
                        "url": original_job.get('job_url'),
                        "data_posted": str(original_job.get('date_posted')),
                        "description": original_job.get('description')
                    })
            print(f"   ✅ Success with {model_name}")
            return final_jobs
        except exceptions.ResourceExhausted:
            # ERROR 429 : too many requests, changing models
            print(f"    ⚠️ Current quota exceeded for {model_name} : {e}")
            print("Changing model")
        except Exception as e:
            print(f"    ⚠️ Gemini technical Error with {model_name}: {e}")
            continue
    
    #If everything fails, no quotas left for free models, 
    print(" ❌ You've exceeded all free quotas from Gemini, or all models are in error state.")
    return []