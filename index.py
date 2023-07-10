import string
import requests
from bs4 import BeautifulSoup

states = [
    ["act", "Australian Capital Territory"],
    ["nsw", "New South Wales"],
    ["nt", "Northern Territory"],
    ["qld", "Queensland"],
    ["sa", "South Australia"],
    ["tas", "Tasmania"],
    ["vic", "Victoria"],
    ["wa", "Western Australia"],
]

base_utl = "https://auspost.com.au/locate/post-office/"
data = []
for state in states:
    url = base_utl + state[0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # iterate from a to z
    for letter in string.ascii_lowercase:
        target_class = "list-" + letter
        ul = soup.find("ul", {"class": target_class})
        for li in ul.find_all("li"):
            a = li.find("a")
            suburb_name = a.text
            suburb_url = a["href"]
            postcode = suburb_url.split("/")[-1]
            obj = {
                "postcode": postcode,
                "suburb": suburb_name,
                "state": state[1],
                "state_code": state[0].upper(),
            }
            data.append(obj)
# sort data by postcode
data = sorted(data, key=lambda k: k["postcode"])

# save in json file
import json

with open("data.json", "w") as outfile:
    json.dump(data, outfile)

# print the length of data
print(len(data))
