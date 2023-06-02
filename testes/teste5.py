from tkinter import *
import math
import random
from PIL import ImageTk,Image

root = Tk()
root.title("Campo Minado do Dani!")
root.configure(bg='#BDBDBD')

tamanho_x = 15
tamanho_y = 7.5

imagens = [
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/flag resized.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/1.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/2.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/3.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/4.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/5.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/6.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/7.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/8.png"),
    Image.open("C:/Programas/Projetos Pessoais/tkinter/icones/fundo.png")
]
imagens_prontas = []

for i in range(len(imagens)):
    # Load an image in the script
    img = imagens[i]

    tkimage = ImageTk.PhotoImage(img)
    h = tkimage.height()
    w = tkimage.width()

    # Resize the Image using resize method
    if i == 0:
        resized_image = img.resize((int(tamanho_x*2), int(tamanho_x*2)), Image.ANTIALIAS)
    else:
        resized_image = img.resize((int(tamanho_x*2.3), int(tamanho_x*2.3)), Image.ANTIALIAS)
    imagens_prontas.append(ImageTk.PhotoImage(resized_image))

botoes = []
numeros = []
colunas = 3
linhas = 3
bombas = 3
lugar_bombas = []

def desabilita(label):
    label.configure(borderwidth=1, highlightbackground = "#7F7F7F", highlightcolor= "#7F7F7F")

def desabilitado(label):
    if label["borderwidth"] == 1:
        return True
    else:
        return False

def marca(label):
    label.configure(image=imagens_prontas[0])

def desmarca(label):
    label.configure(image=None)

def marcado(label):
    if label["image"] == imagens_prontas[0]:
        return True
    else:
        return False

def coloca_icone(label, numero):
    label.configure(image=imagens_prontas[numero], padx=tamanho_x-1)

def bandeirinha(event):
    if not marcado(event.widget):
        marca(event.widget)
        checa_ganhou()
    else:
        desmarca(event.widget)

def checa_ganhou():
    falso_pos = 0
    falso_neg = 0
    for indice in range(linhas * colunas):
        if indice in lugar_bombas and (not marcado(botoes[indice])):
            falso_neg += 1
        elif (indice not in lugar_bombas) and marcado(botoes[indice]):
            falso_pos += 1
    if falso_pos + falso_neg == 0:
        # VOCÊ GANHOU!
        for indice in range(linhas * colunas):
            botoes[indice].configure(bg="blue")
            root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window

# Sorteando as bombas
for i in range(bombas):
    local_bomba = random.randint(0, (colunas * linhas) - 1)
    if local_bomba not in lugar_bombas:
        lugar_bombas.append(local_bomba)

# Colocando os números nos quadrados sem bomba
# for i in range(colunas * linhas):
#     num = 0
#     for vizinho in obter_vizinhos(i):
#         if vizinho in lugar_bombas:
#             num += 1
#     numeros.append(num)

# Definindo os botões
for i in range(colunas * linhas):
    if i in lugar_bombas:
        botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="red")
    else:
        botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
    botao.bind("<Button-3>", bandeirinha)
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].grid(row=math.floor(i / colunas), column=i % colunas)

root.mainloop()