#from .docdata import CustomDocdataFacade
import logging
from oscar.apps.payment.models import Source
from . import gateway
from oscar.apps.checkout import views as oscar_views

from paypal.payflow import facade
from django.contrib import messages
from . import forms
from django.shortcuts import redirect
from oscar.apps.payment.models import SourceType
from oscar.apps.payment.forms import BankcardForm
from .forms import BillingAddressForm
from oscar.apps.checkout import exceptions
from django.urls import reverse, reverse_lazy
from oscar.core.loading import get_model, get_class
OscarPaymentMethodView = get_class("checkout.views", "PaymentMethodView")
OscarPaymentDetailsView = get_class("checkout.views", "PaymentDetailsView")
OscarShippingMethodView = get_class("checkout.views", "ShippingMethodView")
OscarCheckoutSessionMixin = get_class("checkout.views", "CheckoutSessionMixin")
from django.views.generic import FormView
from django.conf import settings
BillingAddress = get_model("order", "BillingAddress")
from django.views import generic
from oscar.core.loading import get_classes, get_model


logger = logging.getLogger(__name__)
Country = get_model('address', 'Country')
ShippingAddressForm, ShippingMethodForm, GatewayForm \
    = get_classes('checkout.forms', ['ShippingAddressForm', 'ShippingMethodForm', 'GatewayForm'])




# Sample pre-condition
class CheckCountryPreCondition(object):
    """DRY class for check country in session pre_condition"""

    def get_pre_conditions(self, request):
        if 'check_country_in_session' not in self.pre_conditions:
            return self.pre_conditions + ['check_country_in_session']
        return super().get_pre_conditions(request)

    def check_country_in_session(self, request):
        if request.session.get('country', None) is None:
            raise exceptions.FailedPreCondition(
                    url=reverse('checkout:shipping-address'),
                )



# Inspired by https://github.com/django-oscar/django-oscar-docdata/blob/master/sandbox/apps/checkout/views.py
class PaymentMethodView(OscarPaymentMethodView, FormView):
    """
    View for a user to choose which payment method(s) they want to use.

    This would include setting allocations if payment is to be split
    between multiple sources. It's not the place for entering sensitive details
    like bankcard numbers though - that belongs on the payment details view.
    """
    template_name = "oscar/checkout/payment_method.html"
    step = 'payment-method'
    form_class = forms.PaymentMethodForm
    pre_conditions = []
    skip_conditions = []
    success_url = reverse_lazy('checkout:payment-details')


    def get(self, request, *args, **kwargs):

        # if only single payment method, store that
        # and then follow default (redirect to preview)
        # else show payment method choice form
        if len(settings.OSCAR_PAYMENT_METHODS) == 1:
            self.checkout_session.pay_by(settings.OSCAR_PAYMENT_METHODS[0][0])
            return redirect(self.get_success_url())
        else:

            return FormView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #print("Context")
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self, *args, **kwargs):

        # Redirect to the correct payments page as per the method (different methods may have different views &/or additional views)
        if (self.checkout_session.payment_method() == 'cod'):
            return reverse_lazy('checkout:preview')
        return reverse_lazy('checkout:payment-details')



    def get_initial(self):
        print("Initial")
        return {
            'payment_method': self.checkout_session.payment_method(),
        }

    def form_valid(self, form):
        # Store payment method in the CheckoutSessionMixin.checkout_session (a CheckoutSessionData object)
        self.checkout_session.pay_by(form.cleaned_data['payment_method'])
        return super().form_valid(form)





class PaymentDetailsView(oscar_views.PaymentDetailsView):
    """
    An example view that shows how to integrate BOTH PayPal Express
    (see `get_context_data method`) and PayPal Flow (the other methods).
    Naturally, you will only want to use one of the two.
    """
    #template_name = 'website/payment_details.html'
    #template_name = "oscar/checkout/payment_details.html"
    #template_name_preview = 'website/preview.html'
    #template_name_preview = 'oscar/checkout/preview.html'

    def get_billing_address_form(self, billing_address):
        """
        Return an instantiated billing address form
        """
        addr = self.get_default_billing_address()
        if not addr:
            return BillingAddressForm(billing_address)
        billing_addr = BillingAddress()
        addr.populate_alternative_model(billing_addr)
        return BillingAddressForm(billing_address,
                                  instance=billing_addr)

    def get_context_data(self, **kwargs):
        """
        Add data for Paypal Express flow.
        """
        # Override method so the bankcard and billing address forms can be
        # added to the context.
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get(
            'bankcard_form', BankcardForm())
        #ctx['billing_address_form'] = kwargs.get(
        #    'billing_address_form', BillingAddressForm())
        if 'billing_address_form' not in kwargs:
            ctx['billing_address_form'] = self.get_billing_address_form(
                ctx['shipping_address']
            )
        method = self.checkout_session.payment_method()
        ctx['payment_method'] = {
            'code': method,
            'title': self.get_payment_method_display(method),
        }
        #print("Context "+str(ctx))
        return ctx

    def get_payment_method_display(self, payment_method):

        return dict(settings.OSCAR_PAYMENT_METHODS).get(payment_method)

    def handle_place_order_submission(self, request):
        # Collect all the data!
        submission = self.build_submission()

        # docdata needs to have a lot of information to start the payment.
        # TODO: Is this the right way to pass the information??
        submission['payment_kwargs']['submission'] = submission

        # Start the payment process!
        # This jumps to handle_payment()
        return self.submit(**submission)

    def post(self, request, *args, **kwargs):

        # Override so we can validate the bankcard/billing_address submission.
        # If it is valid, we render the preview screen with the forms hidden
        # within it.  When the preview is submitted, we pick up the 'action'
        # parameters and actually place the order.
        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)

            #paypal
            if (self.checkout_session.payment_method() == 'paypal'):

                bankcard_form = forms.BankcardForm(request.POST)
                billing_address_form = forms.BillingAddressForm(request.POST)
                if not all([bankcard_form.is_valid(),
                    billing_address_form.is_valid()]):
                 # Form validation failed, render page again with errors
                    self.preview = False
                    ctx = self.get_context_data(
                    bankcard_form=bankcard_form,
                    billing_address_form=billing_address_form)
                    return self.render_to_response(ctx)

            # Render preview with bankcard and billing address details hidden
                return self.render_preview(request,
                                   bankcard_form=bankcard_form,
                                   billing_address_form=billing_address_form)
            #cod
            #if (self.checkout_session.payment_method() == 'cod'):
            #    return self.handle_place_order_submission(request)
        #else:
            return self.handle_payment_details_submission(request)

    def do_place_order(self, request):

        # Helper method to check that the hidden forms wasn't tinkered
        # with.
        submission = self.build_submission()
        # paypal
        if (self.checkout_session.payment_method() == 'paypal'):
            bankcard_form = forms.BankcardForm(request.POST)
            billing_address_form = forms.BillingAddressForm(request.POST)
            if not all([bankcard_form.is_valid(),
                    billing_address_form.is_valid()]):
                messages.error(request, "Invalid submission")
                return redirect('checkout:payment-details')

            # Attempt to submit the order, passing the bankcard object so that it
            # gets passed back to the 'handle_payment' method below.

            submission['payment_kwargs']['bankcard'] = bankcard_form.bankcard
            submission['payment_kwargs']['billing_address'] = billing_address_form.cleaned_data
        return self.submit(**submission)

    def handle_payment(self, order_number, total, **kwargs):
        """
                    Make submission to PayPal
                    """

        if (self.checkout_session.payment_method() == 'paypal'):

            # Using authorization here (two-stage model).  You could use sale to
            # perform the auth and capture in one step.  The choice is dependent
            # on your business model.
            facade.authorize(
                order_number, total.incl_tax,
                kwargs['bankcard'], kwargs['billing_address'])

            # Record payment source and event
            source_type, is_created = SourceType.objects.get_or_create(
                name='PayPal')
            source = source_type.sources.model(
                source_type=source_type,
                amount_allocated=total.incl_tax, currency=total.currency)
            self.add_payment_source(source)
            self.add_payment_event('Authorised', total.incl_tax)
        if (self.checkout_session.payment_method() == 'cod'):

            reference = gateway.create_transaction(order_number, total)

            source_type, is_created = SourceType.objects.get_or_create(
                name='Cash on Delivery')
            source = Source(source_type=source_type,
                            currency=total.currency,
                            amount_allocated=total.incl_tax,
                            amount_debited=total.incl_tax)
            self.add_payment_source(source)
            self.add_payment_event('Issued', total.incl_tax,
                                   reference=reference)
            #self.add_payment_event('Issued', total.incl_tax
            #                       )