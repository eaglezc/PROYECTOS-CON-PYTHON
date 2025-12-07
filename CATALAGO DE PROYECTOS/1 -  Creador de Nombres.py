print("Hola, nombraré tu cerveza con dos de tus respuestas.")

respuesta1 = input("Tiene buen sabor la cerveza: ")
respuesta2 = input("¿La cerveza es dulce?: ")

"# Tomamos, por ejemplo, las dos primeras letras de cada respuesta"
parte1 = respuesta1[:2].capitalize()
parte2 = respuesta2[:2].lower()

nombre = parte1 + parte2

print(f"\n{parte1} + {parte2} = {nombre}")
print(f"El nombre perfecto para tu cerveza es: \"La {nombre}\"")
