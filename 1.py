import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets, especially Notebook
from tkinter import font as tkfont
import pyautogui
import time
import sqlite3

# --- Database Setup ---
def setup_database():
    """Connects to the database and ensures the 'empregados' table exists and is populated."""
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS empregados (nome TEXT, maodeobra TEXT)")

    listaFuncionarios = [
        ("ADRIANO", "T083413177"), ("ALEXANDRE DE OLIVEIRA", "T084846967"),
        ("ANDRÉ LUIZ DOS SANTOS CARNEIRO", "T070908137"), ("ANDRÉ LUIZ GUERREIRO", "T032323127"),
        ("AUGUSTO CESAR", "T108752617"), ("CAIO DE ALMEIDA", "T189293597"),
        ("CARLOS JORGE DA SILVA OLIVEIRA", "T000853027"), ("DEIVER GOMES", "T082951967"),
        ("FABIO DE FREITAS", "T080925577"), ("FLAVIO RODRIGUES", "T076942977"),
        ("IVAN MARCELINO", "T107535307"), ("JEFFERSON MARCELO PEREIRA PINHEIRO", "T116297987"),
        ("JOÃO PEDRO GOULART", "T158289707"), ("JOÃO VICTOR", "T185915207"),
        ("JOHN GREISON", "T112999667"), ("JONATHAN SODRÉ", "T175557747"),
        ("JUCIANO", "T116398974"), ("JULIO CEZAR", "T152501977"),
        ("LEANDRO SILVA", "T089556007"), ("LEONARDO SIQUEIRA", "T123334397"),
        ("LUCIANO CHAVES", "T044019597"), ("LUCIANO FIGUEREDO", "T027235407"),
        ("LUIS ALBERTO", "T084053577"), ("MARCELO GOMES", "T015619407"),
        ("MAURO JOSÉ VILLARINHO JUNIOR", "T087764707"), ("PABLO LIMA FRANCO", "T173220207"),
        ("PABLO PEREIRA DA SILVA", "T138183317"), ("PAULO MARQUES DE OLIVEIRA", "T158813506"),
        ("PAULO VITOR DE OLIVEIRA GUINA", "T134249567"), ("REGINALDO FERREIRA DA PENHA", "T135383327"),
        ("RICARDO", "T103416317"), ("ROBSON PINTO", "T095551577"),
        ("RODRIGO BALA", "T090621807"), ("ULYSSES", "T000257897"),
        ("WELLINGTON", "T142545197"), ("YAN MOREIRA", "T146569937"),
        ("YGOR GABRIEL", "T137582997")
    ]

    # Insert only new employees to avoid duplicates
    for nome, maodeobra in listaFuncionarios:
        cursor.execute("SELECT COUNT(*) FROM empregados WHERE nome = ? AND maodeobra = ?", (nome, maodeobra))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO empregados VALUES (?,?)", (nome, maodeobra))

    conn.commit()
    conn.close()

# Initialize the database
setup_database()

def buscar_funcionarios(termo):
    """Busca funcionários no banco de dados que contenham o termo fornecido, retornando nome e maodeobra."""
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, maodeobra FROM empregados WHERE nome LIKE ? ORDER BY nome ASC", (f'%{termo}%',))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

class AutocompleteEntry(tk.Entry):
    """Um widget Entry que fornece sugestões de autocompletar de um banco de dados,
    e armazena a matrícula do funcionário selecionado."""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.lista_sugestoes = None
        self.termo_anterior = ''
        self.maodeobra_selecionada = None
        self.bind("<KeyRelease>", self._check_typing)
        self.bind("<Down>", self._move_to_suggestions)
        self.bind("<Return>", self._select_suggestion_enter)
        self.master.bind("<Button-1>", self._hide_suggestions_on_click_outside, add="+")

    def _check_typing(self, event):
        """Verifica a digitação do usuário e atualiza as sugestões."""
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Prior', 'Next', 'Home', 'End', 'Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R'):
            return

        current_term = self.get()
        if current_term == self.termo_anterior:
            return

        self.termo_anterior = current_term
        self._hide_suggestions()
        self.maodeobra_selecionada = None

        if current_term:
            suggestions = buscar_funcionarios(current_term)
            if suggestions:
                self._show_suggestions(suggestions)
        
    def _show_suggestions(self, suggestions):
        """Exibe as sugestões em um Listbox, mostrando 'Nome (Matrícula)'."""
        if not self.lista_sugestoes:
            self.lista_sugestoes = tk.Listbox(self.master, height=min(len(suggestions), 5), relief="flat",
                                                bg="white", highlightthickness=1, highlightcolor="#4a7a8c")
            
            # Position the listbox relative to the entry widget
            self.update_idletasks()
            x = self.winfo_x()
            y = self.winfo_y() + self.winfo_height()
            self.lista_sugestoes.place(x=x, y=y, width=self.winfo_width())

            self.lista_sugestoes.bind("<<ListboxSelect>>", self._select_suggestion)
            self.lista_sugestoes.bind("<Return>", self._select_suggestion_enter)
            self.lista_sugestoes.bind("<Button-1>", self._select_suggestion)

        self.lista_sugestoes.delete(0, tk.END)
        for nome, maodeobra in suggestions:
            self.lista_sugestoes.insert(tk.END, f"{nome} ({maodeobra})")
        
        self.lista_sugestoes.config(height=min(len(suggestions), 5))

    def _hide_suggestions(self):
        """Esconde a Listbox de sugestões."""
        if self.lista_sugestoes:
            self.lista_sugestoes.destroy()
            self.lista_sugestoes = None

    def _hide_suggestions_on_click_outside(self, event):
        """Esconde as sugestões se o clique do mouse ocorrer fora da Listbox ou da Entry."""
        if self.lista_sugestoes:
            x_mouse, y_mouse = event.x_root, event.y_root
            
            lb_x1, lb_y1 = self.lista_sugestoes.winfo_rootx(), self.lista_sugestoes.winfo_rooty()
            lb_x2, lb_y2 = lb_x1 + self.lista_sugestoes.winfo_width(), lb_y1 + self.lista_sugestoes.winfo_height()

            entry_x1, entry_y1 = self.winfo_rootx(), self.winfo_rooty()
            entry_x2, entry_y2 = entry_x1 + self.winfo_width(), entry_y1 + self.winfo_height()

            if not ((lb_x1 <= x_mouse <= lb_x2 and lb_y1 <= y_mouse <= lb_y2) or \
                    (entry_x1 <= x_mouse <= entry_x2 and entry_y1 <= y_mouse <= entry_y2)):
                self._hide_suggestions()

    def _select_suggestion(self, event):
        """Preenche a Entry com a MATRÍCULA selecionada e armazena a matrícula."""
        if self.lista_sugestoes and self.lista_sugestoes.curselection():
            index = self.lista_sugestoes.curselection()[0]
            displayed_value = self.lista_sugestoes.get(index)

            # Extract matricula from the displayed string "Name (Matricula)"
            matricula_start = displayed_value.rfind('(') + 1
            matricula_end = displayed_value.rfind(')')
            selected_matricula = displayed_value[matricula_start:matricula_end].strip()
            
            self.maodeobra_selecionada = selected_matricula
            self.delete(0, tk.END)
            self.insert(0, self.maodeobra_selecionada)
            self._hide_suggestions()
            self.focus_set()

    def _select_suggestion_enter(self, event):
        """Permite selecionar a sugestão com Enter tanto na Entry quanto na Listbox."""
        if self.lista_sugestoes and self.lista_sugestoes.curselection():
            self._select_suggestion(event)
        else:
            self.event_generate('<Tab>')

    def _move_to_suggestions(self, event):
        """Move o foco para a lista de sugestões ao pressionar Seta para Baixo."""
        if self.lista_sugestoes:
            self.lista_sugestoes.focus_set()
            self.lista_sugestoes.selection_set(0)
            self.lista_sugestoes.see(0)

# --- PyAutoGUI Automation Functions ---

def execute_pyautogui_actions(data):
    """Executes a series of PyAutoGUI actions based on provided data."""
    pyautogui.moveTo(87, 221)
    pyautogui.click()
    pyautogui.typewrite("OS" + data["Ordem"])
    pyautogui.press('enter')
    time.sleep(3.5)

    pyautogui.moveTo(1357, 704)
    pyautogui.doubleClick()

    pyautogui.moveTo(909, 671)
    pyautogui.click()
    time.sleep(2)

    # Helper for repetitive entry
    def fill_employee_data(matricula, data_val, hora_inicial, hora_final, is_first=False):
        if not is_first:
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.moveTo(1355, 337) # Scroll up
            pyautogui.click()
            pyautogui.moveTo(567, 559) # Position for subsequent employees
        else:
            pyautogui.moveTo(567, 579) # Position for first employee
        
        pyautogui.click()
        time.sleep(0.75)
        pyautogui.typewrite(matricula)
        
        pyautogui.press('tab')
        pyautogui.press('tab')
        time.sleep(0.75)
        pyautogui.typewrite(data_val)
        
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.typewrite(hora_inicial)
        
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.typewrite(hora_final)

    fill_employee_data(
        data["Funcionario1_matricula"] if data["Funcionario1_matricula"] else data["Funcionario1_nome_exibido"],
        data["Data1"], data["HoraInicial1"], data["HoraFinal1"], is_first=True
    )
    
    # Handle second employee for standard and third for supervisor
    if "Funcionario2_matricula" in data: # Standard Form
        fill_employee_data(
            data["Funcionario2_matricula"] if data["Funcionario2_matricula"] else data["Funcionario2_nome_exibido"],
            data["Data1"], data["HoraInicial1"], data["HoraFinal1"]
        )
    elif "Funcionario3_matricula" in data: # Supervisor Form
         fill_employee_data(
            data["Funcionario2_matricula"] if data["Funcionario2_matricula"] else data["Funcionario2_nome_exibido"],
            data["Data1"], data["HoraInicial1"], data["HoraFinal1"]
        )
         fill_employee_data(
            data["Funcionario3_matricula"] if data["Funcionario3_matricula"] else data["Funcionario3_nome_exibido"],
            data["Data1"], data["HoraInicial1"], data["HoraFinal2"]
        )


    pyautogui.moveTo(293, 221) # Save button
    pyautogui.click()
    time.sleep(2)

def get_and_execute_standard():
    """Obtém os dados do formulário padrão e executa as ações do PyAutoGUI."""
    data = {
        "Ordem": entries_padrao["OS"].get(),
        "Funcionario1_nome_exibido": entries_padrao["Funcionário 1"].get(),
        "Funcionario1_matricula": entries_padrao["Funcionário 1"].maodeobra_selecionada,
        "Funcionario2_nome_exibido": entries_padrao["Funcionário 2"].get(),
        "Funcionario2_matricula": entries_padrao["Funcionário 2"].maodeobra_selecionada,
        "Data1": entries_padrao["Data"].get(),
        "HoraInicial1": entries_padrao["Hora Inicial"].get(),
        "HoraFinal1": entries_padrao["Hora Final"].get(),
    }
    root.destroy()
    execute_pyautogui_actions(data)

def get_and_execute_encarregado():
    """Obtém os dados do formulário de encarregado e executa as ações do PyAutoGUI."""
    data = {
        "Ordem": entries_encarregado["OS"].get(),
        "Funcionario1_nome_exibido": entries_encarregado["Funcionário 1"].get(),
        "Funcionario1_matricula": entries_encarregado["Funcionário 1"].maodeobra_selecionada,
        "Funcionario2_nome_exibido": entries_encarregado["Funcionário 2"].get(),
        "Funcionario2_matricula": entries_encarregado["Funcionário 2"].maodeobra_selecionada,
        "Funcionario3_nome_exibido": entries_encarregado["Encarregado"].get(), # Renamed for clarity
        "Funcionario3_matricula": entries_encarregado["Encarregado"].maodeobra_selecionada, # Renamed for clarity
        "Data1": entries_encarregado["Data"].get(),
        "HoraInicial1": entries_encarregado["Hora Inicial"].get(),
        "HoraFinal1": entries_encarregado["Hora Final"].get(),
        "HoraFinal2": entries_encarregado["Final Encarregado"].get(),
    }
    root.destroy()
    execute_pyautogui_actions(data)

# --- GUI Setup ---
root = tk.Tk()
root.title("AUTOMAÇÃO")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Styles
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
BUTTON_TEXT_COLOR = "white"
ENTRY_BG_COLOR = "white"
LABEL_FONT = tkfont.Font(family="Segoe UI", size=10)
BUTTON_FONT = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

# --- Function to create form fields ---
def create_form_fields(parent_frame, fields_config, is_autocomplete_form=False):
    """Creates labels and entry widgets in the given frame based on configuration."""
    entries = {}
    for i, (label_text, entry_type) in enumerate(fields_config):
        label = tk.Label(parent_frame, text=label_text, bg=BG_COLOR, font=LABEL_FONT)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
        entry = entry_type(parent_frame, bg=ENTRY_BG_COLOR, relief="flat", highlightthickness=1,
                            highlightcolor="#4a7a8c", highlightbackground="#cccccc")
        entry.grid(row=i, column=1, padx=10, pady=5, ipady=3)
        entries[label_text.replace(":", "")] = entry # Store entry by cleaned label text
    return entries

# --- Standard Form Tab ---
frame_padrao = ttk.Frame(notebook, style="TFrame")
notebook.add(frame_padrao, text="Formulário Padrão")

standard_fields = [
    ("OS:", tk.Entry),
    ("Funcionário 1:", AutocompleteEntry),
    ("Funcionário 2:", AutocompleteEntry),
    ("Data:", tk.Entry),
    ("Hora Inicial:", tk.Entry),
    ("Hora Final:", tk.Entry),
]
entries_padrao = create_form_fields(frame_padrao, standard_fields)

botao_enviar_padrao = tk.Button(
    frame_padrao, 
    text="INICIAR PREENCHIMENTO (Padrão)", 
    command=get_and_execute_standard,
    bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT,
    relief="flat", padx=20, pady=8, bd=0,
    activebackground="#3a6a7c", activeforeground="white"
)
botao_enviar_padrao.grid(row=len(standard_fields), column=0, columnspan=2, pady=20)

# --- Supervisor Form Tab ---
frame_encarregado = ttk.Frame(notebook, style="TFrame")
notebook.add(frame_encarregado, text="Formulário com Encarregado")

encarregado_fields = [
    ("OS:", tk.Entry),
    ("Funcionário 1:", AutocompleteEntry), # Changed to AutocompleteEntry
    ("Funcionário 2:", AutocompleteEntry), # Changed to AutocompleteEntry
    ("Encarregado:", AutocompleteEntry),   # Changed to AutocompleteEntry
    ("Data:", tk.Entry),
    ("Hora Inicial:", tk.Entry),
    ("Hora Final:", tk.Entry),
    ("Final Encarregado:", tk.Entry),
]
entries_encarregado = create_form_fields(frame_encarregado, encarregado_fields)

botao_enviar_encarregado = tk.Button(
    frame_encarregado,
    text="Iniciar Preenchimento (Encarregado)",
    command=get_and_execute_encarregado,
    bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT,
    relief="flat", padx=20, pady=8, bd=0,
    activebackground="#3a6a7c", activeforeground="white"
)
botao_enviar_encarregado.grid(row=len(encarregado_fields), column=0, columnspan=2, pady=20)

root.mainloop()