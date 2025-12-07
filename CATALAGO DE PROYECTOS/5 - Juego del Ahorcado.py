import random

# Lista de palabras
palabras = ["python", "programa", "ahorcado", "computadora", "desafío",
            "variable", "funcion", "algoritmo", "desarrollador"]

# Dibujos del ahorcado (7 estados)
ahorcado_visual = [
    r"""
       _______
      |      |
      |      O
      |     \|/
      |      |
      |     / \
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |      O
      |     \|/
      |      |
      |     /
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |      O
      |     \|/
      |      |
      |
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |      O
      |     \|
      |      |
      |
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |      O
      |      |
      |      |
      |
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |      O
      |
      |
      |
     _|_
    |   |______
    |          |
    """,
    r"""
       _______
      |      |
      |
      |
      |
      |
     _|_
    |   |______
    |          |
    """
]

# FUNCIONES ---------------------------------------

def elegir_palabra(lista):
    return random.choice(lista)

def mostrar_palabra(palabra, letras_adivinadas):
    resultado = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            resultado += letra + " "
        else:
            resultado += "_ "
    return resultado.strip()

def letra_valida(letra):
    return len(letra) == 1 and letra.isalpha()

def ha_ganado(palabra, letras_adivinadas):
    for letra in palabra:
        if letra not in letras_adivinadas:
            return False
    return True

def jugar_ahorcado():
    palabra_secreta = elegir_palabra(palabras)
    letras_adivinadas = []
    letras_incorrectas = []
    vidas = 6

    print("\n¡Bienvenido al Ahorcado!\n")

    while vidas > 0:
        # Mostrar dibujo según las vidas
        print(ahorcado_visual[6 - vidas])
        # Mostrar palabra con letras correctas
        print("Palabra: ", mostrar_palabra(palabra_secreta, letras_adivinadas))
        # Mostrar letras incorrectas
        if letras_incorrectas:
            print("Letras incorrectas:", ", ".join(letras_incorrectas))
        print(f"Vidas restantes: {vidas}")
        letra = input("Elige una letra: ").lower()

        if not letra_valida(letra):
            print("Ingresa solo una letra válida.\n")
            continue

        if letra in letras_adivinadas or letra in letras_incorrectas:
            print("Ya elegiste esa letra.\n")
            continue

        if letra in palabra_secreta:
            letras_adivinadas.append(letra)
            print("¡Bien! La letra está en la palabra.\n")
        else:
            vidas -= 1
            letras_incorrectas.append(letra)
            print("Letra incorrecta. Has perdido una vida.\n")

        if ha_ganado(palabra_secreta, letras_adivinadas):
            print(f"\n¡Felicidades! Has adivinado la palabra: {palabra_secreta}\n")
            break
    else:
        print(ahorcado_visual[-1])
        print("Palabra: ", mostrar_palabra(palabra_secreta, letras_adivinadas))
        print(f"\n¡Se te acabaron las vidas! La palabra era: {palabra_secreta}\n")

# Bucle para jugar varias partidas sin reiniciar el programa
while True:
    jugar_ahorcado()
    jugar_otra = input("¿Quieres jugar otra vez? (s/n): ").lower()
    if jugar_otra != "s":
        print("\nGracias por jugar. ¡Hasta luego!")
        break
