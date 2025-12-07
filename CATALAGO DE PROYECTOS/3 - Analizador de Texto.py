# ============================
#    ANALIZADOR DE TEXTO
# ============================

# 1. Ingreso del texto
texto = input("Ingrese un texto: ").lower()

# 2. Ingreso de 3 letras
print("Ahora ingrese 3 letras (una por una):")
letras = []
for i in range(3):
    letra = input(f"Letra {i+1}: ").lower()
    letras.append(letra)

# ======================================
# ANÁLISIS 1: contar apariciones
# ======================================
print("\n--- RESULTADOS DEL ANÁLISIS ---\n")

for letra in letras:
    cantidad = texto.count(letra)
    print(f"La letra '{letra}' aparece {cantidad} veces en el texto.")

# ======================================
# ANÁLISIS 2: cantidad de palabras
# ======================================
palabras = texto.split()
cantidad_palabras = len(palabras)
print(f"\nCantidad total de palabras: {cantidad_palabras}")

# ======================================
# ANÁLISIS 3: primera y última letra
# ======================================
primera_letra = texto[0]
ultima_letra = texto[-1]
print(f"\nPrimera letra del texto: '{primera_letra}'")
print(f"Última letra del texto: '{ultima_letra}'")

# ======================================
# ANÁLISIS 4: texto invertido palabra por palabra
# ======================================
palabras_invertidas = palabras[::-1]
texto_invertido = " ".join(palabras_invertidas)
print(f"\nTexto con palabras en orden inverso:\n{texto_invertido}")

# ======================================
# ANÁLISIS 5: buscar la palabra "python"
# ======================================
existe_python = "python" in texto
respuesta = {True: "Sí, la palabra 'Python' está en el texto.",
             False: "No, la palabra 'Python' no aparece en el texto."}

print(f"\n¿Aparece la palabra 'Python'?: {respuesta[existe_python]}")
