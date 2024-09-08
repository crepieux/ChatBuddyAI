import os
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in the environment variables.")
else:
    logger.info("OPENAI_API_KEY is set in the environment variables.")

try:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {e}")

def send_openai_request(prompt: str) -> str:
    try:
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=100
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        return content
    except Exception as e:
        logger.error(f"Error in send_openai_request: {e}")
        return f"An error occurred: {str(e)}"

# Test the OpenAI integration
test_prompt = "Hello, AI. Can you hear me?"
logger.info(f"Testing OpenAI integration with prompt: '{test_prompt}'")
response = send_openai_request(test_prompt)
logger.info(f"OpenAI response: {response}")
