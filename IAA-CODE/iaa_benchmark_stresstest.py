import time
from z3 import Bool, Implies, Not, Solver

def run_scaling_stress_test():
    print("=== IAA SYMBOLIC BOUNDARY & SCALING STRESS TEST ===\n")
    for num_rules in:
        # Create N symbolic state variables
        vars_list = [Bool(f"State_{i}") for i in range(num_rules)]
        solver = Solver()

        # Build a dense cascade of N-1 interdependent operational rules: State_i -> State_{i+1}
        for i in range(num_rules - 1):
            solver.add(Implies(vars_list[i], vars_list[i + 1]))

        # Add final safety guardrail: State_{N-1} -> NOT State_0
        solver.add(Implies(vars_list[-1], Not(vars_list[0])))

        # Inject Axiomatic Invariant trigger (I x C): State_0 == True
        solver.add(vars_list[0] == True)

        # Measure execution time across 50 runs
        times_ms = []
        for _ in range(50):
            t0 = time.perf_counter()
            result = solver.check()
            times_ms.append((time.perf_counter() - t0) * 1000.0)

        avg_ms = sum(times_ms) / len(times_ms)
        print(f"Rules: {num_rules:3d} | Result: {str(result).upper():5s} | Mean Latency: {avg_ms:.4f} ms")

if __name__ == "__main__":
    run_scaling_stress_test()