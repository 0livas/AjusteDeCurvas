import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Arquivo padrão inicial
ARQUIVO_PADRAO = "Entrada.txt"

def ler_dados(arquivo):
    """Lê os dados de um arquivo e retorna listas de x e y."""
    x, y = [], []
    with open(arquivo, 'r') as f:
        for linha in f:
            valores = linha.strip().split(',')
            if len(valores) == 2:
                x.append(float(valores[0]))
                y.append(float(valores[1]))
    return x, y

def ajuste_linear(x, y):
    """Realiza ajuste linear (y = ax + b)."""
    n = len(x)
    soma_x = sum(x)
    soma_y = sum(y)
    soma_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
    soma_x2 = sum(x_i ** 2 for x_i in x)
    soma_y2 = sum(y_i ** 2 for y_i in y)

    a = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x ** 2)
    b = (soma_y - a * soma_x) / n
    R2 = ((soma_xy - soma_x * soma_y / n) ** 2) / ((soma_x2 - (soma_x ** 2) / n) * (soma_y2 - (soma_y ** 2) / n))

    return a, b, R2

def ajuste_polinomial(x, y, grau):
    """Realiza ajuste polinomial de grau especificado."""
    if grau == 1:
        return ajuste_linear(x, y)

    soma_x = [sum(x_i ** p for x_i in x) for p in range(2 * grau + 1)]
    soma_xy = [sum((x_i ** p) * y_i for x_i, y_i in zip(x, y)) for p in range(grau + 1)]

    A = [[soma_x[i + j] for j in range(grau + 1)] for i in range(grau + 1)]
    B = np.array(soma_xy).reshape(-1, 1)

    coeficientes = np.linalg.solve(A, B)
    return coeficientes

def ajuste_exponencial(x, y):
    """Realiza ajuste exponencial (y = a * e^(bx))."""
    y_log = [math.log(y_i) for y_i in y]
    b, log_a, R2 = ajuste_linear(x, y_log)
    a = math.exp(log_a)
    return a, b, R2

def plotar_grafico(x, y, tipo, grau, frame):
    """Plota o gráfico de acordo com o ajuste escolhido."""
    fig = plt.Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.scatter(x, y, color='red', label="Dados Originais")

    x_min, x_max = min(x), max(x)
    x_plot = np.linspace(x_min, x_max, 500)

    if tipo == "Linear":
        a, b, R2 = ajuste_linear(x, y)
        y_plot = [a * xi + b for xi in x_plot]
        ax.plot(x_plot, y_plot, label=f"y = {a:.4f}x + {b:.4f}")
        ax.text(0.5, 0.95, f'R² = {R2:.4f}', transform=ax.transAxes, fontsize=12, color='blue', ha='center')

    elif tipo == "Polinomial":
        coef = ajuste_polinomial(x, y, grau).flatten()
        y_plot = [sum(c * (xi ** i) for i, c in enumerate(coef)) for xi in x_plot]
        equacao = " + ".join(f"{c:.4f}x^{i}" if i > 0 else f"{c:.4f}" for i, c in enumerate(coef))
        ax.plot(x_plot, y_plot, label=f"y = {equacao}")

    elif tipo == "Exponencial":
        a, b, R2 = ajuste_exponencial(x, y)
        y_plot = [a * math.exp(b * xi) for xi in x_plot]
        ax.plot(x_plot, y_plot, label=f"y = {a:.4f}e^({b:.4f}x)")
        ax.text(0.5, 0.95, f'R² = {R2:.4f}', transform=ax.transAxes, fontsize=12, color='blue', ha='center')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Ajuste {tipo} - {grau}º Grau")
    ax.legend()
    ax.grid()

    # Limpa o frame antes de adicionar o novo gráfico
    for widget in frame.winfo_children():
        widget.destroy()

    # Insere o gráfico no frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def executar_ajuste():
    """Executa o ajuste escolhido e plota o gráfico."""
    arquivo = entrada_arquivo.get()
    if not os.path.exists(arquivo):
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado!")
        return

    x, y = ler_dados(arquivo)
    metodo = metodo_var.get()

    try:
        grau = int(grau_var.get()) if metodo == "Polinomial" else 1
        plotar_grafico(x, y, metodo, grau, right_frame)
    except ValueError:
        print("Erro: O grau informado é inválido!")

def criar_interface():
    global root, entrada_arquivo, right_frame
    root = tk.Tk()
    #root.configure(background='white')
    root.geometry("1600x900")
    root.title("Ajuste de Curvas")

    # Frame fixo para os controles no lado esquerdo
    left_frame = ttk.Frame(root)    
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)  
    ttk.Separator(root, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)


    global metodo_var, grau_var
    metodo_var = tk.StringVar(value="Linear")
    grau_var = tk.StringVar(value="2")

    ttk.Label(left_frame, text="Arquivo:",  font=("Arial", 14)).pack(anchor=tk.W, pady=10)  
    entrada_arquivo = ttk.Entry(left_frame,font=("Arial", 12), width=40)
    entrada_arquivo.insert(0, ARQUIVO_PADRAO)  
    entrada_arquivo.pack(anchor=tk.W, pady=5)

    ttk.Button(left_frame, text="Buscar", command=lambda: entrada_arquivo.delete(0, tk.END) or entrada_arquivo.insert(0, filedialog.askopenfilename())).pack(anchor=tk.CENTER, pady=5)

    ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

    ttk.Label(left_frame, text="Método:",  font=("Arial", 14)).pack(anchor=tk.W, pady=5)
    combo_metodo = ttk.Combobox(left_frame, font=("Arial", 12), textvariable=metodo_var, values=["Linear", "Polinomial", "Exponencial"])
    combo_metodo.pack(anchor=tk.W, pady=5)

    ttk.Label(left_frame, text="Grau:",  font=("Arial", 14)).pack(anchor=tk.W, pady=5)
    combo_grau = ttk.Combobox(left_frame,font=("Arial", 12), textvariable=grau_var, values=["2", "3", "4", "5"])
    combo_grau.pack(anchor=tk.W, pady=5)

    ttk.Button(left_frame, text="Gerar Ajuste", command=executar_ajuste).pack(anchor=tk.W, pady=10)

    # Frame para o gráfico no lado direito
    right_frame = ttk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    return root

