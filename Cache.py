class Cache:
    
    def __init__(self, core_id, stats, num_lines=8, is_MESI=True):
        
        self.core_id = core_id
        self.lines = {i : {'tag': None, 'state': 'I'} for i in range(num_lines)} # Initialize cache lines with I state
        self.num_lines = num_lines
        self.is_MESI=is_MESI #switch between MESI and MSI
        self.stats=stats 

    def _get_index_tag(self, address): 
        index = address % self.num_lines
        tag = address // self.num_lines
        return index, tag

    def processor_read(self, address, bus):
        index, tag = self._get_index_tag(address)
        line = self.lines[index]

        #read hit
        if line['tag'] == tag and line['state'] != 'I':
            self.stats.log_rd_hit(self.core_id) 
            return f"Read Hit (State: {line['state']})"

        #read miss (else condition)
        self.stats.log_rd_miss(self.core_id) 
        
        if line['state'] == 'M': #check if we need to write back before replacing data
            bus.issue_bus_wb(line['tag'] * self.num_lines + index) # writing back

        is_shared = bus.issue_bus_rd(self.core_id, address) # returns true if another copy is available in cache
        
        # updates the cache state
        if self.is_MESI: 
            new_state = 'S' if is_shared else 'E'
        else:
            new_state = 'S'
            
        self.lines[index] = {'tag': tag, 'state': new_state}
        return f"Read Miss -> Transition to {new_state}"

    def processor_write(self, address, bus):
        index, tag = self._get_index_tag(address)
        line = self.lines[index]

        # write hit
        if line['tag'] == tag and line['state'] != 'I':
            self.stats.log_wr_hit(self.core_id) 
            
            # silent upgrade (MESI only)
            if line['state'] == 'E': 
                line['state'] = 'M'
                self.stats.log_silent_upgrade()
                return "Silent Upgrade: E -> M"
                
            # invalidate all other copies
            elif line['state'] == 'S':
                bus.issue_bus_upgr(self.core_id, address) 
                line['state'] = 'M'
                return "BusUpgr: S -> M"
                
            return "Write Hit: Stay in M"

        # write miss (else condition) 
        self.stats.log_wr_miss(self.core_id)
        
        if line['state'] == 'M': #check if we need to write back before replacing data
            bus.issue_bus_wb(line['tag'] * self.num_lines + index) # writing back
            
        bus.issue_bus_rdx(self.core_id, address) # invalidate other copies and get ownership
        
        # update cache line tag and state(M)
        self.lines[index] = {'tag': tag, 'state': 'M'}
        return "Write Miss: -> M"

    def snoop(self, bus_op, address): #does not affect stats
        #React to other cores' bus traffic
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
            
            if bus_op == 'BusRdX' or bus_op == 'BusUpgr': # Invalidate copy
                line['state'] = 'I'
                return "Invalidated"
        return None
