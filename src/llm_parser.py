import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

##Loading API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#Configuration 
generation_config = {
    "temperature":0.1,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json"
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config=generation_config,
)

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
        #We cut description to 500 words
        short_desc = desc[:500] + "..." if desc else "No description"

        jobs_to_check.append({
            "id": idx,
            "title": job.get('title'),
            "company": job.get('company'),
            "summary": short_desc
        })
    prompt = f"""
    CONTEXT : Job search with the keyword : "{search_keyword}".

    TASK : 
    Here is a list of job offers. Identify those that are RELEVANT.
    Reject ads, offers that are too semantically distant, or fake  offers.

    LIST TO BE ANALYSED :
    {json.dumps(jobs_to_check, indent=2)}

    EXPECTED RESPONSE (JSON) :
    A list containing ONLY the IDs of valid offers.
    Exemple : [0, 3, 5]
    """

    try :
        response = model.generate_content(prompt)
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
        return final_jobs
    
    except Exception as e:
        print(f"⚠️ Gemini filter Error : {e}")
        return []
