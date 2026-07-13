# HackethonProject
# AI-Powered Sales Intelligence Agent for Automotive Analytics

An advanced, multi-agent artificial intelligence system built on the **CrewAI** orchestration framework and powered by **Gemini 1.5 Pro**. This autonomous agent network automates complex B2B market research, evaluates corporate vulnerabilities across major Indian automotive firms, and maps specific operational challenges to data-driven consulting frameworks.

## 1. System Architecture & Decision Flow

The system coordinates specialized AI personas to transition raw industry footprints into highly structured corporate dossiers and consulting sales justifications.

```mermaid
graph TD
    A[Inception / Cron Trigger] --> B[CrewAI Orchestrator]
    B --> C[Automotive Market Intelligence Lead]
    C -->|Web Scraping & Search Tools| D[Public Data Ecosystem: NSE/BSE, Moneycontrol, SIAM]
    D -->|Raw Corporate Footprint Data| C
    C -->|Synthesized Operational Bottlenecks| E[B2B Consulting Solutions Architect]
    E -->|RAG Ingestion| F[XYZ Analytics Product Handbook]
    F -->|Framework Mapping & ROI Formulas| E
    E -->|Structured Multi-Agent Consensus| G[Output Engine]
    G --> H[Final Deliverables: Target Matrix, Dossiers & Timelines]
