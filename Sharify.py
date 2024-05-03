//PARA COMPILAR EM LOCAL, EH NECESSARIO SUBSTITUIR OS CAMINHOS DE ARQUIVOS MARCADOS PELA PALAVRA LOCAL
from PIL import Image, ImageTk
import subprocess
import tkinter as tk
import os
import pygame
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import ctypes
import sys
from tkinter import messagebox

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

SW_HIDE = 0

hWnd = kernel32.GetConsoleWindow()
if hWnd:
    user32.ShowWindow(hWnd, SW_HIDE)

subprocess.run(["python", r"LOCAL_tela_de_carregamento.py"])

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.update()  
        self.text_widget.see(tk.END)  

    def flush(self):
        pass

class ConsoleWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Console")
        self.geometry("800x400+10+300")
        self.text = tk.Text(self, wrap="word")
        self.text.pack(expand=True, fill="both")
        self.redirect_output()

    def redirect_output(self):
        sys.stdout = ConsoleRedirector(self.text)
        sys.stderr = ConsoleRedirector(self.text)

def compile_c_file(c_file_path):
    c_directory = os.path.dirname(c_file_path)
    c_filename = os.path.basename(c_file_path)
    c_filename_no_ext = os.path.splitext(c_filename)[0]
    exe_file_path = os.path.join(c_directory, f"{c_filename_no_ext}.exe")
    subprocess.run(["gcc", c_file_path, "-o", exe_file_path])
    return exe_file_path

def run_tests(c_file_path):
    input_lines = input_entry.get("1.0", "end-1c").split("\n")
    output_lines = output_entry.get("1.0", "end-1c").split("\n")
    
    if len(input_lines) != len(output_lines):
        messagebox.showerror("Erro", "A quantidade de entradas e saídas não coincide.")
        return
    
    test_cases = []
    for input_line, output_line in zip(input_lines, output_lines):
        test_cases.append({
            "input": input_line,
            "expected_output": output_line
        })
    
    exe_file_path = compile_c_file(c_file_path)
    
    output_print = os.path.dirname(exe_file_path)
    file_path = os.path.join(output_print, "sharify.txt")
    
    with open(file_path, "w") as file:
        passed_tests = 0
        failed_tests = 0
        for i, case in enumerate(test_cases, start=1):
            input_data = case["input"]
            expected_output = case["expected_output"]
            result = subprocess.run([exe_file_path], input=input_data, text=True, capture_output=True)
            output = result.stdout.strip()
            file.write(f"Teste {i}:\n")
            file.write(f"Input esperado: {expected_output}\n")
            file.write(f"Output obtido: {output}\n")
            if output == expected_output:
                file.write("Resultado: Passou\n\n")
                passed_tests += 1
            else:
                file.write("Resultado: Falhou\n\n")
                failed_tests += 1
        
        file.write(f"Testes aprovados: {passed_tests}\n")
        file.write(f"Testes reprovados: {failed_tests}\n\n")

    pygame.mixer.init()
    pygame.mixer.music.load(r'LOCAL_audio.mp3')
    pygame.mixer.music.play()

    update_results_section(file_path)
    
    passed_label.config(text=f"Testes aprovados: {passed_tests}", fg="green")
    failed_label.config(text=f"Testes reprovados: {failed_tests}", fg="red")

def update_results_section(file_path):
    with open(file_path, "r") as file:
        results_text.delete("1.0", tk.END)
        results_text.insert("1.0", file.read())

def browse_file():
    global c_entry  
    file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
    if file_path:
        c_entry.delete(0, tk.END)
        c_entry.insert(0, file_path)
        with open(file_path, "r") as f:
            text_editor.delete("1.0", tk.END)
            text_editor.insert("1.0", f.read())
        run_tests(file_path)

def repeat_tests():
    current_file = c_entry.get()
    if current_file:
        run_tests(current_file)
    else:
        tk.messagebox.showerror("Erro", "Nenhum arquivo C selecionado.")

def save_file():
    file_path = c_entry.get()
    if file_path:
        with open(file_path, "w") as f:
            f.write(text_editor.get("1.0", tk.END))

root = tk.Tk()
root.title("Sharify")
root.configure(bg='#212121')
icone_path = r"LOCAL_ico.ico"
root.iconbitmap(icone_path)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")  

def open_console_window():
        console_window = ConsoleWindow(root)

console_button = tk.Button(root, text="Possível bug do Sharify? Clique aqui e verifique o console", command=open_console_window, bg='#B77B59', fg='white', font=('Arial', 12))
console_button.pack()

left_frame = tk.Frame(root, bg='#212121', padx=10, pady=10, bd=2, relief=tk.GROOVE)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

logo_image_path = r'LOCAL_logo.png'
logo_image = Image.open(logo_image_path)
logo_image = logo_image.resize((150, 180))
logo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(left_frame, image=logo, bg='#212121')
logo_label.pack()
separator = tk.Frame(left_frame, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)

input_label = tk.Label(left_frame, text="Input (cada linha, 1 input):", bg='#212121', fg='white', font=('Arial', 12))
input_label.pack()
input_entry = tk.Text(left_frame, width=40, height=10, wrap=tk.WORD, bg='#424242', fg='white')
input_entry.pack()

output_label = tk.Label(left_frame, text="Output esperado (cada linha, 1 output):", bg='#212121', fg='white', font=('Arial', 12))
output_label.pack()
output_entry = tk.Text(left_frame, width=40, height=10, wrap=tk.WORD, bg='#424242', fg='white')
output_entry.pack()
code_label6 = tk.Label(left_frame, text="Realize um teste para poder ter acesso ao código.", bg='#212121', fg='white', font=('Arial', 11))
code_label6.pack()
code_label0 = tk.Label(left_frame, text="Insira o arquivo C:", bg='#212121', fg='white', font=('Arial', 12))
code_label0.pack()
browse_button = tk.Button(left_frame, text="Procurar", command=browse_file, bg='#B77B59', fg='white',font=(12))
browse_button.pack()

repeat_tests_button = tk.Button(left_frame, text="Repetir testes", command=repeat_tests, bg='#B77B59', fg='white',font=(12))
repeat_tests_button.pack()
code_label5 = tk.Label(left_frame, text="Arquivo atual:", bg='#212121', fg='white', font=('Arial', 10))
code_label5.pack()
c_entry = tk.Entry(left_frame, width=40, bg='#424242', fg='white')  
c_entry.pack()
separator = tk.Frame(left_frame, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)
code_label2 = tk.Label(left_frame, text="Observações:", bg='#212121', fg='white', font=('Arial', 11))
code_label2.pack()

code_label3 = tk.Label(left_frame, text="Cuidado com espaços para input e output.", bg='#212121', fg='white', font=('Arial', 11))
code_label3.pack()

code_label4 = tk.Label(left_frame, text="O txt e o arquivo .exe estão na mesma pasta do arquivo C.", bg='#212121', fg='white', font=('Arial', 11))
code_label4.pack()

counter_frame = tk.Frame(left_frame, bg='#212121')
counter_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

passed_label = tk.Label(counter_frame, text="Testes aprovados: 0", bg='#212121', fg='green',font=('Arial', 12))
passed_label.pack(side=tk.LEFT)

failed_label = tk.Label(counter_frame, text="Testes reprovados: 0", bg='#212121', fg='red',font=('Arial', 12))
failed_label.pack(side=tk.RIGHT)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

bg_color = '#272822'
fg_color = '#F8F8F2'

font_family = 'Consolas'  
font_size = 14

text_editor = ScrolledText(right_frame, wrap=tk.WORD, bg=bg_color, fg=fg_color, insertbackground='white', selectbackground='darkorange', font=(font_family, font_size))
text_editor.pack(fill=tk.BOTH, expand=True)

results_frame = tk.Frame(right_frame)
results_frame.pack(fill=tk.BOTH, expand=True)

results_text = ScrolledText(results_frame, wrap=tk.WORD, bg=bg_color, fg=fg_color, insertbackground='white', selectbackground='darkorange', font=(font_family, font_size))
results_text.pack(fill=tk.BOTH, expand=True)

text_editor.bind("<KeyRelease>", lambda event: save_file())

root.mainloop()