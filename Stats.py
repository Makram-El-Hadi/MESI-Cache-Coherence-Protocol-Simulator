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
        print("\nStats Summary: ")

        print("\nPer-core statistics:\n")
        for i in range(self.num_cores):
            print("Core " + str(i) + ": "
                + "Read Hits = " + str(self.read_hits[i]) + ", "
                + "Read Misses = " + str(self.read_misses[i]) + ", "
                + "Write Hits = " + str(self.write_hits[i]) + ", "
                + "Write Misses = " + str(self.write_misses[i]) + ", "
                + "Invalidations Received = " + str(self.invalidations_received[i]) + ", "
                + "Invalidations Caused = " + str(self.invalidations_caused[i]))

        print("\nGlobal statistics:\n")
        print("Total read hits: " + str(self.total_read_hits()))
        print("Total read misses: " + str(self.total_read_misses()))
        print("Total write hits: " + str(self.total_write_hits()))
        print("Total write misses: " + str(self.total_write_misses()))
        print("Total Hits: " + str(self.total_hits()))
        print("Total misses: " + str(self.total_misses()))
        print("Total accesses: " + str(self.total_accesses()))
        print("Hit rate: " + str(round(self.hit_rate(), 4)))
        print("Miss rate: " + str(round(self.miss_rate(), 4)))

        print("\nBus transactions:\n")
        for name in self.bus_transactions:
            print(name + ": " + str(self.bus_transactions[name]))

        print("Total bus transactions: " + str(self.total_bus_transactions()))
        print("Silent upgrades: " + str(self.silent_upgrades))
        print("Total invalidations received: " + str(self.total_invalidations_received()))
        print("Total invalidations caused: " + str(self.total_invalidations_caused()))
