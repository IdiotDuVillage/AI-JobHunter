import os
import re
import webbrowser
import markdown
from src.storage import JobDataBase

def clean_job_description(text):
    if not text:
        return ""

    # 1. Keywords list triggering ":" 
    headers = [
        "Type", "Compensation", "Location", "Duration", "Commitment", 
        "Role", "Responsibilities", "Requirements", "Profile", "Profil", 
        "Description", "Missions", "Compétences", "About", "A propos"
    ]
    
    for header in headers:
        pattern = r'(?<!\n)\s+(' + header + r'\s*:)'
        text = re.sub(pattern, r'\n\n\1', text)

    text = re.sub(r'(?<!\n)\s+(\*|-)\s+', r'\n* ', text)
    
    return text

def generate_report(open_browser=True):
    db = JobDataBase()
    #Retrieve the last 100 offers for the grid-view
    jobs = db.get_recent_jobs(limit=100)

    if not jobs:
        print("No Jobs, just 'traverse la rue' ")
        return
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport Job Hunter</title>
        <style>
            :root {{
                --bg-color: #f0f2f5;
                --card-bg: #ffffff;
                --primary: #0a66c2;
                --text-main: #1a1a1a;
                --text-secondary: #666;
            }}
            
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background-color: var(--bg-color); margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            
            /* Header & Controls */
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; gap: 15px; }}
            h1 {{ color: var(--text-main); margin: 0; font-size: 1.8rem; }}
            
            .view-controls button {{
                padding: 8px 16px; border: none; background: #e1e4e8; cursor: pointer; border-radius: 6px; font-weight: 600; color: #444; transition: 0.2s;
            }}
            .view-controls button.active {{ background: var(--primary); color: white; }}
            .view-controls button:hover:not(.active) {{ background: #d0d7de; }}

            /* Layouts */
            #jobs-container {{ display: flex; flex-direction: column; gap: 20px; }}
            #jobs-container.grid-view {{
                display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); align-items: start;
            }}            

            /* Card Styles */
            .job-card {{ 
                background: var(--card-bg); border-radius: 12px; padding: 20px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid var(--primary);
                transition: transform 0.2s, box-shadow 0.2s;
                display: flex; flex-direction: column;
            }}
            .job-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0,0,0,0.1); }}
            
            .header {{ margin-bottom: 15px; }}
            .title {{ font-size: 1.1em; font-weight: 700; color: #333; margin-bottom: 5px; line-height: 1.4; }}
            .company {{ color: #555; font-weight: 600; }}
            .meta {{ font-size: 0.85em; color: #888; margin-top: 8px; display: flex; flex-wrap: wrap; gap: 10px; }}
            
            .tag {{ background: #eef3f8; color: #555; padding: 3px 8px; border-radius: 4px; }}
            .tag.new {{ background: #d1fae5; color: #065f46; border: 1px solid #10b981; }}

            /* --- DESCRIPTION FORMATTING (Markdown Styles) --- */
            details {{ margin-top: auto; background: #f8f9fa; border-radius: 8px; overflow: hidden; border: 1px solid #eee; }}
            summary {{ 
                padding: 12px; cursor: pointer; color: var(--primary); font-weight: 600; user-select: none; font-size: 0.9em;
                background: #f1f3f5;
            }}
            summary:hover {{ background: #e9ecef; }}
            
            .desc-content {{ 
                padding: 15px; 
                font-size: 0.95em; color: #444; line-height: 1.6;
                
                max-height: 400px; overflow-y: auto;
            }}
            /* Style pour le HTML généré depuis le Markdown */
            .desc-content h1, .desc-content h2, .desc-content h3 {{ font-size: 1.1em; color: #333; margin-top: 15px; margin-bottom: 5px; }}
            .desc-content ul, .desc-content ol {{ margin-top: 10x; margin-bottom: 10px; padding-left: 25px; }}
            .desc-content li {{ margin-bottom: 5px; list-style-type: disc; }}
            .desc-content strong {{ color: #000; }}
            .desc-content p {{ margin-bottom: 15px; }}

            .actions {{ margin-top: 15px; text-align: right; }}
            .btn-apply {{ 
                display: inline-block; background-color: var(--primary); color: white; text-decoration: none; 
                padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.9em; transition: background 0.3s;
            }}
            .btn-apply:hover {{ background-color: #004182; }}
            .btn-disabled {{ background-color: #ccc; cursor: not-allowed; pointer-events: none; }}

        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <h1>🎯 ({len(jobs)}) New jobs !</h1>
                <div class="view-controls">
                    <button onclick="setView('list')" id="btn-list" class="active">List</button>
                    <button onclick="setView('grid')" id="btn-grid">Grid</button>
                </div>
            </div>

            <div id="jobs-container" class="list-view">
    """

    for job in jobs:
        final_url = job['url']
        is_disabled = True
        if final_url and len(final_url) > 5:
            if final_url.startswith('/'): final_url = "https://www.linkedin.com" + final_url
            elif not final_url.startswith('http'): final_url = "https://" + final_url
            
            if not ("," in final_url and "http" not in final_url):
                is_disabled = False
        #Styles based on sources
        source_lower = job['source'].lower()
        border_color = "#0a66c2"
        if "indeed" in source_lower: border_color = "#2557a7"
        elif "glassdoor" in source_lower: border_color = "#0caa41"

        #New Icon
        is_new_badge = '<span class="tag new">✨ NEW</span>' if job['is_new'] else ''

        #Description
        desc_block = ""
        raw_desc = job['description']
        
        if raw_desc and len(raw_desc) > 10:
            cleaned_desc = clean_job_description(raw_desc)
            #Markdown is converted in HTML
            html_desc = markdown.markdown(cleaned_desc, extensions=['nl2br'])
            
            desc_block = f"""
            <details>
                <summary>Lire la description</summary>
                <div class="desc-content">{html_desc}</div>
            </details>
            """
        else:
             desc_block = "<div style='padding:10px; color:#999; font-style:italic;'>Pas de description</div>"
        
        btn_html = f'<a href="{final_url}" target="_blank" class="btn-apply">Postuler</a>' if not is_disabled else '<a class="btn-apply btn-disabled">Lien HS</a>'        
        
        html_content += f"""
        <div class="job-card" style="border-left-color: {border_color}">
            <div class="header">
                <div>
                    <div class="title">{job['title']} {is_new_badge}</div>
                    <div class="company">🏢 {job['company']}</div>
                    <div class="meta">
                        <span>📍 {job['location']}</span>
                        <span>📅 {job['date_found'][:16]}</span>
                        <span class="tag">{job['source']}</span>
                    </div>
                </div>
            </div>

            {desc_block}

            <div class="actions">
                {btn_html}
            </div>
        </div>
        """
    
    html_content += """
            </div> </div> <script>
            function setView(view) {
                const container = document.getElementById('jobs-container');
                const btnList = document.getElementById('btn-list');
                const btnGrid = document.getElementById('btn-grid');
                
                if (view === 'grid') {
                    container.classList.add('grid-view');
                    container.classList.remove('list-view');
                    btnGrid.classList.add('active');
                    btnList.classList.remove('active');
                } else {
                    container.classList.add('list-view');
                    container.classList.remove('grid-view');
                    btnList.classList.add('active');
                    btnGrid.classList.remove('active');
                }
                
                // Save User preferences
                localStorage.setItem('jobHunterView', view);
            }

            // Load Users preference at launch
            document.addEventListener('DOMContentLoaded', () => {
                const savedView = localStorage.getItem('jobHunterView');
                if (savedView === 'grid') {
                    setView('grid');
                }
            });
        </script>
    </body>
    </html>
    """
    #Saving
    report_path = os.path.abspath("daily_report.html")
    with open(report_path, 'w', encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Report generated at : {report_path}")

    db.mark_as_seen()
    db.close()

    if open_browser:
        webbrowser.open(f"file://{report_path}")

if __name__ == "__main__":
    generate_report()
