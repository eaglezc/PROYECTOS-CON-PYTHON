import random

print("¡Bienvenido al juego de adivinar el número!")

nombre = input("¿Cuál es tu nombre? ")
print(f"Bueno, {nombre}, he pensado un número entre 1 y 100.")
print("Tienes solo 12 intentos para adivinar cuál es.")

numero_secreto = random.randint(1, 100)
intentos = 0
max_intentos = 12

while intentos < max_intentos:
    try:
        eleccion = int(input(f"\nIntento {intentos + 1}: Elige un número: "))
    except ValueError:
        print("Por favor, ingresa un número válido.")
        continue

    # Verificar si está fuera del rango
    if eleccion < 1 or eleccion > 100:
        print("Elegiste un número que no está permitido (debe ser entre 1 y 100).")
        continue

    intentos += 1

    # Comparación con el número secreto
    if eleccion < numero_secreto:
        print("Incorrecto. Elegiste un número menor al número secreto.")
    elif eleccion > numero_secreto:
        print("Incorrecto. Elegiste un número mayor al número secreto.")
    else:
        print(f"\n🎉 ¡Felicidades, {nombre}! ¡Has acertado el número secreto!")
        print(f"Te tomó {intentos} intento(s).")
        break
else:
    print("\n😢 Lo siento, se te han acabado los intentos.")
    print(f"El número secreto era: {numero_secreto}")

print("\nGracias por jugar. ¡Hasta la próxima!")
