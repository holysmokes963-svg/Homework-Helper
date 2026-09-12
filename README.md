# HomeworkHelper

```text
██╗███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

## HOMEWORK HELPER

An AI-powered homework helper that reads your question and provides an answer through a separate AI window.

---

# 🚀 INSTALLATION

## 1. Install Python

Download Python:

https://www.python.org/downloads/

During installation, make sure you check:

> ☑ **Add Python to PATH**

---

## 2. Install Visual Studio Code

Download Visual Studio Code:

https://code.visualstudio.com/

---

## 3. Download HomeworkHelper

Download or clone this GitHub repository.

Open the **HomeworkHelper** folder in Visual Studio Code.

---

## 4. Open the Terminal

In Visual Studio Code:

**View → Terminal**

Or press:

```text
Ctrl + `
```

---

## 5. Install Everything

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

If everything installed successfully, you're ready to configure the API.

---

# 🔑 API KEY SETUP

## 6. Get an OpenAI API Key

> ⚠️ **IMPORTANT: NEVER SHARE YOUR API KEY.**
>
> Your API key can be used to make API requests on your account. Depending on your account and usage, this can result in charges.

Go to:

https://platform.openai.com/

Log into your account or create one.

Find **API Keys** in the OpenAI platform.

Create a new secret key.

Copy the key when it is shown.

### Add the key to HomeworkHelper

Open the `.env` file in Visual Studio Code.

You should see something similar to:

```env
OPENAI_API_KEY=Your_key
```

Replace `Your_key` with your actual API key:

```env
OPENAI_API_KEY=your_actual_key_here
```

Save the file.

### ⚠️ NEVER UPLOAD `.env` TO GITHUB

Your `.env` file contains your private API key.

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

**If you accidentally upload your API key to GitHub, revoke the key immediately and create a new one.**

---

# ▶️ START HOMEWORK HELPER

## 7. Run the Application

Make sure your virtual environment is activated:

```powershell
venv\Scripts\activate
```

Then run:

```powershell
python main.py
```

A window should open shortly afterward.

---

# 🧠 USING HOMEWORK HELPER

## 8. How To Use It

Once the window opens:

1. Press **F3** to start the AI.
2. Click the window containing the question.
3. Wait for the AI to process the question.
4. The answer will appear in the Homework Helper window.
5. Type your answer.

That's it.

---

# 🎮 CONTROLS

| Key    | Action            |
| ------ | ----------------- |
| **F3** | Start / Enable AI |
| **F4** | Stop / Disable AI |

---

# 🛑 STOPPING THE APP

## 9. Completely Shut Down HomeworkHelper

Go back to the terminal in Visual Studio Code.

Press:

```text
Ctrl + C
```

This will stop the Python program.

---

# 🔧 TROUBLESHOOTING

## Python Is Not Recognized

If you see something like:

```text
'python' is not recognized as an internal or external command
```

Python is either not installed correctly or was not added to PATH.

Reinstall Python and make sure:

> ☑ **Add Python to PATH**

is checked during installation.

---

## Module Not Found

If you see:

```text
ModuleNotFoundError
```

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Then reinstall the requirements:

```powershell
pip install -r requirements.txt
```

---

## API Key Error

If you see an error such as:

```text
API key not provided
```

make sure your `.env` file exists and contains:

```env
OPENAI_API_KEY=your_actual_key_here
```

Make sure there are no unnecessary quotation marks or spaces.

**DO NOT post your API key publicly.**

---

## F3 Doesn't Work

Make sure:

* HomeworkHelper is running.
* The AI has been started with **F3**.
* The HomeworkHelper window is open.
* The program has not been stopped with `Ctrl + C`.

---

## The App Won't Start

Try:

```powershell
venv\Scripts\activate
```

Then:

```powershell
pip install -r requirements.txt
```

Then:

```powershell
python main.py
```

---

# 💰 API COST WARNING

HomeworkHelper uses the OpenAI API.

API usage may cost money depending on your OpenAI account, model, and usage.

**HomeworkHelper itself is not responsible for API charges.**

Keep your API key private and monitor your API usage and billing through the OpenAI platform.

---

```text
██████╗  ██████╗ ███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║  ██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝

                         HAVE FUN :)
```

## Disclaimer

HomeworkHelper is provided for educational and personal use.

Always follow your school's rules and academic policies when using AI assistance.
