# rasi-palan — Jodiik n8n Workflow

This repository contains a single n8n workflow named **Jodiik** that fetches daily zodiac (rasi) predictions for all 12 signs from the VedicAstro API and then transforms those predictions into punchy, multi-lingual blog-style horoscopes (English + 5 Indian languages) using a Google Gemini (PaLM) model.

---

## What this workflow does ✅

- Generates a list of zodiac signs (Aries — Pisces) and iterates through each.
- Calls the VedicAstroAPI daily-sun endpoint to fetch a small daily prediction for each zodiac sign.
- Sends the raw API response to a Google Gemini model with a Persona prompt (the `Cosmic Z` persona) to convert the prediction into an engaging blog-style horoscope.
- Produces a final JSON containing content in 6 languages — English, Tamil, Hindi, Telugu, Malayalam, Kannada — with both a full blog post and short summary for each zodiac sign.

---

## Workflow Details (nodes) 🔧

The `jodiik.json` workflow uses these nodes:

- **When clicking ‘Execute workflow’** (Manual Trigger)
	- Triggers the workflow manually from the n8n editor (useful while developing or testing).
	- You can replace this with a Cron node for scheduled runs.

- **Code in JavaScript** (Node: `Code in JavaScript`)
	- Creates the item list of 12 zodiacs:
		- It returns an array of JSON items like { sign_id: 1, sign_name: 'Aries', lang: 'en' }.
	- Example snippet from node:
		```js
		const signs = [
			{ id: 1, name: 'Aries' },
			{ id: 2, name: 'Taurus' },
			// ... all 12 signs ...
		];
		const lang = 'en';
		return signs.map(sign => ({ json: { sign_id: sign.id, sign_name: sign.name, lang } }));
		```

- **HTTP Request** (Node: `HTTP Request`)
	- Calls: `https://api.vedicastroapi.com/v3-json/prediction/daily-sun` using JSON body
	- Example JSON body (the node currently uses static date "28/11/2025"):
		```json
		{
			"date": "28/11/2025",
			"zodiac": {{ $json.sign_id }},
			"type": "small",
			"lang": "{{ $json.lang }}",
			"api_key": "<YOUR_VEDIC_ASTRO_API_KEY>"
		}
		```
	- Tip: Replace date with a dynamic expression if you want to always fetch today's date, e.g. `={new Date().toLocaleDateString('en-GB')}` to obtain dd/mm/yyyy.

- **Message a model** (Google Gemini / PaLM node)
	- Model ID: `models/gemini-2.5-flash`
	- Prompt instructions convert raw API responses to a multi-lingual blog-style horoscope using the `Cosmic Z` persona and produce a single JSON object with language keys.
	- Make sure `GooglePaLM` credentials are configured in your n8n instance (see details below).

---

## Setup and Credentials 🔐

1. Install and run an n8n instance (desktop, cloud, or docker).
2. Import `jodiik.json` into n8n (from the editor: workflows > import).
3. Configure your credentials:
	 - **VedicAstro API**: Obtain an API key from https://vedicastroapi.com/ and put it in the HTTP Request node or use n8n Credentials / environment variable to keep it secret.
	 - **Google Gemini / PaLM**: Add a Google PaLM (or Gemini) credential in n8n. The node references a `googlePalmApi` credential — don't commit secrets in code.
4. Optional: Update the date so it uses the current date rather than a hard-coded one.

Security note: Never commit API keys or secrets to your git repository. Use n8n credentials or environment variables.

---

## Running the workflow ▶️

1. Open the workflow in n8n.
2. Replace the placeholder `<YOUR_VEDIC_ASTRO_API_KEY>` in the HTTP Request node with your key or set as a secure n8n credential/config.
3. Configure the Google PaLM credentials in n8n (Model ID: `models/gemini-2.5-flash` by default).
4. Click `Execute Workflow` (manual trigger), or replace the manual trigger with a Cron node to schedule daily runs.

---

## Output structure (expected) 📦

The final response from the Gemini model should be a single JSON object with this structure (per the node's prompt):

{
	"english": [ { "zodiac": "Aries", "blog_post": "String", "short_summary": "One sentence" }, ... (12 signs) ],
	"tamil": [ ... ],
	"hindi": [ ... ],
	"telugu": [ ... ],
	"malayalam": [ ... ],
	"kannada": [ ... ]
}

Each language array should contain 12 objects (one per zodiac sign).

---

## Tips & Extending the Workflow 💡

- Use a Cron node instead of the manual trigger to schedule daily posts.
- Add logging and error handling: check the HTTP request response codes and add a fallback message for the model if the API fails.
- Add additional output formats (e.g., tweet/post for social media) or integrate with a CMS.

---

## Troubleshooting & FAQs ⚠️

- If you hit API errors for VedicAstro: ensure your api_key is valid and the endpoint is reachable.
- If the model node fails: check Google PaLM credentials and the node's input formatting.
- If the workflow returns invalid JSON: verify that the model output is a strictly valid JSON string (model prompts can produce extra text if not constrained properly).

---

## Contributing

If you'd like to improve the workflow:

- Add tests or run-locally helpers.
- Make the `date` field dynamic and add a configuration node for `lang` or the list of zodiac signs.
- Add support for more languages or different content styles.

---

## License

MIT
