class Cache:
    def __init__(self, core_id, stats, num_lines=8):#changed
        self.core_id = core_id
        # State mapping: {index: {'tag': tag, 'state': state}}
        # Initial state is 'I' (Invalid)
        self.lines = {i : {'tag': None, 'state': 'I'} for i in range(num_lines)}
        self.num_lines = num_lines
        
        # Stats tracking
        #self.stats = {'rd_hit': 0, 'rd_miss': 0, 'wr_hit': 0, 'wr_miss': 0, 'silent_upgrades': 0}
        self.stats=stats #changed

    def _get_index_tag(self, address):
        index = address % self.num_lines
        tag = address // self.num_lines
        return index, tag

    def processor_read(self, address, bus):
        index, tag = self._get_index_tag(address)
        line = self.lines[index]

        # PrRd Hit: State is M, E, or S and tag matches
        if line['tag'] == tag and line['state'] != 'I':
            #self.stats['rd_hit'] += 1
            self.stats.log_rd_hit(self.core_id) # Real-time push
            return f"Read Hit (State: {line['state']})"

        # PrRd Miss: Issue BusRd
        #self.stats['rd_miss'] += 1
        self.stats.log_rd_miss(self.core_id) # Real-time push
        
        # Check if line is Modified before evicting
        if line['state'] == 'M':
            bus.issue_bus_wb(line['tag'] * self.num_lines + index) # Evicted line's address

        # Bus returns True if another cache has a copy
        is_shared = bus.issue_bus_rd(self.core_id, address)
        
        # MESI Transition: If shared found -> S, else -> E
        new_state = 'S' if is_shared else 'E'
        self.lines[index] = {'tag': tag, 'state': new_state}
        return f"Read Miss -> Transition to {new_state}"

    def processor_write(self, address, bus):
        index, tag = self._get_index_tag(address)
        line = self.lines[index]

        # 1. Check for Write Hit
        if line['tag'] == tag and line['state'] != 'I':
            #self.stats['wr_hit'] += 1
            self.stats.log_wr_hit(self.core_id) # Real-time push
            
            # MESI SPECIAL CASE: Silent Upgrade
            if line['state'] == 'E': 
                line['state'] = 'M'
                #self.stats['silent_upgrades'] += 1 # Required metric for Experiment 4
                self.stats.log_silent_upgrade() # Real-time push
                return "Silent Upgrade: E -> M"
                
            # If in S, we must invalidate others before writing
            elif line['state'] == 'S':
                bus.issue_bus_upgr(self.core_id, address) # BusUpgr signal
                line['state'] = 'M'
                return "BusUpgr: S -> M"
                
            return "Write Hit: Stay in M"

        # 2. Write Miss Logic
        #self.stats['wr_miss'] += 1 
        self.stats.log_wr_miss(self.core_id) # Real-time push
        
        # Eviction: If current line is Modified, write it back first
        if line['state'] == 'M':
            bus.issue_bus_wb(line['tag'] * self.num_lines + index) # Evicted line's address
            
        # Issue BusRdX (Read-Exclusive): Get data and invalidate everyone else
        bus.issue_bus_rdx(self.core_id, address)
        
        # Transition to Modified (M)
        self.lines[index] = {'tag': tag, 'state': 'M'}
        return "Write Miss: -> M"

    def snoop(self, bus_op, address):
        """React to other cores' bus traffic"""
        index, tag = self._get_index_tag(address)
        line = self.lines[index]

        if line['tag'] == tag and line['state'] != 'I':
            if bus_op == 'BusRd':
                # If we are M, we must write back and move to S
                if line['state'] == 'M':  
                    line['state'] = 'S'
                    return "Flush" # Signal to bus that we had data
                line['state'] = 'S' # Stay in S if already S or E
                return "Hit"
            
            if bus_op == 'BusRdX' or bus_op == 'BusUpgr':
                # Invalidation: move to I
                line['state'] = 'I'
                return "Invalidated"
        return None
