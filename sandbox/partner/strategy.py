from decimal import Decimal as D
from oscar.apps.partner import strategy, prices
from oscar.core.loading import get_class
UnavailablePrice = get_class('partner.prices', 'Unavailable')
FixedPrice = get_class('partner.prices', 'FixedPrice')


class Selector(object):
    """
    Custom selector to return a UK-specific strategy that charges VAT
    """

    def strategy(self, request=None, user=None, **kwargs):
        print("Drin")
        return UK()

from oscar.apps.partner.strategy import UseFirstStockRecord,StockRequired,Structured,TaxInclusiveFixedPrice
class FixedRateTax(object):
    """
    Pricing policy mixin for use with the ``Structured`` base strategy.  This
    mixin applies a fixed rate tax to the base price from the product's
    stockrecord.  The price_incl_tax is quantized to two decimal places.
    Rounding behaviour is Decimal's default
    """
    rate = D('0')  # Subclass and specify the correct rate
    exponent = D('0.01')  # Default to two decimal places

    def pricing_policy(self, product, stockrecord):

        if not stockrecord or stockrecord.price is None:
            return UnavailablePrice()
        #rate = self.get_rate(product, stockrecord)
        rate = product.product_tax.Taxvalue
        rate = D(rate/100)


        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price * rate).quantize(exponent)
        return TaxInclusiveFixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price,
            tax=tax)

    def parent_pricing_policy(self, product, children_stock):
        stockrecords = [x[1] for x in children_stock if x[1] is not None]
        if not stockrecords:
            return UnavailablePrice()

        # We take price from first record
        stockrecord = stockrecords[0]
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price * rate).quantize(exponent)

        return FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price,
            tax=tax)

    def get_rate(self, product, stockrecord):
        """
        This method serves as hook to be able to plug in support for varying tax rates
        based on the product.

        TODO: Needs tests.
        """
        return self.rate

    def get_exponent(self, stockrecord):
        """
        This method serves as hook to be able to plug in support for a varying exponent
        based on the currency.
        TODO: Needs tests.
        """
        return self.exponent





class UK(UseFirstStockRecord, StockRequired, FixedRateTax, Structured):
    """
    Sample strategy for the UK that:

    - uses the first stockrecord for each product (effectively assuming
        there is only one).
    - requires that a product has stock available to be bought
    - applies a fixed rate of tax on all products

    This is just a sample strategy used for internal development.  It is not
    recommended to be used in production, especially as the tax rate is
    hard-coded.
    """
    # Use UK VAT rate (as of December 2013)
    rate = D('0.20')
