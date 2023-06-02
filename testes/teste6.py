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
    label._image_ref = imagens_prontas[0]

def desmarca(label):
    label.configure(image=None)

def marcado(label):
    foo = root.call(label.cget('image'), 'cget', '-file')
    bar = imagens_prontas[0]['file']
    if foo == bar:
        return True
    else:
        return False

def bandeirinha(event):
    if not marcado(event.widget):
        print("marquei")
        marca(event.widget)
    else:
        print("desmarquei")
        desmarca(event.widget)

# Definindo os botões
for i in range(colunas * linhas):
    botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
    botao.bind("<Button-3>", bandeirinha)
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].grid(row=math.floor(i / colunas), column=i % colunas)

root.mainloop()