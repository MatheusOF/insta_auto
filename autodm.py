import pyautogui
import time
import pyperclip
import webbrowser
import csv
import customtkinter as ctk
import threading

# Função para abrir o Instagram a partir de um link
def abrir_instagram(link):
    webbrowser.open(link)
    time.sleep(5)  # Espera a página carregar (ajuste conforme necessário)

# Função para enviar mensagem
def enviar_mensagem(mensagem):
    # Copia a mensagem para a área de transferência
    pyperclip.copy(mensagem)

    # Move o mouse até a posição para clicar (ajustar conforme necessário)
    pyautogui.click(963, 176)
    time.sleep(4)

    # Cola a mensagem
    pyautogui.hotkey('ctrl', 'v')  # Cola a mensagem copiada
    time.sleep(3)

    # Pressiona Enter para enviar a mensagem
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
        entry_arquivo_csv.delete(0, ctk.END)  # Limpa o campo de entrada
        entry_arquivo_csv.insert(0, file_path)  # Insere o caminho do arquivo

# Função para selecionar o arquivo de mensagem (.txt)
def selecionar_arquivo_texto():
    file_path = ctk.filedialog.askopenfilename(title="Selecione o arquivo de mensagem (.txt)", filetypes=[("Text Files", "*.txt")])
    if file_path:
        entry_arquivo_texto.delete(0, ctk.END)  # Limpa o campo de entrada
        entry_arquivo_texto.insert(0, file_path)  # Insere o caminho do arquivo

# Função para ler o conteúdo do arquivo .txt
def ler_arquivo_txt(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        return file.read().strip()  # Lê e remove espaços em branco extras

# Função chamada quando o botão "Iniciar Envio" for pressionado
def iniciar_envio():
    global enviando
    # Obtém o caminho do arquivo CSV e o arquivo de mensagem (.txt)
    nome_arquivo_csv = entry_arquivo_csv.get()
    nome_arquivo_txt = entry_arquivo_texto.get()

    # Verifica se os arquivos estão preenchidos
    if not nome_arquivo_csv or not nome_arquivo_txt:
        ctk.messagebox.showerror("Erro", "Por favor, selecione o arquivo CSV e o arquivo de texto.")
        return

    # Lê os links do arquivo CSV
    try:
        links_instagram = ler_links_csv(nome_arquivo_csv)
    except Exception as e:
        ctk.messagebox.showerror("Erro", f"Erro ao ler o arquivo CSV: {e}")
        return

    # Lê o conteúdo do arquivo de mensagem (.txt)
    try:
        mensagem = ler_arquivo_txt(nome_arquivo_txt)
    except Exception as e:
        ctk.messagebox.showerror("Erro", f"Erro ao ler o arquivo de mensagem: {e}")
        return

    # Desabilitar o botão "Iniciar Envio" enquanto o processo estiver em andamento
    button_iniciar.configure(state=ctk.DISABLED)
    button_pausar.configure(state=ctk.NORMAL)

    # Variável de controle para saber se o processo deve ser pausado
    enviando = True

    # Passo 1: Abre cada link de perfil do Instagram
    for link in links_instagram:
        if not enviando:
            ctk.messagebox.showinfo("Pausado", "O envio foi pausado.")
            break

        print(f"Abrindo o link: {link}")
        abrir_instagram(link)

        # Passo 2: Dê tempo para a página carregar
        time.sleep(5)  # Aguarda o tempo necessário para carregar o perfil

        # Passo 3: Envia a mensagem
        print(f"Enviando mensagem para o perfil: {link}")
        enviar_mensagem(mensagem)

        # Passo 4: Adiciona um pequeno delay entre as interações
        time.sleep(2)

    button_iniciar.configure(state=ctk.NORMAL)
    button_pausar.configure(state=ctk.DISABLED)

    ctk.messagebox.showinfo("Concluído", "Mensagens enviadas para todos os perfis.")

# Função chamada para pausar o envio
def pausar_envio():
    global enviando
    enviando = False
    button_pausar.configure(state=ctk.DISABLED)
    button_iniciar.configure(state=ctk.NORMAL)

# Função para iniciar o envio em uma thread separada (evitar travamento da interface)
def thread_iniciar_envio():
    threading.Thread(target=iniciar_envio).start()

# Criação da janela principal
root = ctk.CTk()
root.title("Insta auto")
root.geometry("500x450")

# Adicionar o ícone à janela (caminho para o arquivo .ico)
root.iconbitmap("icone.ico")  # Coloque o caminho correto para o seu arquivo .ico
root.configure(bg="#242424")  # Alterado para 'configure' em vez de 'config'

# Título
label_titulo = ctk.CTkLabel(root, text="Auto DM", font=("TT Rounds Neue Trial ExtraBold", 24))
label_titulo.pack(pady=10)

# Campo para inserir o arquivo CSV
label_arquivo_csv = ctk.CTkLabel(root, text="Selecione o arquivo CSV com os links:")
label_arquivo_csv.pack(pady=5)

entry_arquivo_csv = ctk.CTkEntry(root, width=40)
entry_arquivo_csv.pack(pady=5)

button_selecionar_csv = ctk.CTkButton(root, text="Selecionar Arquivo", command=selecionar_arquivo_csv)
button_selecionar_csv.pack(pady=5)

# Campo para inserir o arquivo de mensagem (.txt)
label_arquivo_texto = ctk.CTkLabel(root, text="Selecione o arquivo de mensagem (.txt):")
label_arquivo_texto.pack(pady=5)

entry_arquivo_texto = ctk.CTkEntry(root, width=40)
entry_arquivo_texto.pack(pady=5)

button_selecionar_texto = ctk.CTkButton(root, text="Selecionar Arquivo", command=selecionar_arquivo_texto)
button_selecionar_texto.pack(pady=5)

# Botão para iniciar o envio
button_iniciar = ctk.CTkButton(root, text="Começar a Enviar", command=thread_iniciar_envio)
button_iniciar.pack(pady=10)

# Botão para pausar o envio
button_pausar = ctk.CTkButton(root, text="Pausar", command=pausar_envio, state=ctk.DISABLED)
button_pausar.pack(pady=5)

# Inicia o loop da interface gráfica
enviando = False
root.mainloop()
