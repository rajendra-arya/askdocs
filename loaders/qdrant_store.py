from pathlib import Path

import pymupdf
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .embedder import create_embeddings
from .pdf_loader import add_document_metadata, make_chunks

# initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")


# create collection
if not client.collection_exists("askdocs"):
    # find all PDF files in the directory
    pdf_files = list(Path("./data").glob("*.pdf"))

    all_chunks = []

    for pdf_path in pdf_files:
        doc = pymupdf.open(pdf_path)

        # use the filename as the document identifier
        doc_id = pdf_path.stem

        # create chunks
        chunks = make_chunks(
            doc=doc, chunk_size=500, chunk_overlap=100, min_chunk_size=250
        )

        # attach document id to every chunk
        chunks_with_meta = add_document_metadata(chunks=chunks, doc_id=doc_id)

        # combine chunks from all documents for indexing
        all_chunks.extend(chunks_with_meta)

    # create embeddings for all chunks
    embeddings = create_embeddings(data=[i["chunk"] for i in all_chunks])

    # store embeddings and document metadata in Qdrant
    ## create collection
    client.create_collection(
        collection_name="askdocs",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    ## upsert doc chunk embeddings and metadata
    info = client.upsert(
        collection_name="askdocs",
        points=[
            PointStruct(
                id=rank,
                vector=vector,
                payload={
                    "text": chunk["chunk"],
                    "page_no": chunk["page_no"],
                    "doc_id": chunk["doc_id"],
                },
            )
            for rank, (vector, chunk) in enumerate(zip(embeddings, all_chunks), start=1)
        ],
    )
    print(info)


# get chunks and metadata
def retrieve_chunks(query):
    query_embedding = create_embeddings(query)

    # search
    search_result = client.query_points(
        collection_name="askdocs",
        query=query_embedding,
        with_payload=True,
        limit=3,
    ).points

    if search_result:
        data = [
            {
                "score": point.score,
                "text": point.payload["text"],
                "page_no": point.payload["page_no"],
                "doc_id": point.payload.get("doc_id") or "Unknown",
            }
            for point in search_result
        ]
        return data
    else:
        return []


# delete collection
# client.delete_collection("askdocs")
