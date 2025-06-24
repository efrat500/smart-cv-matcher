import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_job_from_url(url: str) -> dict:
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError(f"Failed to fetch URL: {res.status_code}")

    text = BeautifulSoup(res.text, "html.parser").get_text(separator="\n")

    prompt = f"""
    You are a helpful assistant. Extract the job posting details from the following text from a job listing page. \
    Output JSON exactly matching this schema:

    {{
    "title": "",
    "company": "",
    "location": "",
    "employment_type": "",
    "experience_level": "",
    "technologies": [],
    "description": "",
    "requirements": [],
    "nice_to_have": [],
    "salary_range": {{"min": null, "max": null, "currency": "ILS"}},
    "remote": false,
    "posted_date": "",
    "source": "{url}",
    "url": "{url}"
    }}

    Here is the page text:
    \"\"\"{text[:2000]}\"\"\"
    Only output JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You extract job data from webpage text."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    raw_json = response.choices[0].message.content.strip()

    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        raise ValueError(f"❌ Failed to parse JSON: {raw_json}")
    
from bson import ObjectId

def convert_objectid(data):
    if isinstance(data, dict):
        return {k: convert_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data
