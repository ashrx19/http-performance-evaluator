import os

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    TESTING = os.getenv("TESTING", "False") == "True"
    ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", 2.0))  # seconds
    REPEAT_COUNT = int(os.getenv("REPEAT_COUNT", 3))  # number of times to repeat the benchmark
    TARGET_URL = os.getenv("TARGET_URL", "http://www.example.com")  # default target URL for benchmarking
    HTTP1_ENABLED = os.getenv("HTTP1_ENABLED", "True") == "True"
    HTTP2_ENABLED = os.getenv("HTTP2_ENABLED", "True") == "True"