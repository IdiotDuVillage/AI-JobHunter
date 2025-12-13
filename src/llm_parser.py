import os
import time
import json
import ollama
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()
# --- CONFIGURATION ---
PROMPT_FILE_GEMINI = "data/prompt_gemini.txt"
PROMPT_FILE_LOCAL = "data/prompt_local"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hybrid").lower()
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "llama3.2")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


#Gemini configuration 
if GEMINI_API_KEY:
    print(GEMINI_API_KEY)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#List of Gemini Models for fallback
GEMINI_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-flash-latest",
]

def _build_prompt(file_path, keyword, json_data):
    """Load prompt and replace variables (keywords and json)"""
    template = 'CONTEXTE: Keyword "{{keyword}}". DATA: {{json_data}}. TASK: JSON {"ids": []}.'

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content: template = content
        except:
            print("No prompt file found, using basic template ")

    return template.replace("{{keyword}}", keyword).replace("{{json_data}}", json_data)

def _call_gemini(keyword, json_data):
    """Get Gemini prompt and call API"""
    #Loading Gemini prompt file
    prompt = _build_prompt(PROMPT_FILE_GEMINI, keyword, json_data)

    if not GEMINI_API_KEY:  raise Exception("Missing API key")

    for model_name in GEMINI_MODELS:
        print(f"🧠 {model_name}'s analyzing offers")
        try : 
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature":0.1,
                    "response_mime_type": "application/json"
                }
            )
            response = model.generate_content(prompt)
            return response.text
        except exceptions.RessourceExhausted:
            print(f"    ⚠️ Current quota exceeded for {model_name}")
            print("Changing model")
            continue
        except Exception as e:
            print(f"    ⚠️ Gemini technical Error with {model_name}: {e}")
            continue
    raise Exception("No Gemini model available at the moment")

def _call_ollama(keyword, json_data):
    """Get local model prompt and call it"""
    prompt = _build_prompt(PROMPT_FILE_LOCAL, keyword, json_data)

    print(f"🧠 {LOCAL_MODEL}'s analyzing offers")
    response = ollama.chat(model=LOCAL_MODEL, messages=[
        {'role': 'system', 'content': 'Output ONLY JSON.'},
        {'role': 'user', 'content': prompt},
    ], format='json')
    return response['message']['content']

def filter_jobs_with_LM(jobs_list, search_keyword):
    """
    Take an already structured by JobSpy and filter it using LLM of SLM.
    Use description if available to validate pertinence.
    """
    if not jobs_list: return []
    # --- Data preprocessing ---
    #generating a light sum-up to not overuse tokens if list if long
    #Send ID to retrieve original objects
    jobs_to_check = []
    for idx, job in enumerate(jobs_list):
        desc = job.get('description')
        if not isinstance(desc, str): desc = ""
        #We cut description to 800 words
        short_desc = desc[:800] + "..." if desc else "No description"
        jobs_to_check.append({
            "id": idx,
            "title": job.get('title'),
            "company": job.get('company'),
            "summary": short_desc
        })
    json_str_data = json.dumps(jobs_to_check, indent=2)
    raw_response = None
    model_used = "Unknown"

    if LLM_PROVIDER=="ollama":
        try : 
            print(f"🧠 Ollama's analyzing {len(jobs_list)} offers...")
            raw_response = _call_ollama(search_keyword, json_str_data)
            model_used = "Local (Ollama)"
        except Exception as e:
            print(f"   ❌ Error Ollama : {e}")
            return []
    else : 
        try:
            raw_response = _call_gemini(search_keyword, json_str_data)
            model_used = f"Gemini"
        except Exception as e:
            print(f"    ⚠️ Technical Error with Gemini : {e}")     
            if LLM_PROVIDER == "hybrid" :
                print("   🔄 SWITCHING TO LOCAL SLM...")
                try:
                    raw_response = _call_ollama(search_keyword, json_str_data)
                    used_model = "Local (Ollama)"
                except Exception as local_e:
                    print(f"   ❌ Ollama error: {local_e}")
                    return []
            else :
                return[]

    #Parsing JSON
    try : 
        parsed_json = json.loads(raw_response)
        valids_id = []
        if isinstance(parsed_json, list): valid_ids = parsed_json
        elif isinstance(parsed_json, dict):
            for key in ["ids", "valid_ids", "jobs"]:
                if key in parsed_json and isinstance(parsed_json[key], list):
                    valid_ids = parsed_json[key]
                    break
        final_jobs = []
        for idx in valid_ids:
            if isinstance(idx, int) and 0 <= idx < len(jobs_list):
                original_job = jobs_list[idx]
                # URL check
                raw_url = original_job.get('job_url') or original_job.get('apply_url') or original_job.get('url')
                if raw_url and ("," in raw_url or " " in raw_url) and "http" not in raw_url: raw_url = None

                final_jobs.append({
                    "title": original_job.get('title'),
                    "company": original_job.get('company'),
                    "location": original_job.get('location'),
                    "url": raw_url,
                    "date_posted": str(original_job.get('date_posted')),
                    "description": original_job.get('description'),
                    "source": original_job.get('site', 'Unknown')
                })
        
        print(f"   ✅ Great Success ! {model_used} retrieved ({len(final_jobs)} offers)")
        return final_jobs
    
    except Exception as e:
        print(f"   ⚠️ Errror while parsing JSON : {e}")
        return []