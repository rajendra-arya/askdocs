# import pymupdf


def make_chunks(doc, chunk_size, chunk_overlap, min_chunk_size):
    """
    Split PDF pages into overlapping chunks while preserving page provenance.

    Args:
        doc: PDF document pages containing text and page numbers.
        chunk_size (int): Maximum number of characters per chunk.
        chunk_overlap (int): Number of characters shared between chunks.
        min_chunk_size (int): Minimum characters required to keep a chunk.

    Returns:
        list[dict]: Chunks containing text and their source page numbers.
    """

    # Stores the small remainder from the current page so it can be carried over to the next page.
    temp = {
        "chunk": "",
        "page_no": [],
    }

    chunks = []

    # Loop through each page of the document
    for page in doc:
        current_pg_data = page.get_text()
        current_pg_no = page.number

        # If there is a leftover chunk from the previous page, combine it with the current page's text.
        if len(temp["chunk"]) != 0:
            data = temp["chunk"] + current_pg_data
        else:
            data = current_pg_data

        # Calculate how far we move forward for the next chunk.
        step = chunk_size - chunk_overlap

        # Extra iteration helps capture the remaining text at the end.
        for i in range(chunk_size, len(data) + chunk_size, step):
            # Take the previous chunk_size characters.
            chunk = data[i - chunk_size : i]

            if min_chunk_size <= len(chunk) <= chunk_size:
                # If the chunk is smaller than chunk_size and temp is empty, store it as the remainder to carry into the next page.
                if (
                    len(chunk) < chunk_size and temp["chunk"] == ""
                ):  # best/earliest remainder to carry forward
                    temp = {"chunk": chunk, "page_no": [current_pg_no]}
                    # print("Found Small chunk! added to temp: ", temp)

                # If temp already contains a remainder, don't overwrite it with another smaller overlapping chunk.
                elif len(chunk) < chunk_size and temp["chunk"] != "":
                    pass
                else:
                    temp_len = len(temp["chunk"])
                    start = i - chunk_size
                    end = i

                    # Check whether the carried-over temp belongs inside the current complete chunk.
                    if start < temp_len < end:  # issue here <= boundary cases
                        # This chunk contains text from both the previous page and the current page, so store both page numbers.
                        chunks.append(
                            {
                                "chunk": chunk,
                                "page_no": [*temp["page_no"], current_pg_no],
                            }
                        )
                        # Temp has now been consumed. Clear it so old page information doesn't leak into future chunks.
                        temp["chunk"] = ""
                        temp["page_no"] = []

                    else:
                        # Normal chunk that belongs only to the current page.
                        chunks.append({"chunk": chunk, "page_no": [current_pg_no]})

        # On the last page, add any remaining text stored in temp.
        if current_pg_no == (len(doc) - 1):
            # Only add the final remainder if it meets the minimum size.
            if len(temp["chunk"]) >= min_chunk_size:
                chunks.append({"chunk": temp["chunk"], "page_no": temp["page_no"]})
            else:
                print(
                    f"remainder temp chunk is less than min_chunk_size({min_chunk_size})"
                )
                print(f'last iteration chunk "{chunk}".')

    return chunks


# doc = pymupdf.open("../data/The Accidental CTO Book.pdf")
# chunks_with_pg = make_chunks(doc, chunk_size=500, chunk_overlap=100, min_chunk_size=100)
# print(chunks_with_pg)
