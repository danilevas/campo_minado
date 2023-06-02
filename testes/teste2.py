# from tkinter import *

# def left_click(event):
#     event.widget.configure(bg="green")

# def right_click(event):
#     event.widget.configure(bg="red")

# root = Tk()
# button = Button(root, width=20, height=20, background="gray")
# button.pack(padx=20, pady=20)

# button.bind("<Button-1>", left_click)
# button.bind("<Button-2>", right_click)
# button.bind("<Button-3>", right_click)

# root.mainloop()


import tkinter
from tkinter import *
import math

root = Tk()
botoes = []
colunas = 10
linhas = 10
clicadas = 0

def clica():
    global clicadas
    clicadas += 1
    L = Label(root, text ="E", width = 5, height = 5)
    L.grid(row=linhas+clicadas, column=int(colunas/2)-1, columnspan=2)

def clica_dir(event):
    event.widget.configure(bg="red")

# Definindo os botões
for i in range(colunas * linhas):
    botao = LabelFrame(root, padx=10, pady=3, borderwidth=3)
    botao.bind("<Button-1>", clica)
    botao.bind("<Button-3>", clica_dir)
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].grid(row=math.floor(i / colunas), column=i % colunas)

mainloop()
