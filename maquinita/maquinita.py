'''
Created on 08/12/2013

@author: sergioo
'''

class Maquinita(object):

    def __init__(self, hardware_device=None):
        self.credit = 0
        self.price = None
        self.change = []
        if hardware_device is None: 
            self.hardware_device = HardwareDevice()
    
    def insert_coin(self, coin):
        self.credit += coin.value
        if self.price is not None and self.credit >= self.price:
            self.expend_ticket()

    def get_credit(self):
        return self.credit
    
    def set_price(self, price):
        self.price = price
    
    def expend_ticket(self):
        try:
            self.hardware_device.expend_ticket(self.price)
        except NoMorePaperException, e:
            self.hardware_device.display_message(e.message)
        self.expend_change()
    
    def expend_change(self):
        change = self.calculate_change()
        self.hardware_device.expend_coins(change)
        self.credit = 0
        self.change = []
        self.price = None
    
    def calculate_change(self):
        excedente = self.get_credit() - self.price
        coins = []
        
        for value in Coin.VALUES:
            while excedente - value > 0:
                coins.append(Coin(value))
                excedente -= value
        
        return coins


class Coin(object):
    
    VALUES = (1, 0.50, 0.25, 0.10, 0.05)
    
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        return self.value == other.value
    

class NoMorePaperException(Exception):
    pass


class HardwareDevice(object):
    
    def expend_ticket(self, value):
        pass
    
    def expend_coins(self, coins):
        pass
    
    def display_message(self, message):
        pass
    
