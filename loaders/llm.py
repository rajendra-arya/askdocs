import os
import re

import dotenv
from google import genai

# load variables from .env and set in os.environ
dotenv.load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# construct prompt using the chunks and query
def generate_response(chunks, query):
    context = [
        {
            "source_id": id,
            "score": chunk["score"],
            "text": chunk["text"],
            "page_no": chunk["page_no"],
        }
        for id, chunk in enumerate(chunks, start=1)
    ]

    formatted_context = "\n-----\n".join(
        f"Source: {i['source_id']}\nText: {i['text']}" for i in context
    )
    # print(formatted_context)

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        system_instruction=f"""
        You are an expert assistant. Answer the user's query using only the provided sources.
        When making a claim, cite the relevant source using exactly this format: [Source N].
        Do not generate or infer page numbers.
        If the provided sources do not contain enough information to answer the query, politely say you don't know.

        {formatted_context}
        """,
        input=query,
    )

    response = interaction.output_text

    def replace_citation(match):
        # Extract all source numbers from: [Source 1] -> ["1"] , [Source 1, Source 2] -> ["1", "2"]
        source_ids = re.findall(r"\d+", match.group(1))

        pages = []

        for source_id in source_ids:
            for chunk in context:
                if chunk["source_id"] == int(source_id):
                    pages.extend(chunk["page_no"])
                    break

        return (
            f"[Page {pages[0]}]"
            if len(pages) == 1
            else f"[Pages {', '.join(map(str, pages))}]"
        )

    # Replace both single and combined citations
    response = re.sub(r"\[Source (.+?)\]", replace_citation, response)

    return response
