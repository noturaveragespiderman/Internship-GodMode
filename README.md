# Internship-GodMode
End-to-end career automation engine: Uses Gemini 2.0 Flash to research Notion leads, generate personalized cover letters, and manage Gmail outreach via a Telegram command center.

# AI-Powered Job Application Pipeline

An automated "Human-in-the-Loop" outreach system that monitors **Notion** for job leads, performs deep company research using **Gemini 2.0 Flash**, and sends personalized applications through **Gmail**, all managed via an interactive **Telegram** bot.

---

## 🛠️ System Overview

This pipeline automates the most time-consuming parts of a job search while keeping you in total control:

1. **Lead Monitoring:** Polls a Notion database for companies marked as "New".
2. **Autonomous Research:** Extracts company missions, recent news, and careers page links using Google Search tools.
3. **Human Approval:** Pings you on Telegram with the research findings to decide whether to proceed or skip.
4. **Contact Discovery:** Finds key hiring/talent contacts once a company is approved.
5. **Document Generation:** Drafts a sector-specific cover letter and outreach email using your CV data.
6. **Validated Sending:** Sends a test email to yourself first, then fires the final application to the recruiter upon your "SEND" command.

---

## 📂 Project Structure

| File | Description |
| --- | --- |
| **`main.py`** | Orchestrates the system by running the Notion monitor and Telegram bot concurrently. |
| **`config.py`** | Central configuration for all API keys, tokens, and file paths. |
| **`research.py`** | Uses Gemini 2.0 Flash with Google Search to gather company intelligence. |
| **`telegram_handler.py`** | Manages the interactive state machine and user approvals via Telegram. |
| **`cover_letter.py`** | Generates personalized documents based on your CV and specific sector templates. |
| **`email_sender.py`** | Handles SMTP logic to send HTML emails with PDF and Text attachments. |
| **`state_db.py`** | A local SQLite database that tracks the progress of every application. |
| **`notion_trigger.py`** | Interfaces with the Notion API to fetch new rows and update statuses. |

---

## ⚙️ Setup Instructions

To protect your privacy, all sensitive information has been removed from the code. Follow these steps to set up your credentials.

### 1. Configuration (`config.py`)

Create a `config.py` file in the root directory and fill in your details:

```python
# Gemini / Perplexity API (Code currently uses PERPLEXITY_API_KEY for Gemini client)
PERPLEXITY_API_KEY = "YOUR_GEMINI_API_KEY" 

# Telegram Settings (Get these from @BotFather and @userinfobot)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID   = "YOUR_CHAT_ID"

# Notion Settings (Create an integration at developers.notion.com)
NOTION_TOKEN       = "YOUR_NOTION_INTERNAL_INTEGRATION_TOKEN"
NOTION_DATABASE_ID = "YOUR_DATABASE_ID"

# Email Settings (Use a Gmail App Password, NOT your main password)
GMAIL_ADDRESS      = "yourname@gmail.com"
GMAIL_APP_PASSWORD = "abcd efgh ijkl mnop" 

# Local File Paths
CV_TEXT_PATH       = "cv.txt"
CV_PDF_PATH        = "cv.pdf"

```

### 2. Google Cloud Credentials

Place your `service_account.json` in the root directory. This file is required for the system to authenticate with Google Cloud services.

> **Warning:** Never commit this file to a public repository as it contains your private RSA key.

### 3. CV & Templates

* **CV:** Ensure `cv.txt` and `cv.pdf` are present in the root directory.
* **Templates:** Create a `templates/` folder and add `.txt` files for different industries (e.g., `fintech.txt`, `consulting.txt`). These act as "Gold Standard" guides for the AI.

---

## 🚀 Usage

1. **Install dependencies:**
```bash
pip install -r requirements.txt

```


2. **Add a lead:** Create a new entry in Notion and set the "Status" to **New**.
3. **Launch:**
```bash
python main.py

```


4. **Interact:** Open your Telegram bot and follow the prompts to research, review, and send your applications.


