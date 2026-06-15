# Domain

My domain is student reviews and experiences with professors and courses at Stevens Institute of Technology. This information is valuable because students often want to know about teaching quality, workload, grading style, and course difficulty before registering. Official course descriptions do not usually provide this information, so students must search through multiple review sites and discussion forums.

# Documents

Sources include:

1. Rate My Professors - Stevens Institute of Technology
2. Rate My Professors professor directory
3. Erisa Terolli review page
4. Paul Schwartz review page
5. David Klappholz review page
6. Stevens reviews on Niche
7. Stevens overview on Niche
8. Reddit discussion about attending Stevens
9. Reddit discussion about CS and Math professors
10. Reddit discussion about professor quality and student experiences

# Chunking Strategy

Most documents are short reviews and discussion posts. I will use chunks of approximately 500 characters with 100 characters of overlap. This size is large enough to keep a complete student opinion together while still allowing precise retrieval. The overlap helps preserve context when important information spans chunk boundaries.

# Retrieval Approach

I plan to use the all-MiniLM-L6-v2 embedding model through sentence-transformers. I will retrieve the top 5 most relevant chunks for each query. Retrieving too few chunks may miss useful information, while retrieving too many may introduce irrelevant context and reduce answer quality.

# Architecture

Document Sources
|
v
Document Ingestion
|
v
Chunking
(500 chars, 100 overlap)
|
v
Embeddings
(all-MiniLM-L6-v2)
|
v
Vector Store
(ChromaDB)
|
v
Retrieval
(top-k = 5)
|
v
Generation
(Groq LLM)

# Evaluation Plan

Question 1:
Which Stevens professors are frequently praised for clear explanations?

Expected Answer:
The response should identify professors who receive repeated positive comments about teaching clarity in the collected reviews.

Question 2:
Which professors are described as difficult graders?

Expected Answer:
The response should identify professors who are repeatedly described as grading harshly or assigning difficult exams.

Question 3:
What concerns do students mention about CS courses?

Expected Answer:
The response should summarize recurring concerns found in the collected documents.

Question 4:
What positive qualities do students mention about office hours?

Expected Answer:
The response should reference comments about accessibility, helpfulness, or responsiveness.

Question 5:
Which courses are commonly described as workload-intensive?

Expected Answer:
The response should identify courses that multiple students describe as having heavy workloads.

# Anticipated Challenges

1. Reviews may be subjective and sometimes contradictory.
2. Important information may be spread across multiple reviews.
3. Retrieval may return off-topic comments.
4. Some professors may have limited review data.

# AI Tool Plan

I will use AI tools to help implement specific components of the RAG pipeline while making the final design and debugging decisions myself.

* For chunking, I will provide my chunking strategy and ask the AI tool to help implement the chunk_text() function.
* For embeddings, I will provide my retrieval requirements and ask for code that generates embeddings using all-MiniLM-L6-v2.
* For vector storage, I will ask for assistance integrating ChromaDB and storing document chunks with metadata.
* For retrieval, I will ask for code that performs semantic search and returns the top 5 most relevant chunks.
* For generation, I will ask for help constructing prompts that combine retrieved context with a Groq-hosted LLM while requiring source attribution.
* I will review, test, and modify all generated code before using it in the final project.
