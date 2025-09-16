from django.urls import path
from main.views import show_main
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('products/add/', views.create_product, name='create_product'),
    path('products/<int:id>/', views.show_product, name='show_product'),
    path('xml/', views.show_xml, name='show_xml'),
    path('json/', views.show_json, name='show_json'),
    path('xml/<int:product_id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:product_id>/', views.show_json_by_id, name='show_json_by_id'),
    path('products/<int:id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:id>/delete/', views.delete_product, name='delete_product'),
]

