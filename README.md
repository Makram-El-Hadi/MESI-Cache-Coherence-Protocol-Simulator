# EECE422-Project



================================================================================
  Project 1: Snooping Cache Coherence Simulator
  EECE 422 — Parallel Computer Architecture, Spring 2026
  American University of Beirut
================================================================================

GROUP MEMBERS
-------------
  [Student Name 1] — [ID]
  [Student Name 2] — [ID]
  [Student Name 3] — [ID]


--------------------------------------------------------------------------------
REQUIREMENTS
--------------------------------------------------------------------------------

  - Python 3.7 or later (no third-party packages required)
  - All source files must be in the same directory


--------------------------------------------------------------------------------
FILE OVERVIEW
--------------------------------------------------------------------------------

  main.py           Entry point. Runs all five experiments in sequence.
  Experiments.py    run_simulation() and interleave_traces() helpers.
  Cache.py          MESI/MSI cache with processor_read, processor_write, snoop.
  Bus.py            Shared bus: BusRd, BusRdX, BusUpgr, BusWB.
  Memory.py         Flat address-space memory with write-back support.
  Stats.py          Per-core and global statistics collection and printing.
  Traces.py         Definitions of Trace A, B, and C as Python lists.


--------------------------------------------------------------------------------
HOW TO RUN
--------------------------------------------------------------------------------

  Run all experiments at once:

      python main.py

  This will print results for all five experiments to standard output.

  To run a single custom simulation from a Python shell or script:

      from Experiments import run_simulation
      import Traces

      run_simulation(
          trace_name = "MyRun",
          trace_data = Traces.trace_a,
          num_cores  = 4,       # number of processor cores (default: 4)
          num_lines  = 8,       # cache lines per cache (default: 8)
          is_mesi    = True     # True = MESI protocol, False = MSI protocol
      )


--------------------------------------------------------------------------------
REPRODUCING EACH EXPERIMENT
--------------------------------------------------------------------------------

  All experiments are executed automatically by running:

      python main.py

  Below is a description of what each experiment does:

  Experiment 1 — Baseline Protocol Behavior
    Runs Traces A, B, and C with the default configuration:
      N = 4 cores, C = 8 cache lines, MESI protocol.
    Reports all statistics (hits, misses, bus transactions, invalidations,
    silent upgrades) for each trace.

  Experiment 2 — Effect of Number of Cores
    Runs Trace B (Producer-Consumer) with N in {2, 4, 6, 8},
    keeping C = 8 and MESI enabled.
    Shows how total bus transactions scale with core count.

  Experiment 3 — Effect of Cache Size
    Runs Trace C (Migratory Sharing) with C in {4, 8, 16, 32},
    keeping N = 4 and MESI enabled.
    Shows the relationship between cache capacity and coherence traffic.

  Experiment 4 — MESI vs. MSI Silent Upgrade Analysis
    Runs Trace A twice with N=4, C=8:
      - Once with MESI (is_mesi=True)
      - Once with MSI  (is_mesi=False)
    Quantifies the bus traffic reduction from the Exclusive state.

  Experiment 5 — Simultaneous Trace Execution (A || B)
    Interleaves Trace A and Trace B in strict round-robin order using
    interleave_traces(), then runs the merged trace with N=8, C=8, MESI.
    Also runs each trace alone (Trace A with N=4, Trace B with N=8) as
    baselines for comparison.
    Demonstrates emergent coherence behavior (silent upgrades, conflict
    misses) that appears only when both workloads share the bus.


--------------------------------------------------------------------------------
PROTOCOL SWITCH
--------------------------------------------------------------------------------

  To switch between MESI and MSI, pass is_mesi=True or is_mesi=False to
  run_simulation(). The Cache class uses this flag to decide whether to use
  the Exclusive state. All other logic (invalidations, writebacks) is shared.


--------------------------------------------------------------------------------
NOTES
--------------------------------------------------------------------------------

  - The simulator processes trace events sequentially (one at a time) in the
    order they appear in the trace list. Bus transactions are atomic: all
    caches snoop and respond before the next trace event is processed.

  - The interleave_traces() function merges two traces in strict round-robin
    order. This models one possible bus arbitration outcome for simultaneous
    execution; it does not model all possible interleavings.

  - Memory size defaults to 1024 addresses, which is larger than any address
    used in the provided traces. It can be changed in Experiments.py if needed.

  - Trace events with a core_id >= num_cores are silently skipped. This allows
    traces designed for more cores (e.g., Trace B with cores 0-7) to be run
    with fewer cores without errors.

================================================================================
