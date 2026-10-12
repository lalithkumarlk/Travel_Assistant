"""Streamlit interface for the conversational AI travel planner."""

import json
import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from google.genai import types


class DailyPlan(BaseModel):
    day: int = Field(description="The day number in the trip")
    plan: str = Field(description="A detailed plan for this day")


class TravelItinerary(BaseModel):
    destination: str = Field(description="The destination city and country")
    duration_days: int = Field(description="The number of days in the trip")
    budget_category: str = Field(description="The budget level: Low, Medium, or High")
    activities: List[str] = Field(description="Three to five core activities or themes")
    daily_itinerary: List[DailyPlan] = Field(
        description="A detailed plan for each day of the trip"
    )


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-3.6-flash"

st.set_page_config(page_title="AI Travel Assistant", page_icon="✈️")
st.title("✈️ AI Travel Assistant")
st.write(
    "Tell me where you want to go and what matters to you. Share preferences over "
    "multiple messages, then generate a complete itinerary."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

if not API_KEY:
    st.info(
        "Add `GEMINI_API_KEY` to a `.env` file in this folder to enable the assistant."
    )
else:
    client = genai.Client(api_key=API_KEY)

    for message in st.session_state.chat_history:
        with st.chat_message("assistant" if message["role"] == "model" else "user"):
            st.markdown(message["parts"][0]["text"])

    if prompt := st.chat_input("Where would you like to travel?"):
        st.session_state.itinerary = None
        st.session_state.chat_history.append(
            {"role": "user", "parts": [{"text": prompt}]}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=st.session_state.chat_history,
                    )
                    reply = (
                        response.text
                        or "I couldn't create a response. Please try again."
                    )
                    st.markdown(reply)
                    st.session_state.chat_history.append(
                        {"role": "model", "parts": [{"text": reply}]}
                    )
                except Exception as exc:
                    st.error(f"I couldn't process that message: {exc}")
                    # Remove the unanswered prompt so it is not sent again as history.
                    st.session_state.chat_history.pop()

    if st.button(
        "Generate final itinerary",
        type="primary",
        disabled=not any(m["role"] == "user" for m in st.session_state.chat_history),
    ):
        transcript = "\n".join(
            f"{message['role']}: {message['parts'][0]['text']}"
            for message in st.session_state.chat_history
        )
        final_prompt = f"""
You are a travel assistant. Use the conversation below to create a complete itinerary
based strictly on the user's stated preferences. Fill every field and include one
daily plan for each trip day. If a detail is missing, make a reasonable assumption.

Conversation:
{transcript}
"""
        with st.spinner("Compiling your itinerary..."):
            try:
                result = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=final_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TravelItinerary,
                    ),
                )
                itinerary_json = result.text
                # Validate against the same schema before showing the structured result.
                itinerary = TravelItinerary.model_validate_json(itinerary_json)
                st.session_state.itinerary = json.loads(itinerary.model_dump_json())
            except Exception as exc:
                st.error(f"I couldn't generate a valid itinerary: {exc}")

    if st.session_state.itinerary:
        st.subheader("Your travel itinerary")
        st.json(st.session_state.itinerary)
