from shop import settings

def show_tax_separately(request):
    show_tax_separately  = getattr(settings, 'OSCAR_SHOW_TAX_SEPARATELY', False)
    return {'show_tax_separately': show_tax_separately}
