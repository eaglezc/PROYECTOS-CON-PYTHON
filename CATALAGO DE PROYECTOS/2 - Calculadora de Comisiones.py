"Programa para calcular comisiones del 13%"

"Pedimos datos al usuario"
nombre = input("¿Cuál es tu nombre? ")
ventas_str = input("¿Cuánto has vendido este mes? ")

"Convertimos el ingreso de ventas a float"
ventas = float(ventas_str)

"Calculamos la comisión (13%)"
comision = ventas * 13 / 100

"Redondeamos a 2 decimales"
comision = round(comision, 2)

"Mostramos el resultado con formato"
print(f"{nombre}, tu comisión por tus ventas este mes es de Q. {comision}.")