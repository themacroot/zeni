📌 Key Design Notes

Component	        Notes
backend/app/	    Use FastAPI routers, keep logic clean and modular
llm_server/	        Keep your LLaMA model files and serving logic separate for GPU optimization
knowledge_base/	    Plug in FAISS, ChromaDB, or other RAG tools (with embeddings from SentenceTransformers or HuggingFace)
frontend/	        Use Vite or CRA, talk to backend using Axios or Fetch
environments/	    Helps you export + recreate everything on your airgapped IBM server
scripts/	        You’ll need startup + deployment scripts, especially offline


zeni /
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── api/                 # All API routes
│   │   ├── core/                # Config, constants, utils
│   │   ├── services/            # Logic to talk to LLaMA, KB, etc.
│   │   ├── models/              # Pydantic models / schemas
│   │   ├── tasks/               # Background / async tasks
│   │   └── main.py              # Entry point for FastAPI app
│   └── tests/                   # Unit/integration tests
│
├── llm_server/                  # Local LLaMA 370B integration
│   ├── launcher/                # Script to load/serve LLaMA (e.g. llama-cpp-python or HuggingFace)
│   ├── quantized_models/        # LLaMA model files
│   └── config/                  # Model config, tokenizer, etc.
│
├── knowledge_base/             # RAG components
│   ├── data/                    # Uploaded & indexed documents
│   ├── indexing/                # Code to parse and embed documents
│   └── retriever/               # Vector store and search logic
│
├── frontend/                   # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/            # API calls to backend
│   │   └── App.jsx
│   └── package.json
│
├── environments/              # Dependency management
│   ├── environment.yml         # Conda + pip packages for backend
│   └── frontend.env            # Node version, npm/yarn setup
│
├── scripts/                   # One-off scripts or utilities
│   ├── start_server.sh         # Start backend + LLM + KB
│   ├── sync_to_airgapped.py    # Create export bundles
│   └── validate_env.py
│
└── README.md

Sample curl 


curl --location 'http://localhost:8001/    generate' \--header 'Content-Type: application/json' \--data '{  "context": [    {"role": "user", "content": "Rewrite         professionally glad to meet you         today mark, hope to connect in         future to discuss further on the         project "}  ]}'


Future work 

        +------------------------+
        |   Frontend UI (Chat)  |
        +----------+------------+
                   |
                   ↓
        +------------------------+
        |   App Backend Router   |
        +----------+-------------+
         |                        |
         ↓                        ↓
+-------------------+    +---------------------+
| Sync: HTTP to LLM |    | Async: Push to Queue|
+-------------------+    +---------------------+
                                 ↓
                      +------------------------+
                      |  Worker Calls LLM API  |
                      +------------------------+
