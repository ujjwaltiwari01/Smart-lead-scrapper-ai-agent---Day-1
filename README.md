# It’s Day 1 of our 30 Days, 30 AI Agents Challenge  
We just built the Smart Google Maps Scraper Agent — a fully open-source AI tool that extracts business Name, Website, Email, and Phone directly from Google Maps in seconds.  
Just enter your city, niche, and number of leads — and it delivers a ready CSV file of verified leads.  
No paid APIs. No subscriptions. No hidden limits.

---

## What you get

- ✅ Extracts Name, Website, Email, Phone from Google Maps
- ✅ CSV download in one click
- ✅ No API keys or subscriptions
- ✅ Simple Streamlit UI
- ✅ Works on Windows (Edge + EdgeDriver)

---

## Quick Preview

- Open the app
- Type: City (e.g., Lucknow), Business (e.g., marketing agencies), Number of leads
- Click Start — watch progress — Download CSV

Output file path:
- `output/final_leads_<timestamp>.csv`

---

## Setup (5-year-old friendly guide)

- Follow these steps exactly. No coding needed.

### 1) Install Python

- Download Python 3.10 or newer from python.org
- During install, check the box “Add Python to PATH”
- To verify:
  - Open Command Prompt
  - Run: `python --version`  
  - If you see a version number (like 3.11.6), you’re good

### 2) Install Microsoft Edge

- Make sure Microsoft Edge is installed (it already is on Windows 10/11)

### 3) Get Microsoft Edge WebDriver

- You need a tiny file called `msedgedriver.exe` that matches your Edge version
- Find your Edge version:
  - Open Edge
  - Go to `edge://version`
- Download matching Edge WebDriver:
  - Search the web for “Microsoft Edge WebDriver download”
  - Pick the version that matches your Edge version
- After download:
  - Put `msedgedriver.exe` in the `smart_maps_scraper` folder (the same folder where `app.py` is)
  - Simple rule: `app.py` and `msedgedriver.exe` should be neighbors

### 4) Download this project

- Put the folder anywhere on your computer (for example: `D:\30 days 30 agent\smart_maps_scraper day 1\`)

Folder structure should look like:
- `smart_maps_scraper/`
  - `app.py`
  - `main.py`
  - `requirements.txt`
  - `msedgedriver.exe`  ← you added this here
- `.env` is NOT required

### 5) Install the required packages

- Open Command Prompt
- Go to the project folder:
  - `cd "D:\30 days 30 agent\smart_maps_scraper day 1"`
- Create a virtual environment (recommended):
  - `python -m venv .venv`
  - Activate it:
    - Windows: `.venv\Scripts\activate`
- Install dependencies:
  - `pip install -r smart_maps_scraper/requirements.txt`

You’ll see installs for:
- streamlit
- selenium
- pandas
- requests
- python-dotenv

### 6) Run the app

- From the same Command Prompt:
  - `streamlit run smart_maps_scraper/app.py`
- A browser window will open at `http://localhost:8501`

If the browser doesn’t open, just visit `http://localhost:8501` manually.

---

## How to use

- Type your city, business/niche, and choose number of businesses
- Click “Start Scraping”
- Watch the progress bar update
- When done, click “Download CSV” or find it in the `output/` folder

CSV columns:
- Name
- Website
- Email
- Phone

---

## Troubleshooting

- “WebDriver could not be found”
  - Make sure `msedgedriver.exe` is placed inside the `smart_maps_scraper` folder next to `app.py`
  - Make sure its version matches your Edge version (check `edge://version`)
- “Streamlit command not found”
  - Activate the virtual environment first: `.venv\Scripts\activate`
  - Or install Streamlit: `pip install streamlit`
- “CSV not generated”
  - Check the app’s messages
  - Try reducing the number of businesses (e.g., 50)
  - Ensure internet connection is active
- Empty “Email” or “Phone”
  - Not all websites publish contact details
  - The scraper does a best-effort extraction from the business website and a Google fallback
- Want to see the browser for debugging?
  - Open `smart_maps_scraper/main.py`
  - In `setup_driver()`, remove the line `edge_options.add_argument("--headless")`
  - Save and run again

---

## Project Structure

- `smart_maps_scraper/app.py`
  - Streamlit UI
  - Start/Stop controls
  - Progress and CSV download
- `smart_maps_scraper/main.py`
  - Google Maps scraping
  - Website crawling for Email and Phone
  - CSV writing to `output/`
- `smart_maps_scraper/requirements.txt`
  - Python package list
- `output/`
  - Created automatically for CSV files

No `.env` file is required.

---

## Command cheatsheet

- Create venv:
  - `python -m venv .venv`
- Activate venv (Windows):
  - `.venv\Scripts\activate`
- Install deps:
  - `pip install -r smart_maps_scraper/requirements.txt`
- Run app:
  - `streamlit run smart_maps_scraper/app.py`

---

## Notes on responsible use

- Respect Google’s Terms of Service and robots.txt
- Use reasonable limits to avoid heavy automated traffic
- This tool is for educational and ethical lead generation

---

## How it works (in simple words)

- Searches Google Maps for your query (e.g., “marketing agencies in Lucknow”)
- Opens each business page and tries to find the official website
- Visits the website and looks for emails and phone numbers
- Saves all results to a CSV file you can download

---

## Like this? Days 2–30 coming next

We’re building 30 AI agents in 30 days — all open-source.  
Star the repo, share your ideas, and stay tuned for tomorrow’s agent!
