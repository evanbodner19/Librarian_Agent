import ollama
import logging

logger = logging.getLogger('librarian')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/ai_poc.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def test_connection():
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': 'Reply with just the word: connected'}]
        )
        print(response.message.content)
    except Exception as e:
        print(f"Failed to connect to Ollama: {e}")

def classify(filename, ext, file_size):
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{
                'role': 'user',
                'content': f"You are a file classifier. Given a file\'s details, return ONLY a single category name from this list: School, Coding, Audio, Video, Personal, Other. Return nothing else — no explanation, just the category name.\n\n File name: {filename}\n Extension: {ext}\n Size: {file_size} bytes"
            }]
        )
        category = response.message.content.strip()
        logger.info(f"Classified file '{filename}' as category: {category}")
        return category
    except Exception as e:
        logger.error(f"Failed to classify file: {e}")
        return "Other"


if __name__ == "__main__":
    test_connection()
    print(classify("homework.docx", "docx", 204800))
    print(classify("script.py", "py", 10240))
    print(classify("song.mp3", "mp3", 5120000))
    print(classify("movie.mp4", "mp4", 1048576000))
    print(classify("diary.txt", "txt", 4096))
    print(classify("archive.zip", "zip", 52428800))