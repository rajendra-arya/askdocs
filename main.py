from loaders.llm import generate_response
from loaders.qdrant_store import retrieve_chunks


def main():
    while query := input("Enter query: "):
        chunks = retrieve_chunks(query)
        response = generate_response(chunks=chunks, query=query)
        print(response)         

if __name__ == "__main__":
    main()