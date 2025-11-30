# 🚀 ExplainIt
### Transform Code Changes into Human Insights

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)

**ExplainIt** is a powerful developer tool that instantly analyzes code changes, diffs, or raw files to generate human-friendly explanations, structured commit messages, and comprehensive unit test plans.

---

## ✨ Features

### 🔍 Intelligent Analysis
- **Multi-Input Support**: Drag & drop files, paste raw code, or input unified diffs.
- **Deep Context**: Automatically detects change scope, affected components, and file statistics.

### 📖 Human-Readable Explanations
- Converts complex technical changes into clear, natural language summaries.
- Highlights risks, behavior changes, and potential bugs.

### 💬 Smart Commit Generation
- Generates commit messages in multiple styles:
  - **Short**: Concise summary for quick logs.
  - **Medium**: Standard Git commit format.
  - **Full**: Detailed description with body and footer.

### 🧪 Automated Test Planning
- Brainstorms unit test scenarios based on logic changes.
- Suggests positive cases, negative tests, and edge conditions.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Magudeshhmw/ExplainIt.git
   cd ExplainIt
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have `streamlit`, `boto3`, and `requests` installed)*

3. **Run the Application**
   ```bash
   streamlit run explainit_app.py
   ```

---

## 🚀 Usage

1. **Launch the App**: Open your browser to the URL shown in the terminal (usually `http://localhost:8501`).
2. **Input Code**:
   - Paste your code snippet or `git diff` output into the text area.
   - Or, upload modified files directly.
3. **Generate**: Click **✨ Generate Analysis**.
4. **Review Results**:
   - Read the **Change Summary** and **Detailed Explanation**.
   - Copy the suggested **Commit Messages**.
   - Implement the **Suggested Test Cases**.

---

## 🏗️ Architecture

- **Frontend**: Built with [Streamlit](https://streamlit.io/) for a responsive, dark-themed UI.
- **Backend**: Python-based logic handling input parsing and API orchestration.
- **AI Engine**: Powered by **Claude 3.7 Sonnet** (via AWS Bedrock) with automatic fallback to **Google Gemini 2.0 Flash** for robust availability.

---

## 📂 Project Structure

```
ExplainIt/
├── explainit_app.py    # Main Streamlit application entry point
├── explainit_lib.py    # Core logic and AI agent implementations
├── sample_diff.txt     # Sample data for testing
└── README.md           # Project documentation
```

---

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <sub>Built with passion for better code quality.</sub>
</div>
