from tkinter import *
import math
import random
from PIL import ImageTk,Image

# Próximos passos:
#   - A primeira casa que o jogador clica sempre ser vazia para abrir o jogo, ou seja, só colocar as bombas e números depois dele clicar
#   - Ajeitar o tamanho da casa marcada que diminui um pouquinho
#   - Poder clicar nos números quando o requerimento dele já foi preenchido para revelar todos os outros vizinhos (inclusive bombas, que se tiver explode!)
#       - Se o requerimento não tiver sido completo, piscar os vizinhos não marcados
#   - Colocar popups quando ganha e perde
#   - Colocar um botão para reiniciar após esses popups
#   - Colocar som! (tictic para apertar e BOOM para a bomba, yaaay para ganhar)
#   - Contador de bombas marcadas e de tempo corrido
#   - Entender melhor a regra de revelação dos quadrados

root = Tk()
root.title("Campo Minado do Dani!")
root.configure(bg='#BDBDBD')

tamanho_x = 15
tamanho_y = 7.5
botoes = []
numeros = []
colunas = 9
linhas = 9
bombas = 10
lugar_bombas = []
marcados = []
cont = 0

path = "C:/Programas/Projetos Pessoais/tkinter/campo_minado/"
imagens = [
    Image.open(path + "icones/flag resized.png"),
    Image.open(path + "icones/1.png"),
    Image.open(path + "icones/2.png"),
    Image.open(path + "icones/3.png"),
    Image.open(path + "icones/4.png"),
    Image.open(path + "icones/5.png"),
    Image.open(path + "icones/6.png"),
    Image.open(path + "icones/7.png"),
    Image.open(path + "icones/8.png"),
    Image.open(path + "icones/fundo.png"),
    Image.open(path + "icones/fundo.png")
]
imagens_prontas = []

for i in range(len(imagens)):
    # Load an image in the script
    img = imagens[i]

    tkimage = ImageTk.PhotoImage(img)
    h = tkimage.height()
    w = tkimage.width()

    # Resize the Image using resize method
    if i == 0 or i == 10:
        resized_image = img.resize((int(tamanho_x*2), int(tamanho_x*2)), Image.ANTIALIAS)
    else:
        resized_image = img.resize((int(tamanho_x*2.3), int(tamanho_x*2.3)), Image.ANTIALIAS)
    imagens_prontas.append(ImageTk.PhotoImage(resized_image))

def desabilita(label):
    label.configure(borderwidth=1, highlightbackground = "#7F7F7F", highlightcolor= "#7F7F7F")

def desabilitado(label):
    if label["borderwidth"] == 1:
        return True
    else:
        return False

def marca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[0])
    marcados.append(indice)

def desmarca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[10])
    marcados.remove(indice)

def marcado(indice):
    if indice in marcados:
        return True
    else:
        return False

def coloca_icone(label, numero):
    label.configure(image=imagens_prontas[numero], padx=tamanho_x-1)

def revelar_vizinhos(indice):
    inicio = True
    fila = [indice]
    while fila:
        atual = fila.pop(0)
        desabilita(botoes[atual])
            
        if numeros[atual] == 0:
            inicio = False
            for vizinho in obter_vizinhos(atual):
                if (not desabilitado(botoes[vizinho])) and vizinho not in lugar_bombas: # and not bloqueado(vizinho, atual): # mudança
                    desabilita(botoes[vizinho])
                    if numeros[vizinho] > 0:
                        coloca_icone(botoes[vizinho], numeros[vizinho])
                    else:
                        coloca_icone(botoes[vizinho], 9)
                        fila.append(vizinho)

def bloqueado(vizinho, atual):
    diagonais = [atual + colunas + 1, atual + colunas - 1, atual - colunas + 1, atual - colunas - 1]
    if vizinho not in diagonais:
        return False
    else:
        if vizinho == diagonais[0] and (atual + colunas not in lugar_bombas and atual + 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[1] and (atual + colunas not in lugar_bombas and atual - 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[2] and (atual - colunas not in lugar_bombas and atual + 1 not in lugar_bombas):
            return False
        elif vizinho == diagonais[3] and (atual - colunas not in lugar_bombas and atual - 1 not in lugar_bombas):
            return False
        else:
            return True

def clique_botao(indice):
    label = botoes[indice]
    # A label abaixa quando é clicada
    label.config(relief=SUNKEN)

def desclique_botao(indice):
    label = botoes[indice]
    primeira = True
    
    global cont
    if primeira == True:
        cont = 0
    
    if cont == 0:
        global lugar_bombas
        lugar_bombas = sortea_bombas(indice)
        global numeros
        numeros = coloca_numeros()
        cont += 1
        primeira = False

    label.config(relief=RAISED)
    
    if indice in lugar_bombas:
        # VOCÊ PERDEU!
        label.configure(text="B!", padx=tamanho_x*0.65)
        for botao in botoes:
            if botao != label:
                botao.configure(state=DISABLED) # Para ninguém poder clicar mais em nada depois que o jogo termina
        root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window
        
    else:
        if numeros[indice] > 0:
            coloca_icone(label, numeros[indice])
        else:
            coloca_icone(label, 9)
        desabilita(label)
        revelar_vizinhos(indice)

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

def bandeirinha(indice):
    if desabilitado(botoes[indice]):
        return
    if not marcado(indice):
        marca(indice)
        checa_ganhou()
    else:
        desmarca(indice)

def checa_ganhou():
    marcados.sort()
    if lugar_bombas == marcados:
        # VOCÊ GANHOU!
        for indice in range(linhas * colunas):
            botoes[indice].configure(bg="blue")
            root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window

def sortea_bombas(clicado):
    # Sorteando as bombas
    vizinhos_clicado = obter_vizinhos(clicado)
    for i in range(bombas):
        local_bomba = random.randint(0, (colunas * linhas) - 1)
        if local_bomba not in lugar_bombas and local_bomba not in vizinhos_clicado:
            lugar_bombas.append(local_bomba)
    lugar_bombas.sort()
    return lugar_bombas

def coloca_numeros():
    # Colocando os números nos quadrados sem bomba
    for i in range(colunas * linhas):
        num = 0
        for vizinho in obter_vizinhos(i):
            if vizinho in lugar_bombas:
                num += 1
        numeros.append(num)
    return numeros

# Definindo os botões
for i in range(colunas * linhas):
    botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
    botao.bind("<Button-1>", lambda event, i=i: clique_botao(i))
    botao.bind("<ButtonRelease-1>", lambda event, i=i: desclique_botao(i))
    botao.bind("<Button-3>", lambda event, i=i: bandeirinha(i))
    botoes.append(botao)

# Colocando os botões na tela
for i in range(colunas * linhas):
    botoes[i].grid(row=math.floor(i / colunas), column=i % colunas)

root.mainloop()