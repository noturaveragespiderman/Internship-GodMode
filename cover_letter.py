import os
from google import genai
from google.genai import types
from config import PERPLEXITY_API_KEY, CV_TEXT_PATH

client = genai.Client(api_key=PERPLEXITY_API_KEY)
MODEL_ID = "gemini-2.0-flash"

def get_template(sector):
    safe_sector = "".join(c.lower() for c in sector if c.isalnum())
    template_path = f"templates/{safe_sector}.txt"
    
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()
            
    general_path = "templates/general.txt"
    if os.path.exists(general_path):
        with open(general_path, "r") as f:
            return f.read()
    return "Professional and direct."

def generate_cover_letter(record):
    with open(CV_TEXT_PATH, "r") as f:
        cv_text = f.read()

    style_guide = get_template(record.get("sector", "General"))

    prompt = f"""
    Write a personalized cover letter. You MUST strictly follow the structure, tone, and vocabulary of the GOLD STANDARD TEMPLATE below. 

    === GOLD STANDARD TEMPLATE ===
    {style_guide}
    
    === MY CV DATA ===
    {cv_text}

    === TARGET COMPANY ===
    Company: {record['company_name']}
    Context: {record.get('brief_description', '')}
    Recipient: {record.get('ind_a_name', 'Hiring Manager')}

    STRICT RULES:
    1. Mimic the SENTENCE STRUCTURE, PARAGRAPH COUNT, and LENGTH of the Gold Standard Template.
    2. Do NOT use generic AI buzzwords like "passionate," "synergy," or "tapestry."
    3. Use my CV data to swap out the placeholders in the template.
    4. Sign off exactly as: "Best regards, Leonardo Sommariva"
    
    Return ONLY the cover letter text.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID, 
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2)
    )
    return response.text.strip()

def generate_email_draft(record):
    prompt = f"""
    Write a short outreach email to {record.get('ind_a_name', 'Hiring Manager')} at {record['company_name']}.
    Name: Leonardo Sommariva.
    Rule: Maximum 5 sentences. Sign off with "Best regards, Leonardo Sommariva".
    
    Format:
    SUBJECT: Internship Inquiry - Leonardo Sommariva
    BODY: [email text]
    """
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return response.text.strip()
