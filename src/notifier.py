import requests

#Configuration
NTFY_TOPIC = "Job_hunter_report_Antoine_Bochet"

def send_notification(new_count, top_jobs=None):
    """
    Send a push notification with notify.sh
    """
    if new_count == 0:
        return
    
    base_url= f"https://ntfy.sh/{NTFY_TOPIC}"

    #Constructing message
    title = f"🎯 {new_count} New opportunities !"
    message = f"Job Hunter has completed his patrol 🫡."

    if top_jobs:
        message += "\nTop offers :"
        for i, job in enumerate(top_jobs[:3]):
            message += f"\n- {job['title']} ({job['company']})"
    
    message += "\n\nOpen Computer to see complete report."

    try:
        requests.post(base_url,
            data=message.encode(encoding='utf-8'),
            headers={
                "Title": title.encode(encoding="utf-8"),
                "Priority": "default",
                "Tags": "briefcase"
            }
        )
        print(f"🔔 Notification sent on ntfy.sh/{NTFY_TOPIC}")
    except Exception as e:
        print(f"⚠️ Error notification Ntfy : {e}")

#rapid_test
if __name__ == "__main__":
    send_notification(5, [{"title": "Test_job", "company": "Google"}])