from Cache import Cache
from Bus import Bus
from Memory import Memory
from Stats import Stats

def run_simulation(trace_name, trace_data, num_cores=4, num_lines=8, memory=64, is_mesi=True):
    
    print(f"\nRunning: {trace_name}")
    print(f"Cores = {num_cores}, Lines = {num_lines}, Protocol = {'MESI' if is_mesi else 'MSI'}\n")

    # creating new instances
    stats = Stats(num_cores)
    caches = []
    system_bus = Bus(caches, memory, stats)

    for core_id in range(num_cores): # building caches for each core
        caches.append(Cache(core_id, stats, num_lines=num_lines, is_MESI=is_mesi))

    # running the trace
    for core_id, operation, address in trace_data:
        if core_id >= num_cores: # avoids out of range error if trace has more cores than we are simulating
            continue
        if operation == "R":
            caches[core_id].processor_read(address, system_bus)
        elif operation == "W":
            caches[core_id].processor_write(address, system_bus)

    stats.print_summary() # print the results
