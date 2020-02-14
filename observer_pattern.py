class Inventory:
    def __init__(self):
        self.observers = []
        self._num_product1 = 0
        self._num_product2 = 0
        
    def attach(self, observer):
        self.observers.append(observer)
        
    @property
    def num_product1(self):
        return self._num_product1
    
    @num_product1.setter
    def num_product1(self, value):
        self._num_product1 = value
        self._update()
        
    @property
    def num_product2(self):
        return self._num_product2
    
    @num_product2.setter
    def num_product2(self, value):
        self._num_product2 = value
        self._update()
    
    def _update(self):
        for observer in self.observers:
            observer()


class ConsoleObserver:
    def __init__(self, inventory):
        self.inventory = inventory
    
    def __call__(self):
        print('Number of products 1: {}'.format(self.inventory.num_product1))
        print('Number of products 2: {}'.format(self.inventory.num_product2))
