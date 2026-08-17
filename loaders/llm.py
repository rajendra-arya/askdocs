import os

import dotenv
from google import genai

# load variables from .env and set in os.environ
dotenv.load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# construct prompt using the chunks and query
def generate_response(chunks, query):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        system_instruction=f"""You are expert user helper, your work is to answer query based on the following below context only. 
        if the query is out of the context just say i don't know polietly.
        {chunks}
        """,
        input=f"{query}"
    )
    return interaction.output_text