import ollama

def test_connection():
    try:
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': 'Reply with just the word: connected'}]
        )
        print(response.message.content)
    except Exception as e:
        print(f"Failed to connect to Ollama: {e}")


if __name__ == "__main__":
    test_connection()