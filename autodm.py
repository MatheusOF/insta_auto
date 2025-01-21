import mysql.connector
import pyautogui
import time
import pyperclip
import webbrowser
import csv
import customtkinter as ctk
import threading
import tkinter.messagebox  # Importando o messagebox do tkinter

# Função para verificar o login no banco de dados
def validar_login(username, password):
    try:
        # Conecta ao banco de dados (substitua com suas credenciais)
        conn = mysql.connector.connect(
            host="localhost",  # Endereço do servidor (pode ser localhost ou um IP do servidor remoto)
            user="root",  # Seu nome de usuário do banco de dados
            password="",  # Sua senha do banco de dados
            database="autodm"  # Nome do banco de dados que você criou
        )

        cursor = conn.cursor()

        # Consulta para verificar se o usuário e senha existem
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Verifica se o usuário foi encontrado
        usuario = cursor.fetchone()

        conn.close()  # Fecha a conexão com o banco de dados

        # Se o usuário for encontrado, retorna True
        return usuario is not None
    except mysql.connector.Error as err:
        print(f"Erro ao conectar com o banco de dados: {err}")
        return False

# Função chamada quando o botão de login for pressionado
def fazer_login():
    username = entry_username.get()  # Obtém o nome de usuário inserido
    password = entry_password.get()  # Obtém a senha inserida

    if validar_login(username, password):
        tkinter.messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {username}!")  # Alterado para tkinter.messagebox
        root_login.destroy()  # Fecha a janela de login
        abrir_janela_principal()  # Abre a janela principal
    else:
        tkinter.messagebox.showerror("Erro de login", "Nome de usuário ou senha incorretos.")  # Alterado para tkinter.messagebox

# Função para abrir a janela principal do programa após o login
def abrir_janela_principal():
    global root

    # Função para abrir o Instagram a partir de um link
    def abrir_instagram(link):
        webbrowser.open(link)
        time.sleep(5)  # Espera a página carregar (ajuste conforme necessário)

    # Função para enviar mensagem
    def enviar_mensagem(mensagem):
        pyperclip.copy(mensagem)
        pyautogui.click(963, 176)
        time.sleep(4)
        pyautogui.hotkey('ctrl', 'v')  # Cola a mensagem copiada
        time.sleep(3)
        pyautogui.press('enter')

    # Função para ler os links de um arquivo CSV
    def ler_links_csv(nome_arquivo):
        links = []
        with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                links.append(row[0])  # Adiciona o primeiro valor de cada linha (o link)
        return links

    # Função para selecionar o arquivo CSV
    def selecionar_arquivo_csv():
        file_path = ctk.filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            entry_arquivo_csv.delete(0, ctk.END)
            entry_arquivo_csv.insert(0, file_path)

    # Função para selecionar o arquivo de mensagem (.txt)
    def selecionar_arquivo_texto():
        file_path = ctk.filedialog.askopenfilename(title="Selecione o arquivo de mensagem (.txt)", filetypes=[("Text Files", "*.txt")])
        if file_path:
            entry_arquivo_texto.delete(0, ctk.END)
            entry_arquivo_texto.insert(0, file_path)

    # Função para ler o conteúdo do arquivo .txt
    def ler_arquivo_txt(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            return file.read().strip()

    # Função chamada quando o botão "Iniciar Envio" for pressionado
    def iniciar_envio():
        global enviando
        nome_arquivo_csv = entry_arquivo_csv.get()
        nome_arquivo_txt = entry_arquivo_texto.get()

        if not nome_arquivo_csv or not nome_arquivo_txt:
            tkinter.messagebox.showerror("Erro", "Por favor, selecione o arquivo CSV e o arquivo de texto.")  # Alterado para tkinter.messagebox
            return

        try:
            links_instagram = ler_links_csv(nome_arquivo_csv)
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")  # Alterado para tkinter.messagebox
            return

        try:
            mensagem = ler_arquivo_txt(nome_arquivo_txt)
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Erro ao ler o arquivo de mensagem: {e}")  # Alterado para tkinter.messagebox
            return

        button_iniciar.configure(state=ctk.DISABLED)
        button_pausar.configure(state=ctk.NORMAL)

        enviando = True
        for link in links_instagram:
            if not enviando:
                tkinter.messagebox.showinfo("Pausado", "O envio foi pausado.")  # Alterado para tkinter.messagebox
                break

            print(f"Abrindo o link: {link}")
            abrir_instagram(link)

            time.sleep(5)  # Aguarda o tempo necessário para carregar o perfil

            print(f"Enviando mensagem para o perfil: {link}")
            enviar_mensagem(mensagem)

            time.sleep(2)

        button_iniciar.configure(state=ctk.NORMAL)
        button_pausar.configure(state=ctk.DISABLED)

        tkinter.messagebox.showinfo("Concluído", "Mensagens enviadas para todos os perfis.")  # Alterado para tkinter.messagebox

    # Função chamada para pausar o envio
    def pausar_envio():
        global enviando
        enviando = False
        button_pausar.configure(state=ctk.DISABLED)
        button_iniciar.configure(state=ctk.NORMAL)

    # Função para iniciar o envio em uma thread separada
    def thread_iniciar_envio():
        threading.Thread(target=iniciar_envio).start()

    # Criação da janela principal
    root = ctk.CTk()
    root.title("Insta auto")
    root.geometry("500x450")
    root.iconbitmap("icone.ico")
    root.configure(bg="#242424")

    label_titulo = ctk.CTkLabel(root, text="Auto DM", font=("TT Rounds Neue Trial ExtraBold", 24))
    label_titulo.pack(pady=10)

    label_arquivo_csv = ctk.CTkLabel(root, text="Selecione o arquivo CSV com os links:")
    label_arquivo_csv.pack(pady=5)

    entry_arquivo_csv = ctk.CTkEntry(root, width=40)
    entry_arquivo_csv.pack(pady=5)

    button_selecionar_csv = ctk.CTkButton(root, text="Selecionar Arquivo", command=selecionar_arquivo_csv)
    button_selecionar_csv.pack(pady=5)

    label_arquivo_texto = ctk.CTkLabel(root, text="Selecione o arquivo de mensagem (.txt):")
    label_arquivo_texto.pack(pady=5)

    entry_arquivo_texto = ctk.CTkEntry(root, width=40)
    entry_arquivo_texto.pack(pady=5)

    button_selecionar_texto = ctk.CTkButton(root, text="Selecionar Arquivo", command=selecionar_arquivo_texto)
    button_selecionar_texto.pack(pady=5)

    button_iniciar = ctk.CTkButton(root, text="Começar a Enviar", command=thread_iniciar_envio)
    button_iniciar.pack(pady=10)

    button_pausar = ctk.CTkButton(root, text="Pausar", command=pausar_envio, state=ctk.DISABLED)
    button_pausar.pack(pady=5)

    enviando = False
    root.mainloop()

# Criação da janela de login
root_login = ctk.CTk()
root_login.title("Login")
root_login.geometry("400x300")

# Campos de entrada para o login
label_username = ctk.CTkLabel(root_login, text="Nome de usuário:")
label_username.pack(pady=10)
entry_username = ctk.CTkEntry(root_login, width=250)
entry_username.pack(pady=5)

label_password = ctk.CTkLabel(root_login, text="Senha:")
label_password.pack(pady=10)
entry_password = ctk.CTkEntry(root_login, width=250, show="*")
entry_password.pack(pady=5)

button_login = ctk.CTkButton(root_login, text="Entrar", command=fazer_login)
button_login.pack(pady=20)

root_login.mainloop()
