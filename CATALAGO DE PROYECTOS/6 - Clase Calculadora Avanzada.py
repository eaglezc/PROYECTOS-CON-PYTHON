# CLASES ---------------------------------------

class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido


class Cliente(Persona):
    def __init__(self, nombre, apellido, numero_cuenta, balance=0):
        super().__init__(nombre, apellido)  # Heredamos nombre y apellido
        self.numero_cuenta = numero_cuenta
        self.balance = balance

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}\n" \
               f"Número de cuenta: {self.numero_cuenta}\n" \
               f"Balance: Q{self.balance:.2f}"

    def depositar(self, monto):
        self.balance += monto
        print(f"Has depositado Q{monto:.2f}. Nuevo balance: Q{self.balance:.2f}\n")

    def retirar(self, monto):
        if monto > self.balance:
            print("No tienes suficiente dinero para retirar esa cantidad.\n")
        else:
            self.balance -= monto
            print(f"Has retirado Q{monto:.2f}. Nuevo balance: Q{self.balance:.2f}\n")


# FUNCIONES ---------------------------------------

def crear_cliente():
    print("Bienvenido. Vamos a crear tu cuenta bancaria.\n")
    nombre = input("Ingresa tu nombre: ")
    apellido = input("Ingresa tu apellido: ")
    numero_cuenta = input("Ingresa tu número de cuenta: ")
    cliente = Cliente(nombre, apellido, numero_cuenta)
    print("\nCuenta creada exitosamente:\n")
    print(cliente)
    print("\n")
    return cliente


def inicio():
    cliente = crear_cliente()

    while True:
        print("¿Qué deseas hacer?")
        print("1. Depositar dinero")
        print("2. Retirar dinero")
        print("3. Mostrar balance")
        print("4. Salir")
        opcion = input("Ingresa el número de la opción: ")

        if opcion == "1":
            monto = float(input("Ingresa el monto a depositar: "))
            cliente.depositar(monto)
        elif opcion == "2":
            monto = float(input("Ingresa el monto a retirar: "))
            cliente.retirar(monto)
        elif opcion == "3":
            print(cliente, "\n")
        elif opcion == "4":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta nuevamente.\n")


# INICIO DEL PROGRAMA --------------------------------
inicio()
