import os
import webbrowser
from src.storage import JobDataBase

def generate_report(open_browser=True):
    db = JobDataBase()

    #REtrieve the last 50 offers, not just the new ones
    new_jobs = db.get_recent_jobs()

    if not new_jobs:
        print("No New jobs")
        return
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Rapport Job Hunter</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            h1 {{ color: #1a1a1a; text-align: center; margin-bottom: 30px; }}
            
            .job-card {{ 
                background: white; 
                border-radius: 12px; 
                padding: 20px; 
                margin-bottom: 20px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
                border-left: 5px solid #0a66c2; /* Bleu LinkedIn par défaut */
                transition: transform 0.2s;
            }}
            .job-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); }}
            
            .header {{ display: flex; justify-content: space-between; align-items: start; }}
            .title {{ font-size: 1.25em; font-weight: bold; color: #333; margin: 0; }}
            .company {{ color: #666; font-weight: 600; margin-top: 5px; }}
            .meta {{ font-size: 0.9em; color: #888; margin-top: 5px; display: flex; gap: 15px; }}
            
            .tag {{ 
                background: #eef3f8; color: #666; padding: 4px 8px; 
                border-radius: 4px; font-size: 0.8em; font-weight: bold;
            }}
            .tag.new {{ background: #d1fae5; color: #065f46; border: 1px solid #10b981; }}
            .tag.indeed {{ border-left-color: #2557a7; }}
            .tag.glassdoor {{ border-left-color: #0caa41; }}

            .actions {{ margin-top: 15px; display: flex; gap: 10px; align-items: center; }}
            
            .btn-apply {{ 
                background-color: #0a66c2; color: white; text-decoration: none; 
                padding: 10px 20px; border-radius: 20px; font-weight: bold; font-size: 0.9em;
                transition: background 0.3s;
            }}
            .btn-apply:hover {{ background-color: #004182; }}
            
            details {{ margin-top: 15px; background: #fafafa; padding: 10px; border-radius: 8px; }}
            summary {{ cursor: pointer; color: #0a66c2; font-weight: 600; outline: none; }}
            .desc-text {{ white-space: pre-wrap; font-size: 0.9em; color: #444; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 {len(new_jobs)} New jobs found !</h1>
    """

    for job in new_jobs:
        final_url = job['url']
        if final_url:
            #Case 1 linkedin
            if final_url.startswith('/'):
                final_url = "https://www.linkedin.com" + final_url
            
            #Case2 link without protocol
            elif not final_url.startswith('http'):
                final_url = "https://" + final_url
        else :
            final_url = "#"
        #Styles based on sources
        source_lower = job['source'].lower()
        border_color = "#0a66c2"
        if "indeed" in source_lower: border_color = "#2557a7"
        elif "glassdoor" in source_lower: border_color = "#0caa41"

        #New Icon
        is_new_badge = '<span class="tag new">✨ NEW</span>' if job['is_new'] else ''

        #Description
        desc_html = ""
        if job['description'] and len(job['description']) > 10:
            desc_html = f"""
            <details>
                <summary>See description</summary>
                <div class="desc-text">{job['description']}</div>
            </details>
            """
        else : 
            desc_html = "<div style='margin-top:10px; color:#999; font-style:italic; font-size:0.9em'>Pas de description disponible</div>"

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

            {desc_html}

            <div class="actions">
                <a href="{final_url}" target="_blank" class="btn-apply">Voir l'offre ➔</a>
            </div>
        </div>
        """
    
    html_content += "</body></html>"


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
