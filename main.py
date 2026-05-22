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
        if word.isalpha() and word not in stop_words:
            word = stemmer.stem(word)
            cleaned_token.append(word)

    return " ".join(cleaned_token)

model = joblib.load("Model\\KaylaGPT.pkl")

def ActionDetecter(user_input: str):
    user = user_input.lower()
    
    open_action = ["run", "open", "running", "opening", "start", "starting", "launch", "launching", "opening", "opening", "execute", "executing"]
    open_targets = {
        "youtube music": "youtube music",
        "youtube": "youtube",
        "facebook": "facebook",
        "browser": "browser",
        "discord": "discord",
        "steam": "steam",
        "vscode": "vscode",
        "visual studio code": "visual studio code"
    }

    clear_action = ["clear", "cls", "clear screen", "clearscreen"]
    exit_action = ["exit", "quit", "close"]

    for word in open_action:
        if word in user:
            for target, value in open_targets.items():
                if target in user:
                    return "open", value
    
    for word in clear_action:
        if word in user:
            return "clear", None
        
    for word in exit_action:
        if word in user:
            return "exit", None

    return None, None
    
def clear_screen():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run(["clear"])


def opening_app(target: str):
    target = target.lower()

    app_direct = {
        "discord": "C:/Users/Admin/AppData/Local/Discord/Update.exe --processStart Discord.exe",
        "steam": "C:/Program Files (x86)/Steam/steam.exe"
    }

    websites = {
        "browser": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "youtube": "https://www.youtube.com",
        "youtube music": "https://music.youtube.com"
    }

    if target in app_direct:
        try:
            subprocess.Popen(r"{}".format(app_direct[target]))
            running_text(f"I am open {target} right now!")
            #print(r"{}".format(app_direct[target]))
        except Exception as e:            
            running_text(f"Sorry, I couldn't open {target}. Error: {e}")

    if target in websites:
        try:
            webbrowser.open(websites[target])
            print(f"I am open Website name {target} right now!")
        except Exception as e:
            print(f"Sorry, I couldn't open the website {target}. Error: {e}")

def action_handler(action: str, keyword: str):
    if action == "open":
        opening_app(keyword)
    elif action == "clear":
        clear_screen()
    elif action == "exit":
        print("Goodbye!")
        exit()
    else:
        print("Sorry, I didn't understand that command.")

def search_wikipedia(query: str):
    summary = wikipedia.summary(query)
    return summary

def researching(text: str):
    text =  text.lower()

    if text in Data['prompts']:
        return None

    else:
        if text.startswith("what is"):
            querty = text.replace('what is ', "", 1).strip()
            answer = search_wikipedia(querty)
            return answer
        
        elif text.startswith("who is"):
            querty = text.replace('who is ', "", 1).strip()
            answer = search_wikipedia(querty)
            return answer

    return None


def running_text(text:str):
    for char in str(text):
            print(f"{char}", flush= True, end= "")
            time.sleep(0.02)
    print("\n") 

print("Kayla: Hey I am Kayla GPT, I hope I can help you")
while True:
    user = input("You >> ").lower().strip()
    action, target = ActionDetecter(user)
    if action:
        action_handler(action, target) #type: ignore
        continue
    
    if user.startswith("what is") or user.startswith("who is"):
        print("Kayla: Researching ", end= '\r', flush= True)

        research = researching(user)

        print("." * 100, end= "\r", flush= True)
        
        if research is not None:
            print("Kayla: ", end="", flush=True)

        for char in str(research):
            print(char, end="", flush=True)
            time.sleep(0.02)
        
        continue

    if user == "":
        continue
    else:
        prediction = model.predict([user])[0]
        
        res = rd.choice(Response[prediction])
        print("Kayla: ", end= "")
        running_text(res)

