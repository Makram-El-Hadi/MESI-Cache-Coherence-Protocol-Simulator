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

    # Invalidation tracking (used in Bus.py)
    def record_invalidation_received(self, core_id):
        self.invalidations_received[core_id] += 1

    def record_invalidation_caused(self, core_id):
        self.invalidations_caused[core_id] += 1

    # Collect stats from caches
    # IMPORTANT: call this AFTER simulation
    def collect_cache_stats(self, caches): # Each cashe already tracks: rd_hit, rd_miss, wr_hit, wr_miss, silent_upgrades
        self.silent_upgrades = 0
        
        for cache in caches: # Now we copy them into global stats.
            cid = cache.core_id

            self.read_hits[cid] = cache.stats.get("rd_hit", 0)
            self.read_misses[cid] = cache.stats.get("rd_miss", 0)
            self.write_hits[cid] = cache.stats.get("wr_hit", 0)
            self.write_misses[cid] = cache.stats.get("wr_miss", 0)

            self.silent_upgrades += cache.stats.get("silent_upgrades", 0)

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
        return (
            self.total_read_hits()
            + self.total_read_misses()
            + self.total_write_hits()
            + self.total_write_misses()
        )

    def total_misses(self):
        return self.total_read_misses() + self.total_write_misses()

    def hit_rate(self):
        if self.total_accesses() == 0:
            return 0
        return (self.total_read_hits() + self.total_write_hits()) / self.total_accesses()

    def miss_rate(self):
        if self.total_accesses() == 0:
            return 0
        return self.total_misses() / self.total_accesses()

    # Simple prints to see nicer
    def print_summary(self):
        print("\n==================== STATS SUMMARY ====================")

        print("\nPer-core statistics:")
        for cid in range(self.num_cores):
            print(
                f"Core {cid}: "
                f"RH={self.read_hits[cid]}, "
                f"RM={self.read_misses[cid]}, "
                f"WH={self.write_hits[cid]}, "
                f"WM={self.write_misses[cid]}, "
                f"InvRecv={self.invalidations_received[cid]}, "
                f"InvCause={self.invalidations_caused[cid]}"
            )

        print("\nGlobal statistics:")
        print(f"Total read hits: {self.total_read_hits()}")
        print(f"Total read misses: {self.total_read_misses()}")
        print(f"Total write hits: {self.total_write_hits()}")
        print(f"Total write misses: {self.total_write_misses()}")
        print(f"Total accesses: {self.total_accesses()}")
        print(f"Total misses: {self.total_misses()}")
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