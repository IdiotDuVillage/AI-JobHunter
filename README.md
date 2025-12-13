# 🕵️‍♂️ AI Job Hunter Agent

An autonomous and intelligent job search agent. It scrapes job listings on LinkedIn, Glassdoor, and Indeed using [JobSpy](https://github.com/speedyapply/JobSpy) then uses AI (Google Gemini or Ollama Local) to analyse semantic relevance, and generates a daily interactive report. 

## 🚀 Why should I use AI-JobHunter over mails-alert ?
Traditional email alerts are full of false positives and polluted by adds and sponsred content. This agent :
1. **Scrape** multiple countries and platforms simultaneously
2. **Reads** each description using AI(LLM)
3. **Semantically filters** offers to extract the truly relevant ones
4. **Store locally** relevant offers with an SQLite database
5. **Generates** a clean interactive **HTML report** (List/Grid) 

## ✨ Keys fonctionalities 
- 🌍 **Worldwide :** Retrieve offers from differents countries with one call
- 🧠 **Hybrid Architectur :**
   - Uses Gemini 1.5/2.0 (Cloud) for speed.
   - Automatically Switch locally on Ollama (Llama 3.2) when API call-quotas are reeched.
   - 100% Local mode available for confidentiality.
- 📊 **Complete Reports :** Job description, sorted by date, Duplicates detection, link to apply.
- 📱 **No mobile configuraiton needed :** Generate a unique Ntfy key for your Phone alerts.

_______

## 🛠️ Installation

1. **Prequisites
- Python 3.10 (or above)
- [Ollama](https://ollama.com/) (for Hybrid and local mode).

2. **Clone project**
   ```bash
   git clone [https://github.com/VOTRE_USER/Job_Hunter_Agent.git](https://github.com/VOTRE_USER/Job_Hunter_Agent.git)
   cd Job_Hunter_Agent

   #Create a virtual environment 
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Installer les dépendances
   pip install -r requirements.txt

2. **Install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    pip install -r requirements

3. **(Optional) Setting-up local Model**
If you wish to use Local or Hybrid mode, get the recommended model 
    ```bash
    ollama pull llama3.2 

   _(For slower computers, replace llama3.2 by qwen2.5:1.5b)_


## ⚙️ Configuration

1. **.env file**
Rename .en.example to .env and chose your mode : 
Manual launch :
   ```Ini, TOML
    # --- AI Model choice ---
    # "gemini" = Quick, requires an API key.
    # "ollama" = 100% Local, private, free (slower).
    # "hybrid" = Use Gemini by default, and switch to Ollama if quota is reached (recommended).
    LLM_PROVIDER="hybrid"

    # Google Key (Leave empty if you only plan to use local mode)
    GEMINI_API_KEY="votre_cle_api_ici"

    # Local model (ex: llama3.2 or qwen2.5:1.5b)
    LOCAL_MODEL="llama3.2" 
   ```

2. **Search criteria** (data/) :
- data/keywords.txt : your keywords (1 by line).
   - Tips : Use english for worldwide scope Utilisez l'anglais pour une recherche internationale (ex: Bioinformatics Scientist).
- data/countries.txt : Les pays ciblés.
   - ⚠️ Warning : You need to write to write the english name of the country for Indeed.
   - Example :
       ```Plaintext
       France
       Switzerland
       United States
       ```

3. **Prompts** 
AI-JobHunter uses 2 differents primpts depanding of the model, to optimize results. Feel free to experiment with your owns and share it if you get better results ! 
- (data/prompt_gemini.txt) : Nuanced Prompt for Gemini models (LLM)
- (data/prompt_local.txt) : Robotic prompt for local AI (SLM)

## 🛡️ Proxies & Anti-Ban (Recommanded)

To prevent LinkedIn or Indeed from blocking your IP address (Error 429), especially if you are scanning multiple countries, the use of proxies is highly recommended.

1.  If it does not exists, Create **`data/proxies.txt`**.
2.  Add on proxy by line.
3.  Supported format : `http://user:password@ip:port` or `ip:port`.

# Simple IP format
[http://11.22.33.44:8080](http://11.22.33.44:8080)

Tip: Free proxies found on the internet are often slow and already banned. Basic residential proxies can be retrieved by register on sites such as Webshare (10 free), Smartproxy, etc.

____

## ▶️ Usages
Manual launch of the agent (recommanded for the 1st usage to check if it work) :
    ```Bash
    python main.py
    ```

AI-JobHunter will : 
1. Scan sites with each keywords and countries
2. Analyze offers with choosen model
3. Automatically open report (daily_report.html) in your navigator
3. Send a push notification to your phone

📱 **Notifications Mobile**
At the end of the first launch, AI-JobHunter wil display : 

   "👉 Subscribe to this canal on the Ntfy app : job_hunter_YourUniqueKey"

Download **Ntfy** (Android/iOS), subscribe to this topic, and you will freely get notified on your Phone after each run.

____

**🤖 Automation**
To automatically set the Agent to run at 9am and 6pm (Mac/Linux) :
    ```Bash
    crontab -e
    ```

Add this :
    ```Bash
    0 9,18 * * * cd /path/to/ai-job-hunter && venv/bin/python main.py >> cron.log 2>&1
    ```
____
**📂 Structure du projet**
- (src/scraper.py) : Call JobSpy, with keywords and countries rotation, proxy rotation

- (src/llm_parser.py) : Hybrid Brain (Gemini + Ollama). 

- (src/reporter.py) : Generate HTML .

- (data/job_history.db) : SQLite database (local).

**🛡️ Beware**
This project uses scraping techniques. Please use it responsibly. The author is not responsible for any IP blocking by the target platforms. Please use proxies if you are making intensive requests.
