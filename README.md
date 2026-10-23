# 🎁 Giftling

Giftling is an AI-powered gift-finding web app built with Python and Streamlit.

Users describe who they are buying for, their budget, the occasion, and the recipient’s interests. Giftling may ask one clarifying follow-up question, then returns 5–8 personalised gift ideas with a short explanation, estimated price, suggested place to buy, and a search link.

## How it works

1. The user enters details about the gift recipient.
2. The app sends the information to Anthropic Claude.
3. Claude either asks one useful follow-up question or returns gift recommendations.
4. The user receives clear, personalised gift ideas.

## Built with

- Python
- Streamlit — web interface
- Anthropic Claude Python SDK — AI recommendations
- python-dotenv — securely loads the API key from a local `.env` file
- Streamlit Community Cloud — free hosting

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Important

Add your Anthropic API key to a `.env` file:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

Never commit or share your `.env` file.
