# CITS3403 Group Project - BobaBoard

This is the readme file for the BobaBoard website.

**Group members:**

| Name             | UWA Student Number | Github username                                          |
| ---------------- | ------------------ | -------------------------------------------------------- |
| Henuka Daluwatta | 23335255           | [@Teloshav](https://github.com/Teloshav)                 |
| Marco Gunawan    | 23780778           | [@marcogunawan9763](https://github.com/marcogunawan9763) |
| Austin Ngo       | 23801606           | [@mrtwiggy](https://github.com/mrtwiggy)                 |
| Kyaw Paing Hein  | 23318983           | [@AndrewHein999](https://github.com/AndrewHein999)       |

---

## What is BobaBoard?

BobaBoard is an online hub to review bubble tea from various shops, to keep track of your personal preferences and to see what like minded bubble tea fans all over have to say about the best drink around!

## How do you use BobaBoard?

You make an account and start reviewing drinks you've tried at various stores! This allows us to enhance our website to be the most up to date source about what's hot and what's not!

---

## Features
- Create personal accounts to upload bubbletea reviews onto public and private forums
- Find and connect with friends to share private reviews with one another
- Compete with other bubbletea addicts to see who can drink the most bubbleteas on the leaderboard
- See your lifetime bubbletea stats 

## Deployment instructions

**Set up Instructions:**
1. Create a .env file:
   - Note: you can choose to change your secret key to whatever value you would like.
   ```shell
   python create_env.py
   ```

1. Create the environment:
   
   ```shell
   python3 -m venv venv
   ```

2. Enter the environment:
   for wsl/linux/macOS:
   ```shell
   source venv/bin/activate
   ```
   or for Windows powershell:
   ```shell
   .\venv\Scripts\activate
   ```

3. Install the required packages:
   
   ```python
   pip install -r requirements.txt
   ```

4. Launch the Flask application:
   - Note: if you want to change the port, set ```PORT = <your chosen port nunber>``` in config.py. Otherwise the default server port is set to 5000.
   ```shell
   python app.py
   ```

5. Go to `http://localhost:<your chosen port number or 5000>`.

---

## Testing:

**How to run tests for BobaBoard:**
   In the project root directory:
```shell
python test.py
```

**Basic instructions for Selenium are as such:**
- Install Selenium (individually done due to difficulty in installation and variety of methods per operating system).
- Run instance.
- Run Python files in the folder ```/my_app/tests/selenium_tests``` RUN CREATE USERS TESTS FIRST!

---


## Referencing and Credits
The project was developed with the assistance of LLMs, including code suggestions, changes, and optimisations provided by models such as ChatGPT, Claude, Gemini, and CoPilot. 
