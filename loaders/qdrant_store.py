import pymupdf4llm
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .embedder import create_embeddings
from .pdf_loader import make_chunks

## intialize connection with client
client = QdrantClient(url="http://localhost:6333")

# create collection
if not client.collection_exists("askdocs"):
    # load pdf
    doc_text = pymupdf4llm.to_text("./data/The Accidental CTO Book.pdf")

    # create chunks
    text_chunks = make_chunks(
        data=doc_text, chunk_size=500, chunk_overlap=100, min_chunk_size=250
    )

    # create embeddings
    embeddings = create_embeddings(data=text_chunks)

    # store embedddings in qdrant
    ## create collection
    client.create_collection(
        collection_name="askdocs",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    ## upsert doc chunk embeddings to qdrant collection
    info = client.upsert(
        collection_name="askdocs",
        points=[
            PointStruct(id=rank, vector=vector, payload={"text": text})
            for rank, (vector, text) in enumerate(zip(embeddings, text_chunks), start=1)
        ],
    )
    print(info)


# retrieve
while query := input("Enter query: "):
    query_embedding = create_embeddings(query)
    # search
    search_result = client.query_points(
        collection_name="askdocs", query=query_embedding, with_payload=True, limit=2
    ).points

    if search_result:
        # display top 2 result
        for rank, point in enumerate(search_result, start=1):
            print(f"""
        Rank: {rank}
        Score:{point.score:.3f}
        Text: \n{point.payload["text"]}
        """)
    else:
        print("No relevant documents found.")
