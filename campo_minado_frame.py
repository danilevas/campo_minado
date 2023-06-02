from tkinter import *
import math
import random
from PIL import ImageTk,Image

root = Tk()
root.title("Campo Minado do Dani!")

# Load an image in the script
img = (Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/flag.png"))

tkimage = ImageTk.PhotoImage(img)
h = tkimage.height()
w = tkimage.width()

# Resize the Image using resize method
resized_image = img.resize((23, 23), Image.ANTIALIAS)
img_bandeira = ImageTk.PhotoImage(resized_image)

botoes = []
numeros = []
colunas = 10
linhas = 10
lugar_bombas = []

class meuFrame():
    def __init__(self, frame, indice):
        self.frame = frame
        self.indice = indice 
        
def revelar_vizinhos(indice):
    inicio = True
    fila = [indice]
    while fila:
        atual = fila.pop(0)
        botoes[atual].frame.configure(state=DISABLED, borderwidth=0)
            
        if (inicio == True) or (inicio == False and numeros[atual] == 0 ):
            inicio = False
            for vizinho in obter_vizinhos(atual):
                if botoes[vizinho].frame["state"] == NORMAL and vizinho not in lugar_bombas: # mudança
                    fila.append(vizinho)
                    botoes[vizinho].frame.configure(state=DISABLED, borderwidth=0)
                    if numeros[vizinho] > 0:
                        botoes[vizinho].frame.configure(text=numeros[vizinho], padx=9)

def clique_botao(event):
    if event.widget.frame["state"] == DISABLED:
        return
    event.widget.frame.configure(state=DISABLED, borderwidth=0)
    if event.widget.indice in lugar_bombas:
        event.widget.frame.configure(text="B!", padx=8)
        for botao in botoes:
            botao.frame.configure(state=DISABLED)
        root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window
    else:
        if numeros[event.widget.indice] > 0:
            event.widget.frame.configure(text=numeros[event.widget.indice], padx=9)
        revelar_vizinhos(event.widget.indice)

def obter_vizinhos(indice):
    vizinhos = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            linha = indice // colunas
            coluna = indice % colunas
            nova_linha = linha + dy
            nova_coluna = coluna + dx
            if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
                vizinhos.append(nova_linha * colunas + nova_coluna)
    return vizinhos

def bandeirinha(event):
    if event.widget["image"] != img_bandeira:
        event.widget.configure(image=img_bandeira)
        continua = 0
        for indice in lugar_bombas:
            if botoes[indice].frame["state"] != DISABLED:
                continua += 1
        if continua == 0:
            # VOCÊ GANHOU!
            for indice in range(linhas * colunas):
                botoes[indice].frame.configure(bg="blue")
    else:
        event.widget.configure(image=None)
            

# Sorteando as bombas
for i in range(colunas*3):
    local_bomba = random.randint(0, colunas * linhas)
    if local_bomba not in lugar_bombas and local_bomba != i:
        lugar_bombas.append(local_bomba)

# Colocando os números nos quadrados sem bomba
for i in range(colunas * linhas):
    num = 0
    for vizinho in obter_vizinhos(i):
        if vizinho in lugar_bombas:
            num += 1
    numeros.append(num)

# Definindo os botões
for i in range(colunas * linhas):
    if i in lugar_bombas:
        botao = meuFrame(Frame(root, padx=10, pady=3, borderwidth=3, bg="red"), i)
    else:
        botao = meuFrame(Frame(root, padx=10, pady=3, borderwidth=3), i)
    botao.frame.bind("<Button-1>", clique_botao)
    botao.frame.bind("<Button-2>", bandeirinha)
    botao.frame.bind("<Button-3>", bandeirinha)
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].frame.grid(row=math.floor(i / colunas), column=i % colunas)

root.mainloop()