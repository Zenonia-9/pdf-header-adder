📄 Telegram PDF Header Bot

A Telegram bot that automatically adds an image header to PDF files sent by users and returns the modified PDF.

The bot:

Accepts PDF files from users

Adds a header image to each page

Sends back the processed PDF

Supports multi-user handling

Can be built into a standalone .exe

⚙️ Requirements

Python 3.10 – 3.12

❗ Python must be lower than 3.13

Windows (for .exe build)

Check your Python version:
```bash
python --version
```

🧱 Project Structure
```text
PDF_editer/
│
├── pdf_bot.py
├── pdf_processor.py
├── config.py
├── requirements.txt
├── .env
│
├── images/
│   └── header.jpg
│
├── input_pdfs/
├── output_pdfs/
```
🔐 Environment Variables (.env)

Create a file named:
```text
.env
```

Inside it:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_telegram_user_id
```

🐍 Create Virtual Environment

From your project root folder:
```bash
python -m venv .venv
```

Activate it:

Windows:
```bash
.venv\Scripts\activate
```
Mac/Linux:
```bash
source .venv/bin/activate
```
📦 Install Requirements
```bash
pip install -r requirements.txt
```
▶️ Run the Bot (Development)
```bash
python pdf_bot.py
```

If successful, you should see:
```text
Bot is running...
```

🛠 Build Standalone EXE

Build:
```powershell
pyinstaller --onefile --noconsole --add-data "images;images" --add-data ".env;." pdf_bot.py

```

After build completes:
```text
dist/pdf_bot.exe
```

This is your standalone bot.

📂 Log File Location

Make sure your logging writes to a persistent directory like:
```text
Your-Home-Dir/
    PDF Header Bot/
        logs/
            bot.log
```
🚀 Auto Start on Windows

To auto-run on startup:

Press 
```text
Win + R
```
Type:
```text
taskschd.msc
```

Click Create Task

In General:

Enable: Run whether user is logged on or not

Enable: Run with highest privileges

In Triggers:

Click New

Choose: At startup

Optional: Delay 30 seconds

In Actions:

Choose: Start a program

Program:
```text
C:\Path\To\pdf_bot.exe
```

Click OK

Your bot will now:

Start automatically on boot

Run silently

Restart if configured in Settings

🛑 Shutdown Command

Your bot supports:
```text
/shutdown
```

This:

Stops the Telegram application

Optionally kills the process if needed

🧠 How It Works

User sends PDF

Bot saves it to user-specific folder

Header image is added to all pages

Bot sends back modified file

User folders are cleaned automatically

Supports multiple users simultaneously.

🧯 Common Issues
❌ ModuleNotFoundError

Install missing packages:
```bash
pip install -r requirements.txt
```
❌ Python 3.13 Errors

Downgrade to Python 3.12.

Python must be < 3.13

Always build exe inside activated venv

Keep header image inside images/