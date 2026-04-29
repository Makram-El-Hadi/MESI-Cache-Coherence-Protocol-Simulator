import Traces
from Experiments import run_simulation, interleave_traces

def main():
    # --- Experiment 1: Baseline Protocol Behavior ---
    # Goal: Default config (N=4, C=8, M=64) for all traces.
    print("EXECUTING EXPERIMENT 1...")
    for label, trace in [("A", Traces.trace_a), ("B", Traces.trace_b), ("C", Traces.trace_c)]:
        run_simulation(f"Exp1_Trace_{label}", trace, num_cores=4, num_lines=8, is_mesi=True)

    # --- Experiment 2: Effect of Number of Cores ---
    # Goal: Using Trace B, vary N in {2, 4, 6, 8}. Keep C=8.
    print("\nEXECUTING EXPERIMENT 2...")
    for n in [2, 4, 6, 8]:
        run_simulation(f"Exp2_TraceB_N{n}", Traces.trace_b, num_cores=n, num_lines=8, is_mesi=True)

    # --- Experiment 3: Effect of Cache Size ---
    # Goal: Using Trace C, vary C in {4, 8, 16, 32}. Keep N=4.
    print("\nEXECUTING EXPERIMENT 3...")
    for c in [4, 8, 16, 32]:
        run_simulation(f"Exp3_TraceC_C{c}", Traces.trace_c, num_cores=4, num_lines=c, is_mesi=True)

    # --- Experiment 4: Silent Upgrade Analysis (Groups of 3) ---
    # Goal: Using Trace A, compare MESI vs MSI to quantify traffic reduction.
    print("\nEXECUTING EXPERIMENT 4...")
    run_simulation("Exp4_TraceA_MESI", Traces.trace_a, num_cores=4, num_lines=8, is_mesi=True)
    run_simulation("Exp4_TraceA_MSI", Traces.trace_a, num_cores=4, num_lines=8, is_mesi=False)

    # --- Professor's Special Request: Simultaneous Traces ---
    # This isn't in the handout but handles the "running at the same time" question.
    print("\nEXECUTING SIMULTANEOUS TRACE TEST...")
    sim_trace = interleave_traces(Traces.trace_a, Traces.trace_b)
    run_simulation("Simultaneous_A_and_B", sim_trace, num_cores=4, num_lines=8, is_mesi=True)

if __name__ == "__main__":
    main()