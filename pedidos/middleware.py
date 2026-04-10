from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class BloquearNavegacionManualMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Solo aplicar si el usuario está autenticado y es una petición GET 
        # a una página dentro de /pedidos/ que no sea el inicio
        if request.user.is_authenticated and request.method == 'GET' and path.startswith('/pedidos/'):
            ruta_inicio = reverse('inicio')
            # Si intentan ir a clientes, productos o cualquier otra ruta que no sea el inicio
            if path != ruta_inicio:
                referer = request.META.get('HTTP_REFERER')
                
                # Si no hay referer, significa que copiaron/pegaron la URL o escribieron a mano
                if not referer:
                    messages.warning(request, "Acceso bloqueado por seguridad: Usa el menú de navegación, no escribas la URL.")
                    return redirect('inicio')
                
        return self.get_response(request)
