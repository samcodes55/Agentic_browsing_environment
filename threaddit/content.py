import requests, time, sys

BASE = "http://localhost:5173"  # or backend port if different
EMAIL = "26100218@lums.edu.pk"
PASSWORD = "12345678"

S = requests.Session()
S.headers.update({"User-Agent": "threaddit-seeder/1.0"})

def login():
    print("[LOGIN] JSON login...")
    r = S.post(f"{BASE}/api/user/login", json={"email": EMAIL, "password": PASSWORD})
    print("[LOGIN] status:", r.status_code)
    print("[LOGIN] cookies:", S.cookies.get_dict())
    
    if "session" not in S.cookies.get_dict():
        print("❌ No session cookie. Login failed.")
        sys.exit(1)
    
    print("✅ Login OK")

def create_thread(name, description):
    print(f"[THREAD] Creating: {name}")

    # EXACT FORM FIELDS FROM YOUR BROWSER
    data = {
        "name": name,
        "content_type": "image",
        "content_url": "",
        "description": description
    }

    r = S.post(f"{BASE}/api/thread", data=data, files={})
    print("[THREAD] status:", r.status_code, "|", r.text[:200])
    
    try:
        j = r.json()
        tid = j.get("id") or j.get("thread_id")
    except:
        tid = None

    if not tid:
        print("❌ Thread creation failed.")
        return None
    
    print(f"✅ Thread ID = {tid}")
    return tid

def create_post(thread_id, title, content):
    if not thread_id:
        return
    
    print(f"[POST] -> {title}")
    
    # MIMIC NEWPOST.JSX DEFAULTS
    data = {
        "title": title,
        "content": content,
        "content_type": "media",
        "content_url": "",
        "subthread_id": thread_id
    }

    r = S.post(f"{BASE}/api/post", data=data, files={})
    print("[POST] status:", r.status_code, "|", r.text[:200])

def main():
    login()

    THREADS = {
        "MachineLearning": "All things ML",
        "AgenticBrowsing": "AI agents browsing the web",
        "StudentLife": "Uni advice",
    }

    POSTS = [
        ("How to learn ML fast?", "Which courses are best for ML beginners?"),
        ("What are agentic AI systems?", "Examples of autonomous web agents?"),
        ("Study hacks?", "How do you manage stress during exams?"),
    ]

    for name, desc in THREADS.items():
        tid = create_thread(name, desc)
        time.sleep(0.2)
        for i in range(3):
            title, content = POSTS[i]
            create_post(tid, f"{title} #{i+1}", content)
            time.sleep(0.15)

if __name__ == "__main__":
    main()
