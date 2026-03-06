# 🧠 Cognicode

<div align="center">

**A VS Code companion for mastering DSA — detects patterns, estimates complexity, and explains better approaches.**

<br/>

[![VS Code Extension](https://img.shields.io/badge/VS%20Code-Extension-007ACC?logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-Extension-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-Backend-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LLM](https://img.shields.io/badge/LLM-Groq%20(OpenAI%20Compatible)-6A5ACD)](https://groq.com/)

**Jump to:** [✨ Features](#-features) • [🧩 How-It-Works](#-how-it-works) • [🚀 Quick Start](#-quick-start) • [▶️ Usage](#️-usage) • [🗺️ Roadmap](#️-future-improvements)

</div>

---

## 🎯 What is Cognicode?

When practicing **DSA (Data Structures & Algorithms)**, getting an accepted solution is only half the battle:

- “Is this the *best* algorithm for this problem?”
- “What’s my **time complexity**?”
- “Why does my solution TLE even though it’s correct?”

**Cognicode** helps answer those questions *inside VS Code*.

It’s a **VS Code extension** backed by a **Flask analysis service** that:
- extracts signals from your code (loops/recursion/memoization),
- detects likely DSA patterns,
- estimates complexity,
- and produces **structured feedback** (with explanations) using an LLM.

---

## ✨ Features

### 🧩 In VS Code (Extension)
- ✅ **Command:** `Cognicode: Analyze Code` (`cognicode.analyze`)
- ✅ **Right where you code:** shows an **Activity Bar** panel (**Cognicode**) with an analysis webview
- ✅ **One click analyze:** also available from the editor title menu (when editor is focused)
- ✅ **Sends active file content + language id** to the backend for analysis

### 🔬 In the Backend (Analysis Engine)
- ✅ **Static feature extraction (AST-based)**  
  Uses Python’s AST to extract code signals like:
  - max loop depth (nested loops)
  - recursion detection
  - memoization hints
  - log-step loop patterns (e.g., halving)
- ✅ **Complexity estimation (heuristics)**  
  Estimates common Big‑O like `O(n)`, `O(n^2)`, `O(log n)`, `O(n log n)` etc.
- ✅ **DSA pattern detection (heuristics / regex)**  
  Detects multiple common patterns (examples in repo: Sliding Window, Two Pointer, Binary Search, DP, BFS/DFS, Heap, Union-Find, Bit Manipulation, and more).
- ✅ **LLM structured feedback (Groq / OpenAI-compatible)**  
  Generates a prompt and returns a **JSON** analysis object with fields like:
  - `algorithm_detected`
  - `best_time_complexity`, `worst_time_complexity`, `space_complexity`
  - `explanation`
  - `suggested_algorithm`
  - `improved_complexity`
  - `improved_code`
  - plus scoring/impact fields (e.g., `speedup_score`)
- ✅ **History-aware analysis**  
  Stores previous detected patterns/complexities per `user_id` (defaults to `"anonymous"`).

> Important: The extension currently calls `http://localhost:5000/analyze` directly.  
> A VS Code setting `cognicode.apiUrl` exists in the manifest, but it is **not yet used** by the extension code.

---

## 🧩 How It Works

**Flow (conceptual):**

**Write code → Run analyze → Backend inspects → Pattern + complexity detected → LLM explains → Results shown in sidebar**

```text
┌──────────────────────────────┐
│ VS Code Extension            │
│ - grabs active editor code   │
│ - runs command analyze       │
│ - renders sidebar webview    │
└───────────────┬──────────────┘
                │ POST /analyze
                ▼
┌──────────────────────────────┐
│ Flask Backend                │
│ 1) AST feature extraction    │
│ 2) Complexity estimate       │
│ 3) Pattern detection         │
│ 4) History lookup            │
│ 5) LLM prompt + JSON output  │
└──────────────────────────────┘
```

---

## 👩‍💻 Developer Experience

Cognicode is designed for a tight DSA practice loop:

- **Stay in VS Code**: no switching tabs to search “time complexity of this pattern”
- **Learn the “why”**: explanations are returned as part of the analysis output
- **Iterate quickly**: refactor your approach and re-run analysis

Think of it as a lightweight **DSA mentor panel** that lives next to your code.

---

## 🧪 Example Analysis (Brute Force → Better Approach)

### Brute-force approach (nested loops)

```python
def has_pair(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True
    return False
```

### What Cognicode can surface
- **Nested loops detected** → likely **`O(n^2)`**
- Suggest a **hashing-based** approach (often **`O(n)`**) and explain the tradeoff

> The exact “improved_code” and explanation are LLM-generated, but the backend enforces a consistent JSON response schema.

---

## 🚀 Quick Start

## 1) Start the Backend (Flask)

```bash
cd backend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
# Edit .env:
# GROQ_API_KEY=your_key_here
```

Run:

```bash
python app.py
```

Backend endpoints:
- `GET /health` → `{ "status": "healthy" }`
- `POST /analyze` → JSON analysis response

---

## 2) Run the Extension in VS Code

```bash
cd Extension
npm install
```

Open **`Extension/`** in VS Code and press:

- `F5` — launches **Extension Development Host**

---

## ▶️ Usage

1. Ensure backend is running: `http://localhost:5000`
2. In the Extension Development Host:
   - open any code file you want to evaluate
   - run **Cognicode: Analyze Code**
     - Command Palette: `Ctrl/Cmd + Shift + P` → “Cognicode: Analyze Code”
     - or click the editor title menu action
3. Open the **Cognicode** Activity Bar panel to view the results.

---

## ⚙️ Configuration

The extension contributes the following setting:

- `cognicode.apiUrl` (default: `http://localhost:5000/analyze`)

> Current status: The manifest defines this setting, but the extension code currently posts to a hard-coded URL.

---

## 🗺️ Future Improvements

Ideas aligned with the current design:

- 🔧 **Wire `cognicode.apiUrl` into the extension fetch call**
- 🧠 **Recognize more patterns** and boost confidence scoring
- ⚡ **Real-time feedback** (on-save / as-you-type with throttling)
- 📏 **Deeper complexity analysis**
  - better space complexity inference
  - multi-phase / multi-function analysis
- 📈 **Personalized learning insights** using stored history

---

## 📁 Project Structure (From This Repo)

```text
.
├── README.md
├── Extension/
│   ├── package.json
│   ├── esbuild.js
│   ├── src/
│   │   ├── extension.ts
│   │   ├── CognicodeViewProvider.ts
│   │   └── test/extension.test.ts
│   └── vsc-extension-quickstart.md
└── backend/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── verify_key.py
    ├── api/analyze.py
    ├── analyzers/
    │   ├── ast_parser.py
    │   ├── complexity_analyzer.py
    │   └── pattern_detector.py
    └── llm/llm_service.py
```

---
