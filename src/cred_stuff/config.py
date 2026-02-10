"""Credential Stuffing Config"""
TARGET_URL = ""
THREADS = 10
DELAY = 0.5
PROXY_LIST = []
USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"]
MAX_RETRIES = 3
SUCCESS_INDICATORS = ["dashboard", "welcome", "logout", "my-account"]
FAILURE_INDICATORS = ["invalid", "incorrect", "failed", "error"]
SAFE_MODE = True
