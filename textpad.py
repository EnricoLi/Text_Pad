from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

from fpdf import FPDF

import os
import sys
import win32print
import win32api

raiz = Tk()
raiz.title('TextPad')
#raiz.iconbitmap()
raiz.geometry("1200x660")

# Define a variavel global para vericar o nome do arquivo
global open_status_name
open_status_name = False

global selected
selected = False

# Criar novo arquivo
def new_file():
    texto.delete("1.0", END)
    raiz.title('New File - TextPad')
    global open_status_name
    open_status_name = False

# Abre arquivos
def open_file():
    texto.delete("1.0", END)

    # Pegar o nome do arquivo
    text_file = filedialog.askopenfilename(initialdir="C:/", 
                        title="Open File", 
                        filetypes=(("Text Files", "*.txt"), 
                        ("HTML Files", "*html"), 
                        ("Python Files", "*.py"), 
                        ("All Files", "*.*")))
    
    # Verifica o nome do arquivo e salva em uma variavel global
    if text_file:
        global open_status_name
        open_status_name = text_file

    # Abrir o arquivo
    text_file = open(text_file, 'r')
    stuff = text_file.read()

    # Adiciona o arquivo a caixa de texto
    texto.insert(END, stuff)
    # Fecha o arquivo
    text_file.close()

# Salva os arquivos como
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", 
                            initialdir="C:/", title="Save file", 
                            filetypes=(("Text Files", "*.txt"), 
                            ("HTML Files", "*.html"), 
                            ("Python Files", "*.py"), 
                            ("All Files", "*.*")))
    if text_file:
        name = text_file
        name = name.replace("C:/", "")
        raiz.title('Save As - TextPad')

    # Salvar o arquivo
    text_file = open(text_file, 'w')
    text_file.write(texto.get(1.0, END))
    # Fecha o arquivo
    text_file.close()

# Salvar o arquivo
def save_file():
    global open_status_name
    if open_status_name:
        # Salvar o arquivo
        text_file = open(open_status_name, 'w')
        text_file.write(texto.get(1.0, END))
        # Fecha o arquivo
        text_file.close()
    else:
        save_as_file()

# Recorta o texto
def cut_text(e):
    global selected
    # Verifica se está utilizando o atalho do teclado
    if e:
        selected = raiz.clipboard_get()
    else:
        if texto.selection_get():
            # Pega o texto selecionado da caixa de texto
            selected = texto.selection_get()
            # Deleta o texto selecionado da caixa de texto
            texto.delete("sel.first", "sel.last")
            # Limpa o clipboard e adiciona o selecionado
            raiz.clipboard_clear()
            raiz.clipboard_append(selected)


# Copia o texto
def copy_text(e):
    global selected
    # Verifica se está utilizando o atalho do teclado
    if e:
        selected = raiz.clipboard_get()
    if texto.selection_get():
        # Pega o texto selecionado da caixa de texto
        selected = texto.selection_get()
        # Limpa o clipboard e adiciona o selecionado
        raiz.clipboard_clear()
        raiz.clipboard_append(selected)

# Cola o texto
def paste_text(e):
    global selected
    # Verifica se está utilizando o atalho do teclado
    if e:
        selected = raiz.clipboard_get()
    else:
        if selected:
            position = texto.index(INSERT)
            texto.insert(position, selected)

# Bold Text
def bold_it():
    bold_font = font.Font(texto, texto.cget("font"))
    bold_font.configure(weight="bold")

    # Configura um tag
    texto.tag_configure("bold", font=bold_font)

    # Define current tags
    current_tags = texto.tag_names("sel.first")

    # Verifica se o estado está ativo
    if "bold" in current_tags:
        texto.tag_remove("bold", "sel.first", "sel.last")
    else:
        texto.tag_add("bold", "sel.first", "sel.last")

# Italics Text
def italics_it():
    italics_font = font.Font(texto, texto.cget("font"))
    italics_font.configure(slant="italic")

    # Configura um tag
    texto.tag_configure("italic", font=italics_font)

    # Define current tags
    current_tags = texto.tag_names("sel.first")

    # Verifica se o estado está ativo
    if "italics" in current_tags:
        texto.tag_remove("italic", "sel.first", "sel.last")
    else:
        texto.tag_add("italic", "sel.first", "sel.last")

# Muda a cor do texto selecionado
def text_color():
    # Escolhe a cor
    minha_cor = colorchooser.askcolor()[1]
    if minha_cor:
        # Cria a fonte
        color_font = font.Font(texto, texto.cget("font"))

        # Configura um tag
        texto.tag_configure("colored", font=color_font, foreground=minha_cor)

        # Define current tags
        current_tags = texto.tag_names("sel.first")

        # Verifica se o estado está ativo
        if "colored" in current_tags:
            texto.tag_remove("colored", "sel.first", "sel.last")
        else:
            texto.tag_add("colored", "sel.first", "sel.last")

# Muda a cor de fundo
def bg_color():
    minha_cor = colorchooser.askcolor()[1]
    if minha_cor:
        texto.config(bg=minha_cor)

# Muda a cor de todo o texto
def all_text_color():
    minha_cor = colorchooser.askcolor()[1]
    if minha_cor:
        texto.config(fg=minha_cor)
# Cria um toolbar
toolbar_frame = Frame(raiz)
toolbar_frame.pack(fill=X)

# Função imprimir o arquivo
def print_file():
    file_to_print= filedialog.askopenfilename(initialdir="C:/", 
                        title="Open File", 
                        filetypes=(("Text Files", "*.txt"), 
                        ("HTML Files", "*.html"), 
                        ("Python Files", "*.py"), 
                        ("All Files", "*.*")))
    if file_to_print:
        win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)

# Seleciona todo o texto
def select_all(e):
    # Adiciona a tag de seleção de todo o texto
    texto.tag_add('sel', '1.0', 'end')

# Limpa a caixa de texto
def clear_all(e):
    texto.delete(1.0, END)
# Cria a tela principal
tela_principal = Frame(raiz)
tela_principal.pack(pady=5)

# Gera um arquivo em pdf
def pdf_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".pdf", 
                            initialdir="C:/", title="Save file",
                            filetypes=(("PDF Files", "*.pdf"),
                                        ("All Files", "*.*")))
                            
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 13.0)
    pdf.cell(ln=0, h=5.0, align='L', w=0, txt=texto.get(1.0, END), border=0)
    pdf.output(text_file, 'F')


# Cria a Scrollbar para a caixa de texto
text_scroll = Scrollbar(tela_principal)
text_scroll.pack(side=RIGHT, fill=Y)

# Cria Scrollbar horizontal
hor_scroll = Scrollbar(tela_principal, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# Cria a caixa de texto
texto = Text(tela_principal, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
texto.pack()

# Configura a Scrollbar
text_scroll.config(command=texto.yview)
hor_scroll.config(command=texto.xview)

# Cria o menu
menu = Menu(raiz)
raiz.config(menu=menu)

# Adiciona as opções de arquivo ao menu 
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Print File", command=print_file)
file_menu.add_command(label="PDF File", command=pdf_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=raiz.quit)

# Adiciona as opções de editar ao menu
editar_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Editar", menu=editar_menu)
editar_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
editar_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
editar_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
editar_menu.add_separator()
editar_menu.add_command(label="Undo", command=texto.edit_undo, accelerator="(Ctrl+z)")
editar_menu.add_command(label="Redo", command=texto.edit_redo, accelerator="(Ctrl+y)")
editar_menu.add_separator()
editar_menu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")
editar_menu.add_command(label="Clear", command=lambda: clear_all(True), accelerator="(Ctrl+k)")

# Adiciona as opções de cor ao menu
cor_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Cores", menu=cor_menu)
cor_menu.add_command(label="Texto Selecionado", command=text_color)
cor_menu.add_command(label="Todo o Texto", command=all_text_color)
cor_menu.add_command(label="Cor de Fundo", command=bg_color)

# Edit teclas
raiz.bind('<Control-Key-x>', cut_text)
raiz.bind('<Control-Key-c>', copy_text)
raiz.bind('<Control-Key-v>', paste_text)
# Teclas de Seleção
raiz.bind('<Control-Key-a>', select_all)
raiz.bind('<Control-Key-k>', clear_all)

# Cria botões

# Bold botão
bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

# Italics botão
italics_button = Button(toolbar_frame, text="Italics", command=italics_it)
italics_button.grid(row=0, column=1, padx=5)

# Undo/Redo botões
undo_button = Button(toolbar_frame, text="Undo", command=texto.edit_undo)
undo_button.grid(row=0, column=2, padx=5)
redo_button = Button(toolbar_frame, text="Redo", command=texto.edit_redo)
redo_button.grid(row=0, column=3, padx=5)

# Cor do Texto
color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5)

raiz.mainloop()