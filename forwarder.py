import requests
from bs4 import BeautifulSoup
import config

def extract_sms(driver):
    driver.get(config.SMS_URL)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table')
    if not table:
        return

    rows = table.find_all('tr')[1:]
    for row in rows[:1]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            sender = cells[1].text.strip()
            message = cells[2].text.strip()
            send_to_telegram(f"📥 New OTP Received:\nFrom: {sender}\nMessage: {message}")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": config.CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram Error] {e}")
