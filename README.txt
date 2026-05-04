# EECE422 Snooping Cache Coherence Simulator

## Project Members

1. Bassam Yaacoub
2. Hussein Kharroubi  
3. Makram El Hadi


Project Description
-------------------

This project implements a snooping cache coherence simulator in Python for EECE 422 Parallel Computer Architecture. 

The simulator models:
- Multiple processor cores.
- A private direct-mapped cache for each core.
- A shared bus used for snooping coherence transactions.
- A main memory model.
- Workload traces for testing coherence behavior.
- Statistics collection for hits, misses, invalidations, bus transactions, and silent upgrades.


Files Included
--------------

1. "main.py"
   - Runs all required experiments.

2. "Experiments.py"
   - Contains the simulation runner.
   - Creates the caches, bus, memory, and stats objects.
   - Executes each trace operation in order.

3. "Cache.py"
   - Implements the private cache for each core.
   - Handles processor reads and writes.
   - Implements MESI state transitions.
   - Handles snooping responses to bus transactions.

4. "Bus.py"
   - Implements the shared bus.
   - Broadcasts BusRd, BusRdX, BusUpgr, and BusWB operations.
   - Notifies all other caches during snooping.

5. "Memory.py"
   - Implements the memory model.
   - Checks address validity.
   - Accepts writebacks from caches.

6. "Stats.py"
   - Tracks all required statistics.
   - Records read hits, read misses, write hits, write misses.
   - Records bus transactions.
   - Records invalidations and silent upgrades.
   - Prints the final results for each experiment.

7. "Traces.py"
   - Contains the fixed workload traces:
     - Trace A: Read-dominated private access.
     - Trace B: Producer-consumer sharing.
     - Trace C: Migratory sharing.


Running the Simulator
---------------------

1. Copy all Python files into the same working directory.

2. Make sure the following files are present:
   - "main.py"
   - "Experiments.py"
   - "Cache.py"
   - "Bus.py"
   - "Memory.py"
   - "Stats.py"
   - "Traces.py"

3. Run:

   "python main.py"

4. The program will execute:
   - Experiment 1: Baseline protocol behavior.
   - Experiment 2: Effect of number of cores.
   - Experiment 3: Effect of cache size.
   - Experiment 4: Silent upgrade analysis.


Experiments
-----------

### 1. Experiment 1: Baseline Protocol Behavior

- Runs Trace A, Trace B, and Trace C.
- Uses the default configuration:
  - "N = 4" cores.
  - "C = 8" cache lines.
  - "M = 64" memory size
  - MESI protocol enabled.
- Reports:
  - Read hits and misses.
  - Write hits and misses.
  - Bus transactions.
  - Invalidations.
  - Silent upgrades.

### 2. Experiment 2: Effect of Number of Cores

- Runs Trace B while varying the number of cores.
- Core counts used:
  - "N = 2"
  - "N = 4"
  - "N = 6"
  - "N = 8"
- Cache size remains fixed at "C = 8".
- Memory size remains "M = 64".
- Reports how bus traffic changes as more cores are added.

### 3. Experiment 3: Effect of Cache Size

- Runs Trace C while varying cache size.
- Cache sizes used:
  - "C = 4"
  - "C = 8"
  - "C = 16"
  - "C = 32"
- Number of cores remains fixed at "N = 4".
- Memory size remains "M = 64".
- Reports the effect of cache size on miss rate and bus traffic.

### 4. Experiment 4: Silent Upgrade Analysis

- Runs Trace A twice:
  - once using MESI behavior.
  - once using MSI-equivalent behavior.
- Compares the number of bus transactions.
- Shows the effect of MESI silent upgrades.


Output
------

For each simulation, the program prints:

- Per-core statistics:
  - Read hits.
  - Read misses.
  - Write hits.
  - Write misses.
  - Invalidations received.
  - Invalidations caused.

- Global statistics:
  - Total read hits.
  - Total read misses.
  - Total write hits.
  - Total write misses.
  - Total hits.
  - Total misses.
  - Total accesses.
  - Hit rate.
  - Miss rate.

- Bus transactions:
  - BusRd.
  - BusRdX.
  - BusUpgr.
  - BusWB.
  - Total bus transactions.
  - Silent upgrades.
  - Total invalidations received.
  - Total invalidations caused.

Notes:
-----

- The simulator does not model actual data values.
- The memory only checks address validity and accepts writebacks.
- The bus is treated as atomic, meaning one transaction happens at a time.
- All traces are processed in order.
- The project focuses on cache coherence state transitions and statistics, not timing or pipelining.
