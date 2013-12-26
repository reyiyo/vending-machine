# coding: utf-8
'''
Created on 08/12/2013

@author: sergioo
'''
import unittest
from maquinita import Maquinita, Coin, HardwareDevice, NoMorePaperException
from mock import Mock

class MaquinitaTest(unittest.TestCase):

    def setUp(self):
        self.maquinita = Maquinita()

    def tearDown(self):
        pass

    def test_insert_coin(self):
        self.maquinita.insert_coin(Coin(0.10))
        self.assertEqual(0.10, self.maquinita.get_credit(), "El crédito es el mismo que la moneda insertada")
    
    def test_get_credit(self):
        self.maquinita.insert_coin(Coin(0.10))
        self.maquinita.insert_coin(Coin(0.25))
        self.maquinita.insert_coin(Coin(0.50))
        self.assertEqual(0.85, self.maquinita.get_credit(), "El crédito coinicide con la suma de las monedas insertadas")
    
    def test_dar_boleto_cuando_llega_al_valor(self):
        hardware_device = HardwareDevice()
        hardware_device.expend_ticket = Mock()
        self.maquinita.hardware_device = hardware_device
        self.maquinita.set_price(1.70)
        self.maquinita.insert_coin(Coin(1.0))
        self.maquinita.insert_coin(Coin(0.50))
        self.maquinita.insert_coin(Coin(0.10))
        self.maquinita.insert_coin(Coin(0.10))
        
        hardware_device.expend_ticket.assert_called_once_with(1.70)
    
    def test_el_credito_es_cero_despues_de_dar_el_ticket(self):
        self.maquinita.set_price(1.70)
        self.maquinita.insert_coin(Coin(1.0))
        self.maquinita.insert_coin(Coin(0.50))
        self.maquinita.insert_coin(Coin(0.10))
        self.maquinita.insert_coin(Coin(0.10))
        
        self.assertEqual(self.maquinita.get_credit(), 0, "El crédito es 0 después de haber impreso el boleto")
    
    def test_da_bien_el_vuelto(self):
        hardware_device = HardwareDevice()
        hardware_device.expend_coins = Mock()
        self.maquinita.hardware_device = hardware_device
        
        self.maquinita.set_price(1.70)
        self.maquinita.insert_coin(Coin(1.0))
        self.maquinita.insert_coin(Coin(1.0))
        
        call_args = hardware_device.expend_coins.call_args
        self.assertSequenceEqual([Coin(0.25), Coin(0.05)], call_args[0][0], "Me devolvió una moneda de 25 y otra de 5", list)
    
    def test_no_devuelve_monedas_cuando_el_importe_esta_justo(self):
        hardware_device = HardwareDevice()
        hardware_device.expend_coins = Mock()
        self.maquinita.hardware_device = hardware_device
        
        self.maquinita.set_price(1.70)
        self.maquinita.insert_coin(Coin(1.0))
        self.maquinita.insert_coin(Coin(0.50))
        self.maquinita.insert_coin(Coin(0.10))
        self.maquinita.insert_coin(Coin(0.10))
        
        call_args = hardware_device.expend_coins.call_args
        self.assertSequenceEqual([], call_args[0][0], "Me devolvió una moneda de 25 y otra de 5", list)

    def test_mensaje_cuando_no_hay_mas_papel(self):
        hardware_device = HardwareDevice()
        message = 'No hay más papeeeel!'
        
        hardware_device.expend_ticket = Mock(side_effect=NoMorePaperException(message))
        hardware_device.display_message = Mock()
        self.maquinita.hardware_device = hardware_device
        
        self.maquinita.set_price(1.70)
        self.maquinita.insert_coin(Coin(1.0))
        self.maquinita.insert_coin(Coin(0.50))
        self.maquinita.insert_coin(Coin(0.10))
        self.maquinita.insert_coin(Coin(0.10))
        
        hardware_device.expend_ticket.assert_called_once_with(1.70)
        hardware_device.display_message.assert_called_once_with(message)
        
        self.assertEqual(self.maquinita.get_credit(), 0, "El crédito después de emitir un ticket sin papel es cero")