import requests
import os
import uuid

#Configuration
CONFIG_FILE = "data/ntfy_topic.txt"

def get_or_create_topic():
    """
    Get the Ntfy key or generate a new one
    """

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            topic = f.read().strip()
            if topic:
                return topic
    
    unique_id = str(uuid.uuid4())[:8]
    new_topic = f"job_Hunter_{unique_id}"

    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(new_topic)

    print(f"\n📢 --- CONFIGURATION NTFY ---")
    print(f"A new Ntfy canal has been generated for this automation.")
    print(f"👉 Subscribe to this canal on the Ntfy app : {new_topic}")
    print(f"----------------------------\n")

    return new_topic



def send_notification(new_count, top_jobs=None):
    """
    Send a push notification with notify.sh
    """
    if new_count == 0:
        return
    
    topic = get_or_create_topic()
    base_url= f"https://ntfy.sh/{topic}"

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
        print(f"🔔 Notification sent on ntfy.sh/{topic}")
    except Exception as e:
        print(f"⚠️ Error notification Ntfy : {e}")

#rapid_test
if __name__ == "__main__":
    current_topic = get_or_create_topic()
    print(f"Canal generated: {current_topic}")
    send_notification(5, [{"title": "Test_job", "company": "Google"}])