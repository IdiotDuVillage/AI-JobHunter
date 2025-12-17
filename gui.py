import streamlit as st
import os
from dotenv import load_dotenv, set_key
import subprocess
import threading
import queue

st.set_page_config(page_title='AI Job Hunter', page_icon="🕵️‍♂️", layout='wide')

FILES = {
    "keywords": "data/keywords.txt",
    "countries": "data/countries.txt",
    "proxies": "data/proxies.txt",
    "prompt_gemini": "data/prompt_gemini.txt",
    "prompt_local": "data/prompt_local.txt",
    "env": ".env"
}

#--- Files management ---
def load_file(filepath):
    """read a text file"""
    if not os.path.exists(filepath): return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def save_file(filepath, content):
    """Save a text file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def save_env_var(key, value):
    """Upgrade .env file"""
    if not os.path.exists(".env"):
        open(".env", "a").close() # create .env if not found
    set_key(".env", key, value)

# --- HEADER ---
st.title("🕵️‍♂️ AI Job Hunter - Control center")
st.markdown("---")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Manual Launch", "📝 Criteria", "⚙️ AI Configuration", "🤖 Developper"])

# --- TAB 1 ---
with tab1 : 
    st.header("Launching AI Job Hunter")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.info("Click to launch the agent. Search can take a while (several minutes)")
        if st.button("▶️ Send 🕵️‍♂️ AI Job Hunter on Watch", type="primary", use_container_width=True):
            with st.spinner("Job Hunter is looking through offers..."):
                # Launching main.py and recovering logs
                process = subprocess.Popen(
                    ["python", "main.py"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True,
                    encoding='utf-8'
                )
                
                log_placeholder = st.empty()
                logs = ""
                
                # Logs reading
                for line in iter(process.stdout.readline, ''):
                    logs += line
                    log_placeholder.code(logs, language="bash")
                
                process.stdout.close()
                return_code = process.wait()
                
                if return_code == 0:
                    st.success("✅ 🕵️‍♂️ AI Job Hunter finished its watch ! Report has been generated.")
                    if os.path.exists("daily_report.html"):
                        with open("daily_report.html", "rb") as file:
                            st.download_button("📥 Download HTML Report", file, file_name="daily_report.html", mime="text/html")
                else:
                    st.error("❌ An error has occured.")

    with col2:
        st.subheader("Last report")
        if os.path.exists("daily_report.html"):
            st.success("A report is available, open it in a navigator.")
        else:
            st.warning("No report generated yet.")

# --- TAB 2: CRITERIA (Keywords & Pays) ---
with tab2:
    col_k, col_c = st.columns(2)
    
    with col_k:
        st.subheader("🔎 Keywords")
        st.caption("One by line")
        k_content = st.text_area("Keywords", value=load_file(FILES["keywords"]), height=300, label_visibility="collapsed")
        if st.button("Save keywords"):
            save_file(FILES["keywords"], k_content)
            st.toast("Keywords saved !", icon="✅")

    with col_c:
        st.subheader("🌍 Targetted countries")
        st.caption("One by line (YOU MUST USE THE ENGLISH NAME ex: France, Switzerland)")
        c_content = st.text_area("Countries", value=load_file(FILES["countries"]), height=300, label_visibility="collapsed")
        if st.button("Save countries"):
            save_file(FILES["countries"], c_content)
            st.toast("Countries saved !", icon="✅")

# -- TAB 3: CONFIGURATION AI (.env) ---
with tab3 :
    st.header("IA Brain")
    load_dotenv() # Recharge les vars
    
    provider = st.selectbox(
        "AI model (Provider)", 
        options=["hybrid", "ollama", "gemini"], 
        index=["hybrid", "ollama", "gemini"].index(os.getenv("LLM_PROVIDER", "hybrid"))
    )
    
    api_key = st.text_input("Goggle API key (for hybrid and gemini mode)", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    local_model = st.text_input("Local Ollama model", value=os.getenv("LOCAL_MODEL", "llama3.2"))
    
    if st.button("Save Configuration"):
        save_env_var("LLM_PROVIDER", provider)
        save_env_var("GEMINI_API_KEY", api_key)
        save_env_var("LOCAL_MODEL", local_model)
        st.success("Configuration updated ! Relaunch the app !")
    
    # --- TAB 4: Developpers (Prompts & Proxies) ---
with tab4:
    st.warning("Prompts and proxies setting")
    
    with st.expander("🛠️ Proxies"):
        p_content = st.text_area("Proxies (user:pass@ip:port)", value=load_file(FILES["proxies"]))
        if st.button("Save Proxies"):
            save_file(FILES["proxies"], p_content)
            st.toast("Proxies saved")
            
    with st.expander("🧠 Prompt Gemini (Cloud)"):
        pg_content = st.text_area("Prompt Gemini", value=load_file(FILES["prompt_gemini"]), height=200)
        if st.button("Save Prompt Cloud"):
            save_file(FILES["prompt_gemini"], pg_content)
            st.toast("Prompt Cloud saved")

    with st.expander("🧠 Prompt Ollama (Local)"):
        pl_content = st.text_area("Prompt Local", value=load_file(FILES["prompt_local"]), height=200)
        if st.button("Save Prompt Local"):
            save_file(FILES["prompt_local"], pl_content)
            st.toast("Prompt Local saved")