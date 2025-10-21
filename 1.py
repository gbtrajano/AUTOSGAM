import customtkinter as ctk
import pyautogui
import time

# DICIONÁRIO DE NOMES DE FUNCIONÁRIOS E SUAS MATRÍCULAS
funcionarios = {
    "Adriano": "T083413177",
    "Alexandre": "T084846967",
    "Andre Carneiro": "T070908137",
    "Andre Guerreiro": "T032323127",
    "Caio": "T189293597",
    "Carlos": "T000853027",
    "Genivaldo": "T076337747",
    "Ivan": "T107535307",
    "John": "T112999667",
    "Jonathan": "T175557747",
    "Leonardo": "T123334397",
    "Luis": "T084053577",
    "Paulo Vitor Guina": "T134249567",
    "Marcelo": "T015619407",
    "Mauricio": "T093844777",
    "Reginaldo": "T135383327",
    "Ricardo": "T103416317",
    "Robson": "T095551577",
    "Rodrigo": "T090621807",
    "Leandro": "T089556007",
    "Ulysses": "T000257897",
    "Ygor": "T137582997"
}

class AutocompleteEntry(ctk.CTkEntry):
    def __init__(self, dict_funcionarios, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.dict_funcionarios = dict_funcionarios
        self.nomes = sorted(dict_funcionarios.keys())
        self.var = ctk.StringVar()
        self.configure(textvariable=self.var)
        self.bind("<KeyRelease>", self.check_input)
        self.bind("<FocusOut>", self.hide_listbox)
        self.bind("<Return>", self.select_item)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)

        self.toplevel_suggestions = None # CTkToplevel window for suggestions
        self.suggestions_frame = None    # CTkScrollableFrame inside toplevel
        self.lb_visible = False
        self.current_selection_index = -1
        self.suggestion_labels = []
        self.hide_id = None # To store the after job ID for delayed hiding

    def check_input(self, event):
        value = self.var.get()
        if value == "":
            self.hide_listbox()
        else:
            data = [nome for nome in self.nomes if value.lower() in nome.lower()]
            if data:
                self.update_suggestions(data)
                self.show_listbox()
            else:
                self.hide_listbox()

    def update_suggestions(self, data):
        for label in self.suggestion_labels:
            label.destroy()
        self.suggestion_labels.clear()

        max_display_items = 5
        item_height = 30
        calculated_height = min(len(data), max_display_items) * item_height

        # Create/re-create toplevel and scrollable frame if not existing or destroyed
        if self.toplevel_suggestions is None or not self.toplevel_suggestions.winfo_exists():
            self.toplevel_suggestions = ctk.CTkToplevel(self.master)
            self.toplevel_suggestions.overrideredirect(True) # Remove window decorations
            self.toplevel_suggestions.attributes("-topmost", True) # Keep on top

            # Bind a click event to the toplevel itself to prevent hide if background is clicked
            self.toplevel_suggestions.bind("<Button-1>", lambda e: "break")

            # Create suggestions_frame inside the toplevel with specified width and height
            self.suggestions_frame = ctk.CTkScrollableFrame(
                master=self.toplevel_suggestions,
                width=self.winfo_width(), # Set width in constructor
                height=calculated_height, # Set height in constructor
                fg_color=("gray90", "gray18")
            )
            self.suggestions_frame.pack(fill="both", expand=True)
        else:
            # If toplevel already exists, just update the height and width of the scrollable frame
            self.suggestions_frame.configure(height=calculated_height)
            self.suggestions_frame.configure(width=self.winfo_width()) # Update width in case entry resized

        for i, nome in enumerate(data):
            label = ctk.CTkLabel(
                master=self.suggestions_frame,
                text=nome,
                fg_color="transparent",
                corner_radius=0,
                padx=5,
                pady=2,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=11)
            )
            label.bind("<Enter>", lambda e, l=label, i=i: self.on_label_hover(l, i))
            label.bind("<Leave>", lambda e, l=label, i=i: self.on_label_leave(l, i))
            label.bind("<Button-1>", lambda e, n=nome: self.select_item_by_click(n))
            label.pack(fill="x", padx=2, pady=1)
            self.suggestion_labels.append(label)

        self.current_selection_index = -1
        if self.suggestion_labels:
            self.current_selection_index = 0
            self.highlight_selection()

    def on_label_hover(self, label, index):
        if index != self.current_selection_index:
            label.configure(fg_color=("gray70", "gray30"))

    def on_label_leave(self, label, index):
        if index != self.current_selection_index:
            label.configure(fg_color="transparent")

    def show_listbox(self):
        if not self.lb_visible and self.toplevel_suggestions:
            # Get absolute coordinates of the entry on screen
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.toplevel_suggestions.geometry(f"+{x}+{y}")
            self.toplevel_suggestions.deiconify() # Show the window
            self.lb_visible = True

    def hide_listbox(self, event=None):
        # Get the root window for scheduling 'after' calls
        root_window = self.master.winfo_toplevel()
        if self.hide_id:
            root_window.after_cancel(self.hide_id)
            self.hide_id = None

        # Schedule a delayed hide to allow click events on suggestions to register
        self.hide_id = root_window.after(150, self._perform_hide_listbox)

    def _perform_hide_listbox(self):
        if self.toplevel_suggestions and self.toplevel_suggestions.winfo_exists():
            self.toplevel_suggestions.withdraw() # Hide the window
        self.lb_visible = False
        self.current_selection_index = -1
        for label in self.suggestion_labels:
            label.destroy()
        self.suggestion_labels.clear()
        self.hide_id = None

    def select_item_by_click(self, nome_selecionado):
        root_window = self.master.winfo_toplevel()
        if self.hide_id:
            root_window.after_cancel(self.hide_id)
            self.hide_id = None # Cancel pending hide
        matricula = self.dict_funcionarios[nome_selecionado]
        self.var.set(matricula)
        self._perform_hide_listbox() # Immediately hide after selection
        self.icursor(ctk.END)

    def select_item(self, event=None):
        root_window = self.master.winfo_toplevel()
        if self.hide_id:
            root_window.after_cancel(self.hide_id)
            self.hide_id = None # Cancel pending hide

        if self.lb_visible and self.suggestion_labels and self.current_selection_index != -1:
            nome_selecionado = self.suggestion_labels[self.current_selection_index].cget("text")
            matricula = self.dict_funcionarios[nome_selecionado]
            self.var.set(matricula)
            self._perform_hide_listbox()
            self.icursor(ctk.END)
        return "break"

    def highlight_selection(self):
        for i, label in enumerate(self.suggestion_labels):
            if i == self.current_selection_index:
                label.configure(fg_color=("blue", "darkblue"), text_color="white")
            else:
                label.configure(fg_color="transparent", text_color=("black", "white"))

    def move_up(self, event):
        if self.lb_visible and self.suggestion_labels:
            if self.current_selection_index > 0:
                self.current_selection_index -= 1
                self.highlight_selection()
            elif self.current_selection_index == 0:
                self.current_selection_index = len(self.suggestion_labels) - 1
                self.highlight_selection()
        return "break"

    def move_down(self, event):
        if self.lb_visible and self.suggestion_labels:
            if self.current_selection_index < len(self.suggestion_labels) - 1:
                self.current_selection_index += 1
                self.highlight_selection()
            elif self.current_selection_index == len(self.suggestion_labels) - 1:
                self.current_selection_index = 0
                self.highlight_selection()
        return "break"

def obter_texto_e_executar():
    Ordem = entry1.get()
    Funcionario1 = entry2.get()
    Data1 = entry4.get()
    HoraInicial1 = entry5.get()
    HoraFinal1 = entry6.get()


    # CAMPO DA OS
    pyautogui.moveTo(87, 221)
    pyautogui.click()
    pyautogui.typewrite("OS52" + Ordem)
    pyautogui.press('enter')

    entry1.delete(0, ctk.END)

    time.sleep(3.5)

    # SCROLL
    pyautogui.moveTo(1357, 704)
    pyautogui.doubleClick()

    # NOVA LINHA
    pyautogui.moveTo(909, 671)
    pyautogui.click()

    time.sleep(2)

    # NOME ( PRIMEIRO FUNCIONÁRIO )
    pyautogui.moveTo(567, 579)
    pyautogui.click()
    pyautogui.typewrite(Funcionario1)

    # DATA 
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(0.75)
    pyautogui.typewrite(Data1)

    # INÍCIO 
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(HoraInicial1)

    # FIM 
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(HoraFinal1)

    entry5.delete(0, ctk.END)
    entry5.insert(0, HoraFinal1)
    entry6.delete(0, ctk.END)

    # SALVAR
    pyautogui.moveTo(293, 221)
    pyautogui.click()
    time.sleep(2)

app = ctk.CTk()
app.title("Programa Python")
app.geometry("300x350")
app.resizable(False, False)

cor_fundo_frame = ("gray92", "gray14")
cor_botao_fg = "blue"
cor_botao_text = "white"
cor_entry_fg = ("white", "gray14")
cor_entry_border = "#c1c1c1"

main_frame = ctk.CTkFrame(app, fg_color=cor_fundo_frame)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

def criar_campo(frame, texto, linha, autocomplete=False):
    label = ctk.CTkLabel(frame, text=texto, font=ctk.CTkFont(family="Segoe UI", size=13))
    label.grid(row=linha, column=0, padx=10, pady=5, sticky="e")

    if autocomplete:
        entry = AutocompleteEntry(
            funcionarios,
            master=frame,
            fg_color=cor_entry_fg,
            border_width=1,
            border_color=cor_entry_border,
            corner_radius=5,
            height=30
        )
    else:
        entry = ctk.CTkEntry(
            frame,
            fg_color=cor_entry_fg,
            border_width=1,
            border_color=cor_entry_border,
            corner_radius=5,
            height=30
        )

    entry.grid(row=linha, column=1, padx=10, pady=5, sticky="ew")
    return entry

entry1 = criar_campo(main_frame, "OS", 0)
entry2 = criar_campo(main_frame, "Funcionário", 1, autocomplete=True)
entry4 = criar_campo(main_frame, "Data", 4)
entry5 = criar_campo(main_frame, "Início", 5)
entry6 = criar_campo(main_frame, "Fim", 6)

botao_enviar = ctk.CTkButton(
    main_frame,
    text="Iniciar",
    command=obter_texto_e_executar,
    fg_color=cor_botao_fg,
    text_color=cor_botao_text,
    hover_color="dodgerblue",
    corner_radius=50,
    height=40,
    font=ctk.CTkFont(size=20, weight="bold") # Adicione esta linha
)
botao_enviar.grid(row=9, column=0, columnspan=2, pady=20)

main_frame.grid_columnconfigure(1, weight=1)

app.mainloop()