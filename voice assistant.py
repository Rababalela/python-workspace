import datetime
import webbrowser
import math
import random
import pyttsx3
import speech_recognition as sr

# ─────────────────────────────────────────
#  JARVIS - Voice Assistant (Windows)
#  Author: Tumelo | CMPG111 Project 2
# ─────────────────────────────────────────

ASSISTANT_NAME = "Jarvis"
reminders = []

# ── Engine Setup ──────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 170)       # Speaking speed
engine.setProperty("volume", 1.0)     # Max volume

# __ Voice ______________________________________
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id) 


def speak(text):
    """Convert text to speech and print it."""
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen via microphone and return text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio).lower()
            print(f" You said: {command}")
            return command
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError:
            speak("Speech service is unavailable. Check your internet.")
        return ""


# ── Features ──────────────────────────────

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"The current time is {now}")


def tell_date():
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    speak(f"Today is {today}")


def calculate(expression):
    allowed = {
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "tan": math.tan, "log": math.log, "pi": math.pi,
        "e": math.e, "abs": abs, "round": round
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        speak(f"The result is {result}")
    except Exception:
        speak("Sorry, I couldn't calculate that.")


def set_reminder():
    speak("What should I remind you about?")
    note = listen()
    if note:
        reminders.append({
            "note": note,
            "created": datetime.datetime.now().strftime("%H:%M on %d %b")
        })
        speak(f"Reminder saved: {note}")


def view_reminders():
    if not reminders:
        speak("You have no reminders.")
    else:
        speak(f"You have {len(reminders)} reminder(s).")
        for i, r in enumerate(reminders, 1):
            speak(f"{i}. {r['note']}")


def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the Python programmer break up with Java? Too much class.",
        "How many programmers does it take to change a light bulb? None, it's a hardware problem.",
    ]
    speak(random.choice(jokes))


def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    speak(f"Searching Google for {query}")


def open_wiki(topic):
    webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
    speak(f"Opening Wikipedia for {topic}")


def open_weather(city):
    webbrowser.open(f"https://www.google.com/search?q=weather+{city.replace(' ', '+')}")
    speak(f"Opening weather for {city}")


# ── Command Router ─────────────────────────

def process_command(command):
    if not command:
        return True

    if any(w in command for w in ["hello", "hi", "hey"]):
        speak(f"Hello! I'm {ASSISTANT_NAME}. How can I help?")

    elif "time" in command:
        tell_time()

    elif "date" in command or "day" in command:
        tell_date()

    elif "calculate" in command or "math" in command:
        speak("What should I calculate?")
        expr = listen()
        calculate(expr)

    elif "reminder" in command and "show" not in command:
        set_reminder()

    elif "show" in command and "reminder" in command:
        view_reminders()

    elif "joke" in command:
        tell_joke()

    elif "search" in command:
        speak("What should I search for?")
        query = listen()
        google_search(query)

    elif "wikipedia" in command or "wiki" in command:
        speak("What topic should I look up?")
        topic = listen()
        open_wiki(topic)

    elif "weather" in command:
        speak("Which city?")
        city = listen()
        open_weather(city)

    elif any(w in command for w in ["bye", "quit", "exit", "stop"]):
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak(f"Sorry, I don't understand that command.")

    return True


# ── Main Loop ─────────────────────────────

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "Good morning"
    elif hour < 18:
        period = "Good afternoon"
    else:
        period = "Good evening"
    speak(f"{period}! I'm {ASSISTANT_NAME}, your personal assistant. Say 'hello' to begin.")


def main():
    greet()
    running = True
    while running:
        command = listen()
        running = process_command(command)


if __name__ == "__main__":
    main()