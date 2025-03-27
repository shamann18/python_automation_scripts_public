import psutil
import time
import subprocess
import aiohttp
import asyncio
import re
import os

bot_token = 'your_tg_token'
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
chat_id = 'your_chat_id'
process_list = [
    {
        'exe_name': 'your_exe',
        'exe_path': 'your_path',
        'launcher': 'launcher_path'
    },
    {
        'exe_name': 'your_exe',
        'exe_path': 'your_path',
        'launcher': 'launcher_path'
    },
    {
        'exe_name': 'your_exe',
        'exe_path': 'your_path',
        'launcher': 'launcher_path'
    },
    {
        'exe_name': 'your_exe',
        'exe_path': 'your_path',
        'launcher': 'launcher_path'
    },
    {
        'exe_name': 'your_exe',
        'exe_path': 'your_path',
        'launcher': 'launcher_path'
    }
]


# TODO - Класс для хранения состояний
class AppState:
    def __init__(self):
        self.state = None

app_state = AppState()


# Функция вывода стартового сообщения
def intro():
    app_state.state = 'intro'
    welcome_text = ['Simple Process Checker', 'Written by shaman18', 'Script version 0.2', "Process check occurs every 360 seconds", " "]
    get_timestamp()
    for text in welcome_text:
        time.sleep(0.170)
        print(text)


# Печать текущего времени
def get_timestamp():
    timestamp = time.strftime('%d.%m.%Y %H:%M:%S')
    if app_state.state == 'intro':
        print(timestamp)
    else:
        return timestamp


# Запись лога в файл
def write_log(log_msg):
    log_time = time.strftime('%Y-%m-%d')
    work_directory = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(work_directory, "log")
    os.makedirs(log_path, exist_ok=True)
    log_file = os.path.join(log_path, f"{log_time}_log.txt")
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(log_msg + "\n")


# Функция отправки сообщения в телегу
async def send_message_to_telegram(msg_text):
    timestamp = get_timestamp()
    session_timeout = aiohttp.ClientTimeout(total=6)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        try:
            async with session.post(url, data={'chat_id': chat_id, 'text': msg_text, 'parse_mode': 'MarkdownV2'}) as response:
                if response.status != 200:
                    print(f"{timestamp} - Error sending POST. Response code: {response.status}")
        
        except Exception:
            print(f"An Error sending POST occured")
           
        
# Функция экранирования спец. символов из Markdownv2 в переменной exe_name
def make_escaped_markdown(text):
    escaped_chars = r"_*[]()~`>#+-=|{}.!"
    escaped_exe_name = text
    for character in escaped_chars:
        escaped_exe_name = escaped_exe_name.replace(character, f"\\{character}")
    return escaped_exe_name


# Функция 'капитализации' символов до .exe
def upper_to_dot(exe_name):
    matched = re.match(r".*?(?=.exe)", exe_name)
    exe_name = f"{matched.group().upper()}.exe"
    return exe_name
    

# Основная функция поиска процесса 
async def check_proc():
    app_state.state = 'check_process'
    timestamp = get_timestamp()
    escaped_exe_name = None
    found_processes = {proc.info['name']: proc.info['pid'] for proc in psutil.process_iter(['name', 'pid'])}

    for element in process_list:
        exe_name = element['exe_name']
        exe_path = element['exe_path']
        launcher = element['launcher']

        if exe_name not in found_processes:
            try:
                if exe_name == 'your_certain_exe':
                    certain_exe = exe_path[:-15]
                    new_proc = subprocess.Popen([f"{launcher}"], cwd=f"{exe_path}", creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    new_proc = subprocess.Popen([f"{exe_path}/{launcher}"], cwd=f"{exe_path}", creationflags=subprocess.CREATE_NEW_CONSOLE)
                escaped_exe_name = make_escaped_markdown(upper_to_dot(exe_name))
                log_msg = f"{timestamp} - Process {escaped_exe_name} was not found. Restarted successfully."
                write_log(log_msg)
                print(f"{timestamp} - Warning! Process {exe_name} was not found. Started successfully with PID {new_proc.pid}")
                msg_text = f"*Attention\\!*\n\nProcess *{escaped_exe_name}* was not found\\.\nStarted successfully\\."
                asyncio.create_task(send_message_to_telegram(msg_text))
                await asyncio.sleep(0.075)
            except Exception as err:
                log_msg = f"{timestamp} - An error {type(err)} occured: {err}"
                write_log(log_msg)
                print(f"{timestamp} - An error {type(err)} occured: {err}")
                await asyncio.sleep(0.075)
                continue
        else:
            log_msg = f"{timestamp} - Process {exe_name} is running with PID {found_processes[exe_name]}"
            write_log(log_msg)
            print(f"{timestamp} - Process {exe_name} is running with PID {found_processes[exe_name]}")
            await asyncio.sleep(0.075)


async def main():
    intro()
    while True:
        await check_proc()
        await asyncio.sleep(360)

asyncio.run(main())
