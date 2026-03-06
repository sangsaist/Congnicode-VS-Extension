# Cognicode Backend Architecture

## Overview
Cognicode is a scalable backend system designed to analyze DSA code and provide intelligent feedback. It follows **Clean Architecture** principles to ensure low coupling, high cohesion, and ease of maintainability.

## Pipeline Flow
1. **API Layer (`api/analyze.py`)**: Receives the POST request, extracts the code and user metadata.
2. **Static Analysis Stage (`analyzers/ast_parser.py`)**: Parses the code into an Abstract Syntax Tree (AST) to extract features like loop depth, recursion, and function calls.
3. **Pattern Detection Stage (`analyzers/pattern_detector.py` & `complexity_analyzer.py`)**: Uses a combination of AST features and regex-based heuristics to identify DSA patterns (e.g., Two Pointer, Binary Search) and estimate complexity.
4. **History Stage (`history/history_manager.py`)**: Retrieves the user's past performance to provide context for personal growth tracking.
5. **Reasoning Layer (`llm/llm_service.py`)**: Orchestrates the gathered data into a semantic prompt, which is sent to the **xAI Grok API (grok-2-latest)** to generate structured, human-readable feedback.
6. **Response Generation**: Formats the LLM output into a strict JSON schema for the VS Code extension consumption.

## Directory Structure
- `api/`: REST API controllers and route definitions.
- `analyzers/`: Logic for static code analysis, complexity estimation, and pattern matching.
- `history/`: Data access layer for user learning history (JSON based, swappable for DB).
- `llm/`: Client for communicating with large language models.
- `prompts/`: Management of prompt templates and context construction.
- `app.py`: Entry point and application factory.

## Design Choices
- **Application Factory**: Separation of app creation from execution allows for easier testing and environment-specific configuration.
- **Dependency Isolation**: Analyzers do not know about the API; they only process strings/ASTs and return structured data.
- **Heuristic + LLM Hybrid**: We use static analysis for fast, deterministic detection of "hard" features (like nested loops) and LLM for "soft" reasoning and code improvement suggestions.
- **Future-Proof Storage**: The `HistoryManager` class provides a clean interface, allowing for a seamless transition from `user_history.json` to a SQL/NoSQL database in the future.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. (Optional) Create a `.env` file and add `OPENAI_API_KEY=your_key`.
3. Start the server: `python app.py`
4. Base URL: `http://localhost:5000`
