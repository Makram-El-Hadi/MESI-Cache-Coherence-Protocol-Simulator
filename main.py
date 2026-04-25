from Cache import Cache
from Bus import Bus
from Memory import Memory
from Stats import Stats

def main():
    num_cores = 4

    stats = Stats(num_cores)
    memory = Memory(1024)

    caches = []

    system_bus = bus(caches, memory, stats)

    for core_id in range(num_cores):
        caches.append(Cache(core_id))

    trace = [
        (0, "R", 0x10),
        (1, "R", 0x10),
        (0, "W", 0x10),
        (2, "R", 0x10),
    ]

    for core_id, operation, address in trace:
        if operation == "R":
            caches[core_id].processor_read(address, system_bus)

        elif operation == "W":
            caches[core_id].processor_write(address, system_bus)

    stats.collect_cache_stats(caches)
    stats.print_summary()

if __name__ == "__main__":
    main()
