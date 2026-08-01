import pymupdf4llm
import numpy as np
from sentence_transformers import SentenceTransformer

from .pdf_loader import make_chunks

# Load the embedding model from the local cache
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2" , local_files_only=True)
   
# book_text = pymupdf4llm.to_text("./data/The Accidental CTO Book.pdf")

# doc_chunks  = make_chunks(book_text, chunk_size=500, chunk_overlap=100, min_chunk_size=250) #taking around 20% overlap (old data)

def create_embeddings(data):
    return model.encode(data)

# find the top-k most similar chunks
def search(query_embedding, embeddings, topk):
    # compute similarity scores between query and all document embeddings
    similarity = model.similarity(query_embedding, embeddings)

    # convert PyTorch tensor to np array, sort indices by similarity score, reverse(highest first) then slice(top-k) 
    sorted_indices = np.argsort(similarity[0].numpy())[::-1][:topk]

    result = [(int(i), float(similarity[0][i])) for i in sorted_indices] 
    return result


def show_result(result, chunks):
    for idx, (index, sim_score) in enumerate(result, start=1):
        print("*" * 10) 
        print(f"""
        Rank: {idx}
        Score : {sim_score:.4f}
        \t\t{chunks[index]}""")
        print("=" * 10)


# query = "what is the company name?"

# doc_embeddings = create_embeddings(data=doc_chunks)
# query_embedding = create_embeddings(data=query)

# result = search(query_embedding=query_embedding, embeddings=doc_embeddings, topk=3)
# show_result(result=result, chunks=doc_chunks)





