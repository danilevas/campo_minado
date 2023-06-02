from tkinter import *
import math
import random
from datetime import datetime
from PIL import ImageTk, Image
import pygame
from center import centraliza

# Feito: 
#   - A primeira casa que o jogador clica sempre ser vazia para abrir o jogo, ou seja, só colocar as bombas e números depois dele clicar
#   - Poder clicar nos números quando o requerimento dele já foi preenchido para revelar todos os outros vizinhos (inclusive bombas, que se tiver explode!)
#       - Se o requerimento não tiver sido completo, piscar os vizinhos não marcados
#   - Colocar som! (tictic para apertar e BOOM para a bomba, yaaay para ganhar)
#   - Ajeitar problema que quando você marcou errados os vizinhos de um quadrado desabilitado clicado com requerimentos cumpridos, ele buga
#   - Ajeitar o tamanho da casa marcada que diminui um pouquinho
#   - Colocar popups quando ganha e perde
#   - Colocar um botão para reiniciar após esses popups
#   - Escolher nível/tamanho na tela, calcular bombas automaticamente
#   - Contador de bombas marcadas e de tempo corrido

# Próximos passos:
#   - Entender melhor a regra de revelação dos quadrados

root = Tk()
root.title("Campo Minado do Dani!")
pygame.mixer.init()

tamanho_x = 15
tamanho_y = 7.5
botoes = []
numeros = []
colunas = 9
linhas = 9
bombas = 10
lugar_bombas = []
marcados = []
vez = 0
afundados = []
game_over = False
data_tempo = None
halt = 0
primeira = True
resolvidos = []

path = "C:/Programas/Projetos Pessoais/tkinter/campo_minado_repo/"
root.iconbitmap(path + '/icones/bomba.ico')
imagens = [
    Image.open(path + "icones/flag resized.png"),       # 0
    Image.open(path + "icones/1.png"),                  # 1
    Image.open(path + "icones/2.png"),                  # 2
    Image.open(path + "icones/3.png"),                  # 3
    Image.open(path + "icones/4.png"),                  # 4
    Image.open(path + "icones/5.png"),                  # 5
    Image.open(path + "icones/6.png"),                  # 6
    Image.open(path + "icones/7.png"),                  # 7
    Image.open(path + "icones/8.png"),                  # 8
    Image.open(path + "icones/fundo.png"),              # 9
    Image.open(path + "icones/fundo.png"),              # 10
    Image.open(path + "icones/bomba.png"),              # 11
    Image.open(path + "icones/bomba red.png"),          # 12
    Image.open(path + "icones/bomba X.png"),            # 13
    Image.open(path + "icones/carinha feliz.png"),      # 14
    Image.open(path + "icones/carinha ooo.png"),        # 15
    Image.open(path + "icones/carinha morta.png"),      # 16
    Image.open(path + "icones/carinha oculos.png"),     # 17
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
        resized_image = img.resize((int(tamanho_x*2), int(tamanho_x*2.1)), Image.ANTIALIAS)
    elif i >= 14 and i <= 17:
        resized_image = img.resize((int(tamanho_x*3.2), int(tamanho_x*3.2)), Image.ANTIALIAS)
    else:
        resized_image = img.resize((int(tamanho_x*2.3), int(tamanho_x*2.36)), Image.ANTIALIAS)
    imagens_prontas.append(ImageTk.PhotoImage(resized_image))

num_bombas = Label(root, relief=SUNKEN, padx=tamanho_x*2, pady=tamanho_y, borderwidth=3, text="", font=(24), fg="red", bg="black")
carinha = Label(root, relief=RAISED, padx=tamanho_x*2, pady=tamanho_y*2, borderwidth=3, bg="#BDBDBD", image=imagens_prontas[14])
tempo = Label(root, relief=SUNKEN, padx=tamanho_x*2, pady=tamanho_y, borderwidth=3, text="0", font=(24), fg="red", bg="black")

def janela_menu():
    frame = LabelFrame(root, padx=25, pady=25)
    frame.pack(padx=10, pady=10)
    titulo = Label(frame, text="CAMPO MINADO DO DANI")
    espaco = Label(frame)
    subtitulo = Label(frame, text="ESCOLHA A DIFICULDADE")
    
    btn1 = Button(frame, text="FÁCIL", command= lambda: comeca_jogo(frame, "facil", False))
    btn2 = Button(frame, text="MÉDIO", command= lambda: comeca_jogo(frame, "medio", False))
    btn3 = Button(frame, text="DIFÍCIL", command= lambda: comeca_jogo(frame, "dificil", False))
    
    titulo.grid(row=0, column=0, columnspan=3)
    espaco.grid(row=1, column=0, columnspan=3)
    subtitulo.grid(row=2, column=0, pady=10, columnspan=3)
    btn1.grid(row=3,column=0)
    btn2.grid(row=3,column=1)
    btn3.grid(row=3,column=2)

def desabilita(label):
    label.configure(borderwidth=1, highlightbackground = "#7F7F7F", highlightcolor= "#7F7F7F")

def desabilitado(label):
    if label["borderwidth"] == 1:
        return True
    else:
        return False

def play(som):
    if som == "tic":
        pygame.mixer.music.load(path + "sons/tic_mais_baixo.wav")
        pygame.mixer.music.play(loops=0)
    if som == "boom":
        pygame.mixer.music.load(path + "sons/perdeu.wav")
        pygame.mixer.music.play(loops=0)
    if som == "ganhou":
        pygame.mixer.music.load(path + "sons/ganhou.wav")
        pygame.mixer.music.play(loops=0)

def clock(reseta=0):
    global halt
    global data_tempo
    if reseta == 1 or data_tempo == None:
        data_tempo = datetime.now()
    segundagem = datetime.now() - data_tempo
    if halt == 0:
        seg_exato = round(segundagem.total_seconds(), 0)
    elif halt == 1:
        seg_exato = 0
    if halt < 2:
        tempo.config(text=str(int(seg_exato)))
    if halt == 0:
        tempo.after(1000, clock)

def marca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[0], pady=tamanho_y+1)
    marcados.append(indice)
    num_bombas.configure(text=str(int(num_bombas["text"]) - 1))

def desmarca(indice):
    label = botoes[indice]
    label.configure(image=imagens_prontas[10])
    marcados.remove(indice)
    num_bombas.configure(text=str(int(num_bombas["text"]) + 1))

def marcado(indice):
    if indice in marcados:
        return True
    else:
        return False

def coloca_icone(label, numero):
    label.configure(image=imagens_prontas[numero], padx=tamanho_x-1, pady=tamanho_y+1)

def revelar_vizinhos(indice):
    inicio = True
    fila = [indice]
    while fila:
        atual = fila.pop(0)
        desabilita(botoes[atual])
            
        if numeros[atual] == 0:
            inicio = False
            for vizinho in obter_vizinhos(atual):
                if (not desabilitado(botoes[vizinho])) and vizinho not in lugar_bombas:
                    desabilita(botoes[vizinho])
                    if numeros[vizinho] > 0:
                        coloca_icone(botoes[vizinho], numeros[vizinho])
                    else:
                        coloca_icone(botoes[vizinho], 9)
                        fila.append(vizinho)
                        
def revelar_vizinhos_desabilitado(indice):
    # Primeiro checando se algum dos vizinhos era uma bomba desmarcada
    for vizinho in obter_vizinhos(indice):
        if vizinho in lugar_bombas and (not marcado(vizinho)):
            perdeu(vizinho)
            return

    for vizinho in obter_vizinhos(indice):
        if (not desabilitado(botoes[vizinho])) and vizinho not in lugar_bombas:
            desabilita(botoes[vizinho])
            if numeros[vizinho] > 0:
                coloca_icone(botoes[vizinho], numeros[vizinho])
            else:
                coloca_icone(botoes[vizinho], 9)
                revelar_vizinhos(vizinho)

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
    carinha.configure(image=imagens_prontas[15])
    
    # Se estiver marcado, não faz nada
    if indice in marcados or game_over == True:
        return
    
    # A label abaixa quando é clicada
    label.config(relief=SUNKEN)
    
    if desabilitado(botoes[indice]) and numeros[indice] > 0:
        num = 0
        for vizinho in obter_vizinhos(indice):
            if marcado(vizinho):
                num += 1
        if num < numeros[indice]:
            global afundados
            afundados = []
            for vizinho in obter_vizinhos(indice):
                if not marcado(vizinho) and not desabilitado(botoes[vizinho]):
                    botoes[vizinho].config(relief=SUNKEN)
                    afundados.append(botoes[vizinho])

def desclique_botao(indice):
    global primeira
    primeira = False
    label = botoes[indice]
    carinha.configure(image=imagens_prontas[14])
    
    play("tic")
    
    # Se estiver marcado, não faz nada
    if indice in marcados or game_over == True:
        return
    
    for elemento in afundados:
        elemento.config(relief=RAISED)
    
    global vez
    if vez == 0:
        sortea_bombas(indice)
        coloca_numeros()
        vez += 1

    label.config(relief=RAISED)
    
    if indice in lugar_bombas:
        # VOCÊ PERDEU!
        perdeu(indice)
        
    elif not desabilitado(botoes[indice]):
        if numeros[indice] > 0:
            coloca_icone(label, numeros[indice])
        else:
            coloca_icone(label, 9)
        desabilita(label)
        revelar_vizinhos(indice)
        checa_ganhou()
    
    # Clicar no número já revelado para revelar seus vizinhos se seu requerimento já foi cumprido
    else:
        if numeros[indice] > 0:
            num = 0
            for vizinho in obter_vizinhos(indice):
                if marcado(vizinho):
                    num += 1
            if num == numeros[indice]:
                revelar_vizinhos_desabilitado(indice)
                checa_ganhou()

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
    if desabilitado(botoes[indice]) or game_over == True:
        return
    if not marcado(indice):
        marca(indice)
        checa_ganhou()
    else:
        desmarca(indice)

def checa_ganhou():
    temp = 0
    marcados.sort()
    for i in range(colunas * linhas):
        if desabilitado(botoes[i]) and i not in lugar_bombas:
            temp += 1
    if lugar_bombas == marcados and temp == (colunas * linhas) - bombas:
        # VOCÊ GANHOU!
        global halt
        halt = 2
        carinha.configure(image=imagens_prontas[17])
        janela_vitoria()
        play("ganhou")

def janela_vitoria():
    top = Toplevel()
    top.title = "VITÓRIA"
    top.configure(bg="#BDBDBD")
    
    # frame = LabelFrame(top, padx=25, pady=25)
    # frame.pack(padx=10, pady=10)
    titulo = Label(top, text="PARABÉNS VOCÊ GANHOU!", bg="#BDBDBD")
    espaco = Label(top, bg="#BDBDBD")
    
    btn1 = Button(top, bg="#BDBDBD", text="OK! Sou brabo hehe", command= lambda: top.destroy())
    
    titulo.grid(row=0, column=0, columnspan=3)
    espaco.grid(row=1, column=0, columnspan=3)
    btn1.grid(row=2,column=0)
    centraliza(top, 250, 140)

def perdeu(indice):
    carinha.configure(image=imagens_prontas[16])
    label = botoes[indice]
    print(f"Clicado: {indice}")
    print(f"Bombas estão nos índices: {lugar_bombas}")
    
    label.configure(image=imagens_prontas[12], padx=tamanho_x*0.65) # bomba com fundo vermelho
    desabilita(label)
    global game_over
    game_over = True # Para ninguém poder clicar mais em nada depois que o jogo termina
    global halt
    halt = 2
    
    for i in range(linhas * colunas):
        if i != indice:
            if i in lugar_bombas and not marcado(i):
                botoes[i].configure(image=imagens_prontas[11]) # , padx=tamanho_x*0.65)
                desabilita(botoes[i])
            elif i not in lugar_bombas and marcado(i):
                botoes[i].configure(image=imagens_prontas[13]) # , padx=tamanho_x*0.65)
                desabilita(botoes[i])

    janela_derrota()
    play("boom")
    # root.after(2000, root.destroy)  # Delay for 2 seconds before closing the window

def janela_derrota():
    top = Toplevel()
    top.title = "DERROTA"
    top.configure(bg="#BDBDBD")
    
    frame = LabelFrame(top, padx=25, pady=25)
    frame.pack(padx=10, pady=10)
    titulo = Label(frame, text="INFELIZMENTE VOCÊ PERDEU") # colocar uma frase inspiracional em itálico
    espaco = Label(frame)
    
    btn1 = Button(frame, text=":( na próxima eu consigo", command= lambda: top.destroy())
    
    titulo.grid(row=0, column=0, columnspan=3)
    espaco.grid(row=1, column=0, columnspan=3)
    btn1.grid(row=3,column=0)
    centraliza(top, 250, 140)

def clique_carinha(event):
    event.widget.configure(relief=SUNKEN)

def desclique_carinha( dificuldade):
    global carinha
    carinha.configure(relief=RAISED, image=imagens_prontas[14])
    restart(dificuldade)

def restart(dificuldade):
    global botoes
    global numeros
    global lugar_bombas
    global marcados
    global afundados
    global game_over
    global vez
    pygame.mixer.music.stop()
    for i in range(colunas*linhas):
        botoes[i].destroy()
    botoes = []
    numeros = []
    lugar_bombas = []
    marcados = []
    afundados = []
    game_over = False
    vez = 0
    comeca_jogo(None, dificuldade, False)

def sortea_bombas(clicado):
    # Sorteando as bombas
    vizinhos_clicado = obter_vizinhos(clicado)
    vizinhos_clicado.append(clicado)
    print(f"Botão clicado: {clicado}\nSeus vizinhos: {vizinhos_clicado}")
    i = 0
    while i < bombas:
        local_bomba = random.randint(0, (colunas * linhas) - 1)
        if local_bomba not in lugar_bombas and local_bomba not in vizinhos_clicado:
            lugar_bombas.append(local_bomba)
            # botoes[local_bomba].configure(bg="red")
            i += 1
    lugar_bombas.sort()
    print(f"Bombas estão nos índices: {lugar_bombas}")

def coloca_numeros():
    # Colocando os números nos quadrados sem bomba
    for i in range(colunas * linhas):
        if i in lugar_bombas:
            numeros.append(0)
            print(f"Botão {i} : é bomba!")
            continue
        num = 0
        for vizinho in obter_vizinhos(i):
            if vizinho in lugar_bombas:
                num += 1
        numeros.append(num)
        print(f"Botão {i} : {num} bombas a seu redor")
    
    # Iniciando o relógio
    global halt
    halt = 0
    clock(1)

def comeca_jogo(frame, dificuldade, inicio):
    global primeira
    global resolvidos
    primeira = True
    resolvidos = []
    
    if frame != None:
        frame.destroy()
    
    # Parando o relógio
    global halt
    halt = 1
    tempo.configure(text="0")
    
    root.configure(bg='#BDBDBD')
    global colunas
    global linhas
    global bombas
    
    # Colocando um menuzinho para escolher a dificuldade
    menubar = Menu(root)
    dif_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Dificuldade", menu=dif_menu)
    dif_menu.add_command(label="Fácil", command= lambda dificuldade="facil": restart(dificuldade))
    dif_menu.add_command(label="Médio", command= lambda dificuldade="medio": restart(dificuldade))
    dif_menu.add_command(label="Difícil", command= lambda dificuldade="dificil": restart(dificuldade))
    
    res_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Resolver", menu=res_menu)
    res_menu.add_command(label="Resolver?", command=resolve)
    res_menu.add_command(label="Resolver rápido?", command=resolve_rapido)
    root.config(menu=menubar)
    
    if dificuldade == "facil":
        colunas = 9
        linhas = 9
        bombas = 10
        if inicio == True:
            centraliza(root, int(colunas*36), int(linhas*(36.85 + 11.8 + 2.2)))
        else:
            centraliza(root, int(colunas*36), int(linhas*(36.85 + 11.8)))
    if dificuldade == "medio":
        colunas = 16
        linhas = 16
        bombas = 40
        centraliza(root, int(colunas*36), int(linhas*(36.85 + 6.7)))
    if dificuldade == "dificil":
        colunas = 30
        linhas = 16
        bombas = 99
        centraliza(root, int(colunas*36), int(linhas*(36.85 + 6.7)))
    
    # Definindo os botões
    for i in range(colunas * linhas):
        botao = Label(root, relief=RAISED, padx=tamanho_x, pady=tamanho_y, borderwidth=3, bg="#BDBDBD")
        botao.bind("<Button-1>", lambda event, i=i: clique_botao(i))
        botao.bind("<ButtonRelease-1>", lambda event, i=i: desclique_botao(i))
        botao.bind("<Button-3>", lambda event, i=i: bandeirinha(i))
        botoes.append(botao)

    # Colocando os botões na tela
    carinha.bind("<Button-1>", clique_carinha)
    carinha.bind("<ButtonRelease-1>", lambda event, dificuldade=dificuldade: desclique_carinha(dificuldade))
    num_bombas.configure(text=str(bombas))
    tempo.configure(text=str(0))
    padding1 = Label(root, padx=tamanho_x/3, pady=tamanho_y/3, bg="#BDBDBD")
    padding2 = Label(root, padx=tamanho_x/3, pady=tamanho_y/3, bg="#BDBDBD")
    
    padding1.grid(row=1, column=0, columnspan=colunas)
    num_bombas.grid(row=2, column=0, columnspan=int(colunas/3))
    carinha.grid(row=2, column=int(colunas/3), columnspan=int(colunas/3))
    tempo.grid(row=2, column=int(colunas/3)*2, columnspan=int(colunas/3))
    padding2.grid(row=3, column=0, columnspan=colunas)
    for i in range(colunas * linhas):
        botoes[i].grid(row=math.floor(i / colunas) + 4, column=i % colunas)

# Resolve checando apenas os números dos quadrados à vista, se não conseguir assim, marca uma bomba
def resolve():
    global primeira
    if not primeira:
        mudei = False
        for i in range(linhas * colunas):
            
            # Marca os que só tem a quantidade certa pra marcar
            if desabilitado(botoes[i]) and numeros[i] > 0 and (i not in resolvidos):
                marcados = 0
                candidatos = []
                for v in obter_vizinhos(i):
                    if not desabilitado(botoes[v]) and not marcado(v):
                        candidatos.append(v)
                    if marcado(v):
                        marcados += 1
                if len(candidatos) == numeros[i] - marcados and len(candidatos) != 0:
                    for candidato in candidatos:
                        bandeirinha(candidato)
                    resolvidos.append(i)
                    mudei = True
                    break
                
                # Abre os com requisito concluído
                if numeros[i] - marcados == 0 and len(candidatos) != 0:
                    clique_botao(i)
                    desclique_botao(i)
                    resolvidos.append(i)
                    mudei = True
                    break
                
                # Se já estiver a quantidade certa marcada, está resolvido
                if len(candidatos) == 0:
                    resolvidos.append(i)
        
        # Se não tiver dado break em nenhum outro momento é pq não tem o que fazer usando as regras, então
        # ele vai marcar uma bomba aleatória para ajudar
        if mudei == False:
            for bomba in lugar_bombas:
                if not marcado(bomba):
                    marca(bomba)
                    break

    if primeira:
        inicial = random.randint(0, (colunas * linhas) - 1)
        clique_botao(inicial)
        desclique_botao(inicial)
        primeira = False

# Resolve rápido checando apenas os números dos quadrados à vista, se não conseguir assim, marca uma bomba
def resolve_rapido():
    global primeira
    if not primeira:
        mudei = False
        for i in range(linhas * colunas):
            
            # Marca os que só tem a quantidade certa pra marcar
            if desabilitado(botoes[i]) and numeros[i] > 0 and (i not in resolvidos):
                marcados = 0
                candidatos = []
                for v in obter_vizinhos(i):
                    if not desabilitado(botoes[v]) and not marcado(v):
                        candidatos.append(v)
                    if marcado(v):
                        marcados += 1
                if len(candidatos) == numeros[i] - marcados and len(candidatos) != 0:
                    for candidato in candidatos:
                        bandeirinha(candidato)
                    resolvidos.append(i)
                    mudei = True
                
                # Abre os com requisito concluído
                if numeros[i] - marcados == 0 and len(candidatos) != 0:
                    clique_botao(i)
                    desclique_botao(i)
                    resolvidos.append(i)
                    mudei = True
                
                # Se já estiver a quantidade certa marcada, está resolvido
                if len(candidatos) == 0:
                    resolvidos.append(i)
        
        # Se não tiver dado break em nenhum outro momento é pq não tem o que fazer usando as regras, então
        # ele vai marcar uma bomba aleatória para ajudar
        if mudei == False:
            for bomba in lugar_bombas:
                if not marcado(bomba):
                    marca(bomba)

    if primeira:
        inicial = random.randint(0, (colunas * linhas) - 1)
        clique_botao(inicial)
        desclique_botao(inicial)
        primeira = False

comeca_jogo(None, "facil", True)
root.mainloop()