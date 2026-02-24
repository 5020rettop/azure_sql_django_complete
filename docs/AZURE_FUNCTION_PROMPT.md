# Prompt for Azure Function Creation

Copy and paste the following prompt into another coding agent (e.g., Cursor, GitHub Copilot, ChatGPT) to generate a complete, deployable Azure Function project.

---

**Role**: You are an expert Python Backend Developer specializing in Serverless Architecture on Microsoft Azure.

**Objective**: Create a complete, production-ready **Azure Functions** project (Python v2 Programming Model) that serves as a **Content Filtering Microservice**.

**Requirements**:

1.  **Project Structure**:
    *   **Project Name**: `azure-content-filter`
    *   Use the standard Azure Functions Python structure.
    *   Include `function_app.py` (Main logic).
    *   Include `host.json` (Configuration).
    *   Include `requirements.txt` (Dependencies).
    *   Include `local.settings.json` (Local environment variables).

2.  **Functionality (`function_app.py`)**:
    *   Create an **HTTP Trigger** function named `filter_comment`.
    *   **Auth Level**: `ANONYMOUS` (for easy testing) or `FUNCTION` (for security).
    *   **Input**: The function must accept a `POST` request with a JSON body:
        ```json
        {
          "comment": "This is a really bad example."
        }
        ```
    *   **Logic**:
        *   Define a list of "bad words" (e.g., `["bad", "terrible", "worst"]`) inside the code or load from an environment variable.
        *   Check if the input `comment` contains any of these words (case-insensitive).
        *   If a bad word is found, replace it with `****`.
    *   **Output**: Return a JSON response:
        ```json
        {
            "original": "This is a really bad example.",
            "filtered": "This is a really **** example.",
            "is_safe": false
        }
        ```

3.  **Deployment Support**:
    *   Ensure the `requirements.txt` includes `azure-functions`.
    *   Provide a brief `README.md` explaining how to run it locally using `func start` and how to deploy to Azure using the Azure CLI (`az functionapp up`).

4.  **Quality**:
    *   Includes error handling (e.g., invalid JSON input).
    *   Uses Python type hinting.
    *   Follows PEP 8 style guidelines.

5.  **Integration Helper**:
    *   Include a file named `django_verification_snippet.py`.
    *   This file should contain a Python function `check_comment_with_azure(comment: str, function_url: str) -> dict` that uses the `requests` library to call your Azure Function.
    *   This will help the user verify the connection easily.

**Output Format**:
Please provide the full file contents for:
1.  `function_app.py`
2.  `requirements.txt`
3.  `host.json`
4.  `README.md`
5.  `django_verification_snippet.py`

---
