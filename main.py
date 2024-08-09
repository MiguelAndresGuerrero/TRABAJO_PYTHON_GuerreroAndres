import json
from datetime import datetime

# Conexion del Json general
def abrirArchivo():
    with open("info.json", "r") as openfile:
        return json.load(openfile)

def guardarArchivo(data):
    with open("info.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

# Json que se genera después de realizar una compra
def guardarCompras(compras):
    with open("compras.json", "w") as outfile:
        json.dump(compras, outfile, indent=4)

def cargarCompras():
    try:
        with open("compras.json", "r") as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return []

compras = cargarCompras()

# Bienvenida al usuario
Name = input("Bienvenido usuario, ¿Cómo te llamas? ")
print(f"Bienvenido Usuario {Name}")

# Login de 4 tipos de usuarios
print("¿Cómo quieres ingresar?")
print("""
        1. Cliente
        2. Vendedor
        3. Gerente
        4. Administrador
    """)
Rango = int(input("¿Cuál es tu forma de acceso? "))

# Guardamos la fecha y hora cuando se haga la venta de los medicamentos empleados y pacientes
def registrar_venta(paciente, empleado, medicamentos):
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    venta = {
        "fecha": fecha_venta,
        "paciente": paciente,
        "empleado": empleado,
        "medicamentos": medicamentos
    }
    compras.append(venta)
    guardarCompras(compras)
    print(f"Venta registrada con éxito el {fecha_venta}")

# Guardamos la fecha y hora cuando se haga la compra del provedor y medicamentos
def registrar_compra(proveedor, medicamentos):
    fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    compra = {
        "fecha": fecha_compra,
        "proveedor": proveedor,
        "medicamentos": medicamentos
    }
    compras.append(compra)
    guardarCompras(compras)
    print(f"Compra registrada con éxito el {fecha_compra}")

# Menú de los productos
def productos(grupo):
    print("Tienda:", grupo["Tienda"])
    for producto in grupo["Productos"]:
        print("/////////////////////////////////////")
        print("ID del producto:", producto["id"])
        print("Nombre:", producto["producto"])
        print("Precio:", producto["precio"])
        print("/////////////////////////////////////")

# Menú de modificación del producto
def modificar_producto(grupo):
    try:
        productos_id = int(input("Ingrese el ID del producto que desea modificar: "))
    
    except:
        print("Opción no válida")
        return
    
    for producto in grupo["Productos"]:
        if producto["id"] == productos_id:
            opcion = int(input("""
                ¿Qué desea modificar del producto?
                1. Nombre del producto
                2. Precio del producto
                """))
            if opcion == 1:
                producto["producto"] = input("Nuevo nombre del producto: ")
            elif opcion == 2:
                producto["precio"] = input("Nuevo precio del producto: ")
            elif opcion == 0:
                print("Opción inválida.")
                return
            guardarArchivo(data)
            print("Cambio realizado.")
            return
    print("No se encontró ningún producto con ese ID")

def comprar_producto(data):
    print("Lista de tiendas:")
    for i, grupo in enumerate(data):
        print(f"{i+1}. {grupo['Tienda']}")
    tienda_id = int(input("Seleccione el ID de la tienda donde desea comprar: ")) - 1
    if 0 <= tienda_id < len(data):
        tienda = data[tienda_id]
        productos(tienda)
        producto_id = int(input("Ingrese el ID del producto que desea comprar: "))
        for producto in tienda["Productos"]:
            if producto["id"] == producto_id:
                paciente = {
                    "nombre": input("Nombre del paciente: "),
                    "direccion": input("Dirección del paciente: ")
                }
                empleado = {
                    "nombre": input("Nombre del empleado que realiza la venta: "),
                    "cargo": input("Cargo del empleado: ")
                }
                medicamentos = [{
                    "nombre": producto["producto"],
                    "cantidad": int(input("Cantidad: ")),
                    "precio": producto["precio"]
                }]
                registrar_venta(paciente, empleado, medicamentos)
                return
        print("No se encontró ningún producto con ese ID.")
    else:
        print("ID de tienda inválido.")

# Menú de interacción con el cliente
def menu_cliente(data):
    while True:
        print("****************************")
        print("      MENU DEL CLIENTE      ")
        print("****************************")
        print("1. Revisar productos")
        print("2. Comprar producto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            for grupo in data:
                productos(grupo)
                
        elif opcion == "2":
            comprar_producto(data)
                
        elif opcion == "3":
            print("Gracias por usar el programa")
            break
        else:
            print("Opción inválida.")
    
# Menú del moderador
def menu_moderador(data):
    while True:
        print("............................")
        print("      MENU DEL MODERADOR     ")
        print("............................")
        print("1. Revisar productos")
        print("2. Modificar productos")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            for grupo in data:
                productos(grupo)
                
        elif opcion == "2":
            for grupo in data:
                print(f"Tienda: {grupo['Tienda']}")
                modificar_producto(grupo)
                
        elif opcion == "3":
            print("Gracias por usar el programa")
            break
        
        else:
            print("Opción inválida.")

# Informe de ventas
def generar_informe():
    total_ingresos = 0
    print("============================")
    print("     INFORME DE VENTAS      ")
    print("============================")
    for compra in compras:
        if "paciente" in compra:
            print(f"Fecha: {compra['fecha']}")
            print(f"Paciente: {compra['paciente']['nombre']}, Dirección: {compra['paciente']['direccion']}")
            print(f"Empleado: {compra['empleado']['nombre']}, Cargo: {compra['empleado']['cargo']}")
            for medicamento in compra['medicamentos']:
                print(f"Medicamento: {medicamento['nombre']}, Cantidad: {medicamento['cantidad']}, Precio: {medicamento['precio']}")
                precio_numerico = int(medicamento['precio'].split()[0])
                total_ingresos += precio_numerico * medicamento['cantidad']
        elif "proveedor" in compra:
            print(f"Fecha: {compra['fecha']}")
            print(f"Proveedor: {compra['proveedor']['nombre']}, Contacto: {compra['proveedor']['contacto']}")
            for medicamento in compra['medicamentos']:
                print(f"Medicamento: {medicamento['nombre']}, Cantidad: {medicamento['cantidad']}, Precio de compra: {medicamento['precio']}")
    print("============================")
    print(f"Total de ingresos: {total_ingresos} COP")
    print("============================")

# Menú del propietario
def menu_propietario(data):
    while True:
        print("-----------------------------")
        print("      MENU DE PROPIETARIO    ")
        print("-----------------------------")
        print("1. Revisar productos")
        print("2. Modificar productos")
        print("3. Ver registro de ventas")
        print("4. Generar informe de ventas")
        print("5. Registrar compra")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            for grupo in data:
                productos(grupo)
                
        elif opcion == "2":
            for grupo in data:
                print(f"Tienda: {grupo['Tienda']}")
                modificar_producto(grupo)
                
        elif opcion == "3":
            print("Registro de ventas:")
            for compra in compras:
                if "paciente" in compra:
                    print(f"Producto: {compra['medicamentos'][0]['nombre']}, Precio: {compra['medicamentos'][0]['precio']}, Fecha: {compra['fecha']}")
                
        elif opcion == "4":
            generar_informe()
                
        elif opcion == "5":
            proveedor = {
                "nombre": input("Nombre del proveedor: "),
                "contacto": input("Contacto del proveedor: ")
            }
            medicamentos = []
            while True:
                medicamento = {
                    "nombre": input("Nombre del medicamento: "),
                    "cantidad": int(input("Cantidad: ")),
                    "precio": input("Precio de compra: ")
                }
                medicamentos.append(medicamento)
                continuar = input("¿Desea agregar otro medicamento? (s/n): ")
                if continuar.lower() != "s":
                    break
            registrar_compra(proveedor, medicamentos)
                
        elif opcion == "6":
            print("Gracias por usar el programa")
            break
        
        else:
            print("Opción inválida.")

data = abrirArchivo()

if Rango == 1:
    menu_cliente(data)
elif Rango == 2:
    menu_moderador(data)
elif Rango == 3:
    menu_propietario(data)
else:
    print("Opción de acceso inválida")

#Creado por Miguel Guerrero C.C 1090381839