from pynput import keyboard
import pyautogui,pyperclip,time,requests,json

history = []

def process_text(text):
    global history
    url = "%YOUR_PROXY_SITE%/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %YOUR_API_KEY%"
    }
    
    history.append({"role": "user", "content": text})
    if len(history) > 3:
        history.pop(0)

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": 
            "You are an assistant, answering my questions. " \
            "Thank you, I will give a tip. " \
            "Please only focus on the last question, " \
            "the previously asked questions are just a historical record, " \
            "they serve as the background for the final question. "
            }
        ] + history
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_dict = response.json()
    return response_dict['choices'][0]['message']['content']

last_time = 0

def on_press(key):
    global last_time
    if key == keyboard.KeyCode.from_char('-'):
        current_time = time.time()
        if current_time - last_time < 0.3: 
            on_activate()
        last_time = current_time

def key_enter():
    pyautogui.keyDown('shift')
    pyautogui.press('enter')
    pyautogui.keyUp('shift')

def on_activate():
    pyautogui.typewrite('Question:')
    text = pyperclip.paste()
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('ctrl', 'c')
    key_enter()
    pyautogui.hotkey('ctrl', 'v')
    key_enter()
    pyperclip.copy('--Answer:')
    pyautogui.hotkey('ctrl', 'v')
    key_enter()
    # text = pyperclip.paste()
    new_text = process_text(text)
    # pyautogui.typewrite(str(new_text))
    pyperclip.copy(str(new_text))
    pyautogui.hotkey('ctrl', 'v')
    key_enter()
    key_enter()
    key_enter()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
