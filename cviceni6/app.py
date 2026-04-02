import os

from flask import Flask, jsonify, render_template, request

from llm import RagLLM
from rag import RateRAG, WeatherRAG, WikiRAG


app = Flask(__name__)


def get_api_key() -> str:
	"""Return Gemini API key from environment variable."""
	return os.getenv("GEMINI_API_KEY", "AIzaSyAk4PV2S5h8QvztwobAo0AcetVsiRf7xEw").strip()


def run_rag_chat(user_prompt: str, max_steps: int = 4) -> str:
	"""Run LLM with retrieval loop until it returns a final user-facing answer."""
	wiki = WikiRAG()
	weather = WeatherRAG()
	rates = RateRAG()

	prompt = user_prompt
	api_key = get_api_key()
	if not api_key:
		raise RuntimeError("Missing GEMINI_API_KEY environment variable.")

	for _ in range(max_steps):
		llm = RagLLM(api_key)
		response = llm.generate_content(prompt).strip()

		if response.startswith("WIKI:"):
			wiki_query = response[len("WIKI:") :].strip()
			wiki_result = wiki.retrieve(wiki_query)
			prompt = (
				"\n\nDoplnene informace z Wikipedie:\n"
				f"{wiki_result}\n\n"
				f"Odpovez na puvodni dotaz: {user_prompt}"
			)
			continue

		if response.startswith("WEATHER:"):
			weather_query = response[len("WEATHER:") :].strip()
			weather_result = weather.retrieve(weather_query)
			prompt = (
				"\n\nDoplnene informace o pocasi:\n"
				f"{weather_result}\n\n"
				f"Odpovez na puvodni dotaz: {user_prompt}"
			)
			continue

		if response.startswith("RATE:"):
			rate_query = response[len("RATE:") :].strip()
			rate_result = rates.retrieve(rate_query)
			prompt = (
				"\n\nDoplnene informace o kurzech:\n"
				f"{rate_result}\n\n"
				f"Odpovez na puvodni dotaz: {user_prompt}"
			)
			continue

		return response

	return "Odpoved se nepodarilo dokoncit, zkuste dotaz upresnit."


@app.get("/")
def index():
	return render_template("index.html")


@app.post("/api/chat")
def chat():
	data = request.get_json(silent=True) or {}
	message = (data.get("message") or "").strip()

	if not message:
		return jsonify({"error": "Zprava je prazdna."}), 400

	try:
		answer = run_rag_chat(message)
		return jsonify({"answer": answer})
	except Exception as exc:
		return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
	app.run(debug=True)
