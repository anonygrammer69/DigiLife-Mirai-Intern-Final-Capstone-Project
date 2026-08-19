# DigiLife 📱: The AI-powered Digital Wellbeing Mentor
```
$ whoami
A wellbeing dashboard, not a guilt machine

$ cat mission.txt
Digital addiction is a modern epidemic.
This is a tool that helps you see the pattern — and fix it.
```

## About
**DigiLife** is a Streamlit dashboard that visualizes your total time spent on a screen in a day, and uses that
data to hand it to Gemini, which plays the role of a brutal-but-fair life
coach: It doesn't just say "use your phone less" — it looks at what you
actually did with your time and suggests real-world replacements.

## Demo Video



## Stack

```
frontend   : streamlit
data       : pandas + screentime.csv (synthetic)
ai         : google-genai (Gemini 2.5 Flash)
secrets    : python-dotenv
```

## How to run it locally

```bash
$ git clone <this-repo-url>
$ cd digilife
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt
$ cp .env        # then paste in your GEMINI_API_KEY
$ streamlit run main_app.py
```

## Features

```
[x] A sidebar, with a daily screen time limit slider, and a button to upload user screen time data as a CSV file.
[x] All essential screen time stats, to help the user reflect on how much time they're actually spending in front of a screen
(Total screen time, average time spent per app, most and least used apps and top category of apps)
+ An app-wise bar graph depicting time spent of each app + A donut-like pie graph to help the user understand their total screen time breakdown app by app
+ A threshold indicator, displaying by how many minutes the user has exceeded the daily screen time limit set by them, if they have so.
[x] AI Insights: All user screen time data is taken into account by Gemini, scrutinizes and provides various tips and suggestions
to improve overall digital wellbeing, and how to effectively and productively utilize screen time.
[x] Shareable Accountability link via st.query_params
```

## Project Structure

```
life-os/
├── app.py              # main streamlit app
├── requirements.txt
└── README.md
```

## Deploy

Pushed to Streamlit Community Cloud. Set `API_KEY` under
**App settings → Secrets** as:

```toml
GEMINI_API_KEY = "your_key_here"
```

---

