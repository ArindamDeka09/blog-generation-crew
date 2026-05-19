# 🤖 Multi-Agent AI Blog Generation Crew 

Welcome to the **BlogGenerationCrew** project. This is a production-grade, multi-agent AI system engineered using the **CrewAI** framework. It leverages a hierarchical management structure to orchestrate autonomous agents that research, draft, and review long-form technical content.

Unlike standard templates, this repository has been optimized to handle complex, high-density reasoning loops entirely through free-tier **NVIDIA NIM** infrastructure, bypassing common token-ceiling and gateway connection limits.

---

## 🧠 System Architecture & Workflow

This project implements a **Hierarchical Process** (`Process.hierarchical`) to mimic a real-world corporate data operations team:

1. **Team Leader (Crew Manager):** Ingests the global assignment topic, dynamically establishes a project roadmap, structures tasks, and handles serialization loops.
2. **Expert Researcher:** Consumes a custom RAG-driven `SerperDevTool` to search the live web, parsing snippets and chunking complex datasets before passing data back.
3. **Expert Blog Writer:** Transforms raw research packets into an expansive, detailed, long-form draft.
4. **Expert Blog Reviewer:** Acts as a quality assurance gate, evaluating structure, tone, and analogies, providing structural feedback scores before finalizing production.

---

## ⚡ Features & Engineering Optimizations

* **NVIDIA NIM Integration:** Configured natively to route high-density operations through `meta/llama-3.1-70b-instruct`.
* **Self-Healing Parsing:** Integrated resilient schema error catching to gracefully recover from transient multi-agent JSON parsing anomalies (`Action Input key-value` slips).
* **Gateway Timeout Buffers:** Tailored underlying HTTP transport socket boundaries (`connect_timeout` and `read_timeout` mapped to 600s) to fully mitigate cloud `504 Gateway Timeout` loops during deep context processing.
* **Extended Token Runways:** Pushed generative runtime horizons (`max_tokens=4000`) to unlock comprehensive, 1,500+ word output generation.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python `3.10` up to `3.12` installed. This project uses `uv` for lightning-fast, isolated dependency management.

### 2. Clone and Install Dependencies
```bash
# Clone the repository
git clone [https://github.com/ArindamDeka09/blog-generation-crew.git](https://github.com/ArindamDeka09/blog-generation-crew.git)
cd blog-generation-crew

# Install litellm and project dependencies using uv
uv sync
