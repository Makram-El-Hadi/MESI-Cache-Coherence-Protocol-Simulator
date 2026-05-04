class Bus:

  def __init__(self, caches, memory, stats):

    self.caches = caches
    self.memory = memory
    self.stats = stats


  def issue_bus_rd(self, core_requester_id, address):

    self.stats.log_BusRd() 

    shared = False

    for cache in self.caches: #checks all core caches

      if cache.core_id == core_requester_id:
        continue
    
      response = cache.snoop('BusRd', address) # Bus asks each cache whether they have the data in their cache or not

      if response == "Hit":
        shared = True

      elif response == "Flush": # if the cache has the data in modified state, it will writeback to memory

        shared = True
        self.issue_bus_wb(address) # if we had to flush, we need to write back to memory
        
        
    return shared

  def issue_bus_rdx(self, core_requester_id, address):

      self.stats.log_BusRdX()

      for cache in self.caches:
          if cache.core_id == core_requester_id:  # if the core id we hit is the same as the core that requested the bus operation we skip
              continue

          response = cache.snoop('BusRdX', address) # The Bus is telling all the cores that the bus operation is BusRdX i.e. invalidate all their caches
          if response == "Invalidated": # if the cache had the data in shared or exclusive state, it will invalidate it

            self.stats.log_invalidation_received(cache.core_id) # record that this cache received an invalidation
            self.stats.log_invalidation_caused(core_requester_id) # record that the requester caused an invalidation
  
  def issue_bus_upgr(self, core_requester_id, address):

    self.stats.log_BusUpgr()

    for cache in self.caches:

      if cache.core_id == core_requester_id: 
          continue

      response = cache.snoop('BusUpgr', address) # The Bus is telling all the cores that the bus operation is BusUpgr i.e. invalidate all their caches
      if response == "Invalidated": 

        self.stats.log_invalidation_received(cache.core_id) # record that this cache received an invalidation
        self.stats.log_invalidation_caused(core_requester_id) # record that the requester caused an invalidation
  
  def issue_bus_wb(self, address):
      
      self.stats.log_BusWB() # Global count not per core
      self.memory.write_back(address) # tells the memory to write back to that address (no need to tell the other caches of this operation)
