# SCRIPT PARA OS COM ENCARREGADO

import tkinter as tk
import pyautogui
import time

def obter_texto_e_executar():
    """Obtém o texto das entradas do formulário Tkinter e executa o PyAutoGUI."""
    Ordem = entry1.get()
    Funcionario1 = entry2.get()
    Funcionario2 = entry3.get()
    Funcionario3 = entry4.get()
    Data1 = entry5.get()
    HoraInicial1 = entry6.get()
    HoraFinal1 = entry7.get()
    HoraFinal2 = entry8.get()
    

    root.destroy()  # Fecha a janela Tkinter após obter os dados

    # CAMPO DA OS
    pyautogui.moveTo(87, 221)
    pyautogui.click()
    pyautogui.typewrite(Ordem)
    pyautogui.press('enter')

    time.sleep(2)

    # # CAMPO UTILIZADOS
    # pyautogui.moveTo(909, 258)
    # pyautogui.click()

    # time.sleep(2)

    # SCROLL 
    pyautogui.moveTo(1357, 704)
    pyautogui.doubleClick()

    # NOVA LINHA
    pyautogui.moveTo(909, 671)
    pyautogui.click()

    time.sleep(1)

    # PRIMEIRA MÃO DE OBRA
    pyautogui.moveTo(567, 579)
    pyautogui.click()
    pyautogui.typewrite(Funcionario1)

    # PRIMEIRA DATA
    pyautogui.moveTo(993, 579)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # PRIMEIRA HORA INICIAL
    pyautogui.moveTo(1113, 579)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraInicial1)

    # PRIMEIRA HORA FINAL
    pyautogui.moveTo(1200, 579)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraFinal1)

    # NOVA LINHA SEGUNDO FUNCIONÁRIO
    pyautogui.press('enter')

    time.sleep(1)

    # SCROLL PRA CIMA
    pyautogui.moveTo(1355, 337)
    pyautogui.click()

    # NOME SEGUNDO FUNCIONÁRIO
    pyautogui.moveTo(567, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(Funcionario2)

    # DATA SEGUNDO FUNCIONÁRIO
    pyautogui.moveTo(994, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # HORA INICIAL SEGUNDO FUNCIONÁRIO
    pyautogui.moveTo(1111, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraInicial1)

    # HORA FINAL SEGUNDO FUNCIONÁRIO
    pyautogui.moveTo(1197, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraFinal1)

    # NOVA LINHA TERCEIRO FUNCIONÁRIO
    pyautogui.press('enter')

    time.sleep(1)

    # SCROLL PRA CIMA
    pyautogui.moveTo(1355, 337)
    pyautogui.click()

    # NOME TERCEIRO FUNCIONÁRIO
    pyautogui.moveTo(567, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(Funcionario3)

    # DATA TERCEIRO FUNCIONÁRIO
    pyautogui.moveTo(994, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # HORA INICIAL TERCEIRO FUNCIONÁRIO
    pyautogui.moveTo(1111, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraInicial1)

    # HORA FINAL TERCEIRO FUNCIONÁRIO
    pyautogui.moveTo(1197, 559)
    pyautogui.click()
    time.sleep(0.75)
    pyautogui.typewrite(HoraFinal2)

    # BOTÃO SALVAR
    pyautogui.moveTo(293, 221)
    pyautogui.click()
    time.sleep(2)

    # BOTÃO EMAND
    pyautogui.moveTo(427, 222)
    pyautogui.click()
    time.sleep(3)

    # BOTÃO SALVAR EMAND
    pyautogui.moveTo(1007, 657)
    pyautogui.click()
    # time.sleep(15)

    # # BOTÃO EMAND NOVAMENTE
    # pyautogui.moveTo(427, 222)
    # pyautogui.click()
    # time.sleep(2)

    # # BOTÃO SALVAR EMAND NOVAMENTE
    # pyautogui.moveTo(1007, 657)
    # pyautogui.click()

# Cria a janela principal do Tkinter
root = tk.Tk()
root.title("SGAM")

# Cria os rótulos e campos de entrada
label1 = tk.Label(root, text="OS:")
label1.grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=5, pady=5)

label2 = tk.Label(root, text="Funcionário 1:")
label2.grid(row=1, column=0, padx=5, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=5, pady=5)

label3 = tk.Label(root, text="Funcionário 2:")
label3.grid(row=2, column=0, padx=5, pady=5)
entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, padx=5, pady=5)

label4 = tk.Label(root, text="Encarregado:")
label4.grid(row=3, column=0, padx=5, pady=5)
entry4 = tk.Entry(root)
entry4.grid(row=3, column=1, padx=5, pady=5)

label5 = tk.Label(root, text="Data:")
label5.grid(row=4, column=0, padx=5, pady=5)
entry5 = tk.Entry(root)
entry5.grid(row=4, column=1, padx=5, pady=5)

label6 = tk.Label(root, text="Hora Inicial:")
label6.grid(row=5, column=0, padx=5, pady=5)
entry6 = tk.Entry(root)
entry6.grid(row=5, column=1, padx=5, pady=5)

label7 = tk.Label(root, text="Hora Final:")
label7.grid(row=6, column=0, padx=5, pady=5)
entry7 = tk.Entry(root)
entry7.grid(row=6, column=1, padx=5, pady=5)

label8 = tk.Label(root, text="Final Encarregado:")
label8.grid(row=7, column=0, padx=5, pady=5)
entry8 = tk.Entry(root)
entry8.grid(row=7, column=1, padx=5, pady=5)

# Cria o botão para iniciar o preenchimento
botao_enviar = tk.Button(root, text="Iniciar Preenchimento", command=obter_texto_e_executar)
botao_enviar.grid(row=8, column=0, columnspan=2, pady=10)

# Inicia o loop principal do Tkinter
root.mainloop()