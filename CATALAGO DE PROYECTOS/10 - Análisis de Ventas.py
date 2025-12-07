import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import shutil
import textwrap

# -------------------------------
# Carpeta para almacenar CSVs
# -------------------------------
CARPETA_CSV = "csv_guardados"
if not os.path.exists(CARPETA_CSV):
    os.makedirs(CARPETA_CSV)

# -------------------------------
# Variables globales
# -------------------------------
df = pd.DataFrame()
archivo_actual = None  # CSV abierto actualmente

# -------------------------------
# Funciones principales
# -------------------------------
def cargar_csv_externo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        try:
            # Guardar copia en carpeta del proyecto
            nombre_base = os.path.basename(archivo)
            contador = 1
            nuevo_nombre = nombre_base
            while os.path.exists(os.path.join(CARPETA_CSV, nuevo_nombre)):
                nuevo_nombre = f"{os.path.splitext(nombre_base)[0]}_{contador}.csv"
                contador += 1
            destino = os.path.join(CARPETA_CSV, nuevo_nombre)
            shutil.copy2(archivo, destino)
            messagebox.showinfo("Éxito", f"Archivo copiado en proyecto:\n{destino}")
            actualizar_lista_csv()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar el archivo:\n{e}")

def actualizar_lista_csv():
    lista_csv.delete(0, tk.END)
    for archivo in os.listdir(CARPETA_CSV):
        if archivo.endswith(".csv"):
            lista_csv.insert(tk.END, archivo)

def abrir_csv_guardado():
    global df, archivo_actual
    seleccionado = lista_csv.curselection()
    if not seleccionado:
        messagebox.showwarning("Aviso", "Seleccione un CSV de la lista")
        return
    archivo = lista_csv.get(seleccionado[0])
    ruta = os.path.join(CARPETA_CSV, archivo)
    try:
        df_temp = pd.read_csv(ruta, sep=",", on_bad_lines='skip')
        lineas_totales = sum(1 for _ in open(ruta)) - 1
        lineas_cargadas = len(df_temp)
        lineas_omitidas = lineas_totales - lineas_cargadas

        df = df_temp
        archivo_actual = ruta
        actualizar_tabla()
        actualizar_grafico()
        resumen_text.delete("1.0", tk.END)

        mensaje = f"Archivo cargado correctamente: {archivo}"
        if lineas_omitidas > 0:
            mensaje += f"\nSe omitieron {lineas_omitidas} fila(s) con formato incorrecto."
        messagebox.showinfo("Éxito", mensaje)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

def guardar_csv_actual():
    global df, archivo_actual
    if df.empty or archivo_actual is None:
        messagebox.showwarning("Aviso", "No hay CSV abierto para guardar")
        return
    try:
        df.to_csv(archivo_actual, index=False)
        messagebox.showinfo("Éxito", f"Archivo guardado:\n{archivo_actual}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def eliminar_csv(event):
    try:
        seleccionado = lista_csv.curselection()
        if not seleccionado:
            return
        archivo = lista_csv.get(seleccionado[0])
        ruta = os.path.join(CARPETA_CSV, archivo)
        menu = tk.Menu(ventana, tearoff=0)
        menu.add_command(label=f"Eliminar '{archivo}'", command=lambda: confirmar_eliminacion(ruta))
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def confirmar_eliminacion(ruta):
    global df, archivo_actual
    if messagebox.askyesno("Confirmar Eliminación", f"¿Desea eliminar el archivo:\n{os.path.basename(ruta)}?"):
        try:
            os.remove(ruta)
            if archivo_actual == ruta:
                df.drop(df.index, inplace=True)
                archivo_actual = None
                actualizar_tabla()
                resumen_text.delete("1.0", tk.END)
                actualizar_grafico()
            actualizar_lista_csv()
            messagebox.showinfo("Éxito", f"Archivo eliminado: {os.path.basename(ruta)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el archivo:\n{e}")

def actualizar_tabla():
    for i in tabla.get_children():
        tabla.delete(i)
    if df.empty:
        return
    for _, row in df.iterrows():
        tabla.insert("", "end", values=list(row))

def analisis_resumen():
    if df.empty:
        messagebox.showwarning("Aviso", "Primero abra un CSV")
        return
    resumen_text.delete("1.0", tk.END)
    total_ventas = (df["Cantidad"] * df["Precio"]).sum()
    promedio_ventas = df.groupby("Producto")["Cantidad"].sum().mean()
    top_productos = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(5)
    resumen_text.insert(tk.END, f"💰 Total de ventas: {total_ventas:.2f}\n")
    resumen_text.insert(tk.END, f"📊 Promedio de unidades vendidas por producto: {promedio_ventas:.2f}\n")
    resumen_text.insert(tk.END, "🏆 Top 5 productos más vendidos:\n")
    for producto, cantidad in top_productos.items():
        resumen_text.insert(tk.END, f"   {producto}: {cantidad}\n")

# -------------------------------
# Gráfica mejorada con nombres largos
# -------------------------------
def actualizar_grafico():
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    if df.empty:
        return

    top_productos = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).head(10)

    # Ajustar nombres largos
    nombres_envueltos = ["\n".join(textwrap.wrap(p, width=10)) for p in top_productos.index]
    altura_extra = max([len(p.split("\n")) for p in nombres_envueltos]) * 0.2  # Ajusta altura según líneas

    fig, ax = plt.subplots(figsize=(6, 3 + altura_extra))
    ax.bar(nombres_envueltos, top_productos.values, color="#00BFFF")
    ax.set_title("Top 10 productos vendidos", fontsize=10)
    ax.set_ylabel("Cantidad", fontsize=8)
    ax.set_xlabel("Producto", fontsize=8)
    ax.tick_params(axis='x', labelrotation=0, labelsize=7)
    ax.tick_params(axis='y', labelsize=7)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def graficar_ventas():
    if df.empty:
        messagebox.showwarning("Aviso", "Primero abra un CSV")
        return
    actualizar_grafico()

def exportar_resumen():
    if df.empty:
        messagebox.showwarning("Aviso", "Primero abra un CSV")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if archivo:
        resumen = pd.DataFrame({
            "Producto": df.groupby("Producto")["Cantidad"].sum().index,
            "Cantidad vendida": df.groupby("Producto")["Cantidad"].sum().values
        })
        try:
            resumen.to_csv(archivo, index=False)
            messagebox.showinfo("Éxito", f"Resumen exportado a {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

# -------------------------------
# Funciones para edición manual
# -------------------------------
def abrir_menu_edicion():
    global df, archivo_actual
    if df.empty and archivo_actual is None:
        crear_nuevo_csv()

    ventana_edicion = tk.Toplevel(ventana)
    ventana_edicion.title("Gestión de Datos")
    ventana_edicion.geometry("400x350")
    ventana_edicion.configure(bg="#1E1E1E")

    tk.Label(ventana_edicion, text="Fecha (YYYY-MM-DD):", bg="#1E1E1E", fg="white").pack(pady=5)
    entry_fecha = tk.Entry(ventana_edicion)
    entry_fecha.pack(pady=5)

    tk.Label(ventana_edicion, text="Producto:", bg="#1E1E1E", fg="white").pack(pady=5)
    entry_producto = tk.Entry(ventana_edicion)
    entry_producto.pack(pady=5)

    tk.Label(ventana_edicion, text="Cantidad:", bg="#1E1E1E", fg="white").pack(pady=5)
    entry_cantidad = tk.Entry(ventana_edicion)
    entry_cantidad.pack(pady=5)

    tk.Label(ventana_edicion, text="Precio:", bg="#1E1E1E", fg="white").pack(pady=5)
    entry_precio = tk.Entry(ventana_edicion)
    entry_precio.pack(pady=5)

    tk.Label(ventana_edicion, text="Cliente:", bg="#1E1E1E", fg="white").pack(pady=5)
    entry_cliente = tk.Entry(ventana_edicion)
    entry_cliente.pack(pady=5)

    def agregar_fila():
        try:
            nueva_fila = {
                "Fecha": entry_fecha.get(),
                "Producto": entry_producto.get(),
                "Cantidad": int(entry_cantidad.get()),
                "Precio": float(entry_precio.get()),
                "Cliente": entry_cliente.get()
            }
            global df
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            actualizar_tabla()
            actualizar_grafico()
            messagebox.showinfo("Éxito", "Fila agregada correctamente")
            ventana_edicion.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la fila:\n{e}")

    def editar_fila():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione una fila para editar")
            return
        index = tabla.index(seleccionado[0])
        try:
            df.loc[index, "Fecha"] = entry_fecha.get()
            df.loc[index, "Producto"] = entry_producto.get()
            df.loc[index, "Cantidad"] = int(entry_cantidad.get())
            df.loc[index, "Precio"] = float(entry_precio.get())
            df.loc[index, "Cliente"] = entry_cliente.get()
            actualizar_tabla()
            actualizar_grafico()
            messagebox.showinfo("Éxito", "Fila editada correctamente")
            ventana_edicion.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la fila:\n{e}")

    def eliminar_fila():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione una fila para eliminar")
            return
        index = tabla.index(seleccionado[0])
        df.drop(index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        actualizar_tabla()
        actualizar_grafico()
        messagebox.showinfo("Éxito", "Fila eliminada correctamente")
        ventana_edicion.destroy()

    tk.Button(ventana_edicion, text="Agregar Fila", command=agregar_fila, bg="#00FF00", width=15).pack(side="left", padx=5, pady=10)
    tk.Button(ventana_edicion, text="Editar Fila Seleccionada", command=editar_fila, bg="#FFA500", width=20).pack(side="left", padx=5, pady=10)
    tk.Button(ventana_edicion, text="Eliminar Fila Seleccionada", command=eliminar_fila, bg="#FF0000", width=20).pack(side="left", padx=5, pady=10)

def crear_nuevo_csv():
    global df, archivo_actual
    df = pd.DataFrame(columns=["Fecha", "Producto", "Cantidad", "Precio", "Cliente"])
    archivo_actual = os.path.join(CARPETA_CSV, "nuevo.csv")
    df.to_csv(archivo_actual, index=False)
    actualizar_tabla()
    actualizar_grafico()
    actualizar_lista_csv()

# -------------------------------
# Interfaz gráfica
# -------------------------------
ventana = tk.Tk()
ventana.title("Analizador de Ventas - Gestión de CSV")
ventana.geometry("1000x650")
ventana.configure(bg="#1E1E1E")

# Botones principales
frame_botones = tk.Frame(ventana, bg="#1E1E1E")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Cargar CSV Externo", command=cargar_csv_externo, bg="#00BFFF", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Abrir CSV Guardado", command=abrir_csv_guardado, bg="#00FF00", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Guardar CSV Actual", command=guardar_csv_actual, bg="#CCCC00", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Ingresar/Editar Datos", command=abrir_menu_edicion, bg="#00CCCC", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Resumen Ventas", command=analisis_resumen, bg="#FFA500", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Graficar Ventas", command=graficar_ventas, bg="#FF00FF", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Exportar Resumen", command=exportar_resumen, bg="#FF66FF", fg="#000000", width=20).pack(side="left", padx=5)

# Lista de CSV guardados
frame_lista = tk.Frame(ventana, bg="#1E1E1E")
frame_lista.pack(pady=5)
tk.Label(frame_lista, text="CSV Guardados:", bg="#1E1E1E", fg="white").pack(anchor="w")
lista_csv = tk.Listbox(frame_lista, height=5)
lista_csv.pack(fill="x", padx=10)
lista_csv.bind("<Button-3>", eliminar_csv)

# Tabla de datos
tabla_frame = tk.Frame(ventana)
tabla_frame.pack(fill="both", expand=True, padx=10, pady=5)
columns = ("Fecha", "Producto", "Cantidad", "Precio", "Cliente")
tabla = ttk.Treeview(tabla_frame, columns=columns, show="headings")
for col in columns:
    tabla.heading(col, text=col)
tabla.pack(fill="both", expand=True)

# Resumen de texto
resumen_text = tk.Text(ventana, height=6, bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Arial", 9))
resumen_text.pack(fill="x", padx=10, pady=2)

# Frame para gráficos
canvas_frame = tk.Frame(ventana, bg="#1E1E1E", height=250)
canvas_frame.pack(fill="both", expand=True, padx=10, pady=2)

# Inicializar lista de CSV guardados
actualizar_lista_csv()

ventana.mainloop()
