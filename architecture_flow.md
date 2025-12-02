graph TB
    Start([Document Upload]) --> Router[Router Agent<br/>Complexity Assessment]
    Router --> SimplePath[Simple Processing Path]
    Router --> ComplexPath[Complex Processing Path]

    SimplePath --> Extractor[Extractor Agent<br/>Data Extraction]
    Extractor --> Summarizer[Summarizer Agent<br/>Content Summary]
    Summarizer --> Output[Generate Output]

    ComplexPath --> Orchestrator[Orchestrator Agent<br/>Workflow Planning]
    Orchestrator --> Extractor2[Extractor Agent<br/>Deep Analysis]
    Extractor2 --> Analyzer[Analyzer Agent<br/>Content Analysis]
    Analyzer --> Validator[Validator Agent<br/>Quality Check]
    Validator --> Summarizer2[Summarizer Agent<br/>Insight Generation]
    Summarizer2 --> Output2[Generate Output]

    Output --> Memory[Save to Federated Memory]
    Output2 --> Memory2[Save to Federated Memory]

    Memory --> End([Complete])
    Memory2 --> End2([Complete])

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style End2 fill:#FFB6C1
    style Router fill:#FFE66D
    style Orchestrator fill:#4ECDC4

   graph LR
    subgraph "External API Layer"
        API[OpenAI GPT-4 API]
    end

    subgraph "Control Layer"
        Router[Router Agent<br/>Document Classification]
        Orchestrator[Orchestrator Agent<br/>Workflow Management]
        Memory[Federated Memory<br/>Knowledge Base]
    end

    subgraph "Processing Agent Layer"
        Extractor[Extractor Agent<br/>Data Extraction]
        Analyzer[Analyzer Agent<br/>Content Analysis]
        Summarizer[Summarizer Agent<br/>Insight Generation]
        Validator[Validator Agent<br/>Quality Assurance]
    end

    subgraph "Storage Layer"
        Redis[Redis Cache]
        Postgres[PostgreSQL Database]
    end

    Router --> Orchestrator
    Router --> Memory
    Orchestrator --> Extractor
    Orchestrator --> Analyzer
    Orchestrator --> Summarizer
    Orchestrator --> Validator

    Extractor --> API
    Analyzer --> API
    Summarizer --> API
    Validator --> API

    API -.Return Analysis.-> Extractor
    API -.Return Analysis.-> Analyzer
    API -.Return Analysis.-> Summarizer
    API -.Return Analysis.-> Validator

    Memory --> Redis
    Memory --> Postgres

    style Router fill:#FFE66D
    style API fill:#FF6B6B
    style Orchestrator fill:#4ECDC4

    sequenceDiagram
    participant User as User
    participant API as FastAPI Server
    participant Router as Router Agent
    participant Extractor as Extractor Agent
    participant Summarizer as Summarizer Agent
    participant Memory as Federated Memory
    participant GPT as OpenAI API

    User->>API: Upload Document
    API->>Router: Send Document Data
    
    rect rgb(240, 240, 240)
        Note over Router: Complexity Assessment
        Router->>Router: Analyze document type
        Router->>Router: Calculate complexity score
        Router->>Router: Choose processing path
    end

    Router->>Extractor: Route to Simple Path
    Extractor->>GPT: Request data extraction
    GPT-->>Extractor: Return extracted data
    Extractor->>Summarizer: Send extracted data

    Summarizer->>GPT: Request summary generation
    GPT-->>Summarizer: Return generated summary
    Summarizer->>Memory: Store processing results
    Memory-->>API: Confirm storage

    API-->>User: Return final output
