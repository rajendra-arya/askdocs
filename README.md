# AskDocs

**AskDocs is a from-scratch RAG-based document question-answering system for PDF documents. It uses semantic retrieval, Qdrant vector search, and an LLM to generate grounded answers with source citations.**

## What AskDocs Does

AskDocs indexes PDF documents, retrieves relevant passages for a user's question, and uses an LLM to generate an answer grounded in the retrieved context.

```text
PDF documents
      ↓
Text extraction
      ↓
Chunking + metadata
      ↓
Embeddings
      ↓
Qdrant vector search
      ↓
Relevant chunks
      ↓
     LLM
      ↓
Grounded answer + citations
```

## Features

- PDF text extraction
- Custom chunking with overlap
- Page-level provenance
- Sentence Transformers embeddings
- Semantic retrieval
- Qdrant vector search
- Grounded LLM answer generation
- Source and page citations
- Multi-document indexing
- Grounded refusal when retrieved context is insufficient
- Conversational memory *(in progress)*

## Multi-Document Retrieval

AskDocs supports indexing multiple PDF documents in the same Qdrant collection.

Each chunk retains metadata including:

- `doc_id`
- `page_no`
- `text`

This metadata allows retrieved content to be traced back to its source document and page.

To test retrieval across documents, the term **"agent"** was used across documents covering different concepts:

- AI agents
- Reinforcement-learning agents
- Physical/security agents

This test showed that ambiguous queries may require retrieving enough candidates to surface different relevant interpretations across documents.

## Source Citations

Document and page metadata are preserved from indexing through retrieval.

The LLM is instructed to reference retrieved sources, and the application maps those references to the corresponding document and page.

Example:

```text
[agent_reinforcement_learning, Pages: 0, 1]
```

This allows generated answers to be traced back to the retrieved evidence.

## Retrieval Behavior

AskDocs was tested with ambiguous queries to examine how retrieval depth affects the results.

For example:

> What are the different meanings of the term "agent" across the provided documents?

With a smaller retrieval depth, not all three relevant agent documents were retrieved. Increasing the retrieval depth allowed all three to be retrieved.

This highlighted a practical RAG trade-off: retrieval depth affects how many relevant interpretations can be surfaced, while increasing it can also introduce more context for the generation step.

AskDocs also tests questions outside the information contained in the indexed documents. When the retrieved context is insufficient, the system is instructed not to fabricate an answer.

Example:

```text
Question: What is the capital of Japan?

Answer: I don't know.
```

## Architecture

### Indexing Pipeline

```text
PDF
 ↓
Extract text
 ↓
Create chunks
 ↓
Attach document + page metadata
 ↓
Generate embeddings
 ↓
Store vectors + payload in Qdrant
```

### Query Pipeline

```text
User question
 ↓
Generate query embedding
 ↓
Search Qdrant
 ↓
Retrieve relevant chunks
 ↓
Construct grounded prompt
 ↓
Generate answer
 ↓
Resolve source citations
```

## Technology Stack

- **Python**
- **PyMuPDF** — PDF processing and text extraction
- **Sentence Transformers** — text embeddings
- **Qdrant** — vector database and semantic retrieval
- **Google Gemini** — LLM-based answer generation

## Roadmap

### Completed

- [x] PDF ingestion and text extraction
- [x] Custom chunking
- [x] Semantic embeddings and retrieval
- [x] Qdrant vector search
- [x] Grounded RAG generation
- [x] Source and page citations
- [x] Multi-document retrieval

### In Progress

- [ ] Conversational memory
- [ ] Streaming responses
- [ ] Hybrid search

### Planned

- [ ] Web application
- [ ] Document management
- [ ] Deployment and monitoring

## Current Limitations

- Changing the indexed PDF set currently requires rebuilding the Qdrant collection.
- Conversation memory is currently session-level and stored in memory.
- There is no web frontend yet.
- Persistent conversation storage is not implemented.
- Authentication, deployment, and monitoring are not yet implemented.