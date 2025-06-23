import tkinter as tk
import pyautogui
import time
from tkinter import font as tkfont

# Dicionário de nomes de funcionários e suas matrículas
funcionarios = {
    "Adriano": "T083413177",
    "Andre Carneiro": "T070908137",
    "Andre Guerreiro": "T032323127",
    "Carlos": "T000853027",
    "Genivaldo": "T076337747",
    "Ivan": "T107535307",
    "Jonathan": "T175557747",
    "Leonardo": "T123334397",
    "Luis": "T084053577",
    "Marcelo": "T015619407",
    "Reginaldo": "T135383327",
    "Ricardo": "T103416317",
    "Robson": "T095551577",
    "Rodrigo": "T090621807",
    "Leandro": "T089556007",
    "Ulysses": "T000257897",
    "Ygor": "T137582997"
}

class AutocompleteEntry(tk.Entry):
    def __init__(self, dict_funcionarios, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict_funcionarios = dict_funcionarios
        self.nomes = sorted(dict_funcionarios.keys())  # Lista de nomes ordenada
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.bind("<KeyRelease>", self.check_input)
        self.bind("<FocusOut>", self.hide_listbox)
        self.bind("<Return>", self.select_item)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        
        # Listbox para exibir sugestões
        self.lb = tk.Listbox(width=self["width"], height=5)
        self.lb.bind("<Button-1>", self.select_item)
        self.lb_visible = False

    def check_input(self, event):
        value = self.var.get()
        if value == "":
            self.hide_listbox()
        else:
            # Filtra a lista de nomes com base no texto digitado
            data = [nome for nome in self.nomes if value.lower() in nome.lower()]
            if data:
                if not self.lb_visible:
                    self.show_listbox()
                self.lb.delete(0, tk.END)
                for nome in data:
                    self.lb.insert(tk.END, nome)
            else:
                self.hide_listbox()

    def show_listbox(self):
        if not self.lb_visible:
            self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
            self.lb_visible = True

    def hide_listbox(self, event=None):
        if self.lb_visible:
            self.lb.place_forget()
            self.lb_visible = False

    def select_item(self, event=None):
        if self.lb_visible and self.lb.size() > 0:
            if event and event.widget == self.lb:
                index = self.lb.nearest(event.y)
            else:
                index = self.lb.curselection()[0] if self.lb.curselection() else 0
            nome_selecionado = self.lb.get(index)
            matricula = self.dict_funcionarios[nome_selecionado]
            self.var.set(matricula)
            self.hide_listbox()
            self.icursor(tk.END)
        return "break"

    def move_up(self, event):
        if self.lb_visible and self.lb.size() > 0:
            index = self.lb.curselection()[0] if self.lb.curselection() else 0
            if index > 0:
                self.lb.selection_clear(0, tk.END)
                self.lb.selection_set(index - 1)
                self.lb.activate(index - 1)
        return "break"

    def move_down(self, event):
        if self.lb_visible and self.lb.size() > 0:
            index = self.lb.curselection()[0] if self.lb.curselection() else -1
            if index < self.lb.size() - 1:
                self.lb.selection_clear(0, tk.END)
                self.lb.selection_set(index + 1)
                self.lb.activate(index + 1)
        return "break"

def obter_texto_e_executar():
    """Obtém o texto das entradas do formulário Tkinter e executa o PyAutoGUI."""
    Ordem = entry1.get()
    Funcionario1 = entry2.get()
    Funcionario2 = entry3.get()
    Data1 = entry5.get()
    HoraInicial1 = entry6.get()
    HoraFinal1 = entry7.get()

    # CAMPO DA OS
    pyautogui.moveTo(87, 221)
    pyautogui.click()
    pyautogui.typewrite("OS" + Ordem)
    pyautogui.press('enter')

    time.sleep(3.5)

    # SCROLL 
    pyautogui.moveTo(1357, 704)
    pyautogui.doubleClick()

    # NOVA LINHA
    pyautogui.moveTo(909, 671)
    pyautogui.click()

    time.sleep(2)

    # PRIMEIRA MÃO DE OBRA
    pyautogui.moveTo(567, 579)
    pyautogui.click()
    pyautogui.typewrite(Funcionario1)

    # PRIMEIRA DATA
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # PRIMEIRA HORA INICIAL
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(HoraInicial1)

    # PRIMEIRA HORA FINAL
    pyautogui.press('tab')
    time.sleep(1)
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
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # HORA INICIAL SEGUNDO FUNCIONÁRIO
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(HoraInicial1)

    # HORA FINAL SEGUNDO FUNCIONÁRIO
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(HoraFinal1)

    # BOTÃO SALVAR
    pyautogui.moveTo(293, 221)
    pyautogui.click()
    time.sleep(2)

# Configuração da janela principal
root = tk.Tk()
root.title("SCRIPT")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Estilos
cor_fundo = "#eee"
cor_botao = "black"
cor_texto_botao = "white"
cor_entry = "white"
fonte_labels = tkfont.Font(family="Segoe UI", size=10)
fonte_botao = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# Frame principal para organização
main_frame = tk.Frame(root, bg=cor_fundo)
main_frame.pack(pady=10)

# Função para criar campos de forma consistente
def criar_campo(frame, texto, linha, autocomplete=False):
    label = tk.Label(frame, text=texto, bg=cor_fundo, font=fonte_labels)
    label.grid(row=linha, column=0, padx=10, pady=5, sticky="e")
    
    if autocomplete:
        entry = AutocompleteEntry(
            funcionarios,
            frame,
            bg=cor_entry,
            relief="flat",
            highlightthickness=1,
            highlightcolor="#4a7a8c",
            highlightbackground="#cccccc"
        )
    else:
        entry = tk.Entry(
            frame,
            bg=cor_entry,
            relief="flat",
            highlightthickness=1,
            highlightcolor="#4a7a8c",
            highlightbackground="#cccccc"
        )
    
    entry.grid(row=linha, column=1, padx=10, pady=5, ipady=3)
    return entry

# Criando os campos usando a função
entry1 = criar_campo(main_frame, "OS:", 0)
entry2 = criar_campo(main_frame, "Funcionário 1:", 1, autocomplete=True)
entry3 = criar_campo(main_frame, "Funcionário 2:", 2, autocomplete=True)
entry5 = criar_campo(main_frame, "Data:", 3)
entry6 = criar_campo(main_frame, "Hora Inicial:", 4)
entry7 = criar_campo(main_frame, "Hora Final:", 5)

# Botão estilizado
botao_enviar = tk.Button(
    main_frame, 
    text="INICIAR", 
    command=obter_texto_e_executar,
    bg=cor_botao,
    fg=cor_texto_botao,
    font=fonte_botao,
    relief="flat",
    padx=20,
    pady=8,
    bd=0,
    activebackground="#0000ff",
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