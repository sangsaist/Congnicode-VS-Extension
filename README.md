# Cognicode

Cognicode is a VS Code extension that provides real-time analysis of DSA (Data Structures and Algorithms) code using LLMs. It consists of a VS Code extension frontend and a Flask-based backend.

## Project Structure

- `Extension/`: The VS Code extension source code (TypeScript/Node.js).
- `backend/`: The analysis engine backend (Python/Flask/LLM).

## Getting Started

### Backend Setup

1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your GROQ API key.
5. Run the server:
   ```bash
   python app.py
   ```

### Extension Setup

1. Navigate to the `Extension` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Open the folder in VS Code and press `F5` to start debugging.

## Features

- Real-time DSA code analysis.
- Complexity estimation.
- Code optimization suggestions.
- History of analyzed code.

## License

[Add License Info Here]
