# Pitch Room

A brief goes in. A costed, trilingual media plan comes out, priced from a real rate card.

Built as a prototype for a conversation with a large Indian news group. The point it
proves: the language model chooses the media mix, and the code does all the arithmetic.
No model ever states a price.

## What it does

1. Reads an advertiser brief
2. Retrieves from a client corpus of rate cards, past campaigns and audience studies
3. Drafts a plan in English, Japanese or Hindi
4. Prices it from the rate card, print per square centimetre with position and season
   loading, digital on CPM, content and events at fixed price
5. Applies the real commercial ladder: negotiated discount, agency commission, GST on
   space at 5 percent and on services at 18 percent
6. Produces reach, cost per thousand, a release order and an export

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then add your key
streamlit run app.py
```

Without a key it still runs and shows the saved example, so a demo never breaks.

## Put it on GitHub

```bash
git init
git add .
git commit -m "Pitch Room prototype"
git branch -M main
git remote add origin https://github.com/YOURNAME/pitch-room.git
git push -u origin main
```

`.streamlit/secrets.toml` is in `.gitignore`. Never commit a key.

## Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with GitHub
2. New app, pick the repo, branch `main`, file `app.py`
3. Advanced settings, Secrets, paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Deploy. Changes pushed to `main` redeploy automatically.

To change the model without touching code, add `PITCHROOM_MODEL` to the environment.

## Swapping in real data

Everything a client would replace lives in `toi_data.py`:

- `PRINT_EDITIONS` rate per square centimetre and readership per edition
- `POSITION_LOADING` and `SEASON_LOADING` percentages
- `DIGITAL` and `CONTENT` inventory with CPM or fixed price
- `AGENCY_COMMISSION`, `GST_SPACE`, `GST_SERVICE`, `CREDIT_DAYS`
- `CORPUS` the documents retrieval runs over

For production, move the corpus into Postgres with pgvector and keep the rate card in a
normal table. Prices need exact lookups, never similarity search.

## Known limits

Reach figures are modelled, not measured. Deduplication across editions and platforms is
approximated. Rates are illustrative. None of this is a substitute for the client's own
card and their own audience data.
