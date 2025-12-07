import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

# -------------------------------
# Variables globales
# -------------------------------
ventana = tk.Tk()
ventana.title("Descargador de Imágenes Profesional")
ventana.geometry("650x550")
ventana.configure(bg="#1E1E1E")
modo_oscuro = True

carpeta_var = tk.StringVar()

# -------------------------------
# Funciones principales
# -------------------------------
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_var.set(carpeta)

def verificar_imagen(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            raise ValueError("La URL no apunta a una imagen válida.")
        return BytesIO(response.content)
    except Exception as e:
        messagebox.showwarning("Error", f"No se pudo cargar la imagen:\n{e}")
        return None

def previsualizar():
    urls = url_text.get("1.0", tk.END).strip().splitlines()
    if not urls:
        messagebox.showwarning("Aviso", "Ingrese al menos una URL")
        return
    img_data = verificar_imagen(urls[0])
    if img_data:
        img = Image.open(img_data)
        img.thumbnail((250, 250))
        img_tk = ImageTk.PhotoImage(img)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk

def refrescar():
    # Limpiar el área de URLs
    url_text.delete("1.0", tk.END)
    # Limpiar la previsualización
    preview_label.config(image="")
    preview_label.image = None
    # Reiniciar barra de progreso
    progress_bar["value"] = 0

def descargar_imagenes():
    urls = url_text.get("1.0", tk.END).strip().splitlines()
    carpeta = carpeta_var.get()
    if not urls or not carpeta:
        messagebox.showwarning("Aviso", "Ingrese URLs y seleccione una carpeta")
        return

    progress_bar["maximum"] = len(urls)
    progress_bar["value"] = 0
    ventana.update_idletasks()

    for i, url in enumerate(urls, start=1):
        img_data = verificar_imagen(url)
        if img_data:
            try:
                img = Image.open(img_data)
                nombre_archivo = os.path.join(carpeta, f"imagen_{i}.{img.format.lower()}")
                img.save(nombre_archivo)
            except Exception as e:
                messagebox.showwarning("Error", f"No se pudo guardar la imagen {url}:\n{e}")
        progress_bar["value"] = i
        ventana.update_idletasks()

    messagebox.showinfo("Listo", "Descarga completa")

def cambiar_modo():
    global modo_oscuro
    if modo_oscuro:
        ventana.configure(bg="#FFFFFF")
        url_text.configure(bg="#F0F0F0", fg="#000000", insertbackground="#000000")
        preview_label.configure(bg="#FFFFFF")
        frame_botones.configure(bg="#FFFFFF")
        modo_oscuro = False
    else:
        ventana.configure(bg="#1E1E1E")
        url_text.configure(bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF")
        preview_label.configure(bg="#1E1E1E")
        frame_botones.configure(bg="#1E1E1E")
        modo_oscuro = True

# -------------------------------
# Interfaz
# -------------------------------
tk.Label(ventana, text="URLs de imágenes (una por línea):", fg="#FFFFFF", bg="#1E1E1E").pack(pady=(10,0))
url_text = tk.Text(ventana, height=8, bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF")
url_text.pack(fill="x", padx=10, pady=5)

# Carpeta
frame_carpeta = tk.Frame(ventana, bg="#1E1E1E")
frame_carpeta.pack(fill="x", padx=10)
tk.Entry(frame_carpeta, textvariable=carpeta_var, bg="#2E2E2E", fg="#FFFFFF", insertbackground="#FFFFFF").pack(side="left", fill="x", expand=True)
tk.Button(frame_carpeta, text="Seleccionar carpeta", command=seleccionar_carpeta, bg="#FFAA00").pack(side="left", padx=5)

# Previsualización
preview_label = tk.Label(ventana, bg="#1E1E1E")
preview_label.pack(pady=10)

# Barra de progreso
progress_bar = Progressbar(ventana, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Botones
frame_botones = tk.Frame(ventana, bg="#1E1E1E")
frame_botones.pack(pady=10)
tk.Button(frame_botones, text="Previsualizar", command=previsualizar, bg="#00BFFF", fg="#000000", width=15).pack(side="left", padx=5)
tk.Button(frame_botones, text="Refrescar", command=refrescar, bg="#FFA500", fg="#000000", width=15).pack(side="left", padx=5)
tk.Button(frame_botones, text="Descargar imágenes", command=descargar_imagenes, bg="#00FF00", fg="#000000", width=20).pack(side="left", padx=5)
tk.Button(frame_botones, text="Modo Claro/Oscuro", command=cambiar_modo, bg="#FF00FF", fg="#000000", width=20).pack(side="left", padx=5)

ventana.mainloop()
