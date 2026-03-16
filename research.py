import json
import re
import time
from google import genai
from google.genai import types
from config import PERPLEXITY_API_KEY 

client = genai.Client(api_key=PERPLEXITY_API_KEY)
MODEL_ID = "gemini-2.0-flash"

search_tool = types.Tool(google_search=types.GoogleSearch())

def clean_json(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def call_gemini_with_retry(prompt, config, retries=3, delay=35):
    """Helper to handle 429 Resource Exhausted errors by waiting."""
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=config
            )
            return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"⚠️ Rate limit hit. Waiting {delay}s before retry {i+1}/{retries}...")
                time.sleep(delay)
            else:
                raise e
    raise Exception("Max retries exceeded for Gemini API")

def get_company_basics(company_name, website):
    prompt = f"""
    Search the live web for the company '{company_name}' ({website}).
    1. Write a brief 2-sentence description of what they do.
    2. Search for 1-2 recent news items or milestones from the last few months.
    3. Categorize their primary sector.
    4. Find their main Careers page URL.
    5. Provide the URL of the primary article used for the news.
    
    Return ONLY valid JSON with EXACTLY these keys: 
    "brief_description", "sector", "career_page_link", "source_link".
    """
    
    config = types.GenerateContentConfig(
        temperature=0.1,
        tools=[search_tool] 
    )
    
    response = call_gemini_with_retry(prompt, config)
    return json.loads(clean_json(response.text))

def find_key_people(company_name, website):
    prompt = f"""
    Search for two key hiring/talent individuals at '{company_name}' ({website}).
    Return ONLY valid JSON with keys: 
    "ind_a_name", "ind_a_role", "ind_a_email", "ind_a_linkedin",
    "ind_b_name", "ind_b_role", "ind_b_email", "ind_b_linkedin".
    """
    
    config = types.GenerateContentConfig(
        temperature=0.1,
        tools=[search_tool]
    )
    
    response = call_gemini_with_retry(prompt, config)
    return json.loads(clean_json(response.text))

def find_specific_people(company_name, website, specific_input):
    prompt = f"""
    Search for professional details at '{company_name}' ({website}) for: {specific_input}.
    Return ONLY valid JSON with keys: 
    "ind_a_name", "ind_a_role", "ind_a_email", "ind_a_linkedin",
    "ind_b_name", "ind_b_role", "ind_b_email", "ind_b_linkedin".
    """
    
    config = types.GenerateContentConfig(
        temperature=0.1,
        tools=[search_tool]
    )
    
    response = call_gemini_with_retry(prompt, config)
    return json.loads(clean_json(response.text))
