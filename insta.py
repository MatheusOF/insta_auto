import pyautogui
import time
import pyperclip
import webbrowser
import csv

# Função para abrir o Instagram a partir de um link
def abrir_instagram(link):
    webbrowser.open(link)
    time.sleep(5)  # Espera a página carregar (ajuste conforme necessário)

# Função para enviar mensagem
def enviar_mensagem(mensagem, posicao_x, posicao_y):
    # Copia a mensagem para a área de transferência
    pyperclip.copy(mensagem)

    # Move o mouse até a posição para clicar
    pyautogui.click(963, 176 )
    time.sleep(4)
    

    # Cola a mensagem
    pyautogui.hotkey('ctrl', 'v')  # Cola a mensagem copiada
    time.sleep(3)

    # Pressiona Enter para enviar a mensagem (ajuste conforme necessário)
    pyautogui.press('enter')

# Função para ler os links de um arquivo CSV
def ler_links_csv(nome_arquivo):
    links = []
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            links.append(row[0])  # Adiciona o primeiro valor de cada linha (o link)
    return links

# Defina o nome do arquivo CSV contendo os links dos perfis
nome_arquivo = 'links_instagram.csv'  # Altere para o nome do seu arquivo .csv

# Defina a mensagem que você quer enviar
mensagem = "Olá, vi em um post que você acompanha o Pablo Marçal, e tem vontade de investir. Trabalho com investimento em cartas de crédito, um invstimento de um ótimo retorno, 100% seguro. Estou oferecendo uma mentoria totalmente gratuita, responda está mensagem com MENTORIA caso queira mais informações."

# Defina a posição do clique (ajuste conforme necessário para seu caso)
# A posição é dada em pixels (x, y)
posicao_x = 500  # X é a posição horizontal
posicao_y = 500  # Y é a posição vertical

# Lê os links dos perfis do arquivo CSV
links_instagram = ler_links_csv(nome_arquivo)

# Passo 1: Abre cada link de perfil do Instagram
for link in links_instagram:
    print(f"Abrindo o link: {link}")
    abrir_instagram(link)

    # Passo 2: Dê tempo para a página carregar
    time.sleep(5)  # Aguarda o tempo necessário para carregar o perfil

    # Passo 3: Envia a mensagem
    print(f"Enviando mensagem para o perfil: {link}")
    enviar_mensagem(mensagem, posicao_x, posicao_y)

    # Passo 4: Adiciona um pequeno delay entre as interações
    time.sleep(2)

print("Mensagens enviadas para todos os perfis.")
