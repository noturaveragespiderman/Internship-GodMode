import threading
import time
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from state_db import init_db, upsert, get_active
from notion_trigger import get_new_companies, set_status
from research import get_company_basics
from telegram_handler import start_telegram_bot 

init_db()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
processed_ids = set()

def send_telegram_with_buttons(text, reply_markup=None):
    asyncio.run(bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, reply_markup=reply_markup, parse_mode="Markdown"))

def check_notion():
    print("🔍 Notion checker background thread started...")
    while True:
        active = get_active()
        if active:
            company = dict(active).get('company_name', 'a company')
            print(f"⏳ Waiting for you to finish {company} on Telegram...")
            time.sleep(15)
            continue

        print("👀 Checking Notion for new companies...")
        new_entries = get_new_companies(processed_ids)
        
        for page_id, row in new_entries:
            if get_active():
                break

            processed_ids.add(page_id)
            set_status(page_id, "In Progress")
            
            print(f"🚀 Processing new company: {row['Company Name']}")

            try:
                basics = get_company_basics(row["Company Name"], row["Website"])
                
                brief = str(basics.get("brief_description") or "").strip()
                career_link = str(basics.get("career_page_link") or "").strip()
                sector = str(basics.get("sector") or "General").strip()
                source_link = str(basics.get("source_link") or "").strip()

                if (not brief or brief.lower() in ["null", "none", "not found"]) and \
                   (not career_link or career_link.lower() in ["null", "none", "not found"]):
                    
                    print(f"❌ Nothing found for {row['Company Name']}")
                    msg = f"⚠️ *Nothing was found for {row['Company Name']}* ({row['Website']}). \nSkipping to the next company."
                    
                    send_telegram_with_buttons(msg)
                    set_status(page_id, "Not Found")
                    continue
                
                upsert(
                    page_id,
                    notion_page_id=page_id,
                    company_name=row["Company Name"],
                    website=row["Website"],
                    brief_description=brief,
                    career_page_link=career_link,
                    sector=sector,
                    state="AWAITING_CAREER_PAGE_DECISION"
                )

                keyboard = [
                    [InlineKeyboardButton("✅ Proceed (No open roles)", callback_data="proceed_contacts")],
                    [InlineKeyboardButton("⏭️ Skip (I applied directly)", callback_data="skip_applied")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Format links to ensure they are clickable
                fmt_source = f"https://{source_link}" if source_link and not source_link.startswith("http") else source_link
                fmt_career = f"https://{career_link}" if career_link and not career_link.startswith("http") else career_link

                msg = (
                    f"🏢 *New Company:* {row['Company Name']}\n"
                    f"🌐 *Website:* {row['Website']}\n"
                    f"📊 *Sector:* {sector}\n\n"
                    f"📝 *Description & News:* \n{brief}\n\n"
                    f"🔎 *Verify News Source:* {fmt_source if source_link and source_link.lower() != 'null' else 'Not found'}\n\n"
                    f"🔗 *Career Page:* {fmt_career if career_link and career_link.lower() != 'null' else 'Not found'}\n\n"
                    "What would you like to do?"
                )
                
                send_telegram_with_buttons(msg, reply_markup)
                break 

            except Exception as e:
                print(f"⚠️ Error processing {row['Company Name']}: {e}")
                set_status(page_id, "Error")

        time.sleep(3600)

if __name__ == "__main__":
    print("🚀 Starting Bot Services...")
    notion_thread = threading.Thread(target=check_notion, daemon=True)
    notion_thread.start()
    start_telegram_bot()
