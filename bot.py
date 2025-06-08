import telebot
import requests
from bs4 import BeautifulSoup
import os

# Environment Variables (to be set in Render.com later)
BOT_TOKEN = os.getenv("8121912599:AAFQCEJCUruTXSLGXwxYwtddr8UeeUDLYxQ")
PORTAL_USERNAME = os.getenv("Vinayak@S")
PORTAL_PASSWORD = os.getenv("Vinayak@S")

# Replace with real portal URLs
PORTAL1_LOGIN_URL = "https://operator.intechonline.net/Partner/Login.aspx"
PORTAL1_DETAIL_URL = "https://operator.intechonline.net/Partner/Accounts.aspx"

PORTAL2_LOGIN_URL = "https://selfdesk2.microscan.co.in/admin/#!/login"
PORTAL2_DETAIL_URL = "https://selfdesk2.microscan.co.in/admin/#!/ViewEditUsers"

# Create bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Add Telegram user IDs of your employees (as strings)
AUTHORIZED_USERS = ["9870880183", "9664607772","9664607772","9833875015"]  # Replace with real user IDs

# Function to log in and fetch customer data
def get_customer_from_portal1(customer_id):
    try:
        session = requests.Session()

        # 1. Load login page to get cookies/viewstate if needed
        login_page = session.get(PORTAL1_LOGIN_URL)
        if login_page.status_code != 200:
            return "⚠️ Failed to load login page."

        # 2. Post login form
        login_data = {
            'ctl00$MainContent$txtUsername': PORTAL_USERNAME,
            'ctl00$MainContent$txtPassword': PORTAL_PASSWORD,
            'ctl00$MainContent$btnLogin': 'Login'
        }

        login_response = session.post(PORTAL1_LOGIN_URL, data=login_data)
        if login_response.status_code != 200:
            return "❌ Login failed for Portal 1."

        # 3. Get customer data
        detail_url = PORTAL1_DETAIL_URL.format(customer_id)
        cust_response = session.get(detail_url)
        if cust_response.status_code != 200:
            return f"❌ Failed to fetch data for customer ID {customer_id}."

        # 4. Parse the HTML response (you may need to inspect HTML IDs)
        soup = BeautifulSoup(cust_response.text, 'html.parser')
        customer_name = soup.find("span", {"id": "MainContent_lblCustomerName"}).text.strip()
        plan = soup.find("span", {"id": "MainContent_lblPlan"}).text.strip()
        status = soup.find("span", {"id": "MainContent_lblStatus"}).text.strip()

        return f"✅ Customer Info (Portal 1):\n👤 Name: {customer_name}\n📶 Plan: {plan}\n📍 Status: {status}"

    except Exception as e:
        return f"❌ Error (Portal 1): {str(e)}"

# ❌ Placeholder for Portal 2 (Microscan - Angular frontend)
def get_customer_from_portal2(customer_id):
    return "⚠️ Portal 2 uses Angular and cannot be scraped directly.\nConsider using Selenium or ask the provider for API access."

# ✅ /start command
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "👋 Welcome!\nUse:\n➡️ /customer1 <id> for IntechOnline\n➡️ /customer2 <id> for Microscan")

# ✅ /customer1 command
@bot.message_handler(commands=['customer1'])
def handle_customer1(message):
    user_id = str(message.from_user.id)
    if user_id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "❌ Unauthorized access.")

    try:
        customer_id = message.text.split()[1]
        bot.reply_to(message, f"🔍 Fetching from Portal 1 for ID: {customer_id}...")
        result = get_customer_from_portal1(customer_id)
        bot.reply_to(message, result)
    except IndexError:
        bot.reply_to(message, "⚠️ Usage: /customer1 <customer_id>")

# ✅ /customer2 command (Microscan - placeholder only)
@bot.message_handler(commands=['customer2'])
def handle_customer2(message):
    user_id = str(message.from_user.id)
    if user_id not in AUTHORIZED_USERS:
        return bot.reply_to(message, "❌ Unauthorized access.")

    try:
        customer_id = message.text.split()[1]
        bot.reply_to(message, f"ℹ️ Fetching from Portal 2 for ID: {customer_id}...")
        result = get_customer_from_portal2(customer_id)
        bot.reply_to(message, result)
    except IndexError:
        bot.reply_to(message, "⚠️ Usage: /customer2 <customer_id>")

# ✅ Start polling (for Render deployment)
bot.infinity_polling()