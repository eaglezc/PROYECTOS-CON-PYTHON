import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from collections import Counter

# Lista global para almacenar los números ingresados
numeros_ingresados = []

# ------------------------------
# Funciones principales
# ------------------------------
def clasificar_numeros(event=None):
    """Clasifica los números que se ingresan en el Entry."""
    global numeros_ingresados
    entrada = entry_numeros.get()
    if not entrada.strip():
        messagebox.showwarning("Aviso", "Ingrese uno o más números separados por comas")
        return

    numeros = entrada.split(",")
    for num_str in numeros:
        num_str = num_str.strip()
        if not num_str:
            continue
        try:
            numero = float(num_str.replace(",", ""))  # Soporta miles y decimales
            numeros_ingresados.append(numero)
        except ValueError:
            messagebox.showerror("Error", f"Número inválido: {num_str}")
            return

    actualizar_resumen()
    entry_numeros.delete(0, tk.END)


def actualizar_resumen():
    """Muestra los números ordenados en columnas con su total al final."""
    resumen_text.delete("1.0", tk.END)

    if not numeros_ingresados:
        return

    contador = Counter(numeros_ingresados)
    numeros_ordenados = sorted(contador.keys(), key=float)

    # Listas repetidas por columna
    columnas = {num: [num] * contador[num] for num in numeros_ordenados}
    max_altura = max(len(col) for col in columnas.values())

    # Escribir filas
    for i in range(max_altura):
        fila = ""
        for num in numeros_ordenados:
            if i < len(columnas[num]):
                fila += f"{str(columnas[num][i]):<12}"
            else:
                fila += f"{'':<12}"
        resumen_text.insert(tk.END, fila + "\n")

    # Línea divisoria
    linea = "".join(["-" * 12 for _ in numeros_ordenados])
    resumen_text.insert(tk.END, linea + "\n")

    # Totales
    totales = ""
    for num in numeros_ordenados:
        totales += f"Total:{contador[num]:<6}"
    resumen_text.insert(tk.END, totales + "\n")


def guardar_csv():
    """Guarda el resumen en formato vertical:
       Número | Cantidad (Opción B)"""
    if not numeros_ingresados:
        messagebox.showwarning("Aviso", "No hay números para guardar")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
        title="Guardar resumen como CSV"
    )
    if not archivo:
        return

    contador = Counter(numeros_ingresados)

    # Crear DataFrame ordenado
    df = pd.DataFrame({
        "Número": sorted(contador.keys()),
        "Cantidad": [contador[n] for n in sorted(contador.keys())]
    })

    # Guardar con BOM para Excel
    df.to_csv(archivo, index=False, encoding="utf-8-sig")

    messagebox.showinfo("Éxito", f"Resumen guardado en:\n{archivo}")


def reiniciar():
    """Reinicia todos los datos."""
    global numeros_ingresados
    if messagebox.askyesno("Confirmar", "¿Desea reiniciar todos los números ingresados?"):
        numeros_ingresados = []
        resumen_text.delete("1.0", tk.END)
        entry_numeros.delete(0, tk.END)


# ------------------------------
# Interfaz gráfica
# ------------------------------
ventana = tk.Tk()
ventana.title("Clasificador de Números")
ventana.geometry("700x450")
ventana.configure(bg="white")

# Entrada de números
tk.Label(ventana, text="Ingrese números separados por coma:", bg="white", fg="black").pack(pady=5)
entry_numeros = tk.Entry(ventana, width=60, bg="white", fg="black")
entry_numeros.pack(pady=5)

# ENTER para clasificar
entry_numeros.bind("<Return>", clasificar_numeros)

# Botones
frame_botones = tk.Frame(ventana, bg="white")
frame_botones.pack(pady=10)

btn_clasificar = tk.Button(frame_botones, text="Clasificar", command=clasificar_numeros, bg="#00BFFF", fg="black", width=15)
btn_guardar = tk.Button(frame_botones, text="Guardar CSV", command=guardar_csv, bg="#00FF00", fg="black", width=15)
btn_reiniciar = tk.Button(frame_botones, text="Reiniciar", command=reiniciar, bg="#FF0000", fg="black", width=15)

btn_clasificar.pack(side="left", padx=5)
btn_guardar.pack(side="left", padx=5)
btn_reiniciar.pack(side="left", padx=5)

# Hacer widgets accesibles con TAB
for widget in [entry_numeros, btn_clasificar, btn_guardar, btn_reiniciar]:
    widget.configure(takefocus=True)

# Zona de resumen
resumen_text = tk.Text(ventana, height=15, bg="white", fg="black", insertbackground="black")
resumen_text.pack(fill="both", expand=True, padx=10, pady=10)

ventana.mainloop()
