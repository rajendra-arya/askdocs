import pymupdf4llm

book_text = pymupdf4llm.to_text("./data/The Accidental CTO Book.pdf")

def make_chunks(data, chunk_size, chunk_overlap, min_chunk_size):
    """
    Split text into overlapping chunks of a specified size.

    Args:
        data (str): Input text to be chunked.
        chunk_size (int): Maximum number of characters per chunk.
        chunk_overlap (int): Number of characters shared between consecutive chunks.
        min_chunk_size (int): Minimum number of characters required to keep the final chunk.

    Returns:
        list[str]: A list of overlapping text chunks.
    """
    
    chunks = []
    step = chunk_size - chunk_overlap #dynamic overlapping
    for i in range(chunk_size ,len(data)+chunk_size, step):
        chunk = data[i-chunk_size:i]
        if(min_chunk_size <= len(chunk) <= chunk_size):
            chunks.append(chunk) 
    return chunks
    
book_chunk = make_chunks(book_text, chunk_size=100, chunk_overlap=80, min_chunk_size=80)

three_chunks = book_chunk[0:3]
for i in three_chunks:
    print(i)
    print("*"*50)

print("no of characters---------------:", len(book_chunk[0]))