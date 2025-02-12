import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Arquivo padrão inicial
ARQUIVO_PADRAO = "Entradas/Entrada.txt"

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

def atualizar_num_pontos():
    """Atualiza a exibição do número de pontos disponíveis no arquivo."""
    arquivo = entrada_arquivo.get()
    if not os.path.exists(arquivo):
        num_pontos_var.set("Arquivo não encontrado")
        return
    x, y = ler_dados(arquivo)
    num_pontos_var.set(f"Total de pontos: {len(x)}")
    spin_pontos.config(to=len(x), state="normal")  # Atualiza limite do spinbox
    spin_pontos.set(len(x))  # Define o valor padrão como o total de pontos disponíveis

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
    """Realiza ajuste polinomial de grau especificado e retorna os coeficientes e R^2."""
    # Cálculo das somas necessárias para o ajuste
    soma_x = [sum(x_i ** p for x_i in x) for p in range(2 * grau + 1)]
    soma_xy = [sum((x_i ** p) * y_i for x_i, y_i in zip(x, y)) for p in range(grau + 1)]

    # Construção do sistema de equações lineares
    A = [[soma_x[i + j] for j in range(grau + 1)] for i in range(grau + 1)]
    B = np.array(soma_xy).reshape(-1, 1)

    # Resolução do sistema para encontrar os coeficientes
    coeficientes = np.linalg.solve(A, B).flatten() 

    # Cálculo de R^2
    y_media = sum(y) / len(y)
    y_previsto = [sum(c * (x_i ** i) for i, c in enumerate(coeficientes)) for x_i in x]
    ss_total = sum((y_i - y_media) ** 2 for y_i in y)
    ss_residual = sum((y_i - yp) ** 2 for y_i, yp in zip(y, y_previsto))
    R2 = 1 - (ss_residual / ss_total)

    return coeficientes, R2


def ajuste_exponencial(x, y):
    """Realiza ajuste exponencial (y = a * e^(bx))."""
    y_log = [math.log(y_i) for y_i in y]
    b, log_a, R2 = ajuste_linear(x, y_log)
    a = math.exp(log_a)

    return a, b, R2

def plotar_grafico(x, y, tipo, grau, frame, left_frame):
    """Plota o gráfico de acordo com o ajuste escolhido."""
    fig = plt.Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.scatter(x, y, color='red', label="Dados Originais")

    x_min, x_max = min(x), max(x)
    x_plot = np.linspace(x_min, x_max, 500)

    if tipo == "Linear":
        a, b, R2 = ajuste_linear(x, y)
        y_plot = [a * xi + b for xi in x_plot]
        ax.plot(x_plot, y_plot, label=f"y = {a:.4f}x + {b:.4f}\n\nR² = {R2:.4f}")
        ttk.Label(left_frame, text=f"B0 = {b}\nB1 = {a}", name="label", font=("Arial", 14)).pack(anchor=tk.W, pady=5)

    elif tipo == "Polinomial":
        coef , R2 = ajuste_polinomial(x, y, grau)
        y_plot = [sum(c * (xi ** i) for i, c in enumerate(coef)) for xi in x_plot]
        equacao = " + ".join(f"({c:.4f}x^{i})" if i > 0 else f"({c:.4f})" for i, c in enumerate(coef))
        ax.plot(x_plot, y_plot, label=f"y = {equacao}\n\nR² = {R2:.4f}")

        texto = "".join(f"B{i} = {c}\n" if i > 0 else f"B{i} = {c}\n"  for i, c in enumerate(coef)) 
        ttk.Label(left_frame, text=texto, name="label", font=("Arial", 14)).pack(anchor=tk.W, pady=5)



    elif tipo == "Exponencial":
        a, b, R2 = ajuste_exponencial(x, y)
        y_plot = [a * math.exp(b * xi) for xi in x_plot]
        ax.plot(x_plot, y_plot, label=f"y = {a:.4f}e^({b:.4f}x)\n\nR² = {R2:.4f}")

        ttk.Label(left_frame, text=f"a = {a}\nb = {b}", name="label", font=("Arial", 14)).pack(anchor=tk.W, pady=5)



    ax.plot
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Ajuste {tipo}")
    ax.legend(fontsize = 7)   
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
    num_pontos = int(spin_pontos.get())
    x, y = x[:num_pontos], y[:num_pontos]  # Pega apenas os pontos selecionados
    
    metodo = metodo_var.get()
    grau = int(grau_var.get()) if metodo == "Polinomial" else 1
    plotar_grafico(x, y, metodo, grau, right_frame, left_frame)


def plot_inicial(frame):
    def resize_image(event):
        # Obter as dimensões do frame
        new_width = event.width
        new_height = event.height

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        label.config(image=photo)
        label.image = photo 


    image = Image.open("img/Ajuste de Curvas.png")

    photo = ImageTk.PhotoImage(image)
    label = tk.Label(frame, image=photo)
    label.image = photo
    label.pack(fill=tk.BOTH, expand=True)

    frame.bind("<Configure>", resize_image)



def criar_interface():
    global root, entrada_arquivo, right_frame, metodo_var, grau_var, num_pontos_var, spin_pontos,left_frame
    root = tk.Tk()
    root.geometry("1600x900")
    root.title("Ajuste de Curvas")
    
    
    left_frame = ttk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    ttk.Separator(root, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
    
    metodo_var = tk.StringVar(value="Linear")
    grau_var = tk.StringVar(value="2")
    num_pontos_var = tk.StringVar(value="Total de pontos: ?")
    
    ttk.Label(left_frame, text="Arquivo:", font=("Arial", 14)).pack(anchor=tk.W, pady=5)
    entrada_arquivo = ttk.Entry(left_frame, font=("Arial", 12), width=40)
    entrada_arquivo.insert(0, ARQUIVO_PADRAO)
    entrada_arquivo.pack(anchor=tk.W, pady=5)
    
    ttk.Button(left_frame, text="Buscar", command=lambda: [entrada_arquivo.delete(0, tk.END), entrada_arquivo.insert(0, filedialog.askopenfilename()), atualizar_num_pontos()]).pack(anchor=tk.CENTER, pady=5)
    
    frame_pontos = ttk.Frame(left_frame)
    frame_pontos.pack(anchor=tk.W, pady=5, fill=tk.X)
    ttk.Label(frame_pontos, textvariable=num_pontos_var, font=("Arial", 12)).pack(side=tk.LEFT)
    ttk.Label(frame_pontos, text=" | Selecionar pontos: ", font=("Arial", 12)).pack(side=tk.LEFT)
    spin_pontos = ttk.Spinbox(frame_pontos, from_=1, to=100, width=5, state="disabled")
    spin_pontos.pack(side=tk.LEFT)
    
    ttk.Label(left_frame, text="Método:", font=("Arial", 14)).pack(anchor=tk.W, pady=5)
    combo_metodo = ttk.Combobox(left_frame, font=("Arial", 12), textvariable=metodo_var, values=["Linear", "Polinomial", "Exponencial"])
    combo_metodo.pack(anchor=tk.W, pady=5)
    
    ttk.Label(left_frame, text="Grau:", font=("Arial", 14)).pack(anchor=tk.W, pady=5)
    combo_grau = ttk.Combobox(left_frame, font=("Arial", 12), textvariable=grau_var, values=["2", "3", "4", "5" , "6", "7", "8", "9"])
    combo_grau.pack(anchor=tk.W, pady=5)
    
    ttk.Button(left_frame, text="Gerar Ajuste", command=executar_ajuste).pack(anchor=tk.W, pady=10)
    
    right_frame = ttk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10, anchor=tk.CENTER)
    right_frame.background = "red"
    atualizar_num_pontos()  # Atualiza os pontos automaticamente ao iniciar
    plot_inicial(right_frame)
    
    return root