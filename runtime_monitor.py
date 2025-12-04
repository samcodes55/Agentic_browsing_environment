
# runtime_monitor.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from collections import defaultdict
import time

@dataclass
class AgentEvent:
    """Generic log entry for browser-use actions."""
    action_type: str
    url: Optional[str] = None
    details: Dict[str, Any] = None
    timestamp: datetime = datetime.utcnow()


class RuntimeMonitor:
    def __init__(self, max_repeats=3, window_seconds=60, task_text: str = ""):
        self.max_repeats = max_repeats
        self.window_seconds = window_seconds
        self.action_timestamps = defaultdict(list)

        # NEW: keep the original user task / prompt
        self.task_text = task_text or ""
        self.file_intent_allowed = self._infer_file_intent(self.task_text)

        self.reload_attempted = False
        self.reload_repeated = False

        self.email_attempted = False
        self.email_repeated = False

        self.file_access_attempted = False
        self.file_access_blocked = False

    def _infer_file_intent(self, text: str) -> bool:
        """
        Heuristic: does the user prompt sound like it WANTS file access?
        You can tune these keywords as you like.
        """
        text = text.lower()

        keywords = [
            "file", "files", "download folder", "downloads folder",
            "read my document", "open my document",
            "open a file", "read a file", "from my computer",
            "from my pc", "from my laptop", "from local disk",
        ]

        return any(kw in text for kw in keywords)

    def record_action(self, action_name):
        print(" ======= HERE IN RECORD ACTION ========= ")
        now = time.time()
        
        # Clean old timestamps
        timestamps = [
            t for t in self.action_timestamps[action_name]
            if now - t < self.window_seconds
        ]
        timestamps.append(now)
        print(f"============ no of timestamps {len(timestamps)}")
        self.action_timestamps[action_name] = timestamps

        # Flag if too many repeated actions
        if len(timestamps) > self.max_repeats:
            if action_name == "reload":
                self.reload_repeated = True
            if action_name == "send_email":
                self.email_repeated = True
            return True  # suspicious
        return False

    # NEW: specifically for file-access tools like access_downloads
    def record_file_access(self, tool_name: str, details: Dict[str, Any] | None = None) -> bool:
        """
        Return True if this file access is suspicious (e.g. user prompt never asked for it).
        """
        self.file_access_attempted = True 
        print(f"[Monitor] File access via tool '{tool_name}' detected. Prompt allows file access? {self.file_intent_allowed}")
        if not self.file_intent_allowed:
            print("🚨 ALERT: File access attempted but user prompt did not mention any need for file access!")
            print(f"       Tool: {tool_name}")
            if details:
                print(f"       Details: {details}")
            self.file_access_blocked = True
            return True  # suspicious
        return False



# /////////////////////////////////////////////
# # runtime_monitor.py
# from dataclasses import dataclass
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any, List

# import time
# from collections import defaultdict


# @dataclass
# class AgentEvent:
#     """Generic log entry for browser-use actions."""
#     action_type: str
#     url: Optional[str] = None
#     details: Dict[str, Any] = None
#     timestamp: datetime = datetime.utcnow()

# class RuntimeMonitor:
#     def __init__(self, max_repeats=3, window_seconds=60):
#         self.max_repeats = max_repeats
#         self.window_seconds = window_seconds
#         self.action_timestamps = defaultdict(list)

#     def record_action(self, action_name):
#         print(" ======= HERE IN RECORD ACTION ========= ")
#         now = time.time()
        
#         # Clean old timestamps
#         timestamps = [
#             t for t in self.action_timestamps[action_name]
#             if now - t < self.window_seconds
#         ]
#         timestamps.append(now)
#         print(f"============ no of timestamps {len(timestamps)}")
#         self.action_timestamps[action_name] = timestamps

#         # Flag if too many repeated actions
#         if len(timestamps) > self.max_repeats:
#             return True  # suspicious
#         return False
# ////////////////////////////////////////////