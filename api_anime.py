import requests
import json
import xmltodict

response = requests.get("https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime=4658")
print(f"status : {response.status_code}")
xml_content = response.content

dictionary_content = xmltodict.parse(xml_content)
json_content = json.loads(json.dumps(dictionary_content, indent=4))

print(list(json_content["ann"]["anime"].keys()))
print(list(dictionary_content["ann"]["anime"].keys()))


print(len(dictionary_content["ann"]["anime"]["episode"]))






