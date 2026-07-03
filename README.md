# Intelligent Handwritten Notes Understanding & Learning Platform

An advanced, full-stack AI-driven educational ecosystem that transforms static handwritten pages into a structured, interactive, and personalized digital knowledge system. This project goes beyond generic OCR digitization by implementing **Context-Locked RAG (Retrieval-Augmented Generation)**, **Automated Knowledge Graph Structuring**, and a **Real-Time Learning Analytics Tracking Engine** to identify user concept gaps.

---

## 🌟 Core Architectural Modules

### 1. Advanced Handwriting Recognition & Processing Pipeline
* Integrates multi-format document scanning architectures (`EasyOCR` for high-density image layers and `PyMuPDF` for PDF document rasterization).
* Filters raw, noisy character outputs through an alignment parsing pipeline to normalize spelling errors, structural anomalies, and text irregularities without destroying domain-specific metrics.

### 2. Concept Map Understanding Engine
* Analyzes the normalized text blocks to map out algorithmic definitions, system dependencies, and theoretical taxonomies.
* Dynamically outputs a visual, hierarchical, nested **Concept Tree Structure** directly on the web interface, mapping core concepts to low-tier subtopics seamlessly.

### 3. Smart Multi-Tier Revision Sheet Generator
* Generates optimized multi-tier contextual outputs customized for rapid academic retention:
    * **Exam-Day Ultra Short Notes:** High-impact, single-sentence conceptual summaries.
    * **7-Day Core Concepts Summary:** Concise 3-bullet core framework breakdowns.
    * **Extended Summaries:** Deep-dive structural references.

### 4. Interactive Gamified MCQ Testing Engine
* Generates custom text-bound Multiple Choice Questions dynamically mapped from the user's specific document context.
* Features an interactive client-side execution layout using asynchronous state freezing logic.

### 5. Weak-Area Learning Analytics Tracker
* Tracks user micro-interactions (wrong selections) in real-time.
* Intercepts incorrect quiz inputs and pushes asynchronous payloads via JSON fetch metrics to persist diagnostic logs, alerting students of conceptual gaps.

### 6. Context-Isolated Document Intelligence (RAG Sidebar)
* Implements a modular, slide-out chat interface driven by **Retrieval-Augmented Generation (RAG-Lite)** via the Google GenAI SDK.
* Enforces strict prompt engineering constraints to restrict conversational dependencies exclusively to the cleaned text limits, mitigating factual hallucinations.

---

## 🛠️ System Architecture & Technology Stack

* **Backend Engineering Framework:** Python, Flask, Flask-Session Management
* **Database Management System:** SQLite3 (Relational Entity Mapping, Thread-Safe Connections)
* **Artificial Intelligence SDK:** Google GenAI SDK (`models/gemini-2.5-flash` Context Routing)
* **Document Parsers & Utilities:** EasyOCR, PyMuPDF (fitz), ReportLab PDF Generator Engine
* **Frontend Interface Layout:** Modern HTML5, Responsive Core CSS3, FontAwesome Vector Icons, Native JavaScript (Asynchronous DOM State Tracking Engine)

---


## 📁 File Structure Configuration

```text
├── app.py                  # Core Application Routing Controller & DB Orchestrator
├── ai_engine.py            # Strict Prompt Architecture & GenAI Integration Module
├── ocr_engine.py           # Document Rasterization & Text Extraction Engine
├── database.py             # Database Initialization & Scheme Definitions Script
├── smart_notes.db          # Relational Storage Engine (User Sessions, Analytical Logs)
├── .env                    # Environment Safeguards & Restricted Configuration Matrix
├── .gitignore              # Access Token Control Filters & Safety Guardrails
├── templates/
│   ├── login.html          # Secure Access Gateway
│   ├── register.html       # Identity Registration Management
│   ├── index.html          # Document Processing Management Launchpad
│   └── dashboard.html      # Multi-Column Intelligence & Analytics Control Workspace
└── static/
    └── uploads/            # Sandboxed Document Repository Path
