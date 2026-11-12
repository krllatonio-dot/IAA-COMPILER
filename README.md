# IAA Structural Logic Compiler (Proof-of-Concept Architecture)

A deterministic, neuro-symbolic formal verification Proof-of-Concept (PoC) based on **Immanent Adversarial Axiomatics (IAA)** for low-compute AI red-teaming and guardrail auditing.

## Overview
Traditional AI red-teaming relies on stochastic prompt fuzzing and high-compute trial-and-error. Grounded in **Karl Popper’s criterion of falsifiability**, this PoC translates a target AI system's administrative directives and safety guardrails into first-order logic and evaluates them using **Microsoft's Z3 SMT Solver** to mathematically isolate exact contradiction thresholds ($\Lambda$) prior to live probing.

## Repository Structure
* `IAA-CODE/benchmark_stresstest.py` — Standalone Z3 symbolic scaling benchmark evaluating solver latency across 5 to 250 interdependent causal rules (reproduces **Table 3**).
* `IAA-CODE/neuro_compiler.py` — Two-stage neuro-symbolic compiler pairing LLM semantic rule parsing with Z3 boundary collision detection (`UNSAT`).
* `IAA-CODE/phase2_probe.py` — Lightweight Phase 2 dynamic falsification probe testing Z3-derived collision payloads against live instruction-tuned models (reproduces **Table 4**).
* `IAA-CODE/requirements.txt` — Python dependencies (`z3-solver`, `openai`).

## Quick Start

1. **Clone the repository and enter the code directory:**
   ```bash
   git clone https://github.com
   cd IAA-COMPILER/IAA-CODE
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

3. **Run the Z3 Symbolic Scaling Stress Test (Standalone CPU — No LLM Required):**
   ```bash
   python iaa_benchmark_stresstest.py
   ```

4. **Run the Neuro-Symbolic Logic Compiler & Phase 2 Falsification Probe:**
   *(Requires a local Ollama server or an OpenAI-compatible API endpoint)*
   ```bash
   ollama pull qwen2.5:1.5b
   python iaa_neuro_compiler.py
   python phase2_probe.py
   ```

## Summary of Empirical Benchmarks
* **Phase 1 Symbolic Verification (Dell Latitude 3420, Intel Celeron 6305 CPU, 8 GB RAM):** Achieved 100.0% deterministic contradiction detection accuracy ($N = 20$ formalized policy suites) and near-linear $O(N)$ scaling up to **250 interdependent rules in 0.4475 ms** using 1 solver query.
* **Phase 2 Live Falsification Probe (CPU-Only Linux Container, `Qwen2.5-1.5B-Instruct`):** Validated single-query zero-shot guardrail collapse on commercial confidentiality collisions (`TC-05`, 20.0% zero-shot ASR) alongside a **2.99× latency spike (12.80 s vs. 4.28 s baseline)** under axiomatic conflict.

## Citation
If you use this framework or code in your research, please cite:

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Method for Constructing Inescapable Truth*. PhilArchive. https://philarchive.org

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Neuro-Symbolic Formal Verification Method*. GitHub: https://github.com
