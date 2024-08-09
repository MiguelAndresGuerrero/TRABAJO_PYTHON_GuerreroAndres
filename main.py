import json
from datetime import datetime

# Conexión al archivo JSON general
def abrir_archivo():
    with open("info.json", "r") as openfile:
        return json.load(openfile)

def guardar_archivo(data):
    with open("info.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

# Guardar las ventas y compras en un archivo JSON separado
def guardar_transacciones(transacciones):
    with open("transacciones.json", "w") as outfile:
        json.dump(transacciones, outfile, indent=4)

def cargar_transacciones():
    try:
        with open("transacciones.json", "r") as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return []

# Inicializar el archivo de transacciones
transacciones = cargar_transacciones()

# Bienvenida al usuario
nombre_usuario = input("Bienvenido usuario, ¿Cómo te llamas? ")
print(f"Bienvenido Usuario {nombre_usuario}")

# Login de usuarios
print("¿Cómo quieres ingresar?")
print("""
        1. Cliente
        2. Vendedor
        3. Gerente
    """)
rango = int(input("¿Cuál es tu forma de acceso? "))

# Registro de ventas
def registrar_venta(data):
    fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Seleccionar paciente
    pacientes = data[4]["Productos"]

    for i, paciente in enumerate(pacientes):
        print(f"{i+1}. {paciente['nombre']}")
    paciente_id = int(input("Seleccione el ID del paciente: "))
    paciente = pacientes[paciente_id]
    
    # Seleccionar empleado
    empleados = data[4]["Productos"]
    
    for i, empleado in enumerate(empleados):
        print(f"{i+1}. {empleado['nombre']} - {empleado['cargo']}")
    empleado_id = int(input("Seleccione el ID del empleado: ")) - 1
    empleado = empleados[empleado_id]
    
    # Seleccionar medicamento
    medicamentos = data[0]["Productos"]

    for i, medicamento in enumerate(medicamentos):
        print(f"{i+1}. {medicamento['producto']} - Precio: {medicamento['precio']} - Stock: {medicamento['stock']}")
    medicamento_id = int(input("Seleccione el ID del medicamento: ")) - 1
    medicamento = medicamentos[medicamento_id]
    
    # Registrar la cantidad vendida
    cantidad = int(input("Ingrese la cantidad vendida: "))
    
    # Verificar si hay suficiente stock
    if cantidad > int(medicamento["stock"]):
        print("No hay suficiente stock.")
        return

    # Actualizar el stock
    medicamento["stock"] = str(int(medicamento["stock"]) - cantidad)
    
    # Registrar la venta
    venta = {
        "fecha": fecha_venta,
        "paciente": paciente,
        "empleado": empleado,
        "medicamento": {
            "nombre": medicamento["producto"],
            "cantidad": cantidad,
            "precio": medicamento["precio"]
        }
    }
    transacciones.append(venta)
    guardar_archivo(data)
    guardar_transacciones(transacciones)
    print(f"Venta registrada con éxito el {fecha_venta}")

# Registro de compras
def registrar_compra(data):
    fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Seleccionar proveedor
    proveedores = data[3]["Productos"]

    for i, proveedor in enumerate(proveedores):
        print(f"{i+1}. {proveedor['Nombre']}")
    proveedor_id = int(input("Seleccione el ID del proveedor: ")) - 1
    proveedor = proveedores[proveedor_id]
    
    # Seleccionar medicamento
    medicamentos = data[0]["Productos"]

    for i, medicamento in enumerate(medicamentos):
        print(f"{i+1}. {medicamento['producto']} - Precio de compra: {medicamento['precio']} - Stock: {medicamento['stock']}")
    medicamento_id = int(input("Seleccione el ID del medicamento: ")) - 1
    medicamento = medicamentos[medicamento_id]
    
    # Registrar la cantidad comprada
    cantidad = int(input("Ingrese la cantidad comprada: "))
    
    # Actualizar el stock
    medicamento["stock"] = str(int(medicamento["stock"]) + cantidad)
    
    # Registrar la compra
    compra = {
        "fecha": fecha_compra,
        "proveedor": proveedor,
        "medicamento": {
            "nombre": medicamento["producto"],
            "cantidad": cantidad,
            "precio_compra": medicamento["precio"]
        }
    }
    transacciones.append(compra)
    guardar_archivo(data)
    guardar_transacciones(transacciones)
    print(f"Compra registrada con éxito el {fecha_compra}")

# Menú de productos
def mostrar_productos(data):
    print("Productos en stock:")

    for producto in data[0]["Productos"]:
        print(f"{producto['id']}. {producto['producto']} - Precio: {producto['precio']} - Stock: {producto['stock']} - Expira: {producto['fecha de expiracion']}")

# Menú de cliente
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
            mostrar_productos(data)
                
        elif opcion == "2":
            registrar_venta(data)
                
        elif opcion == "3":
            print("Gracias por usar el programa")
            break

        else:
            print("Opción inválida")

# Menú de moderador
def menu_moderador(data):

    while True:
        print("............................")
        print("      MENU DEL MODERADOR     ")
        print("............................")
        print("1. Revisar productos")
        print("2. Modificar productos")
        print("3. Registrar compra")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            mostrar_productos(data)
                
        elif opcion == "2":
            modificar_producto(data) # type: ignore
                
        elif opcion == "3":
            registrar_compra(data)
                
        elif opcion == "4":
            print("Gracias por usar el programa")
            break
        
        else:
            print("Opción inválida")

# Menú del gerente y administrador
def menu_gerente(data):

    while True:
        print("-----------------------------")
        print("      MENU DE GERENTE        ")
        print("-----------------------------")
        print("1. Revisar productos")
        print("2. Registrar venta")
        print("3. Registrar compra")
        print("4. Ver registro de ventas y compras")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            mostrar_productos(data)
                
        elif opcion == "2":
            registrar_venta(data)
                
        elif opcion == "3":
            registrar_compra(data)
                
        elif opcion == "4":
            for transaccion in transacciones:
                print(transaccion)
                
        elif opcion == "5":
            print("Gracias por usar el programa")
            break
        
        else:
            print("Opción inválida")

# Cargar datos y seleccionar el menú según el rango del usuario
data = abrir_archivo()

if rango == 1:
    menu_cliente(data)

elif rango == 2:
    menu_moderador(data)

elif rango == 3:
    menu_gerente(data)

else:
    print("Opción de acceso inválida")

#Creado por Miguel Guerrero C.C 1090381839