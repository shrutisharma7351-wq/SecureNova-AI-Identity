import ollama

MODEL = "qwen3:4b"

client = ollama.Client(host="http://localhost:11434")


def ask_llm(prompt: str) -> str:
    try:
        response = client.chat(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]

    except ollama.ResponseError as e:
        raise RuntimeError(f"Ollama error: {e.error}") from e

    except Exception as e:
        raise RuntimeError(f"LLM connection error: {e}") from e