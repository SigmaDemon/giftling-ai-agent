import json
import os

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Giftling",
    page_icon="🎁",
    layout="centered",
)

st.title("gift")
st.title("🎁 Giftling")
st.write("Tell us about the person. We’ll suggest thoughtful gifts.")

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

recipient = st.text_input("Who is the gift for?", placeholder="My sister")
relationship = st.text_input("Your relationship to them", placeholder="Sister")
age = st.text_input("Their age", placeholder="30")
interests = st.text_area(
    "What do they like?",
    placeholder="Plants, true crime podcasts, cooking",
)
budget = st.text_input("Budget", placeholder="£40")
occasion = st.text_input("Occasion", placeholder="Birthday")

extra_answer = ""

if "follow_up_question" in st.session_state:
    st.info(st.session_state.follow_up_question)
    extra_answer = st.text_input("Your answer")

if st.button("Find gifts", use_container_width=True):
    if not recipient or not budget:
        st.warning("Please enter at least who the gift is for and your budget.")
        st.stop()

    with st.spinner("Thinking of gift ideas..."):
        prompt = f"""
You are Giftling, a helpful gift-recommendation assistant.

Return ONLY valid JSON in exactly this shape:

{{
  "follow_up_question": "string or empty string",
  "gifts": [
    {{
      "name": "string",
      "why": "string",
      "estimated_price": "string",
      "where_to_buy": "string",
      "search_url": "string"
    }}
  ]
}}

Rules:
- If you need one more important detail, put a short question in follow_up_question and return an empty gifts list.
- If you have enough information, make follow_up_question an empty string and return 5 to 8 gifts.
- Make suggestions specific, thoughtful, and appropriate for the person.
- Respect the budget.
- Do not recommend gift cards unless the user asks for one.
- Do not suggest weapons, drugs, gambling, alcohol for minors, or unsafe items.
- For search_url, use a Google Shopping search URL.

Recipient: {recipient}
Relationship: {relationship}
Age: {age}
Interests: {interests}
Budget: {budget}
Occasion: {occasion}
Extra answer: {extra_answer}
"""

        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        raw_text = "".join(
            block.text
            for block in message.content
            if getattr(block, "type", "") == "text"
        )

        cleaned_text = (
            raw_text.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            result = json.loads(cleaned_text)
        except json.JSONDecodeError:
            st.error("The AI returned an unexpected response. Please try again.")
            st.stop()

        follow_up_question = result.get("follow_up_question", "")

        if follow_up_question:
            st.session_state.follow_up_question = follow_up_question
            st.rerun()

        gifts = result.get("gifts", [])

        if not gifts:
            st.warning("No gift ideas were returned. Please try again.")
            st.stop()

        st.success("Here are some gift ideas:")

        for gift in gifts:
            with st.container(border=True):
                st.subheader(gift.get("name", "Gift idea"))
                st.write(gift.get("why", ""))
                st.caption(
                    f"Estimated price: {gift.get('estimated_price', 'Unknown')}"
                )
                st.caption(
                    f"Where to buy: {gift.get('where_to_buy', 'Unknown')}"
                )

                search_url = gift.get("search_url", "")

                if search_url:
                    st.link_button(
                        "Search this gift",
                        search_url,
                        use_container_width=True,
                    )