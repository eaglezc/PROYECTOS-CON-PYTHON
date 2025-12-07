import tkinter as tk
from fractions import Fraction
import math

# -------------------------------
# Funciones de la calculadora
# -------------------------------
pantalla_var = None
memoria = 0
modo_cientifico = False
ventana = tk.Tk()

def agregar(texto):
    pantalla_var.set(pantalla_var.get() + str(texto))

def limpiar():
    pantalla_var.set("")

def borrar_uno():
    pantalla_var.set(pantalla_var.get()[:-1])

def calcular():
    try:
        resultado = eval(pantalla_var.get(), {"__builtins__": None, "Fraction": Fraction}, math.__dict__)
        pantalla_var.set(str(resultado))
    except Exception:
        pantalla_var.set("Error")

# Funciones científicas con símbolos intuitivos
def funcion_sin(): agregar("sin(")
def funcion_cos(): agregar("cos(")
def funcion_tan(): agregar("tan(")
def funcion_asin(): agregar("asin(")
def funcion_acos(): agregar("acos(")
def funcion_atan(): agregar("atan(")
def funcion_log(): agregar("log(")
def funcion_ln(): agregar("log(")
def funcion_10x(): agregar("10**")
def funcion_ex(): agregar("exp(")
def funcion_sqrt(): agregar("sqrt(")
def funcion_cbrt(): agregar("pow(")
def funcion_pi(): agregar("pi")
def funcion_e(): agregar("e")
def funcion_fact(): agregar("factorial(")
def funcion_perm(): agregar("perm(")
def funcion_comb(): agregar("comb(")
def memoria_guardar(): global memoria; memoria = eval(pantalla_var.get(), {"__builtins__": None}, math.__dict__)
def memoria_sumar(): global memoria; memoria += eval(pantalla_var.get(), {"__builtins__": None}, math.__dict__)
def memoria_restar(): global memoria; memoria -= eval(pantalla_var.get(), {"__builtins__": None}, math.__dict__)
def memoria_recuperar(): pantalla_var.set(str(memoria))
def memoria_limpiar(): global memoria; memoria=0

# -------------------------------
# Captura de teclado
# -------------------------------
def presionar_tecla(event):
    tecla = event.char
    if tecla in "0123456789.+-*/()":
        agregar(tecla)
    elif tecla == "\r":
        calcular()
    elif tecla == "\x08":
        borrar_uno()

# -------------------------------
# Ventana inicial compacta
# -------------------------------
ventana.title("Calculadora Compacta")
ancho_cm = 6
largo_cm = 8
px_por_cm = 37.8
ventana.geometry(f"{int(ancho_cm*px_por_cm)}x{int(largo_cm*px_por_cm)}")
ventana.configure(bg="#A0A0A0")
ventana.resizable(False, False)
ventana.bind("<Key>", presionar_tecla)

# -------------------------------
# Pantalla
# -------------------------------
pantalla_var = tk.StringVar()
pantalla = tk.Entry(
    ventana, textvariable=pantalla_var, font=("Digital-7", 20, "bold"),
    bd=2, bg="#A0A0A0", fg="#FFFFFF", justify="right", insertbackground="#FFFFFF"
)
pantalla.pack(fill="both", padx=5, pady=5, ipady=10)

# -------------------------------
# Botones compactos
# -------------------------------
botones = [
    ["7","8","9","/","sin","cos","tan"],
    ["4","5","6","*","log","ln","√"],
    ["1","2","3","-","exp","π","e"],
    ["0",".","C","+","(",")","="],
]

colores = {
    "numero":"#555555",
    "operacion":"#FF6600",
    "funcion":"#FFD700",
    "igual":"#00BFFF",
    "limpiar":"#FF0000"
}

frames_botones = []

def crear_boton(frame, text, color, comando):
    btn = tk.Button(
        frame, text=text, font=("Helvetica", 12, "bold"),
        bg=color, fg="#000000" if color=="#FFD700" else "#FFFFFF",
        bd=2, relief="raised",
        activebackground="#AAAAAA", activeforeground="#000000",
        command=comando
    )
    btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)

def crear_botones(lista_botones):
    global frames_botones
    for f in frames_botones:
        f.destroy()
    frames_botones=[]
    for fila in lista_botones:
        frame = tk.Frame(ventana)
        frame.pack(expand=True, fill="both")
        frames_botones.append(frame)
        for boton in fila:
            color = colores["numero"]
            comando = lambda t=boton: agregar(t)
            if boton=="=":
                color = colores["igual"]
                comando = calcular
            elif boton=="C":
                color = colores["limpiar"]
                comando = limpiar
            elif boton in "+-*/":
                color = colores["operacion"]
                comando = lambda t=boton: agregar(t)
            elif boton in ["sin","cos","tan","log","ln","exp","π","e","√"]:
                color = colores["funcion"]
                comandos_especiales = {
                    "sin":funcion_sin,"cos":funcion_cos,"tan":funcion_tan,
                    "log":funcion_log,"ln":funcion_ln,"exp":funcion_ex,
                    "π":funcion_pi,"e":funcion_e,"√":funcion_sqrt
                }
                comando = comandos_especiales[boton]
            crear_boton(frame, boton, color, comando)

crear_botones(botones)

# -------------------------------
# Modo científico
# -------------------------------
def modo_cientifico_func():
    global modo_cientifico
    if modo_cientifico:
        ventana.geometry(f"{int(6*px_por_cm)}x{int(8*px_por_cm)}")
        crear_botones(botones)
        modo_cientifico=False
    else:
        ventana.geometry(f"{int(12*px_por_cm)}x{int(10*px_por_cm)}")
        botones_cientificos = [
            ["7","8","9","/","sin","cos","tan","sin⁻¹","cos⁻¹","tan⁻¹"],
            ["4","5","6","*","log","ln","√","∛","10^x","exp"],
            ["1","2","3","-","x!","P","C","π","e","C"],
            ["0",".","=","+","-","*","/","M+","M-","MR","MC"]
        ]
        crear_botones(botones_cientificos)
        modo_cientifico=True

frame_modo = tk.Frame(ventana)
frame_modo.pack(fill="both")
btn_modo = tk.Button(frame_modo, text="Modo Científico", bg="#FFAA00", fg="#000000",
                     font=("Helvetica",10,"bold"), command=modo_cientifico_func)
btn_modo.pack(expand=True, fill="both", padx=2, pady=2)

ventana.mainloop()
