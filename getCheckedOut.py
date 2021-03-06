import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os

load_dotenv(".env")

s = requests.Session()

r = s.get("https://kcls.bibliocommons.com/user/login", verify=False)

payload = {
    "name": os.environ.get("KCLS_USER"),
    "user_pin": os.environ.get("PIN")
}

p = s.post("https://kcls.bibliocommons.com/user/login", data=payload)
r = s.get("https://kcls.bibliocommons.com/checkedout/index/out")
soup = BeautifulSoup(r.text, "html.parser")
checkedOutList = soup.find("div", { "class": "cp_bib_list" })

checkedOutItems = []

for title in checkedOutList.find_all("div", { "class": "listItem" }):
    title_name = title.find("span", { "class": "title" })
    due_date = title.find("span", { "class": "checkedout_status" })

    checkedOutItems.append({ "title": title_name.text.strip(), "due": due_date.text.strip() })

with open("checkedout.json", "w") as f:
    print "%d title(s) checked out" % len(checkedOutItems)
    f.write(json.dumps(checkedOutItems))
