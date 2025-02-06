import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

arquivo_padrao = "Entrada.txt"

def LerDados(arquivo):  
    x, y = [], []
    with open(arquivo, 'r') as f:
        for linha in f:
            valores = linha.strip().split(',')
            if len(valores) == 2:
                x.append(float(valores[0]))
                y.append(float(valores[1]))
    return x, y

def RotinaLinear(x, y): # y = Ax + B.
    n = len(x)
    soma_x = sum(x)
    soma_y = sum(y)
    soma_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
    soma_x2 = sum(x_i ** 2 for x_i in x)
    soma_y2 = sum(y_i ** 2 for y_i in y)
    
    a = (n * soma_xy - soma_x * soma_y)/(n* soma_x2 - soma_x ** 2)  # b1
    b = (soma_y - a * soma_x)/n                                     # b0
    
    R = ((soma_xy - soma_x*soma_y/n)**2)/((soma_x2 - (soma_x**2)/n)*(soma_y2 - (soma_y**2)/n)) # R^2
    
    return a, b, R

def RotinaPolinomial(x, y, exp): # fazemos só até x^5.
    
    if exp == 1:
        RotinaLinear(x, y)
    
    n = len(x)
    soma_x = sum(x)
    soma_x2 = sum(x_i ** 2 for x_i in x)
    soma_x3 = sum(x_i ** 3 for x_i in x)
    soma_x4 = sum(x_i ** 4 for x_i in x)
    soma_y = sum(y)
    soma_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
    soma_x2y = sum(x_i ** 2 * y_i for x_i, y_i in zip(x, y))
    
    if exp == 2:
        A = [
            [n, soma_x, soma_x2],
            [soma_x, soma_x2, soma_x3 ],
            [soma_x2, soma_x3, soma_x4]]
        
        B = np.array([[soma_y], [soma_xy], [soma_x2y]])
        
        Resultados = np.linalg.solve(A, B)
        return Resultados
        
    if exp == 3:
        soma_x5 = sum(x_i ** 5 for x_i in x)
        soma_x6 = sum(x_i ** 6 for x_i in x)
        soma_x3y = sum(x_i ** 3 * y_i for x_i, y_i in zip(x, y))
        
        A = [
            [n, soma_x, soma_x2, soma_x3],
            [soma_x, soma_x2, soma_x3, soma_x4 ],
            [soma_x2, soma_x3, soma_x4, soma_x5],
            [soma_x3, soma_x4, soma_x5, soma_x6]]
        
        B = np.array([[soma_y], [soma_xy], [soma_x2y], [soma_x3y]])
        
        Resultados = np.linalg.solve(A, B)
        return Resultados
        
    if exp == 4:
        soma_x5 = sum(x_i ** 5 for x_i in x)
        soma_x6 = sum(x_i ** 6 for x_i in x)
        soma_x7 = sum(x_i ** 7 for x_i in x)
        soma_x8 = sum(x_i ** 8 for x_i in x)
        soma_x3y = sum(x_i ** 3 * y_i for x_i, y_i in zip(x, y))
        soma_x4y = sum(x_i ** 4 * y_i for x_i, y_i in zip(x, y))
        
        A = [
            [n, soma_x, soma_x2, soma_x3, soma_x4],
            [soma_x, soma_x2, soma_x3, soma_x4, soma_x5 ],
            [soma_x2, soma_x3, soma_x4, soma_x5, soma_x6],
            [soma_x3, soma_x4, soma_x5, soma_x6, soma_x7],
            [soma_x4, soma_x5, soma_x6, soma_x7, soma_x8]]
        
        B = np.array([[soma_y], [soma_xy], [soma_x2y], [soma_x3y], [soma_x4y]])
        
        Resultados = np.linalg.solve(A, B)
        return Resultados
        
    if exp == 5:
        soma_x5 = sum(x_i ** 5 for x_i in x)
        soma_x6 = sum(x_i ** 6 for x_i in x)
        soma_x7 = sum(x_i ** 7 for x_i in x)
        soma_x8 = sum(x_i ** 8 for x_i in x)
        soma_x9 = sum(x_i ** 9 for x_i in x)
        soma_x10 = sum(x_i ** 10 for x_i in x)
        soma_x3y = sum(x_i ** 3 * y_i for x_i, y_i in zip(x, y))
        soma_x4y = sum(x_i ** 4 * y_i for x_i, y_i in zip(x, y))
        soma_x5y = sum(x_i ** 5 * y_i for x_i, y_i in zip(x, y))
        
        A = [
            [n, soma_x, soma_x2, soma_x3, soma_x4, soma_x5],
            [soma_x, soma_x2, soma_x3, soma_x4, soma_x5, soma_x6],
            [soma_x2, soma_x3, soma_x4, soma_x5, soma_x6, soma_x7],
            [soma_x3, soma_x4, soma_x5, soma_x6, soma_x7, soma_x8],
            [soma_x4, soma_x5, soma_x6, soma_x7, soma_x8, soma_x9],
            [soma_x5, soma_x6, soma_x7, soma_x8, soma_x9, soma_x10]]
        
        B = np.array([[soma_y], [soma_xy], [soma_x2y], [soma_x3y], [soma_x4y], [soma_x5y]])
        
        Resultados = np.linalg.solve(A, B)
        return Resultados
    
    return

def RotinaExponencial(x, y): # y = a*e^(bx) | ln y = ln a + bx
    y_log = [math.log(y_i) for y_i in y]
    b, log_a, R = RotinaLinear(x, y_log)
    a = math.exp(log_a)
    return a, b, R

def Plotar_Grafico(x, y, tipo, grau=1):
    plt.scatter(x, y, color='red', label="Dados Originais")
    
    x_min, x_max = min(x), max(x)
    x_plot = np.linspace(x_min, x_max)
    
    if tipo == "Linear":
        a, b, R = RotinaLinear(x, y)
        y_plot = [a * xi + b for xi in x_plot]
        plt.plot(x_plot, y_plot, label=f"y = {a:.4f}x + {b:.4f}")
        
# Exibindo o R² no gráfico
        plt.text(0.5, 0.95, f'R² = {R:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center', color='blue')
        
    elif tipo == "Polinomial":
        coef = RotinaPolinomial(x, y, grau)
        coef = coef.flatten()  # Garantir que seja um vetor 1D
        y_plot = [sum(c * (xi ** i) for i, c in enumerate(coef)) for xi in x_plot]
        equacao = " + ".join(f"{c:.4f}x^{i}" for i, c in enumerate(coef))
        plt.plot(x_plot, y_plot, label=f"y = {equacao}")         
        
    if tipo == "Exponencial":
        a, b, R = RotinaExponencial(x, y)
        y_plot = [a * math.exp(b * xi) for xi in x_plot]
        plt.plot(x_plot, y_plot, label=f"y = {a:.4f}e^({b:.4f}x)")
#Exibindo o R² no gráfico
        plt.text(0.5, 0.95, f'R² = {R:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center', color='blue')
    
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Ajuste {tipo}")
    plt.grid()
    plt.show()
    
def executar_ajuste():
    arquivo = entrada_arquivo.get()  # Pega o caminho do arquivo na interface
    if not os.path.exists(arquivo):  # Verifica se o arquivo existe
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado!")
        return

    x, y = LerDados(arquivo)
    metodo = metodo_var.get()
    grau = int(grau_var.get()) if metodo == "Polinomial" else None

    Plotar_Grafico(x, y, metodo, grau)

def criar_interface():
    global root, entrada_arquivo
    root = tk.Tk()
    root.title("Ajuste de Curvas")

    # Variáveis da interface
    global metodo_var, grau_var
    metodo_var = tk.StringVar(value="Linear")
    grau_var = tk.StringVar(value="2")

    # Campo para selecionar o arquivo
    ttk.Label(root, text="Arquivo:").grid(row=0, column=0, padx=5, pady=5)
    entrada_arquivo = ttk.Entry(root, width=40)
    entrada_arquivo.insert(0, arquivo_padrao)  # Define "Entrada.txt" como padrão
    entrada_arquivo.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(root, text="Buscar", command=lambda: entrada_arquivo.delete(0, tk.END) or entrada_arquivo.insert(0, filedialog.askopenfilename())).grid(row=0, column=2, padx=5, pady=5)

    # Opções de método
    ttk.Label(root, text="Método:").grid(row=1, column=0, padx=5, pady=5)
    combo_metodo = ttk.Combobox(root, textvariable=metodo_var, values=["Linear", "Polinomial", "Exponencial"])
    combo_metodo.grid(row=1, column=1, padx=5, pady=5)

    # Opções para grau do polinômio
    ttk.Label(root, text="Grau (para Polinomial):").grid(row=2, column=0, padx=5, pady=5)
    combo_grau = ttk.Combobox(root, textvariable=grau_var, values=["2", "3", "4", "5"])
    combo_grau.grid(row=2, column=1, padx=5, pady=5)

    # Botão para executar
    ttk.Button(root, text="Gerar Ajuste", command=executar_ajuste).grid(row=3, column=0, columnspan=3, pady=10)

    return root
    