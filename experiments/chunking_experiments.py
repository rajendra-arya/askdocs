text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

## appraoch 3.3 - final version with docstring
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




## approach 3.2 - clean & resuable
def make_chunks(data, chunk_size, chunk_overlap, min_chunk_size):
    chunks = []
    step = chunk_size - chunk_overlap #dynamic overlapping
    for i in range(chunk_size ,len(data)+chunk_size, step):
        chunk = data[i-chunk_size:i]
        if(min_chunk_size <= len(chunk) <= chunk_size):
            chunks.append(data[i-chunk_size:i]) 
    return chunks
    
print(make_chunks(text, chunk_size=5, chunk_overlap=3, min_chunk_size=4))
# ['ABCDE', 'CDEFG', 'EFGHI', 'GHIJK', 'IJKLM', 'KLMNO', 'MNOPQ', 'OPQRS', 'QRSTU', 'STUVW', 'UVWXY', 'WXYZ']




## approach 3.1 
# removing tiny trailing chunks containing duplicate info, as we are not getting any info gain from it
# making it resusable func
def make_chunks(data, c_size, c_overlap, min_c_size):
    chunks = []
    chunk_size = c_size
    chunk_overlap = c_overlap
    min_chunk_size= min_c_size
    step = chunk_size - chunk_overlap #dynamic overlapping # how much new data chunk will have
    for i in range(chunk_size ,len(data)+chunk_size, step):
        chunk = text[i-chunk_size:i]
        if(min_chunk_size <= len(chunk) <=5):
            chunks.append(text[i-chunk_size:i]) 
    return chunks
    
print(make_chunks(text, 5, 3, 4))
#['ABCDE', 'CDEFG', 'EFGHI', 'GHIJK', 'IJKLM', 'KLMNO', 'MNOPQ', 'OPQRS', 'QRSTU', 'STUVW', 'UVWXY', 'WXYZ']




# approach 3 #finally working -- issue : repetetion of small parts 
def make_chunks(text):
    chunks = []
    chunk_size = 5
    overlap = chunk_size - 2 #dynamic overlapping
    for i in range(chunk_size , len(text), overlap):
        chunks.append(text[i-chunk_size:i])
    print(chunks)

make_chunks(text)
# Output : 
# ['ABCDE', 'CDEFG', 'EFGHI', 'GHIJK', 'IJKLM', 'KLMNO', 'MNOPQ', 'OPQRS', 'QRSTU', 'STUVW', 'UVWXY', 'WXYZ', 'YZ']




#  approach 2:
    # chunks = []
    # start = 0
    # end = 5
    # start = end
    # end = end+5
    # print(text[start:end])
    # start = end
    # end = end+5
    # print(text[start:end])
    # start = end
    # end = end+5
    # print(text[start:end])

# output
# ABCDE, FGHIJ, KLMNO, PQRST



# approch 1:
# def make_chunks():
#     start = 0
#     end = 500
#     chunked_list = []
#     for i in range(start, end):
#         chunked_list.append(i)
#     start+=end