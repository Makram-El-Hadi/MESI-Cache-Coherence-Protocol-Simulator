class Stats:
    def __init__(self, num_cores):
        self.num_cores = num_cores

        # Per-core stats (filled later from caches)
        self.read_hits = [0] * num_cores
        self.read_misses = [0] * num_cores
        self.write_hits = [0] * num_cores
        self.write_misses = [0] * num_cores

        # Invalidation stats
        self.invalidations_received = [0] * num_cores
        self.invalidations_caused = [0] * num_cores

        # Bus transactions (used directly by Bus.py)
        self.bus_transactions = {
            "BusRd": 0,
            "BusRdX": 0,
            "BusUpgr": 0,
            "BusWB": 0
        }

        # MESI-specific metric
        self.silent_upgrades = 0

    # Cache logging functions
    def log_rd_hit(self, core_id):
        self.read_hits[core_id] += 1

    def log_rd_miss(self, core_id):
        self.read_misses[core_id] += 1

    def log_wr_hit(self, core_id):
        self.write_hits[core_id] += 1

    def log_wr_miss(self, core_id):
        self.write_misses[core_id] += 1

    def log_silent_upgrade(self):
        self.silent_upgrades += 1

    # Bus logging functions
    def log_BusRd(self):
        self.bus_transactions["BusRd"] += 1

    def log_BusRdX(self):
        self.bus_transactions["BusRdX"] += 1

    def log_BusUpgr(self):
        self.bus_transactions["BusUpgr"] += 1

    def log_BusWB(self):
        self.bus_transactions["BusWB"] += 1


    # Invalidation logging
    def log_invalidation_received(self, core_id):
        self.invalidations_received[core_id] += 1

    def log_invalidation_caused(self, core_id):
        self.invalidations_caused[core_id] += 1

    # Global totals
    def total_read_hits(self):
        return sum(self.read_hits)

    def total_read_misses(self):
        return sum(self.read_misses)

    def total_write_hits(self):
        return sum(self.write_hits)

    def total_write_misses(self):
        return sum(self.write_misses)

    def total_invalidations_received(self):
        return sum(self.invalidations_received)

    def total_invalidations_caused(self):
        return sum(self.invalidations_caused)

    def total_bus_transactions(self):
        return sum(self.bus_transactions.values())

    def total_accesses(self):
        return self.total_hits() + self.total_misses()
    
    def total_hits(self):
        return self.total_read_hits() + self.total_write_hits()

    def total_misses(self):
        return self.total_read_misses() + self.total_write_misses()

    def hit_rate(self):
        if self.total_accesses() == 0:
            return 0
        return self.total_hits() / self.total_accesses()
    
    def miss_rate(self):
        if self.total_accesses() == 0:
            return 0
        return self.total_misses() / self.total_accesses()

    # Simple prints to see nicer
    def print_summary(self):
        print("\n==================== STATS SUMMARY ====================")

        print("\nPer-core statistics:")
        for i in range(self.num_cores):
            print(
                f"Core {i}: "
                f"RH={self.read_hits[i]}, "
                f"RM={self.read_misses[i]}, "
                f"WH={self.write_hits[i]}, "
                f"WM={self.write_misses[i]}, "
                f"InvRecv={self.invalidations_received[i]}, "
                f"InvCause={self.invalidations_caused[i]}"
            )

        print("\nGlobal statistics:")
        print(f"Total read hits: {self.total_read_hits()}")
        print(f"Total read misses: {self.total_read_misses()}")
        print(f"Total write hits: {self.total_write_hits()}")
        print(f"Total write misses: {self.total_write_misses()}")
        print(f"Total Hits: {self.total_hits()}")
        print(f"Total misses: {self.total_misses()}")
        print(f"Total accesses: {self.total_accesses()}")
        print(f"Hit rate: {self.hit_rate():.4f}")
        print(f"Miss rate: {self.miss_rate():.4f}")

        print("\nBus transactions:")
        for name, count in self.bus_transactions.items():
            print(f"{name}: {count}")

        print(f"Total bus transactions: {self.total_bus_transactions()}")
        print(f"Silent upgrades: {self.silent_upgrades}")
        print(f"Total invalidations received: {self.total_invalidations_received()}")
        print(f"Total invalidations caused: {self.total_invalidations_caused()}")

        print("=======================================================\n")
