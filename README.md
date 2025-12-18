# 🕵️‍♂️ AI Job Hunter Agent

An autonomous and intelligent job search agent. It scrapes job listings on LinkedIn, Glassdoor, and Indeed using [JobSpy](https://github.com/speedyapply/JobSpy), uses AI (Google Gemini or Ollama Local) to analyse semantic relevance, and generates a daily interactive report. 

## 🚀 Why should I use AI-JobHunter over mails-alert ?
Traditional email alerts are full of false positives and polluted by ads and sponsored content. 
This agent :
1. **Scrapes** multiple countries and platforms simultaneously
2. **Reads** each description using AI(LLM)
3. **Semantically filters** offers to extract the truly relevant ones
4. **Stores** relevant offers locally with an SQLite database
5. **Generates** a clean interactive **HTML report** (List/Grid view) 

## ✨ Keys fonctionalities 
- 🌍 **Worldwide :** Retrieve offers from different countries a single run.
- 🧠 **Hybrid Architecture :**
   - Uses **Gemini 1.5/2.0 (Cloud)** for speed.
   - Automatically switches to **Ollama (Llama 3.2)** when API quotas are reeched.
   - 100% Local mode available for privacy.
- 📊 **Complete Reports :** Full Job descriptions, date sorting, duplicate detection and direct apply links.
- 📱 **Zero Config Mobile :** Generates a unique Ntfy key for your phone alerts.
_______
## 🛠️ Easy start for non-coders
1. **Python** installation
   1 - Go to python.org
   2 - Download last version.
   3 - **IMPORTANT :** During installation, check the box "**Add Pyhton to PATH**" 

2. **Launching the App**
- **On Windows** : double-Click on the `Windows_launcher.bat` file
- **On MacOS** : double-Click on the `Mac_launcher.command` file.
   _(Note: On macOS, if it fails to open, right-click the file -> Open)._

3. **Using the interface**
A web page will open automatically, displaying this Tabs :
   1. **"📝 Criteria"** :
      - **Keywords** : Enter job titles/keywords (one per line).
      - **Countries** : Enter target countries (in English, e.g., _France, United States_).
      - Click **Save**
   2. **"⚙️ AI Configuration"**
      - Choose your mode.(**Hybrid** is recommanded)
      - If you have a Google API key, paste-it here.
      - Ensure [Ollama](https://ollama.com/) is installed if you plan to use Hybrid or Local mode.
   3. **"🚀 Manual Launch"** : 
      - Click **"▶️ Send 🕵️‍♂️ AI Job Hunter on Watch"**.
      - Keep the window open to see the progress logs.
      - Once finished, a button will appear to download your report.

⚠️ **Note for macOS users (First Launch)** : If the file doesn't open, it's a security feature. Do this once : 
   1. Open "Terminal" app.
   2. Type `chmod +x ` (include the space at the end)
   3. Slide the `Mac_launcher.command` file in the terminal window.
   4. Press "Enter"
_______

## 🛠️ Developer Installation

1. **Prequisites
- Python 3.10 (or above)
- [Ollama](https://ollama.com/) (for Hybrid and local mode).

2. **Clone project**
   ```bash
   git clone [https://github.com/IdiotDuVillage/AI-JobHunter.git](https://github.com/VOTRE_USER/Job_Hunter_Agent.git)
   cd Job_Hunter_Agent

   #Create a virtual environment 
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

3. **(Optional) Setup local Model**
If you wish to use Local or Hybrid mode, get the recommended model :
    ```bash
    ollama pull llama3.2 

_(For slower computers, replace `llama3.2` by `qwen2.5:1.5b`)_


## ⚙️ Configuration

1. **The `.env` file**

   Rename `.env.example` to `.env` and chose your mode : 

   Manual launch :
   ```Ini, TOML
    # --- AI Model choice ---
    # "gemini" = Quick, requires an API key.
    # "ollama" = 100% Local, private, free (slower).
    # "hybrid" = Uses Gemini by default, switches to Ollama if quota reached (Recommended).
    LLM_PROVIDER="hybrid"

    # Google Key (Leave empty if you only plan to use local mode)
    GEMINI_API_KEY="votre_cle_api_ici"

    # Local model (ex: llama3.2 or qwen2.5:1.5b)
    LOCAL_MODEL="llama3.2" 
   ```

2. **Search criteria** (`data/`) :
- `data/keywords.txt` : your keywords (1 by line).
   - _Tip: Use English terms for a worldwide scope(ex: Bioinformatics Scientist)._
- `data/countries.txt` : Les pays ciblés.
   - ⚠️ **Warning** : You must write the country name for Indeed.
   - Example :
       ```Plaintext
       France
       Switzerland
       United States
       ```

3. **Prompts** 
AI-JobHunter uses 2 differents prompts depanding on the model, to optimize results. Feel free to experiment with your own prompts ! 
- `data/prompt_gemini.txt` : Nuanced Prompt for Gemini models (LLM)
- `data/prompt_local.txt` : Robotic prompt for local AI (SLM)

## 🛡️ Proxies & Anti-Ban (Recommanded)

To prevent LinkedIn or Indeed from blocking your IP address (Error 429), especially if you are scanning multiple countries, using proxies is highly recommended.

1.  If it does not exists, create `data/proxies.txt`.
2.  Add one proxy by line.
3.  Supported format : `http://user:password@ip:port` or `ip:port`.

_Example of a simple IP format : [http://11.22.33.44:8080](http://11.22.33.44:8080_

_Tip: Free proxies found online are often slow and banned. Residential proxies (Webshare, Smartproxy, etc.) are recommended (they often offers 10 proxies when you connect on their site)._

____

## ▶️ Usages
Run the agent via the terminal (recommended for the first run to check logs) :
    ```Bash
    python main.py
    ```

AI-JobHunter will : 
1. Scan sites with each keyword and country
2. Analyze offers with chosen model
3. Automatically open report (`daily_report.html`) in your browser
3. Send a push notification to your phone

📱 **Mobile Notifications**
At the end of the first run, AI-JobHunter wil display : 

   "👉 Subscribe to this canal on the Ntfy app : job_hunter_YourUniqueKey"

Download **Ntfy** (Android/iOS), subscribe to this topic, and you will get free notifications on your Phone after each run.

____

**🤖 Automation (Mac/Linux)**
To automatically run thagent at 9am and 6pm (Mac/Linux) :
    ```Bash
    crontab -e
    ```

Add this line:
    ```Bash
    0 9,18 * * * cd /path/to/ai-job-hunter && venv/bin/python main.py >> cron.log 2>&1
    ```
____
**📂 Structure du projet**
- `src/scraper.py`: Call JobSpy, with keywords and countries rotation, proxy rotation

- `src/llm_parser.py` : Hybrid Brain (Gemini + Ollama). 

- `src/reporter.py` : Generate HTML .

- `data/job_history.db` : SQLite database (local storage).

**🛡️ Beware**
This project uses scraping techniques. Please use it responsibly. The author is not responsible for any IP blocking by the target platforms. Please use proxies if you are making intensive requests.
