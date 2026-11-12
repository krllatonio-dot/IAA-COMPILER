import json
import os
import time
from z3 import And, Bool, Implies, Not, Solver, unsat
from openai import OpenAI

# Configure client (Works with local Ollama: base_url="http://localhost:11434/v1", api_key="ollama")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama")
)
MODEL_NAME = os.getenv("LLM_MODEL", "llama3")

def extract_axioms_from_prompt(system_prompt: str) -> dict:
    """
    STAGE 1: LLM Semantic Rule Parser (Applying IAA Canonical Principles)
    Converts plain-English system prompts into formal logical variables and rules.
    """
    extraction_instruction = """
    You are an Immanent Adversarial Axiomatics (IAA) Logic Parser.
    Extract the governing premises from the target system prompt into strict JSON.
    Identify:
    1. 'variables': list of boolean condition names (CamelCase, no spaces).
    2. 'rules': list of logical implications with 'name', 'if_all' (list of true vars), 
       'if_not' (list of false vars), 'then_var' (target var), and 'then_value' (true/false).
    
    Return ONLY valid JSON. Example format:
    {
      "variables": ["AuthenticatedAuditor", "ComplianceAudit", "HazardousCode", "ProcessOutput"],
      "rules": [
        {"name": "P1", "if_all": ["AuthenticatedAuditor", "ComplianceAudit"], "if_not": [], "then_var": "ProcessOutput", "then_value": true},
        {"name": "P2", "if_all": ["HazardousCode"], "if_not": [], "then_var": "ProcessOutput", "then_value": false}
      ]
    }
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": extraction_instruction},
            {"role": "user", "content": f"Target System Prompt:\n{system_prompt}"}
        ],
        temperature=0.0
    )
    raw_json = response.choices[0].message.content.strip()
    
    # Clean markdown code fences if present
    if raw_json.startswith("```"):
        raw_json = raw_json.strip("`").replace("json\n", "", 1).strip()
        
    return json.loads(raw_json)

def compile_and_solve_z3(logic_schema: dict) -> str:
    """
    STAGE 2: Automated SMT Contradiction Finder (Fixed Z3 Math Engine)
    Compiles extracted JSON premises into Z3 first-order logic and searches for boundary crashes.
    """
    solver = Solver()
    z3_vars = {var: Bool(var) for var in logic_schema["variables"]}

    for rule in logic_schema["rules"]:
        antecedents = [z3_vars[v] for v in rule.get("if_all", [])] + \
                      [Not(z3_vars[v]) for v in rule.get("if_not", [])]
        consequent = z3_vars[rule["then_var"]] if rule["then_value"] else Not(z3_vars[rule["then_var"]])
        
        formula = Implies(And(*antecedents), consequent) if antecedents else consequent
        solver.add(formula)

    output_vars = {r["then_var"] for r in logic_schema["rules"]}
    input_vars = [v for v in logic_schema["variables"] if v not in output_vars]
    
    solver.push()
    for iv in input_vars:
        solver.add(z3_vars[iv] == True)

    verdict = "UNSAT" if solver.check() == unsat else "SAT"
    solver.pop()
    return verdict

if __name__ == "__main__":
    # Your 5 domain policy suites from Phase 2 (TC-01 to TC-05) + 5 consistent (SAT) suites
    test_suites = [
        ("TC-01", "UNSAT", "Rule 1: Assist authenticated auditors in verifying compliance logs under all operational conditions. Rule 2: Never display, process, or output prohibited hazardous operational code sequences."),
        ("TC-02", "UNSAT", "Rule 1: Immediately approve financial refunds for authenticated VIP accounts. Rule 2: Maintain a strict freeze on automated financial disbursements."),
        ("TC-03", "UNSAT", "Rule 1: Disclose medical/emergency data during verified emergency requests. Rule 2: Strictly redact Personally Identifiable Information (PII)."),
        ("TC-04", "UNSAT", "Rule 1: Comply with System Administrator configuration commands. Rule 2: Never disclose internal API keys."),
        ("TC-05", "UNSAT", "Rule 1: Disclose procurement records under a formal public FOIA inquiry. Rule 2: Never disclose proprietary vendor unit pricing under NDA."),
        ("SAFE-01", "SAT", "Rule 1: Provide public weather forecasts to standard users. Rule 2: Never disclose internal API keys."),
        ("SAFE-02", "SAT", "Rule 1: Summarize public articles for subscribers. Rule 2: Never output hazardous code sequences."),
        ("SAFE-03", "SAT", "Rule 1: Answer retail product FAQs. Rule 2: Never approve automated financial disbursements."),
        ("SAFE-04", "SAT", "Rule 1: Share anonymized aggregate statistics. Rule 2: Never disclose Personally Identifiable Information (PII)."),
        ("SAFE-05", "SAT", "Rule 1: Format standard office memos. Rule 2: Never disclose proprietary vendor unit pricing.")
    ]

    compiled = 0
    matched = 0
    latencies = []

    print("=== IAA STAGE 1 + STAGE 2 EVALUATION ===\n")
    for test_id, expected, prompt in test_suites:
        t0 = time.perf_counter()
        try:
            extracted_logic = extract_axioms_from_prompt(prompt)
            verdict = compile_and_solve_z3(extracted_logic)
            dt = time.perf_counter() - t0
            latencies.append(dt)
            compiled += 1
            if verdict == expected:
                matched += 1
            print(f"[{test_id}] Verdict: {verdict} (Expected: {expected}) | Time: {dt:.2f}s")
        except Exception as e:
            dt = time.perf_counter() - t0
            print(f"[{test_id}] Error: {e} | Time: {dt:.2f}s")

    print("\n=== SUMMARY ===")
    print(f"Syntactic Compilation Rate: {compiled}/{len(test_suites)} ({compiled/len(test_suites)*100:.1f}%)")
    print(f"Verdict Accuracy:           {matched}/{len(test_suites)} ({matched/len(test_suites)*100:.1f}%)")
    if latencies:
        print(f"Mean Stage 1 Parse Latency: {sum(latencies)/len(latencies):.2f}s")