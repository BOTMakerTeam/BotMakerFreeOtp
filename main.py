import time
import config
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from forwarder import extract_sms

def solve_question(question_text):
    numbers = re.findall(r'\d+', question_text)
    operator = re.search(r'[\+\-\*/]', question_text)
    
    if len(numbers) != 2 or not operator:
        return None

    num1, num2 = int(numbers[0]), int(numbers[1])
    op = operator.group()

    if op == '+':
        return str(num1 + num2)
    elif op == '-':
        return str(num1 - num2)
    elif op == '*':
        return str(num1 * num2)
    elif op == '/':
        return str(num1 // num2)
    return None

def auto_login(driver):
    print("[*] Trying Auto Login...")

    driver.get(config.LOGIN_URL)
    time.sleep(3)

    driver.find_element(By.NAME, "username").send_keys(config.USERNAME)
    driver.find_element(By.NAME, "password").send_keys(config.PASSWORD)

    question_text = driver.find_element(By.XPATH, "//label[contains(text(), 'What')]").text
    answer = solve_question(question_text)

    if not answer:
        print("[❌] Unable to solve security question.")
        return False

    driver.find_element(By.NAME, "answer").send_keys(answer)

    driver.find_element(By.XPATH, '//button[contains(text(), "LOGIN")]').click()

    time.sleep(5)
    if "Logout" in driver.page_source or "dashboard" in driver.current_url:
        print("[✅] Auto Login successful!")
        return True
    else:
        print("[❌] Login failed.")
        return False

def main():
    print("[*] Launching Chrome browser...")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    if not auto_login(driver):
        driver.quit()
        return

    print("[*] Starting SMS monitoring...")
    while True:
        try:
            extract_sms(driver)
            time.sleep(2)
        except Exception as e:
            print(f"[ERR] {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
