# Travel Assistant

A Streamlit-powered AI travel planner that helps users plan trips through natural conversation and generates a structured travel itinerary.

## Overview

This project combines:

- Streamlit for the chat-based web interface
- Google Gemini via the `google-genai` SDK for conversational travel planning
- Pydantic models to enforce a structured final itinerary schema
- JSON output for a final trip summary with daily planning

Users can chat with the assistant about destination, budget, preferences, activities, and trip duration. Once ready, the app creates a final itinerary with a day-by-day plan.

## Features

- Conversational travel planning in a chat UI
- Destination and trip preference tracking across messages
- Final itinerary generation in a structured JSON format
- Daily itinerary breakdown with per-day activities
- Budget category and key activity summaries

## Project structure

- `app.py` – Streamlit application and itinerary generation logic
- `requirements.txt` – Python dependencies
- `pyproject.toml` – project metadata and dependency configuration
- `assignment_notebook.ipynb` – project notebook / exploratory work

## Prerequisites

- Python 3.10+
- A Google AI API key

## Setup

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run the app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Usage

1. Enter a destination or trip idea in the chat box.
2. Continue the conversation with preferences such as budget, pace, activities, or travel style.
3. Click `Generate final itinerary` to produce a structured travel plan.
4. Review the generated itinerary JSON with the destination, trip duration, budget category, activities, and daily breakdown.

## Notes

- The app expects the environment variable `GOOGLE_API_KEY` to be available at runtime.
- The final itinerary is generated using a schema-validated response model to keep the output consistent.
