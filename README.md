# AI Customer Support Root Cause Analyzer

## One-liner

An AI system that converts messy customer support tickets into clear root causes, actionable fixes, and product insights.

## Problem it solves

Support teams often face challenges with:

- Long, emotional, unstructured tickets.
- Repeated complaints with no clear pattern.
- Slow feedback loops to engineering & product.

This tool addresses these by answering:

- What actually broke?
- Is this a bug, UX issue, or misuse?
- What should engineering/product do next?

## What the AI does

Given a support ticket (email/chat), the AI performs the following:

- **Summarizes** the issue.
- **Extracts key facts** (product area, feature, environment).
- **Identifies root cause**.
- **Classifies the issue** (Bug / UX gap / Performance / Misconfiguration / User error).
- **Suggests fixes** for Engineering, Product, and provides a Support response.
- **Detects patterns** (if similar tickets exist using RAG).
- Outputs structured JSON.

## Minimal Architecture

```
UI (Text input / CLI)
        ↓
API (FastAPI)
        ↓
LLM (LLama with Ollama)
        ↓
RAG (ChromaDB with past tickets + fixes)
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd ai-rca
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: You might need to create `requirements.txt` first by running `pip freeze > requirements.txt` after installing dependencies)


## Running the Application

1.  **Start the FastAPI application:**
    ```bash
    source venv/bin/activate
    uvicorn main:app --reload
    ```

    The API will be available at `http://localhost:8000`.

    ```bash
    curl --location --request POST 'http://localhost:8000/analyze_ticket?ticket=%22payments%20failing%22'
    ```

2.  **Interact via the CLI:**

    In a separate terminal, activate the virtual environment and run the CLI script:
    ```bash
    source venv/bin/activate
    python cli.py
    ```
    You will be prompted to enter a support ticket. Press `Ctrl+D` (Unix/macOS) or `Ctrl+Z` then `Enter` (Windows) to finish input.

## Example Usage (CLI)

```
curl --location --request POST 'http://localhost:8000/analyze_ticket?ticket=%22payments%20failing%22'
```


```
Enter your support ticket (press Ctrl+D or Ctrl+Z and then Enter to finish input):
Subject: Payments failing again!!!

Hi team,
This is the third time this week that payments have failed for our EU customers.
The checkout page just spins and then errors out.
We lost customers because of this.
Please fix ASAP.

{  
  "summary": "EU customers are unable to complete payments due to checkout timeout.",
  "category": "Payment Failure",
  "root_cause": "Third-party payment gateway timeout in EU region",
  "issue_type": "Bug",
  "severity": "High",
  "confidence": 0.86,
  "engineering_actions": [
    "Add timeout handling and retries",
    "Implement regional fallback gateway",
    "Improve gateway monitoring"
  ],
  "product_actions": [
    "Display clearer payment failure messages",
    "Add status page for payment incidents"
  ],
  "support_reply_suggestion": "Acknowledge issue, explain temporary workaround, provide ETA.",
  "similar_incidents": [
    "INC-2024-001"
  ]
}
```

## AI Techniques

-   **Prompt engineering:** Role-based prompting and constraint enforcement.
-   **Classification & reasoning:** Identifying issue types and root causes.
-   **Structured outputs:** Enforcing JSON schema for predictable results.
-   **RAG for pattern detection:** Leveraging ChromaDB to find and utilize similar historical incidents.
-   **Confidence scoring:** Providing a measure of certainty in the analysis.
-   **Multi-audience outputs:** Tailored suggestions for Support, Engineering, and Product teams.

