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
            > The next chunk reuses 80 characters from the previous chunk and introduces only 20 new characters.
        - simple terms : *number of shared characters between consecutive chunks.*