  # RAG Backend API                                                                                
                                                                                                   
  A production-oriented backend service for building Retrieval-Augmented Generation (RAG)          
  pipelines. Built with FastAPI, it handles the full document processing lifecycle — from upload to
   semantic search-ready chunks.                                                                   
                                                                                                   
  ## What it does 
                                                                                                   
  Upload a document and the system automatically:
                                                                                                   
  1. **Saves** the file to disk with a content hash (deduplication built-in)
  2. **Parses** it using Docling — extracts clean text from PDFs, DOCX, images, HTML               
  3. **Chunks** the content using HybridChunker — semantically aware splitting      
  4. **Tracks status** through the entire pipeline in PostgreSQL                                   
                                                                
  UPLOADED → PARSED → CHUNKED → EMBEDDED → COMPLETED                                               
                                                                                                   
  ## Tech Stack                                                                                    
                                                                                                 
  | Layer | Technology |
  |---|---|
  | API | FastAPI |
  | Database | PostgreSQL + SQLAlchemy |                                                           
  | Migrations | Alembic |
  | Document parsing | Docling |                                                                   
  | Chunking | Docling HybridChunker |
  | Async processing | asyncio + to_thread |                                                       
                                                                                                   
  ## Supported File Types                                                                          
                                                                                                   
  | Format | Extension |
  |---|---|
  | PDF | `.pdf` |
  | Word | `.docx` |
  | PowerPoint | `.pptx` |                                                                         
  | Web | `.html` |
  | Images (OCR) | `.png`, `.jpg`, `.tiff`, `.bmp` |                                               
                                                                                                   
  ## Project Structure
                                                                                                   
  ├── app/        
  │   ├── routers/          # API endpoints
  │   ├── services/         # Business logic
  │   │   ├── upload_file_logic.py   # file saving + deduplication                                 
  │   │   ├── file_parsed_content.py # Docling parsing                                             
  │   │   ├── file_chunk.py          # HybridChunker                                               
  │   │   └── file_services.py       # DB operations                                               
  │   ├── schemas/          # Pydantic models                                                      
  │   └── logger/           # Logging config
  ├── database/                                                                                    
  │   ├── models.py         # SQLAlchemy models                                                    
  │   └── database_engine.py
  ├── config/                                                                                      
  │   └── settings.py       # Environment config                                                   
  ├── disc/                 # Uploaded files
  ├── parsed_disc/          # Parsed markdown output                                               
  ├── chunks_disc/          # Chunked JSONL output                                                 
  └── alembic/              # DB migrations
                                                                                                   
  ## API Endpoints
                                                                                                   
  | Method | Endpoint | Description |
  |---|---|---|                                                                                    
  | `GET` | `/` | Server health check |
  | `GET` | `/health` | Database health check |
  | `POST` | `/file/upload_file` | Upload and process document |                                   
  | `GET` | `/file/all_files` | List all files |
  | `GET` | `/file/find_file/{name}` | Find file by name |                                         
  | `DELETE` | `/file/delete_file/{id}` | Delete file |                                            
                                                                                                   
  ## Setup                                                                                         
                  
  ### 1. Clone & install dependencies                                                              
   
  ```bash                                                                                          
  git clone <repo-url>
  cd rag
  python -m venv .venv
  source .venv/bin/activate                                                                        
  pip install -r requirements.txt
                                                                                                   
  2. Configure environment

  Create a .env file:

  DATABASE_HOSTNAME=localhost
  DATABASE_PORT=5432                                                                               
  DATABASE_NAME=rag
  DATABASE_USERNAME=postgres                                                                       
  DATABASE_PASSWORD=yourpassword

  3. Run migrations

  alembic upgrade head
                                                                                                   
  4. Start the server
                                                                                                   
  uvicorn app.main:app --reload

  API docs available at http://localhost:8000/docs

  Roadmap                                                                                          
   
  - Embedding generation (BAAI/bge-m3)                                                             
  - Vector storage (pgvector)
  - Semantic search endpoint                                                                       
  - Async task queue (Celery + Redis)
  - Async database driver (SQLAlchemy async)                                                       
                                                                                                   
  ---