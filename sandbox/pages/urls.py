from django.urls import path, include

from .views import *

urlpatterns = [


    path('impressum/', impressumview, name="impressumview"),
    path('godb/', gobdview, name="godb"),
    path('revisionssicherheit/', revisionssicherheitview, name="revisionssicherheitview"),
    path('teampage/', Teamlistview.as_view(), name="Teamlistview"),
    path('csr/', csr, name="csr"),
    path('payment/', payment, name="payment"),
    path('behavior_rules/', behavior_rules, name="behavior_rules"),
    path('datamigration/', datamigration, name="datamigration"),
    path('contact/', contact, name="contact"),
    path('agb/', agb, name="agb"),
    path('privacy_statement/', privacy_statement, name="privacy_statement"),
    path('contact_us/', contact_us, name="contact_us"),

    path('widerruf/', widerrufview, name="widerruf"),

]
app_name = 'pages'