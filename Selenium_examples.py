import requests
import time
import os
# import aiohttp
# import asyncio
import pickle
# import urllib.parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Аргументы запуска Chrome
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
new_cwd = rf"C:/DEV"
os.chdir(new_cwd)
print(f"Current working directory: {os.getcwd()}")
prefs = {
    "download.default_directory": new_cwd, 
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": False
}
chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = 'normal'
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--no-cache")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-urlfetcher-cert-requests')
chrome_options.add_argument("--window-size=1600,900")
chrome_options.add_argument("--enable-unsafe-webgpu")
chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-gpu")

# переменные для автовыбора таймаута
current_profile = None
variative_timeout = None

# переменные для кукисов
cookie_path = f"{new_cwd}/project/cookies/"
cookie_file_project = f"{cookie_path}/project.pkl"


# функция выбора профиля скорости
def set_network_profile(driver, network_type):
    global current_profile  # используем глобальную переменную
    global variative_timeout
    profiles = {
        '2G': {
            'offline': False,
            'downloadThroughput': 1.25 * 1024 * 1024 / 8,
            'uploadThroughput': 1.25 * 1024 / 8,
            'latency': 400
        },
        '3G': {
            'offline': False,
            'downloadThroughput': 2.5 * 1024 * 1024 / 8,
            'uploadThroughput': 1.75 * 1024 * 1024 / 8,
            'latency': 100
        },
        '4G': {
            'offline': False,
            'downloadThroughput': 10 * 1024 * 1024 / 8,
            'uploadThroughput': 8 * 1024 * 1024 / 8,
            'latency': 60
        },
        '100M': {
            'offline': False,
            'downloadThroughput': 10 * 1024 * 1024 / 8,
            'uploadThroughput': 8 * 1024 * 1024 / 8,
            'latency': 60
        },
        'Offline': {
            'offline': True,
            'downloadThroughput': 0,
            'uploadThroughput': 0,
            'latency': 5000
        },
    }

    if network_type in profiles:
        driver.execute_cdp_cmd('Network.enable', {})
        driver.execute_cdp_cmd('Network.emulateNetworkConditions', profiles[network_type])
        current_profile = network_type

    if network_type == '2G':
        variative_timeout = 60
    elif network_type == '3G':
        variative_timeout = 30
    elif network_type == '4G':
        variative_timeout = 20
    elif network_type == '100M':
        variative_timeout = 15
    elif network_type == 'Offline':
        variative_timeout = 1000

# устанавливаем профиль скорости
set_network_profile(driver, '100M')

# функция получения текущего времени
def get_timestamp():
    timestamp = time.strftime('%d-%m-%Y_%H-%M-%S')
    return timestamp

def tg_send_msg(text):
    bot_token = "YOUR_TOKEN"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    chat_id = "YOURT_CHATID"
    req = requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2'})
    if req.status_code == 200:
        print(f"Telegram message successfully sent: {text}")
    else:
        print(f"An error occured sending Telegram message. {req.status_code}")

# TODO функция вызова WebDriverWait для поиска элемента (подумать над более толковой реализацией)
def wait_for(driver, by, locator, timeout=None, visible=None, clickable=None):
    if timeout is None:
        timeout = variative_timeout or 30
    
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        if visible:
            WebDriverWait(driver, timeout).until(EC.visibility_of(element))
        if clickable:
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))
        return element
    
    except Exception as err:
        print(f"Элемент не найден. {element}")
        return None

try:
    # Авторизация
    driver.get('https://website.ru')
    # wait_for(driver, By.XPATH, '//span[@class="magritte-button__label___zplmt_5-2-29" and contains(text(), "Войти")]').click()
    # wait_for(driver, By.XPATH, '//input[@inputmode="tel"]').send_keys("79000000000")
    # wait_for(driver, By.XPATH, '//input[@name="password"]').send_keys("very_impressive_password")
    # wait_for(driver, By.XPATH, '//span[text()="Войти"]').click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    driver.delete_all_cookies()

    # TODO Дамп кукисов (завязать на условиях в будущем)
    # if not os.path.exists(cookie_path):
    #     os.makedirs(cookie_path)
    # if os.path.exists(upload_file):
    #     os.remove(upload_file)
    # with open(cookie_file_project, "wb") as file:
    #     pickle.dump(driver.get_cookies(), file)

    # Подгрузка кукисов
    with open (cookie_file_project, "rb") as cookies:
        loaded_cookies = pickle.load(cookies)
    
    for cookie in loaded_cookies:
        driver.add_cookie(cookie) 

    driver.refresh()

    # Переход на страницу
    wait_for(driver, By.XPATH, 
            '//div[@class="class_pt_1 ' \
            'class_pt_2" and contains(text(), "Моя страница")]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print(f"{get_timestamp()} - Cookies loaded successfully")
    tg_send_msg(f"Cookies loaded successfully")

    # Логика проверки на доступность кнопки
    while True:
        try:    
            launch_unavailable = wait_for(driver, By.XPATH, '//span[text()="Временно недоступно"]', clickable=True)
            if launch_unavailable:
                driver.refresh()
                time.sleep(60)
            else:
                launch_present = wait_for(driver, By.XPATH, '//span[text()="Запустить"]', clickable=True)
                if launch_present:
                    launch_present.click()
                    time.sleep(5)
                    driver.refresh()
                    print(f"{get_timestamp()} - Процесс запущен успешно")
                    tg_send_msg(f"Процесс запущен успешно")
                else:
                    print(f"{get_timestamp()} - Внимание. Кнопка запуска НЕ НАЖАТА")
                    tg_send_msg(f"Внимание\n\nКнопка запуска НЕ НАЖАТА")
                    
        # TODO - Здесь нормальная обработка ошибок с разными типами error, исходя из контекста скрипта и т.п.       
        except Exception as e:
            print(f"{get_timestamp()} - Произошла ошибка: {e}")
            tg_send_msg(f"Произошла ошибка") # с markdown выводить текст ошибки



