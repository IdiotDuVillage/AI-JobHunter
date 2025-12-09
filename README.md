# 🕵️‍♂️ AI Job Hunter Agent

Autonomous agent based on JobSpy assisted with AI automating Jobs wearches. It retrieve offers from LinkedIn, Glassdoor, Indeed and filter relevant offers with **Google Gemini** to generate a daily interactive report. 

## 🚀 Fonctionalities

- **Multi-sources :** Retrieve offers from LinkedIn, Indeed and Glassdoor through `JobSpy` (https://github.com/speedyapply/JobSpy).
- **AI filter (Smart Filtering) :** Use Gemini 2.5 Flash lite to analyze job description and filter the irrelevants offers. 
- **Local History :** SQLite database to avoid duplicates.
- **HTML Report:** Clean interface with drop-down description and direct links.
- **Notifications :** Mobile push notification with Ntfy.sh at the end of each cycle.
- **Anti-Ban :** Native support for proxy rotation.

## 🛠️ Installation

1. **Clone project**
   ```bash
   git clone [https://github.com/VOTRE_USER/Job_Hunter_Agent.git](https://github.com/VOTRE_USER/Job_Hunter_Agent.git)
   cd Job_Hunter_Agent

2. **Install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    pip install -r requirements

3. **Configuration**
- Rename '.env.example' to '.env' and add you Gemini API key
- Add your proxies in 'data/proxies.txt' (Optional but higly recommended)
- Add your keywords in 'data/keywords.txt' (One by line).


## 🤖 Usage

Manual launch :
   ```bash
    python main.py
   ```
Automation (Mac/Linux) :
   ```bash
    0 9,13,19 * * * cd /path/to/JobHunter && venv/bin/python main.py
   ```

## 🏗️ Architecture
1. Scraper: 'Jobspy' retrieve offers.
2. Parser : 'Gemini API' validate semantic relevance.
3. Storage : 'SQLite' store and delete duplicates.
4. Reporter : Generate interactive HTML page

## 📄 Licence
MIT

