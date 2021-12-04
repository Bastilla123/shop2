from oscar.apps.shipping import methods
from oscar.core import prices
from decimal import Decimal as D

class Free(methods.Base):
    code = 'free'
    name = 'Standard shipping (free)'

    def calculate(self, basket):
        return prices.Price(
            currency=basket.currency,
            excl_tax=D('0.00'), incl_tax=D('0.00'))

class DHL_Standard(methods.FixedPrice):
    code = 'dhl_standard'
    name = 'DHL Standard shipping'
    charge_excl_tax = D('5.00')
    charge_incl_tax = D('5.00')