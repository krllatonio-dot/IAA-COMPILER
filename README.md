# IAA Structural Logic Compiler (Phase 1 Prototype)

A deterministic, neuro-symbolic formal verification prototype based on **Immanent Adversarial Axiomatics (IAA)** for low-compute AI red-teaming and guardrail auditing.

## Overview
Traditional AI red-teaming relies on stochastic prompt fuzzing and high-compute trial-and-error. This prototype demonstrates how a target AI system's administrative directives and safety guardrails can be translated into first-order logic and evaluated using **Microsoft's Z3 SMT Solver** to mathematically pinpoint exact contradiction thresholds prior to live probing.

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krllatonio-dot/IAA-COMPILER
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Phase 1 Compiler:**
   ```bash
   python iaa_neuro_compiler.py
   ```

## Citation
If you use this framework or code in your research, please cite:

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Method for Constructing Inescapable Truth*.

* Latonio, K. A. (2026). *Immanent Adversarial Axiomatics: A Neuro-Symbolic Formal Verification Architecture for Low-Compute Automated AI Red-Teaming*.