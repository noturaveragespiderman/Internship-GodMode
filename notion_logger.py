from notion_client import Client
from config import NOTION_TOKEN, NOTION_DATABASE_ID
from datetime import datetime

def log_to_notion(record):
    notion = Client(auth=NOTION_TOKEN)

    properties = {}

    def set_rich_text(value):
        return {"rich_text": [{"text": {"content": str(value or "")}}]}

    def set_url(value):
        return {"url": str(value)} if value else {"url": None}

    def set_email(value):
        return {"email": str(value)} if value else {"email": None}

    properties["Brief Description"]     = set_rich_text(record.get("brief_description") or record.get("company_name", ""))
    properties["Career Page Link"]      = set_url(record.get("career_page_link"))
    properties["Individual A Name"]     = set_rich_text(record.get("ind_a_name"))
    properties["Individual A Role"]     = set_rich_text(record.get("ind_a_role"))
    properties["Individual A Email"]    = set_email(record.get("ind_a_email"))
    properties["Individual A LinkedIn"] = set_url(record.get("ind_a_linkedin"))
    properties["Individual B Name"]     = set_rich_text(record.get("ind_b_name"))
    properties["Individual B Role"]     = set_rich_text(record.get("ind_b_role"))
    properties["Individual B Email"]    = set_email(record.get("ind_b_email"))
    properties["Individual B LinkedIn"] = set_url(record.get("ind_b_linkedin"))
    properties["Cover Letter"]          = set_rich_text(record.get("cover_letter"))
    properties["Email Sent"]            = set_rich_text(record.get("email_body"))
    properties["Date Sent"]             = {"date": {"start": datetime.now().isoformat()}}
    properties["Status"]                = {"select": {"name": "Sent"}}

    # If we have a Notion page ID, update the existing row
    if record.get("notion_page_id"):
        notion.pages.update(
            page_id=record["notion_page_id"],
            properties=properties
        )
    else:
        # Fallback: create a new row if no page ID exists
        properties["Company Name"] = {
            "title": [{"text": {"content": record.get("company_name", "")}}]
        }
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=properties
        )
