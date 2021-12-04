from oscar.apps.shipping.views import Core
class Repository(object):
    """
    Repository class responsible for returning ShippingMethod
    objects for a given user, basket etc
    """

    # We default to just free shipping. Customise this class and override this
    # property to add your own shipping methods. This should be a list of
    # instantiated shipping methods.
    methods = (Free(),NoShippingRequired())
