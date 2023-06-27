import base64
import json
import sys

import requests

# Construct HTTP request
payload = json.dumps({"speaker": "zh_female_qingxin"})
fn = "/home/netease/Codes/bertsearch/example/1687698395526.mp3"
with open(fn, "rb") as f:
    data = f.read()
    data = base64.b64encode(data).decode('utf-8')
req = {
    "appkey": "lyVwJjLmBb",
    "token": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc3MDIwODAsImlhdCI6MTY4NzY5ODQ4MCwiaXNzIjoiU0FNSSBNZXRhIiwidmVyc2lvbiI6InZvbGMtYXV0aC12MSIsImFjY291bnRfaWQiOjIxMDA1MDEwMzIsImFjY291bnRfbmFtZSI6IjIxMDA1MDEwMzIiLCJhcHBfaWQiOjI0ODQsImFwcF9uYW1lIjoi6L2s5LiA5LiqIiwiYXBwa2V5IjoibHlWd0pqTG1CYiIsInNlcnZpY2UiOiJzYW1pIiwic291cmNlIjoiQWNjb3VudCIsInJlZ2lvbiI6ImNuLW5vcnRoLTEifQ.jO0MlWiQg7p-ZLY_-E-tNNDlO0s4ci9YBu_MPmb-AMaJF8wam_jSDFY23wpw2E38L2TZDKssye1KCWkt3Yr6nQ",
    "namespace": "VoiceConversion",
    "payload": payload,
    "data": data
}

if __name__ == "__main__":
    # HTTP POST request
    resp = requests.post("https://sami.bytedance.com/api/v1/invoke", json=req)

    # Parse HTTP SAMI response
    try:
        sami_resp = resp.json()
        if resp.status_code != 200:
            print(sami_resp)
            sys.exit(1)
    except:
        print(resp)
        sys.exit(1)

    print("response task_id=%s status_code=%d status_text=%s" % (
        sami_resp["task_id"], sami_resp["status_code"], sami_resp["status_text"]), end=" ")
    if "payload" in sami_resp and len(sami_resp["payload"]) > 0:
        print("payload=%s" % sami_resp["payload"], end=" ")
    if "data" in sami_resp and len(sami_resp["data"]) > 0:
        # Save audio data into file
        data = base64.b64decode(sami_resp["data"])
        print("data=[%d]bytes" % len(data))
        with open(fn + ".wav", "wb") as f:
            f.write(data)
