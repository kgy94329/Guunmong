import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("Hello from ai-chatbot!")
    SECRETE_ENV = os.getenv("elevenlabs_api")
    print(SECRETE_ENV)


if __name__ == "__main__":
    main()
