import rumps
import logging
import os
import string
import re
import time
import pyperclip
from pynput import keyboard
import threading
import sys
import Quartz
#from Foundation import NSBundle

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

class TextTransformer:
    def __init__(self):
        logging.info("TextTransformer __init__ called")
        self.listener = None
        self.running = False
        self.thread = None
        self.choose_all_var = 0
        self.eng_to_heb = {
            'q': '/', 'w': '\'', 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
            'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל', 'l': 'ך', ';': 'ף', '\'': ',','’': ',',
            'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ', 'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.', ' ': ' ',
            'Q': '/', 'W': '\'', 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט', 'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ',
            'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח', 'K': 'ל', 'L': 'ך',
            'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ', 'M': 'צ'
        }
        self.heb_to_eng = {
            '/': 'q', '\'': 'w', 'ק': 'e', 'ר': 'r', 'א': 't', 'ט': 'y', 'ו': 'u', 'ן': 'i', 'ם': 'o', 'פ': 'p',
            'ש': 'a', 'ד': 's', 'ג': 'd', 'כ': 'f', 'ע': 'g', 'י': 'h', 'ח': 'j', 'ל': 'k', 'ך': 'l', 'ף': ';', 
            ',': '\'', 'ז': 'z', 'ס': 'x', 'ב': 'c', 'ה': 'v', 'נ': 'b', 'מ': 'n', 'צ': 'm', 'ת': ',', 'ץ': '.', '.': '/', ' ': ' ',
        }
        self.COMBINATIONS = [
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char('g')},
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char('G')},
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char('ע')},
        ]
        self.current = set()
        self.activated = False
        logging.info("TextTransformer initialized")

    def choose_all(self, state):
        self.choose_all_var = state
        logging.info(f"Choose all: {self.choose_all_var}")

    def set_selected_letter(self, letter):
        self.COMBINATIONS = [
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char(letter.lower())},
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char(letter.upper())},
            {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode.from_char(self.eng_to_heb[letter.lower()])},
        ]
        logging.info(f"TextTransformer COMBINATIONS updated: {self.COMBINATIONS}")

    def start(self):
        logging.info("TextTransformer start method called")
        if not self.running:
            logging.info("TextTransformer not running, attempting to start")
            self.running = True
            try:
                logging.info("Creating thread for _run_listener")
                self.thread = threading.Thread(target=self._run_listener)
                logging.info("Starting thread")
                self.thread.start()
                logging.info("TextTransformer thread started")
            except Exception as e:
                logging.error(f"Error starting TextTransformer thread: {str(e)}", exc_info=True)
                self.running = False
        else:
            logging.info("TextTransformer is already running")

    def _run_listener(self):
        logging.info("_run_listener method called")
        try:
            logging.info("Creating keyboard.Listener")
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
                logging.info("Keyboard listener started")
                self.listener.join()
        except Exception as e:
            logging.error(f"Error in _run_listener: {str(e)}", exc_info=True)

    def stop(self):
        logging.info("Attempting to stop TextTransformer")
        if self.running:
            self.running = False
            if self.listener:
                self.listener.stop()
            if self.thread:
                self.thread.join()
            logging.info("TextTransformer stopped")
        else:
            logging.info("TextTransformer is not running")

    def on_press(self, key):
        logging.debug(f"Key pressed: {key}")

        if self.running:
            if key in {keyboard.Key.cmd, keyboard.Key.shift} or (hasattr(key, 'char') and key.char):
                self.current.add(key)
                if any(all(k in self.current for k in combo) for combo in self.COMBINATIONS):
                    if not self.activated:
                        self.on_activate()
                        self.activated = True
        else:
            logging.debug("TextTransformer is not running")

    def on_release(self, key):
        logging.debug(f"Key released: {key}")
        if self.running:
            if key in self.current:
                self.current.remove(key)
            if not any(key in COMBO for COMBO in self.COMBINATIONS):
                self.activated = False

    def switch_input_language(self):
        script = '''
        tell application "System Events"
            key code 49 using {control down}
        end tell
        '''
        os.system(f"osascript -e '{script}'")

    def is_english(self, text):
        text1 = text.replace('’', '').replace(' ', '').replace('\n', '').replace('?', '')
        english_characters = set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
        # Check if most characters are in the set of English characters
        return all(char in english_characters for char in text1)

    def is_hebrew(self, text):
        hebrew_regex = re.compile(r'^[\u0590-\u05FF\s\.,!?\'":()\d_]+$')
        return bool(hebrew_regex.match(text))

    def check_language(self, text):
        text1 = text.replace('\'', '').replace('‘', '').replace('’', '').replace('“', '').replace('”', '').replace('?', '')
        if self.is_english(text1):
            return "English"
        elif self.is_hebrew(text1):
            return "Hebrew"
        else:
            return "Mixed"
    
    def verify_text(self, text):
        language = self.check_language(text)
        logging.debug(f'Language detected: {language}')
        if language == "Hebrew":
            return self.heb_to_eng, "Hebrew"
        elif language == "English":
            return self.eng_to_heb, "English"
        else:
            return {}, "Mixed"  # Return an empty dict if the language is mixed or other

    def transform_text(self, text, char_dict):
        return ''.join(char_dict.get(char, char) for char in text)

    def capitalize_first_letter(self, sentence):
        if not sentence:
            return sentence
        
        first_char = sentence[0]
        if first_char.isalpha():
            capitalized_first_char = first_char.upper()
            return capitalized_first_char + sentence[1:]
        else:
            return sentence

    def press_key(self, keycode, modifiers=0):
        # Simulate a key press using Quartz
        event = Quartz.CGEventCreateKeyboardEvent(None, keycode, True)
        Quartz.CGEventSetFlags(event, modifiers)
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
        time.sleep(0.1)  # Ensure the key press is registered

        # Simulate key release
        event = Quartz.CGEventCreateKeyboardEvent(None, keycode, False)
        Quartz.CGEventSetFlags(event, modifiers)
        Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)

    def copy_text(self):
        command_key = Quartz.kCGEventFlagMaskCommand
        c_keycode = 8
        self.press_key(c_keycode, command_key)

    def paste_text(self):
        command_key = Quartz.kCGEventFlagMaskCommand
        v_keycode = 9
        self.press_key(v_keycode, command_key)

    def select_all(self):
        command_key = Quartz.kCGEventFlagMaskCommand
        a_keycode = 0x00  # Keycode for 'A'
        self.press_key(a_keycode, command_key)

    def on_activate(self):
        logging.info('Activating hotkey action!')

        # Check if the clipboard contains text
        if not pyperclip.paste():
            logging.info('Clipboard is empty')
        else:
            old_text = pyperclip.paste()
            logging.debug(f'Old clipboard text passed')

        if self.choose_all_var == 1:
            self.select_all()
        
        logging.debug('Simulating Command+C to copy text')
        self.copy_text()
        
        text = pyperclip.paste()
        logging.debug(f'Wrong text to transform:::: {text}')
        
        char_dict, correct_lang = self.verify_text(text)
        if correct_lang == "Mixed":
            rumps.notification("Text Transformer", "Mixed or Other language detected", "Please select text in English or Hebrew")
        else:
            transformed_text = self.transform_text(text, char_dict)
            logging.debug(f'Transformed text:::: {transformed_text}')
            
            if correct_lang == "Hebrew":
                transformed_text = self.capitalize_first_letter(transformed_text)
            
            time.sleep(0.1)
            pyperclip.copy(transformed_text)
            
            logging.debug('Simulating Command+V to paste the transformed text')
            self.paste_text()

        if old_text:
            pyperclip.copy(old_text)

        self.switch_input_language()

class TextTransformerApp(rumps.App):
    def __init__(self):
        super(TextTransformerApp, self).__init__("Text Transformer")
        self.text_transformer = TextTransformer()
        letters = list("abcdefghijklmnopqrstuvwxyz".upper())
        new_letters = []
        for letter in letters:
            new_letters.append(rumps.MenuItem(letter, callback=self.choose_key, key=letter))
        self.menu = ["Text Transformer", None, "Start", None, ["Choose Key", new_letters], "Choose All"]
        

    @rumps.clicked("Choose Key")
    def choose_key(self, sender):
        letter = sender.title
        logging.info(f"Selected letter: {letter}")
        rumps.notification("Text Transformer", f"Selected letter: {letter}", "Press the activation key to transform text")
        sender.state = not sender.state
        self.text_transformer.set_selected_letter(letter)

    @rumps.clicked("Choose All")
    def choose_all(self, sender):
        logging.info("All letters pressed")
        rumps.notification("Text Transformer", "All letters selected", "Press the activation key to transform text")
        sender.state = not sender.state
        print(sender.state)
        state = sender.state
        self.text_transformer.choose_all(state)


    @rumps.clicked("Start")
    def start(self, _):
        if not self.text_transformer.running:
            logging.info("Starting TextTransformer")
            rumps.notification("Text Transformer", "TextTransformer started", "Press the activation key to transform text")
            self.text_transformer.start()
            self.menu["Start"].title = "Stop"
        else:
            logging.info("Stopping TextTransformer")
            rumps.notification("Text Transformer", "TextTransformer stopped", "No longer transforming text")
            self.text_transformer.stop()
            self.menu["Start"].title = "Start"


if __name__ == "__main__":
    #info = NSBundle.mainBundle().infoDictionary()
    #info['LSUIElement'] = True
    TextTransformerApp().run()


