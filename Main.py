import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


class MiNegocio(App):

    def build(self):

        # Carpeta segura para los datos de la aplicación
        self.carpeta_datos = self.user_data_dir
        self.archivo = os.path.join(
            self.carpeta_datos,
            "mi_negocio_v14.json"
        )

        self.root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        self.mostrar_menu()

        return self.root

    # ==================================================
    # UTILIDADES
    # ==================================================

    def limpiar(self):
        self.root.clear_widgets()

    def boton(self, texto, funcion):

        b = Button(
            text=texto,
            size_hint_y=None,
            height=55
        )

        b.bind(on_press=funcion)

        return b

    def etiqueta(self, texto, tamano=18, alto=50):

        return Label(
            text=texto,
            font_size=tamano,
            size_hint_y=None,
            height=alto
        )

    def cargar_datos(self):

        if not os.path.exists(self.archivo):
            return {
                "clientes": [],
                "movimientos": []
            }

        try:

            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if "clientes" not in datos:
                datos["clientes"] = []

            if "movimientos" not in datos:
                datos["movimientos"] = []

            return datos

        except Exception:

            return {
                "clientes": [],
                "movimientos": []
            }

    def guardar_datos(self, datos):

        try:

            os.makedirs(
                self.carpeta_datos,
                exist_ok=True
            )

            with open(
                self.archivo,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except Exception:

            return False

    def mostrar_mensaje(self, mensaje, funcion=None):

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                mensaje,
                23,
                100
            )
        )

        if funcion:

            self.root.add_widget(
                self.boton(
                    "CONTINUAR",
                    funcion
                )
            )

        self.root.add_widget(
            self.boton(
                "MENU PRINCIPAL",
                self.mostrar_menu
            )
        )

    # ==================================================
    # MENU PRINCIPAL
    # ==================================================

    def mostrar_menu(self, *args):

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "MI NEGOCIO V14",
                28,
                70
            )
        )

        self.root.add_widget(
            self.boton(
                "👥 CLIENTES",
                self.clientes
            )
        )

        self.root.add_widget(
            self.boton(
                "💰 INGRESOS",
                self.ingresos
            )
        )

        self.root.add_widget(
            self.boton(
                "💸 GASTOS",
                self.gastos
            )
        )

        self.root.add_widget(
            self.boton(
                "📋 HISTORIAL",
                self.historial
            )
        )

        self.root.add_widget(
            self.boton(
                "📊 RESUMEN",
                self.resumen
            )
        )

    # ==================================================
    # CLIENTES
    # ==================================================

    def clientes(self, *args):

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "CLIENTES",
                25,
                60
            )
        )

        self.nombre = TextInput(
            hint_text="Nombre del cliente",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.telefono = TextInput(
            hint_text="Teléfono",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.correo = TextInput(
            hint_text="Correo",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.root.add_widget(self.nombre)
        self.root.add_widget(self.telefono)
        self.root.add_widget(self.correo)

        self.root.add_widget(
            self.boton(
                "GUARDAR CLIENTE",
                self.guardar_cliente
            )
        )

        self.root.add_widget(
            self.boton(
                "VER CLIENTES",
                self.ver_clientes
            )
        )

        self.root.add_widget(
            self.boton(
                "VOLVER",
                self.mostrar_menu
            )
        )

    def guardar_cliente(self, *args):

        nombre = self.nombre.text.strip()
        telefono = self.telefono.text.strip()
        correo = self.correo.text.strip()

        if nombre == "":

            self.mostrar_mensaje(
                "Escribe el nombre del cliente",
                self.clientes
            )

            return

        datos = self.cargar_datos()

        nuevo = {
            "id": datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            ),
            "nombre": nombre,
            "telefono": telefono,
            "correo": correo
        }

        datos["clientes"].append(nuevo)

        if self.guardar_datos(datos):

            self.mostrar_mensaje(
                "CLIENTE GUARDADO",
                self.clientes
            )

        else:

            self.mostrar_mensaje(
                "No se pudo guardar el cliente",
                self.clientes
            )

    # ==================================================
    # VER CLIENTES
    # ==================================================

    def ver_clientes(self, *args):

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "MIS CLIENTES",
                25,
                60
            )
        )

        datos = self.cargar_datos()
        clientes = datos["clientes"]

        contenido = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=8,
            padding=5
        )

        contenido.bind(
            minimum_height=contenido.setter(
                "height"
            )
        )

        if not clientes:

            contenido.add_widget(
                self.etiqueta(
                    "No hay clientes.",
                    18,
                    60
                )
            )

        else:

            for indice, cliente in enumerate(clientes):

                texto = (
                    str(indice + 1)
                    + ". "
                    + cliente.get("nombre", "")
                    + "\nTel: "
                    + cliente.get("telefono", "")
                    + "\nCorreo: "
                    + cliente.get("correo", "")
                )

                contenido.add_widget(
                    self.etiqueta(
                        texto,
                        17,
                        95
                    )
                )

                contenido.add_widget(
                    self.boton(
                        "ABRIR FICHA",
                        lambda x, i=indice:
                        self.ficha_cliente(i)
                    )
                )

                contenido.add_widget(
                    self.boton(
                        "EDITAR",
                        lambda x, i=indice:
                        self.editar_cliente(i)
                    )
                )

                contenido.add_widget(
                    self.boton(
                        "ELIMINAR",
                        lambda x, i=indice:
                        self.eliminar_cliente(i)
                    )
                )

        scroll = ScrollView()

        scroll.add_widget(contenido)

        self.root.add_widget(scroll)

        self.root.add_widget(
            self.boton(
                "VOLVER A CLIENTES",
                self.clientes
            )
        )

        self.root.add_widget(
            self.boton(
                "MENU",
                self.mostrar_menu
            )
        )

    # ==================================================
    # FICHA DEL CLIENTE
    # ==================================================

    def ficha_cliente(self, indice):

        datos = self.cargar_datos()
        clientes = datos["clientes"]

        if indice < 0 or indice >= len(clientes):
            return

        cliente = clientes[indice]

        nombre = cliente.get(
            "nombre",
            ""
        )

        telefono = cliente.get(
            "telefono",
            ""
        )

        correo = cliente.get(
            "correo",
            ""
        )

        movimientos = []

        for movimiento in datos["movimientos"]:

            if movimiento.get(
                "cliente",
                ""
            ) == nombre:

                movimientos.append(movimiento)

        ingresos = 0
        gastos = 0

        for movimiento in movimientos:

            try:

                valor = float(
                    movimiento.get(
                        "valor",
                        0
                    )
                )

            except Exception:

                valor = 0

            if movimiento.get(
                "tipo"
            ) == "ingreso":

                ingresos += valor

            elif movimiento.get(
                "tipo"
            ) == "gasto":

                gastos += valor

        ganancia = ingresos - gastos

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "FICHA DEL CLIENTE",
                25,
                60
            )
        )

        contenido = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=8,
            padding=5
        )

        contenido.bind(
            minimum_height=contenido.setter(
                "height"
            )
        )

        contenido.add_widget(
            self.etiqueta(
                "CLIENTE\n" + nombre,
                20,
                80
            )
        )

        contenido.add_widget(
            self.etiqueta(
                "TELÉFONO\n" + telefono,
                18,
                70
            )
        )

        contenido.add_widget(
            self.etiqueta(
                "CORREO\n" + correo,
                18,
                70
            )
        )

        contenido.add_widget(
            self.etiqueta(
                "INGRESOS: $"
                + self.numero(ingresos)
                + "\n"
                "GASTOS: $"
                + self.numero(gastos)
                + "\n"
                "GANANCIA: $"
                + self.numero(ganancia),
                20,
                130
            )
        )

        contenido.add_widget(
            self.etiqueta(
                "MOVIMIENTOS",
                22,
                60
            )
        )

        if not movimientos:

            contenido.add_widget(
                self.etiqueta(
                    "No hay movimientos.",
                    18,
                    60
                )
            )

        else:

            for movimiento in movimientos:

                texto = (
                    movimiento.get(
                        "tipo",
                        ""
                    ).upper()
                    + "\n"
                    + movimiento.get(
                        "concepto",
                        ""
                    )
                    + "\nValor: $"
                    + self.numero(
                        movimiento.get(
                            "valor",
                            0
                        )
                    )
                    + "\nFecha: "
                    + movimiento.get(
                        "fecha",
                        ""
                    )
                )

                contenido.add_widget(
                    self.etiqueta(
                        texto,
                        17,
                        105
                    )
                )

        scroll = ScrollView()

        scroll.add_widget(contenido)

        self.root.add_widget(scroll)

        self.root.add_widget(
            self.boton(
                "EDITAR CLIENTE",
                lambda x:
                self.editar_cliente(indice)
            )
        )

        self.root.add_widget(
            self.boton(
                "VOLVER",
                self.ver_clientes
            )
        )

        self.root.add_widget(
            self.boton(
                "MENU",
                self.mostrar_menu
            )
        )

    # ==================================================
    # EDITAR CLIENTE
    # ==================================================

    def editar_cliente(self, indice):

        datos = self.cargar_datos()
        clientes = datos["clientes"]

        if indice < 0 or indice >= len(clientes):
            return

        cliente = clientes[indice]

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "EDITAR CLIENTE",
                25,
                60
            )
        )

        self.editar_nombre = TextInput(
            text=cliente.get(
                "nombre",
                ""
            ),
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.editar_telefono = TextInput(
            text=cliente.get(
                "telefono",
                ""
            ),
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.editar_correo = TextInput(
            text=cliente.get(
                "correo",
                ""
            ),
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.root.add_widget(
            self.editar_nombre
        )

        self.root.add_widget(
            self.editar_telefono
        )

        self.root.add_widget(
            self.editar_correo
        )

        self.root.add_widget(
            self.boton(
                "GUARDAR CAMBIOS",
                lambda x:
                self.guardar_cambios(indice)
            )
        )

        self.root.add_widget(
            self.boton(
                "CANCELAR",
                lambda x:
                self.ficha_cliente(indice)
            )
        )

    def guardar_cambios(self, indice):

        datos = self.cargar_datos()

        if indice < 0 or indice >= len(
            datos["clientes"]
        ):
            return

        nuevo_nombre = (
            self.editar_nombre.text.strip()
        )

        if nuevo_nombre == "":

            self.mostrar_mensaje(
                "El nombre no puede estar vacío",
                lambda x=None:
                self.editar_cliente(indice)
            )

            return

        nombre_anterior = datos[
            "clientes"
        ][indice].get(
            "nombre",
            ""
        )

        datos["clientes"][indice][
            "nombre"
        ] = nuevo_nombre

        datos["clientes"][indice][
            "telefono"
        ] = self.editar_telefono.text.strip()

        datos["clientes"][indice][
            "correo"
        ] = self.editar_correo.text.strip()

        # Actualizar el nombre del cliente
        # en sus movimientos
        for movimiento in datos[
            "movimientos"
        ]:

            if movimiento.get(
                "cliente",
                ""
            ) == nombre_anterior:

                movimiento[
                    "cliente"
                ] = nuevo_nombre

        self.guardar_datos(datos)

        self.mostrar_mensaje(
            "CAMBIOS GUARDADOS",
            lambda x=None:
            self.ficha_cliente(indice)
        )

    def eliminar_cliente(self, indice):

        datos = self.cargar_datos()
        clientes = datos["clientes"]

        if indice < 0 or indice >= len(clientes):
            return

        nombre = clientes[indice].get(
            "nombre",
            ""
        )

        datos["clientes"].pop(indice)

        # También eliminamos los movimientos
        # asociados al cliente
        datos["movimientos"] = [
            movimiento
            for movimiento in datos[
                "movimientos"
            ]
            if movimiento.get(
                "cliente",
                ""
            ) != nombre
        ]

        self.guardar_datos(datos)

        self.mostrar_mensaje(
            "CLIENTE ELIMINADO\n" + nombre,
            self.ver_clientes
        )

    # ==================================================
    # INGRESOS
    # ==================================================

    def ingresos(self, *args):

        self.limpiar()

        self.root.add_widget(
            self.etiqueta(
                "REGISTRAR INGRESO",
                25,
                60
            )
        )

        datos = self.cargar_datos()
        clientes = datos["clientes"]

        if not clientes:

            self.root.add_widget(
                self.etiqueta(
                    "Primero crea un cliente.",
                    18,
                    70
                )
            )

            self.root.add_widget(
                self.boton(
                    "IR A CLIENTES",
                    self.clientes
                )
            )

            self.root.add_widget(
                self.boton(
                    "MENU",
                    self.mostrar_menu
                )
            )

            return

        nombres = [
            cliente.get(
                "nombre",
                ""
            )
            for cliente in clientes
        ]

        self.cliente_ingreso = Spinner(
            text="SELECCIONA CLIENTE",
            values=nombres,
            size_hint_y=None,
            height=55
        )

        self.servicio_ingreso = TextInput(
            hint_text="Servicio realizado",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.precio_ingreso = TextInput(
            hint_text="Precio",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50
        )

        self.root.add_widget(
            self.cliente_ingreso
        )

        self.root.add_widget(
            self.servicio_ingreso
        )

        self.root.add_widget(
            self.precio_ingreso
        )

        self.root.add_widget(
            self.boton(
                "GUARDAR INGRESO",
                self.guardar_ingreso
            )
        )

        self.root.add_widget(
            self.boton(
                "VER INGRESOS",
                self.ver_ingresos
            )
        )

        self.root.add_widget(
            self.boton(
                "MENU",
                self.mostrar_men
