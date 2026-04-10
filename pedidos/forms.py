from django import forms
from .models import Cliente, Producto, Pedido, DetallePedido

class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ClienteForm(BootstrapForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoForm(BootstrapForm):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoForm(BootstrapForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'estado'] # fecha es auto_now_add

class DetallePedidoForm(BootstrapForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']