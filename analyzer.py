from fastapi import APIRouter
from models import JobLink, jobdescription
from google import genai
from config_secrets import whois_api_key
import json
from fastapi.responses import HTMLResponse,JSONResponse
import re
from config_secrets import My_API_KEY
from typing import Optional
from google.genai import types
import dns.resolver
from bs4 import BeautifulSoup
import requests
import html
from urllib.parse import urlparse

router = APIRouter(prefix='/analyzer')

def clean_text_for_json(text):
    if not text:
        return ""
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = html.unescape(text.strip())
    text = text.replace('\\', '\\\\').replace('"', '\\"')
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    return text

def check_mx_record(domain):
    print("step2")
    try:
        answers = dns.resolver.resolve(domain, "MX")
        mx_records = [f"{r.preference} {r.exchange.to_text()}" for r in answers]
        return {"has_mx": True, "mx_records": mx_records}
    except dns.resolver.NoAnswer:
        return {"has_mx": False, "mx_records": "No MX records"}
    except dns.resolver.NXDOMAIN:
        return {"has_mx": False, "error": "Domain doesn't exist"}
    except Exception as e:
        return {"has_mx": False, "error": str(e)}

def whoisapi(link):
    try:
        api_key = whois_api_key
        response = requests.get("https://www.whoisxmlapi.com/whoisserver/WhoisService", params={
            "apiKey": api_key,
            "domainName": link,
            "outputFormat": "JSON"
        })
        data = response.json()
        return extract_scamsignals_from_whois(data)
    except Exception as e:
        print("Error parsing WHOIS JSON:", e)
        return {}

def extract_scamsignals_from_whois(my_data: dict) -> dict:

    whois = my_data.get("WhoisRecord", {})
    registry = whois.get("registryData", {})
    registrant = registry.get("registrant", {})
    name_servers = registry.get("nameServers", {}).get("hostNames", [])
    return {
        "domainName": whois.get("domainName"),
        "createdDate": registry.get("createdDate"),
        "expiresDate": registry.get("expiresDate"),
        "estimatedDomainAge": whois.get("estimatedDomainAge"),
        "registrar": whois.get("registrarName"),
        "registrantOrganization": registrant.get("organization"),
        "registrantCountry": registrant.get("country"),
        "status": registry.get("status"),
        "nameServers": name_servers,
        "contactEmail": whois.get("contactEmail"),
        "whoisServer": registry.get("whoisServer"),
    }

def analyzing_job_description(job_description: str, mx_record: Optional[dict] = None, whois_data: Optional[dict] = None):
    print("FRkking came here")
    client = genai.Client(api_key=My_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        You are an expert at detecting scam job listings. Analyze the job description and output raw JSON.
        --- Job Description ---
        {job_description}
        --- MX Record ---
        {mx_record}
        --- WHOIS Info ---
        {whois_data}
        Respond with ONLY a JSON object in this format:
        {{
          "Scam_Verdict": "Yes/No",
          "Trust_Score": 0-100,
          "Reasoning": ["reason 1", "reason 2", "..."],
          "Suggestions": ["suggestion 1", "suggestion 2", "..."]
        }}
        """,
        config=types.GenerateContentConfig(
            system_instruction="Reply in pure JSON only. No code blocks, no comments.",
            max_output_tokens=1000,
            temperature=0.1
        )
    )
    raw = response.text.strip()
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        result = json.loads(cleaned)
        print(json.dumps(result, indent=4))
        return result
    except Exception as e:
        print("Error while parsing JSON:", e)
        return {"error": "Invalid response from LLM", "raw_response": raw}

@router.post('/analyze_text')
def analyze_text(jobtextinput: jobdescription):
    return analyzing_job_description(jobtextinput.description)

@router.post('/scrape_site')
def scrape_site(link: JobLink):
    print('Step1')

    # my_data={
    #     "Scam_Verdict": "No",
    #     "Trust_Score": 100,
    #     "Reasoning": [
    #         "The domain is google.com, a well-established and reputable company.",
    #         "The MX record points to smtp.google.com, confirming its legitimacy.",
    #         "WHOIS information shows a long history and valid registration details."
    #     ],
    #     "Suggestions": []
    # }
    # return my_data
    url = str(link.url)
    print(url)
    response = requests.get(url)
    my_soup = BeautifulSoup(response.text, "html.parser")
    domain = urlparse(url).netloc
    formatted_output = [f"Domain: {domain}"]

    for t in my_soup.find_all(['h1', 'h2']):
        cleaned_title = clean_text_for_json(t.text)
        if cleaned_title:
            formatted_output.append(f"Title: {cleaned_title}")

    for p in my_soup.find_all('p'):
        cleaned_para = clean_text_for_json(p.text)
        if cleaned_para and len(cleaned_para) > 20:
            formatted_output.append(f"Paragraph: {cleaned_para}")

    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", my_soup.text))
    for email in emails:
        cleaned_email = clean_text_for_json(email)
        formatted_output.append(f"Email: {cleaned_email}")

    final_string = "\n".join(formatted_output)


    mx_record = check_mx_record(domain)
    whois_data = whoisapi(domain)
    result = analyzing_job_description(final_string, mx_record, whois_data)
    # print(type({"my_result":result}))
    print(type(result))
    print("ABOUT TO SEND FINALLLl")
    return analyzing_job_description(final_string, mx_record, whois_data)

    # return JSONResponse(content={"my_data": analyzing_job_description(final_string,mx_record,whois_data)})
    # return analyzing_job_description(final_string, mx_record, whois_data)
