class Memory:

    def __init__(self, size):
        
        self.size = size  # initialize the memory system aligned with the size of memory chosen
        self.data = [0] * size

    def check_address_validity(self, address):
        
      if (address < 0) or (address >= self.size): # valid address are from 0 to size - 1

          raise ValueError(f"Address {address} is invalid") # we used the raise a value error in order to stop execution of the code
   
    def read(self, address):
      
      self.check_address_validity(address)
      data_from_mem = self.data[address] # read the data from the memory and then return it 

      return data_from_mem
    
    def write(self, address, value):
        
        self.check_address_validity(address)
        self.data[address] = value # set the data inside memory of that specific address to value

    def write_back(self, address, value):
        
        self.write(address, value)
        