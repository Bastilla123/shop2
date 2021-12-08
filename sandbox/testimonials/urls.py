from django.urls import path, include

from .views import *

urlpatterns = [


    # #CRUD Tabs
    #path('list/', views.TestimonialsListView.as_view(), name="TestimonialsListView"),
    #path('create/', views.TestimonialsCreateView.as_view(),name="TestimonialsCreateView"),
    path("update/<int:pk>/", TestimonialsUpdateView.as_view(), name="TestimonialsUpdateView", ),

    #path('delete/<int:pk>/', views.TestimonialsDeleteView.as_view(),name="TestimonialsDeleteView"),

]
app_name = 'testimonials'