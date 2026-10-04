# enterprise_ai_knowledge_hub


enterprise_ai_knowledge_hub is a production-oriented AI assistant designed to help users interact with enterprise knowledge through natural language. The project demonstrates how modern Generative AI, Retrieval-Augmented Generation (RAG), Agentic AI, and scalable backend architecture can be combined to build an intelligent enterprise knowledge assistant.

The system allows users to upload enterprise documents such as PDF, DOCX, and TXT files. Documents are processed asynchronously using Redis and RQ workers. The ingestion pipeline extracts content, splits documents into meaningful chunks, generates vector embeddings, and stores them in Qdrant for semantic search.

When a user asks a question, the system uses an Agentic RAG workflow built with LangGraph and LangChain. The workflow can understand conversation context, rewrite questions when necessary, retrieve relevant knowledge, evaluate retrieval quality, retry retrieval when the results are insufficient, and generate grounded responses using an LLM.

The application maintains conversation history using PostgreSQL and uses LangGraph's PostgreSQL checkpointer to persist workflow state across requests and application restarts. Each conversation is associated with a unique thread, allowing the AI workflow to maintain state across multiple interactions.

### Technology Stack

* React — Frontend
* Python — Backend and AI services
* FastAPI — REST API
* LangChain — LLM and RAG orchestration
* LangGraph — Agentic workflow orchestration
* OpenAI — LLM and embeddings
* Qdrant — Vector database
* PostgreSQL — Application data and workflow persistence
* Redis — Message broker
* RQ — Background job processing
* Docker — Infrastructure and local development

The project is designed as a practical demonstration of enterprise AI architecture, asynchronous processing, RAG pipelines, vector search, conversational memory, agentic workflows, and scalable AI application development.

