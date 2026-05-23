import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer
import random as rd
import json
import subprocess
import platform
import webbrowser
import wikipedia
import warnings
from bs4 import GuessedAtParserWarning
import time
from spellchecker import SpellChecker

spell = SpellChecker()
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

with open("Data\\Data.json", 'r') as f:
    Data = json.load(f)

Response = Data['responses']

try:
    nltk.data.find("corpora/stopwords")

except:
    nltk.download("stopwords", quiet= True)

stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def preprocessor(text: str):
    text = text.lower()
    token = wordpunct_tokenize(text)

    cleaned_token = []

    for word in token:
        if word.isalpha():
            word = stemmer.stem(word)
            cleaned_token.append(word)

    return " ".join(cleaned_token)

model = joblib.load("Model\\KaylaGPT.pkl")

import subprocess
import platform
import webbrowser
import wikipedia
import time


class ModelAction:
    def __init__(self, data: dict):
        self.data = data

        self.open_action = [
            "run", "open", "running", "opening",
            "start", "starting", "launch", "launching",
            "execute", "executing"
        ]

        self.open_targets = {
            "youtube music": "youtube music",
            "youtube": "youtube",
            "facebook": "facebook",
            "browser": "browser",
            "discord": "discord",
            "steam": "steam",
            "vscode": "vscode",
            "visual studio code": "visual studio code"
        }

        self.clear_action = [
            "clear", "cls", "clear screen", "clearscreen"
        ]

        self.exit_action = [
            "exit", "quit", "close"
        ]

        self.app_direct = {
            "discord": [
                r"C:\Users\Admin\AppData\Local\Discord\Update.exe",
                "--processStart",
                "Discord.exe"
            ],
            "steam": r"C:\Program Files (x86)\Steam\steam.exe",
            "vscode": "code",
            "visual studio code": "code"
        }

        self.websites = {
            "browser": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "youtube": "https://www.youtube.com",
            "youtube music": "https://music.youtube.com"
        }

        self.question_patterns = [
            "can you explain ",
            "could you explain ",
            "explain ",
            "tell me about ",
            "give me information about ",
            "give me info about ",
            "search for ",
            "search ",
            "research ",
            "look up ",
            "find information about ",
            "what is a ",
            "what is an ",
            "what is the ",
            "what is ",
            "who is ",
            "where is ",
            "when was ",
            "when is ",
            "why is ",
            "how does ",
            "how do ",
            "how to ",
        ]

    def spelling_correction(self, text: str):
        words = text.lower().strip().split()
        corrected_words = []

        for word in words:
            corrected = spell.correction(word)

            if corrected is None:
                corrected_words.append(word)
            else:
                corrected_words.append(corrected)

        return " ".join(corrected_words)

    def action_detector(self, user_input: str):
        user = user_input.lower().strip()

        for word in self.open_action:
            if word in user:
                for target, value in self.open_targets.items():
                    if target in user:
                        return "open", value

        for word in self.clear_action:
            if word in user:
                return "clear", None

        for word in self.exit_action:
            if word in user:
                return "exit", None

        return None, None

    def clear_screen(self):
        if platform.system() == "Windows":
            subprocess.run("cls", shell=True)
        else:
            subprocess.run(["clear"])

    def opening_app(self, target: str):
        target = target.lower().strip()

        if target in self.websites:
            try:
                webbrowser.open(self.websites[target])
                self.running_text(f"I am opening website {target} right now!")
            except Exception as e:
                self.running_text(f"Sorry, I couldn't open the website {target}. Error: {e}")
            return

        if target in self.app_direct:
            try:
                app = self.app_direct[target]

                if isinstance(app, list):
                    subprocess.Popen(app)
                else:
                    subprocess.Popen(app, shell=True)

                self.running_text(f"I am opening {target} right now!")
            except Exception as e:
                self.running_text(f"Sorry, I couldn't open {target}. Error: {e}")
            return

        self.running_text(f"Sorry, I do not know how to open {target}.")

    def action_handler(self, action: str, keyword: str | None):
        if action == "open":
            if keyword is None:
                self.running_text("What app do you want me to open?")
                return True

            self.opening_app(keyword)
            return True

        elif action == "clear":
            self.clear_screen()
            return True

        elif action == "exit":
            self.running_text("Goodbye!")
            return False

        else:
            self.running_text("Sorry, I didn't understand that command.")
            return True

    def search_wikipedia(self, query: str):
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary

        except wikipedia.exceptions.DisambiguationError as e:
            return f"This topic is too broad. Try one of these: {e.options[:5]}"

        except wikipedia.exceptions.PageError:
            return "I could not find that page."

        except Exception:
            return "Not found."

    def researching(self, text: str):
        text = text.lower().strip()

        prompts = [prompt.lower().strip() for prompt in self.data["prompts"]]

        blocked_questions = [
            "what is your name",
            "who are you",
            "what are you"
        ]

        if text in prompts:
            return None, False
        
        if text in blocked_questions:
            return None, False

        for pattern in self.question_patterns:
            if text.startswith(pattern):
                query = text.replace(pattern, "", 1).strip()
                return self.search_wikipedia(query), True

        return None, False

    def running_text(self, text: str):
        for char in str(text):
            print(char, flush=True, end="")
            time.sleep(0.02)
        print()

action_model = ModelAction(Data)
print("Kayla: Hey I am Kayla GPT, I hope I can help you")

while True:
    user = input("You >> ").lower().strip()
    user = action_model.spelling_correction(user)
    action, target = action_model.action_detector(user)
    research, statement = action_model.researching(user)

    #print(statement)

    # if corrected_user != user:
    #     action_model.running_text(f"Kayla: What's {user}")
    #     continue

    if action:
        action_model.action_handler(action, target) #type: ignore
        continue
    
    if statement:
        print("Kayla: Researching ", end= '\r', flush= True)

        research, statement = action_model.researching(user)

        print(" " * 100, end= "\r", flush= True)
        
        if research is not None:
            print("Kayla: ", end="", flush=True)

        action_model.running_text(str(research))

        print("\n")
        continue

    if user == "":
        continue

    else:
        prediction = model.predict([user])[0]
        
        res = rd.choice(Response[prediction])
        print("Kayla: ", end= "")
        action_model.running_text(res)
