from notion_client import Client
from config import NOTION_TOKEN, NOTION_DATABASE_ID

notion = Client(auth=NOTION_TOKEN)

def get_new_companies(last_processed_id: set):
    results = notion.databases.query(
        database_id=NOTION_DATABASE_ID,
        filter={
            "property": "Status",
            "select": {"equals": "New"}
        }
    ).get("results", [])

    new_entries = []
    for page in results:
        page_id = page["id"]
        if page_id in last_processed_id:
            continue
        props = page["properties"]

        def get_text(prop):
            items = props.get(prop, {}).get("rich_text", [])
            return items[0]["text"]["content"] if items else ""

        def get_title(prop):
            items = props.get(prop, {}).get("title", [])
            return items[0]["text"]["content"] if items else ""

        def get_url(prop):
            return props.get(prop, {}).get("url") or ""

        def get_email(prop):
            return props.get(prop, {}).get("email") or ""

        new_entries.append((page_id, {
            "Company Name":        get_title("Company Name"),
            "Website":             get_url("Website"),
            "Brief Description":   get_text("Brief Description"),
            "Individual A Name":   get_text("Individual A Name"),
            "Individual A Role":   get_text("Individual A Role"),
            "Individual A Email":  get_email("Individual A Email"),
            "Individual A LinkedIn": get_url("Individual A LinkedIn"),
            "Individual B Name":   get_text("Individual B Name"),
            "Individual B Role":   get_text("Individual B Role"),
            "Individual B Email":  get_email("Individual B Email"),
            "Individual B LinkedIn": get_url("Individual B LinkedIn"),
        }))

    return new_entries


def update_notion_row(page_id: str, data: dict):
    properties = {}

    field_map = {
        "Brief Description":     ("rich_text", "brief_description"),
        "Career Page Link":      ("url", "career_page_link"),
        "Individual A Name":     ("rich_text", "ind_a_name"),
        "Individual A Role":     ("rich_text", "ind_a_role"),
        "Individual A Email":    ("email", "ind_a_email"),
        "Individual A LinkedIn": ("url", "ind_a_linkedin"),
        "Individual B Name":     ("rich_text", "ind_b_name"),
        "Individual B Role":     ("rich_text", "ind_b_role"),
        "Individual B Email":    ("email", "ind_b_email"),
        "Individual B LinkedIn": ("url", "ind_b_linkedin"),
        "Cover Letter":          ("rich_text", "cover_letter"),
        "Email Sent":            ("rich_text", "email_body"),
    }

    for notion_field, (field_type, data_key) in field_map.items():
        value = data.get(data_key) or data.get(notion_field) or ""
        if not value:
            continue
        if field_type == "rich_text":
            properties[notion_field] = {"rich_text": [{"text": {"content": str(value)}}]}
        elif field_type == "url":
            properties[notion_field] = {"url": str(value)}
        elif field_type == "email":
            properties[notion_field] = {"email": str(value)}

    if "date_sent" in data or "email_sent_date" in data:
        from datetime import datetime
        properties["Date Sent"] = {"date": {"start": datetime.now().isoformat()}}
        properties["Status"] = {"select": {"name": "Sent"}}

    notion.pages.update(page_id=page_id, properties=properties)


def set_status(page_id: str, status: str):
    notion.pages.update(
        page_id=page_id,
        properties={"Status": {"select": {"name": status}}}
    )

