from Cache import Cache
from Bus import Bus
from Memory import Memory
from Stats import Stats

def run_simulation(trace_name, trace_data, num_cores=4, num_lines=8, is_mesi=True):
    """
    Sets up a clean environment (Cold Start) and runs a trace[cite: 2, 4].
    """
    print(f"\n>>> Running Experiment: {trace_name}")
    print(f"Configuration: Cores={num_cores}, Lines={num_lines}, Protocol={'MESI' if is_mesi else 'MSI'}")

    # 1. Reset/Initialize components for a clean start[cite: 5, 7]
    stats = Stats(num_cores)
    memory = Memory(1024) 
    caches = []
    system_bus = Bus(caches, memory, stats)

    # 2. Build the cache hierarchy using the boolean-toggle class
    for core_id in range(num_cores):
        caches.append(Cache(core_id, stats, num_lines=num_lines, is_MESI=is_mesi))

    # 3. Execute the trace operations[cite: 4]
    for core_id, operation, address in trace_data:
        if operation == "R":
            caches[core_id].processor_read(address, system_bus)
        elif operation == "W":
            caches[core_id].processor_write(address, system_bus)

    # 4. Output the results
    stats.print_summary()

def interleave_traces(trace1, trace2):
    """
    Merges two traces to simulate simultaneous execution on the bus[cite: 1, 8].
    """
    merged = []
    len1, len2 = len(trace1), len(trace2)
    for i in range(max(len1, len2)):
        if i < len1:
            merged.append(trace1[i])
        if i < len2:
            merged.append(trace2[i])
    return merged