from django.urls import path
from . import views

urlpatterns = [

    # ─────────────────────────────────────────────
    # VISTAS WEB (sin cambios)
    # ─────────────────────────────────────────────
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),

    # Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # Pedidos
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/ver/<int:pk>/', views.ver_pedido, name='ver_pedido'),
    path('pedidos/editar/<int:pk>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:pk>/', views.eliminar_pedido, name='eliminar_pedido'),

    # Detalle Pedido
    path('pedidos/<int:pedido_id>/detalles/crear/', views.crear_detalle, name='crear_detalle'),
    path('pedidos/detalles/eliminar/<int:pk>/', views.eliminar_detalle, name='eliminar_detalle'),

    # Exportaciones
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),


    # ─────────────────────────────────────────────
    # API JWT (nuevas rutas para Postman)
    # ─────────────────────────────────────────────

    # Login → devuelve access + refresh token
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),

    # Clientes API
    path('api/clientes/', views.ClienteAPIView.as_view(), name='api_clientes'),
    path('api/clientes/<int:pk>/', views.ClienteDetalleAPIView.as_view(), name='api_cliente_detalle'),

    # Productos API
    path('api/productos/', views.ProductoAPIView.as_view(), name='api_productos'),
    path('api/productos/<int:pk>/', views.ProductoDetalleAPIView.as_view(), name='api_producto_detalle'),

    # Pedidos API
    path('api/pedidos/', views.PedidoAPIView.as_view(), name='api_pedidos'),
    path('api/pedidos/<int:pk>/', views.PedidoDetalleAPIView.as_view(), name='api_pedido_detalle'),
]