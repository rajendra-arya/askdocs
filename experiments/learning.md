# Chunking
- to split data into small chunks as per requirements
- we do overlapping to preserve context and maintain continuity between consecutive pieces of text.
- Handle duplicate tiny trailing non imp chunks 
    1. we need to handle tiny trailing chunks as its repeating the same last old data only in tiny chunks.
    2. remove tiny trailing chunks containing duplicate info which doesn't help in any info gain.
    3. chunk length measure toatal no character(token, word, para can be modified) in a chunk.
    4. chunk_overlap: "How many characters should the next chunk share with the previous chunk? 
        - Example:
            `chunk_size = 100`, `chunk_overlap = 80`
            - 80 shared characters
            - 20 new characters
                - chunk 1 = 0---100
                - chunk 2 =   20---120
                - chunk 3 =      40---140
            > The next chunk reuses 80 characters from the previous chunk and introduces only 20 new characters.
        - simple terms : *number of shared characters between consecutive chunks.*

# Embedding
- we need a embedding model to convert the string into vector(numerical repesentation)
- we get the model :
    - transformers : General-purpose library for thousands of transformer models.
    - sentence-transformers : Built specifically for sentence embeddings and semantic similarity.

- **Sentence Transformers (a.k.a. SBERT)** is the go-to Python module for using and training state-of-the-art embedding and reranker models.
        - Sbert: sentence transformer module : https://www.sbert.net/
        - run completely offline after the initial download
            - fix caching issue , by explicitly mentioning use local files
            - model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2" , local_files_only=True)
        - u can download the model using .save() to avoid internet access

   - ```py
        from sentence_transformers import SentenceTransformer

        sentences = ["This is an example sentence", "Each sentence is converted"]
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(sentences)
        print(embeddings)
    ```
- A dimension is a single numerical feature tracking a specific trait of a word's meaning. 
    - More dimensions mean deeper nuance but slower speed.
    - example : 
        - Dimension 1 (Is it alive?), Dimension 2 (Is it human?), Dimension 3 (Is it a place?)
        - Imagine the AI rates words on a scale from -1.0 to +1.0 based on three traits
- Industry Standards
    1. 384: Best for speed, mobile apps, and low storage.
    2. 768 - 1,536: The standard sweet spot for standard chatbots, enterprise search, and RAG systems.
    3. 3,072: Best for absolute maximum accuracy in complex legal or medical apps.

- similarity
    - Compare the matrix against another matrix for similarity 
    ```py
    # calculate similarity
    similarities = model.similarity(embedding, embedding)
    print(similarities)
    # tensor([[1.]])
    
    #                "Rajendra"   "Rajesh"   "Banana"
    #"Rajendra"  [[  1.00,        0.82,       0.05  ],
    #"Rajesh"     [  0.82,        1.00,       0.01  ],
    #"Banana"     [  0.05,        0.01,       1.00  ]]

    ```
    - The Score Ranges(cosine similarity)
        - **0.80 to 1.00: Highly identical meaning or context**(e.g., synonyms, close names).
        - **0.30 to 0.79: Broadly related topics** (e.g., "Cat" and "Dog").
        - **s-1.0 to 0.29: Unrelated concepts** (e.g., "Rajendra" and "Banana").
    - Diagonal (1.0): Top-left to bottom-right is always 1.0.
        - A word matching itself.
        - Rajendra == Rajendra
    - Mirror Image: Top-right and bottom-left values match exactly. 
        - A to B equals B to A as both will get same score.
        - Similarity of ("Rajendra" vs "Banana") anyway is 0.05
   
   - One more important lesson
        - **Embedding models don't compare dictionary meanings.**
        -  **They compare usage in language.**
        - That's why sometimes you'll see surprising similarities.
        - ```py           # Apple      Ape     App     Mango
            # Apple ([[1.0000, 0.3066, 0.4841, 0.4006],
            # Ape     [0.3066, 1.0000, 0.2029, 0.3092],
            # App     [0.4841, 0.2029, 1.0000, 0.3500],
            # Mango   [0.4006, 0.3092, 0.3500, 1.0000]])
            ```

# Similarty

- top k:
     ```py
    #sorted_indices[-3:][::-1]  #take last 3 then rev them
    #sorted_indices[::-1][:3] #rev entrie aray and get top 3
    top_k = np.argsort(scores)[::-1][:k] #k can be any value

    # sorted_indices[-1:-4:-1]
    # Rule of thumb
    # One slice ([-1:-k-1:-1]) → compact but harder to understand.
    # Two slices ([::-1][:k] or [-k:][::-1]) → much more readable and commonly seen in NumPy code.

    # we need to convert torch class into numpy asrray for slciing othewise it gives TabError
    # sorted_matrix = np.argsort(similarity[0].numpy())[::-1][:3]

    # find the top-k most similar chunks
    def search(query_embedding, embeddings, topk):
    # compute similarity scores between query and all document embeddings
    similarity = model.similarity(query_embedding, embeddings)

    # convert PyTorch tensor to np array, sort indices by similarity score, reverse(highest first) then slice(top-k) 
    sorted_indices = np.argsort(similarity[0].numpy())[::-1][:topk]

    result = [(int(i), float(similarity[0][i])) for i in sorted_indices] 
    return result
    ```

- Brute-force semantic search computes similarity against every embedding and sorts all results, so its time and memory cost grows with the number of chunks. 
    - 939 chunks → fine.
    - 100,000 chunks → slower.
    - 10,000,000 chunks → very expensive.

- **Vector databases** use **Approximate Nearest-Neighbor** (ANN) indexes to avoid scanning every embedding, making Top-K retrieval much faster at scale.
- **ANN** (Approximate Nearest Neighbor) 
    - it's a search technique used by vector databases to retrieve the most similar embeddings efficiently. 
    - Instead of comparing a query against every vector, ANN uses specialized indexes to search only promising regions of the vector space, trading a tiny amount of accuracy for a significant improvement in speed and scalability."
    - `Query -> Jump directly to vectors that are probably close -> Compare only a small subset -> Return Top 3`
    