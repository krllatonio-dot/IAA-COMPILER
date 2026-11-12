# IAA Structural Logic Compiler (Proof-of-Concept Architecture)

A deterministic, neuro-symbolic formal verification Proof-of-Concept (PoC) based on **Immanent Adversarial Axiomatics (IAA)** for low-compute AI red-teaming and guardrail auditing.

## Overview
Traditional AI red-teaming relies on stochastic prompt fuzzing and high-compute trial-and-error. Grounded in **Karl Popper’s criterion of falsifiability**, this PoC demonstrates how a target AI system's administrative directives and safety guardrails can be translated into first-order logic and evaluated using **Microsoft's Z3 SMT Solver** to mathematically pinpoint exact contradiction thresholds ($\Lambda$) prior to live probing.

## Repository Structure
* `IAA-CODE/stress_test.py` — Symbolic scaling benchmark evaluating Z3 solver latency across 5 to 250 interdependent causal rules (reproduces **Table 3**).
* `IAA-CODE/iaa_neuro_compiler.py` — Two-stage neuro-symbolic compiler pairing LLM semantic rule parsing with Z3 boundary collision detection (`UNSAT`).
* `IAA-CODE/phase2_probe.py` — Lightweight Phase 2 dynamic falsification probe testing Z3-derived collision payloads against live instruction-tuned models.
* `IAA-CODE/requirements.txt` — Python dependencies (`z3-solver`, `openai`).

## Quick Start

1. **Clone the repository and enter the code directory:**
   ```bash
   git clone https://github.com
   cd IAA-COMPILER/IAA-CODE
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Z3 Symbolic Scaling Stress Test (Standalone CPU — No LLM Required):**
   ```bash
   python stress_test.py
   ```

4. **Run the Neuro-Symbolic Logic Compiler (Requires Local Ollama or OpenAI-Compatible API):**
   ```bash
   # Example using local Ollama (qwen2.5:1.5b or llama3)
   ollama pull qwen2.5:1.5b
   python iaa_neuro_compiler.py
   ```

## Baseline Hardware Environment
All reference benchmarks in the accompanying manuscript were executed on entry-level consumer hardware to validate the framework's low-compute footprint:
* **System:** Dell Latitude 3420
* **CPU:** Intel Celeron 6305 (Dual-Core, 1.8 GHz)
* **RAM:** 8 GB DDR4-3200
* **GPU:** Integrated Intel UHD Graphics (No discrete GPU required for Phase 1 symbolic verification)

## Citation
If you use this framework or code in your research, please cite:

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Method for Constructing Inescapable Truth*.

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Neuro-Symbolic Formal Verification Proof-of-Concept Architecture for Low-Compute Automated AI Red-Teaming*.
