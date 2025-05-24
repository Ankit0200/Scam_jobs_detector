import requests

url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
api_key = "at_vcTUbUSGlDdjy4fPNJ7TjDeMKZy28"

params = {
    "apiKey": api_key,
    "domainName": "https://prodigyinfotech.dev/",
    "outputFormat": "JSON"
}

response = requests.get(url, params=params)

# print("Status Code:", response.status_code)
# print("Raw Text Response:", response.text)

try:
    data = response.json()
    print("Parsed JSON:", data)
except Exception as e:
    print("Error parsing JSON:", e)

import dns.resolver

# def check_mx_record(domain):
#     try:
#         answers=dns.resolver.resolve(domain,"MX")
#
#         mx_records = [f"{r.preference} {r.exchange.to_text()}" for r in answers]
#
#         return {
#             "has_mx":True,
#             "mx_records":mx_records
#         }
#     except dns.resolver.NoAnswer:
#         return {"has_mx":False
#                 ,
#                 "mx_records":"No MX records"}
#     except dns.resolver.NXDOMAIN:
#         return {"has_mx":False,
#                 "error":"Domain doesn't exist"}
#     except Exception as e:
#         return {"has_mx":False,
#                 "error":str(e)
#                 }
# my mx checked data





