import os,requests

for file in os.listdir("/data/feedback"):
    if not file.endswith(".txt"):
        continue
    
    with open(os.path.join("/data/feedback", file),"r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        diir={
        "title":lines[0],
        "name":lines[1],
        "date":lines[2],
        "feedback": " ".join(lines[3:])
        }
        res = requests.post("http://34.139.177.248/feedback",json=diir)
        
        print("Status:", res.status_code)
        print("Response:", res.text)
