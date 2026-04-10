from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import RestrictedError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Producto, Pedido, DetallePedido
from .forms import ClienteForm, ProductoForm, PedidoForm, DetallePedidoForm
import openpyxl
from reportlab.pdfgen import canvas

# ── JWT / API imports ─────────────────────────────────────────
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import ClienteSerializer, ProductoSerializer, PedidoSerializer


# =============================================================
# REGISTRO Y INICIO (vistas web — sin cambios)
# =============================================================
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada con éxito. Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def inicio(request):
    return render(request, 'pedidos/inicio.html')

@login_required
def crear_detalle(request, pedido_id):
    return HttpResponse("Crear detalle")


# =============================================================
# CLIENTES (vistas web — sin cambios)
# =============================================================
@login_required
def listar_clientes(request):
    lista = Cliente.objects.all().order_by('-id')
    paginator = Paginator(lista, 5)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    return render(request, 'pedidos/clientes/listar.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado con éxito.")
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Crear Cliente'})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado con éxito.")
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Editar Cliente'})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    try:
        cliente.delete()
        messages.success(request, "Cliente eliminado con éxito.")
    except RestrictedError:
        messages.error(request, "No se puede eliminar el cliente porque tiene pedidos asociados.")
    return redirect('listar_clientes')


# =============================================================
# PRODUCTOS (vistas web — sin cambios)
# =============================================================
@login_required
def listar_productos(request):
    lista = Producto.objects.all().order_by('-id')
    paginator = Paginator(lista, 5)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    return render(request, 'pedidos/productos/listar.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['stock'] < 0:
                messages.error(request, "El stock no puede ser negativo.")
            else:
                form.save()
                messages.success(request, "Producto creado con éxito.")
                return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Crear Producto'})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            if form.cleaned_data['stock'] < 0:
                messages.error(request, "El stock no puede ser negativo.")
            else:
                form.save()
                messages.success(request, "Producto actualizado con éxito.")
                return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Editar Producto'})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    messages.success(request, "Producto eliminado con éxito.")
    return redirect('listar_productos')


# =============================================================
# PEDIDOS (vistas web — sin cambios)
# =============================================================
@login_required
def listar_pedidos(request):
    lista = Pedido.objects.all().order_by('-id')
    paginator = Paginator(lista, 5)
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)
    return render(request, 'pedidos/pedidos/listar.html', {'pedidos': pedidos})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            messages.success(request, "Pedido creado. Añade productos al pedido.")
            return redirect('ver_pedido', pk=pedido.id)
    else:
        form = PedidoForm()
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Crear Pedido'})

@login_required
def ver_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    detalles = pedido.detalles.all()
    total = sum(d.subtotal for d in detalles if d.subtotal)

    if request.method == 'POST':
        form = DetallePedidoForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.pedido = pedido
            if detalle.producto.stock < detalle.cantidad:
                messages.error(request, f"No hay suficiente stock. Stock actual: {detalle.producto.stock}")
            else:
                detalle.producto.stock -= detalle.cantidad
                detalle.producto.save()
                detalle.save()
                messages.success(request, "Producto añadido al pedido.")
                return redirect('ver_pedido', pk=pedido.id)
    else:
        form = DetallePedidoForm()

    return render(request, 'pedidos/pedidos/ver.html', {
        'pedido': pedido,
        'detalles': detalles,
        'total': total,
        'form': form
    })

@login_required
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Estado del pedido actualizado.")
            return redirect('listar_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/generic_form.html', {'form': form, 'titulo': 'Editar Pedido'})

@login_required
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    for detalle in pedido.detalles.all():
        detalle.producto.stock += detalle.cantidad
        detalle.producto.save()
    pedido.delete()
    messages.success(request, "Pedido eliminado.")
    return redirect('listar_pedidos')

@login_required
def eliminar_detalle(request, pk):
    detalle = get_object_or_404(DetallePedido, pk=pk)
    pedido_id = detalle.pedido.id
    detalle.producto.stock += detalle.cantidad
    detalle.producto.save()
    detalle.delete()
    messages.success(request, "Producto removido del pedido.")
    return redirect('ver_pedido', pk=pedido_id)


# =============================================================
# EXPORTACIONES (vistas web — sin cambios)
# =============================================================
@login_required
def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    p = canvas.Canvas(response)
    pedidos = Pedido.objects.all()
    y = 800
    p.drawString(100, y, "Reporte de Pedidos")
    y -= 30
    for pedido in pedidos:
        p.drawString(100, y, f"Pedido: #{pedido.id} | Cliente: {pedido.cliente.nombre} | Fecha: {pedido.fecha.strftime('%d/%m/%Y')} | Estado: {pedido.get_estado_display()}")
        y -= 20
    p.showPage()
    p.save()
    return response

@login_required
def exportar_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pedidos.xlsx"'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pedidos"
    ws.append(['ID', 'Cliente', 'Fecha', 'Estado'])
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        ws.append([pedido.id, pedido.cliente.nombre, pedido.fecha.strftime('%d/%m/%Y'), pedido.get_estado_display()])
    wb.save(response)
    return response


# =============================================================
# API CON JWT — Nuevas vistas para Postman
# =============================================================

# ── Login API → devuelve access + refresh token ──────────────
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # pública, no requiere token

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Usuario o contraseña incorrectos'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': user.username,
        })


# ── API Clientes — protegida con JWT ─────────────────────────
class ClienteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clientes = Cliente.objects.all().order_by('-id')
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    def put(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)
        try:
            cliente.delete()
            return Response({'mensaje': 'Cliente eliminado.'}, status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            return Response(
                {'error': 'No se puede eliminar, tiene pedidos asociados.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ── API Productos — protegida con JWT ────────────────────────
class ProductoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        productos = Producto.objects.all().order_by('-id')
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    def put(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return Response({'mensaje': 'Producto eliminado.'}, status=status.HTTP_204_NO_CONTENT)


# ── API Pedidos — protegida con JWT ──────────────────────────
class PedidoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pedidos = Pedido.objects.all().order_by('-id')
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    def put(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        serializer = PedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        for detalle in pedido.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
        pedido.delete()
        return Response({'mensaje': 'Pedido eliminado.'}, status=status.HTTP_204_NO_CONTENT)