from tkinter import *

def centraliza(raiz, largura, altura):
    # Designate Height and Width of our app
    app_width = largura
    app_height = altura

    screen_width = raiz.winfo_screenwidth()
    screen_height = raiz.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2 ) - (app_height / 2)

    raiz.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    # my_label = Label(root, text=f'Width:{screen_width}  Height:{screen_height}')
    # my_label.pack(pady=20)