class Memory:

    def __init__(self, size):
        
        self.size = size  # initialize the memory system aligned with the size of memory chosen

    def check_address_validity(self, address):
        
      if (address < 0) or (address >= self.size): # valid address are from 0 to size - 1

          raise ValueError(f"Address {address} is invalid") # we used the raise a value error in order to stop execution of the code
   
    def read(self, address):
      
      self.check_address_validity(address)
      return None # we don't care what the value is so we always return None

    def write_back(self, address):
        
        self.check_address_validity(address) # we do not need to make a write function because we have a write_back cache and not a write_through cache, so we only have write_back occuring from caches.
