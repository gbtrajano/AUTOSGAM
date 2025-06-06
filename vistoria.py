# IMPORTS
import tkinter as tk
import pyautogui
import time
from tkinter import font as tkfont

def obter_texto_e_executar():
    """Obtém o texto das entradas do formulário Tkinter e executa o PyAutoGUI."""
    Funcionario = entry1.get()
    Data = entry2.get()
    
    root.destroy()  # Fecha a janela Tkinter após obter os dados

    time.sleep(1)

    pyautogui.moveTo(1196, 493)
    pyautogui.click()

    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    # SCROLL
    pyautogui.moveTo(1355, 337)
    pyautogui.click()

    time.sleep(1)
    pyautogui.moveTo(567, 420)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(Funcionario)
    time.sleep(1)

    pyautogui.moveTo(567, 455)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(Funcionario)
    time.sleep(1)

    pyautogui.moveTo(567, 490)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(Funcionario)
    time.sleep(1)

    pyautogui.moveTo(567, 525)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(Funcionario)
    time.sleep(1)

    pyautogui.moveTo(567, 560)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(Funcionario)
    time.sleep(1)

    pyautogui.moveTo(1001, 420)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(Data)

    integerData = int(Data)
    integerData += 2
    Data = str(integerData)

    pyautogui.moveTo(1001, 455)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(Data)

    pyautogui.moveTo(1001, 490)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(Data)

    integerData += 2
    Data = str(integerData)

    pyautogui.moveTo(1001, 525)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(Data)

    pyautogui.moveTo(1001, 560)
    pyautogui.click()
    time.sleep(2)
    pyautogui.typewrite(Data)



    # BOTÃO SALVAR
    # pyautogui.moveTo(293, 221)
    # pyautogui.click()
    # time.sleep(2)

# # Configuração da janela principal
root = tk.Tk()
root.title("AUTOMAÇÃO")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Estilos
cor_fundo = "#f0f0f0"
cor_botao = "#4a7a8c"
cor_texto_botao = "white"
cor_entry = "white"
fonte_labels = tkfont.Font(family="Segoe UI", size=10)
fonte_botao = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# Frame principal para organização
main_frame = tk.Frame(root, bg=cor_fundo)
main_frame.pack(pady=20)

# Função para criar campos de forma consistente
def criar_campo(frame, texto, linha):
    label = tk.Label(frame, text=texto, bg=cor_fundo, font=fonte_labels)
    label.grid(row=linha, column=0, padx=10, pady=5, sticky="e")
    
    entry = tk.Entry(frame, bg=cor_entry, relief="flat", highlightthickness=1, 
                    highlightcolor="#4a7a8c", highlightbackground="#cccccc")
    entry.grid(row=linha, column=1, padx=10, pady=5, ipady=3)
    
    return entry

# Criando os campos usando a função
entry1 = criar_campo(main_frame, "Funcionário:", 0)
entry2 = criar_campo(main_frame, "Funcionário:", 1)

# Botão estilizado
botao_enviar = tk.Button(
    main_frame, 
    text="INICIAR PREENCHIMENTO", 
    command=obter_texto_e_executar,
    bg=cor_botao,
    fg=cor_texto_botao,
    font=fonte_botao,
    relief="flat",
    padx=20,
    pady=8,
    bd=0,
    activebackground="#3a6a7c",
    activeforeground="white"
)
botao_enviar.grid(row=8, column=0, columnspan=2, pady=20)

# Adicionando um separador visual antes do botão
separador = tk.Frame(main_frame, height=2, bg="#cccccc")
separador.grid(row=7, column=0, columnspan=2, pady=10, sticky="we")

# Centralizar tudo
for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=2)

root.mainloop()