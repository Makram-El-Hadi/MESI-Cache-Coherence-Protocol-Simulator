import Traces
from Experiments import run_simulation

def main():
    # Experiment 1
    print("EXECUTING EXPERIMENT 1:") #what do you want to print here????????
    for label, trace in [("A", Traces.trace_a), ("B", Traces.trace_b), ("C", Traces.trace_c)]:
        run_simulation(f"Exp1_Trace_{label}", trace, num_cores=4, num_lines=8, is_mesi=True)
    # Experiment 2
    print("\nEXECUTING EXPERIMENT 2:")
    for n in [2, 4, 6, 8]:
        run_simulation(f"Exp2_Trace_B", Traces.trace_b, num_cores=n, num_lines=8, is_mesi=True)
    # Experiment 3
    print("\nEXECUTING EXPERIMENT 3:")
    for c in [4, 8, 16, 32]:
        run_simulation(f"Exp3_Trace_C", Traces.trace_c, num_cores=4, num_lines=c, is_mesi=True)
    # Experiment 4
    print("\nEXECUTING EXPERIMENT 4:")
    run_simulation("Exp4_Trace_A", Traces.trace_a, num_cores=4, num_lines=8, is_mesi=True)
    run_simulation("Exp4_Trace_A", Traces.trace_a, num_cores=4, num_lines=8, is_mesi=False)

if __name__ == "__main__":
    main()
