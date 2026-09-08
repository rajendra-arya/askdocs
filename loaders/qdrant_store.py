import pymupdf
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .embedder import create_embeddings
from .pdf_loader import make_chunks

# intialize connection with client
client = QdrantClient(url="http://localhost:6333")

# create collection
if not client.collection_exists("askdocs"):
    # load pdf
    doc = pymupdf.open("./data/The Accidental CTO Book.pdf")

    # create chunks
    chunks = make_chunks(doc=doc, chunk_size=500, chunk_overlap=100, min_chunk_size=250)

    # create embeddings for chunk text only
    embeddings = create_embeddings(data=[i["chunk"] for i in chunks])

    # store embedddings in qdrant
    ## create collection
    client.create_collection(
        collection_name="askdocs",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    ## upsert doc chunk embeddings and metadata to qdrant collection
    info = client.upsert(
        collection_name="askdocs",
        points=[
            PointStruct(
                id=rank,
                vector=vector,
                payload={"text": chunk["chunk"], "page_no": chunk["page_no"]},
            )
            for rank, (vector, chunk) in enumerate(zip(embeddings, chunks), start=1)
        ],
    )
    print(info)


# get chunks and metadata
def retrieve_chunks(query):
    query_embedding = create_embeddings(query)
    # search
    search_result = client.query_points(
        collection_name="askdocs", query=query_embedding, with_payload=True, limit=2
    ).points
    if search_result:
        data = [
            {
                "score": point.score,
                "text": point.payload["text"],
                "page_no": point.payload["page_no"],
            }
            for point in search_result
        ]
        return data
    else:
        return []


# delete collection
# client.delete_collection("askdocs")
