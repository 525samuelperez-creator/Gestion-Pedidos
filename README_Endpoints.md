# Documentación de Endpoints - Gestión de Pedidos MySQL

Este documento describe las URLs (endpoints) disponibles en la aplicación. El sistema está dividido en dos partes: **Endpoints API (JSON)** para comunicación por máquina/Postman, y **Vistas Clásicas (HTML)** que es la interfaz web.

## 🔑 Endpoints de Autenticación API JWT (Formato JSON)
Estas rutas NO devuelven HTML. Están diseñadas para consumirse mediante aplicaciones externas como Postman, Insomnia o frontends separados en JavaScript/React.

| Método | Ruta Endpoint | Descripción | Body Requerido (JSON) |
|---|---|---|---|
| `POST` | `/api/token/` | Autentica al usuario y genera tokens (Access + Refresh). | `{"username": "...", "password": "..."}` |
| `POST` | `/api/token/refresh/`| Genera un nuevo Access Token enviando el Refresh Token anterior. | `{"refresh": "..."}` |

---

## 🌐 Interfaz Web y Vistas Clásicas (Formato HTML)
Estas rutas conforman el sistema visual que opera el usuario desde su navegador de internet.
Todas las rutas de los módulos requieren que haya una sesión iniciada por el usuario (están protegidas).

### 🏠 Inicio y Cuentas
| Método | Ruta | Descripción |
|---|---|---|
| `GET`/`POST` | `/accounts/login/` | Formulario web para Iniciar Sesión. |
| `GET`/`POST` | `/pedidos/registro/` | Formulario web para registrar una cuenta nueva. |
| `GET` | `/` | Ruta base, redirecciona automáticamente a `/pedidos/`. |
| `GET` | `/pedidos/` | **[Protegido]** Vista del Panel Central o Inicio. |

### 🧑‍💼 Módulo: Clientes
| Método | Ruta | Descripción |
|---|---|---|
| `GET`  | `/pedidos/clientes/` | **[Protegido]** Listado paginado de clientes. |
| `GET`/`POST` | `/pedidos/clientes/crear/` | **[Protegido]** Vista de creación de nuevo cliente. |
| `GET`/`POST` | `/pedidos/clientes/editar/<id>/` | **[Protegido]** Actualizar la información de un cliente. |
| `POST` | `/pedidos/clientes/eliminar/<id>/` | **[Protegido]** Borrar un cliente (si no tiene pedidos asignados). |

### 📦 Módulo: Productos
| Método | Ruta | Descripción |
|---|---|---|
| `GET`  | `/pedidos/productos/` | **[Protegido]** Listado e inventario de productos. |
| `GET`/`POST` | `/pedidos/productos/crear/` | **[Protegido]** Crear producto (valida que no haya stock negativo). |
| `GET`/`POST` | `/pedidos/productos/editar/<id>/` | **[Protegido]** Editar datos y precio de un producto. |
| `POST` | `/pedidos/productos/eliminar/<id>/`| **[Protegido]** Quitar un producto de la base de datos. |

### 🛒 Módulo: Pedidos
| Método | Ruta | Descripción |
|---|---|---|
| `GET`  | `/pedidos/pedidos/` | **[Protegido]** Ver el historial completo de pedidos. |
| `GET`/`POST` | `/pedidos/pedidos/crear/` | **[Protegido]** Iniciar un pedido nuevo asignando un cliente y situación. |
| `GET`/`POST` | `/pedidos/pedidos/ver/<id>/` | **[Protegido]** Detalle a fondo del pedido. Aquí también se usa el formulario para **agregar productos al pedido**. |
| `GET`/`POST` | `/pedidos/pedidos/editar/<id>/` | **[Protegido]** Cambiar el estatus u otros datos base del pedido. |
| `POST` | `/pedidos/pedidos/eliminar/<id>/`| **[Protegido]** Eliminar el pedido entero (Restaura todo el stock descontado). |
| `POST` | `/pedidos/pedidos/detalles/eliminar/<id_detalle>/`| **[Protegido]** (Detalle de Pedido) Quita un producto único de un pedido y le repone el respectivo stock. |

### 📄 Exportaciones y Reportes
| Método | Ruta | Descripción |
|---|---|---|
| `GET`  | `/pedidos/exportar/pdf/`| **[Protegido]** Descarga dinámica de todos los pedidos en un formato de documento **PDF** estructurado. |
| `GET`  | `/pedidos/exportar/excel/`| **[Protegido]** Descarga un archivo formato de Excel **(.xlsx)** conteniendo el identificador, cliente y estado. |
