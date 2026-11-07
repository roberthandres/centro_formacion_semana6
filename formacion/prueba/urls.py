from django.urls import path
from . import views


from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_aprendices, name='listar_aprendices'),
    path('crear/', views.crear_aprendiz, name='crear_aprendiz'),
    path('editar/<str:documento>/', views.editar_aprendiz, name='editar_aprendiz'),
    path('eliminar/<str:documento>/', views.eliminar_aprendiz, name='eliminar_aprendiz'),

    # MAPA DE APRENDICES
    path('mapa/', views.mapa_aprendices, name='mapa_aprendices'),
]
