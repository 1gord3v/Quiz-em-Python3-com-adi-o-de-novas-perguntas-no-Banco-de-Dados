import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Quiz de Python")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Conectar ao banco de dados
        self.conn = sqlite3.connect('quiz.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        self.populate_initial_questions()
        
        # Variáveis do quiz
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_answer = tk.IntVar()
        
        # Mostrar tela inicial
        self.show_home_screen()
    
    def setup_database(self):
        """Cria a tabela de perguntas"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta TEXT NOT NULL,
                opcao1 TEXT NOT NULL,
                opcao2 TEXT NOT NULL,
                opcao3 TEXT NOT NULL,
                opcao4 TEXT NOT NULL,
                opcao5 TEXT NOT NULL,
                correta INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def populate_initial_questions(self):
        """Adiciona perguntas iniciais"""
        self.cursor.execute('SELECT COUNT(*) FROM perguntas')
        if self.cursor.fetchone()[0] == 0:
            perguntas = [
                ("Qual palavra-chave é usada para definir uma função em Python?", "function", "def", "func", "define", "method", 2),
                ("Qual estrutura de dados em Python é mutável e ordenada?", "tuple", "set", "list", "dict", "frozenset", 3),
                ("Como se cria um comentário de uma linha em Python?", "// comentário", "/* comentário */", "# comentário", "-- comentário", "<!-- comentário -->", 3),
                ("Qual método adiciona um elemento ao final de uma lista?", "add()", "append()", "insert()", "push()", "extend()", 2),
                ("Qual operador é usado para exponenciação em Python?", "^", "**", "exp()", "pow()", "^^", 2),
                ("Como se importa a biblioteca math em Python?", "include math", "using math", "import math", "require math", "#include <math>", 3),
                ("Qual função retorna o tipo de uma variável?", "typeof()", "type()", "gettype()", "vartype()", "datatype()", 2),
                ("Como se define uma classe em Python?", "class MinhaClasse:", "Class MinhaClasse:", "define class MinhaClasse:", "new class MinhaClasse:", "create MinhaClasse:", 1),
                ("Qual palavra-chave indica herança em Python?", "extends", "inherits", "implements", "parênteses após nome da classe", "inherit", 4),
                ("Como verificar se uma chave existe em um dicionário?", "key.exists()", "dict.has(key)", "key in dict", "dict.contains(key)", "exists(key, dict)", 3),
                ("Qual é o resultado de: 10 // 3 em Python?", "3.33", "3", "4", "3.0", "Erro", 2),
                ("Como se cria uma lista vazia em Python?", "list = empty()", "list = []", "list = new List()", "list = list()", "Ambas B e D", 5),
                ("Qual palavra-chave captura exceções?", "catch", "except", "handle", "error", "trap", 2),
                ("Como concatenar duas strings em Python?", "concat(str1, str2)", "str1.concat(str2)", "str1 + str2", "merge(str1, str2)", "str1 & str2", 3),
                ("Função para obter o comprimento de uma lista?", "length()", "size()", "len()", "count()", "sizeof()", 3),
            ]
            for p in perguntas:
                self.cursor.execute('INSERT INTO perguntas VALUES (NULL,?,?,?,?,?,?,?)', p)
            self.conn.commit()
    
    def clear_window(self):
        """Limpa todos os widgets da janela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        """Tela inicial"""
        self.clear_window()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Título
        title = tk.Label(main_frame, text="🐍 Quiz de Python", 
                        font=("Arial", 36, "bold"), fg="#00d4ff", bg="#1a1a2e")
        title.pack(pady=20)
        
        subtitle = tk.Label(main_frame, text="Teste seus conhecimentos em programação Python", 
                           font=("Arial", 14), fg="#ffffff", bg="#1a1a2e")
        subtitle.pack(pady=10)
        
        # Info
        self.cursor.execute('SELECT COUNT(*) FROM perguntas')
        total = self.cursor.fetchone()[0]
        
        info_frame = tk.Frame(main_frame, bg="#16213e", bd=2, relief="solid")
        info_frame.pack(pady=30, padx=50, fill="x")
        
        info_label = tk.Label(info_frame, text=f"📊 Perguntas disponíveis: {total}", 
                             font=("Arial", 16), fg="#00d4ff", bg="#16213e")
        info_label.pack(pady=20)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        btn_start = tk.Button(btn_frame, text="▶ Iniciar Quiz", font=("Arial", 16, "bold"),
                             bg="#00d4ff", fg="#1a1a2e", padx=30, pady=15,
                             command=self.start_quiz, cursor="hand2",
                             activebackground="#00a8cc", relief="flat")
        btn_start.pack(pady=10)
        
        btn_manage = tk.Button(btn_frame, text="⚙ Gerenciar Perguntas", font=("Arial", 16, "bold"),
                              bg="#9b59b6", fg="#ffffff", padx=30, pady=15,
                              command=self.show_manage_screen, cursor="hand2",
                              activebackground="#8e44ad", relief="flat")
        btn_manage.pack(pady=10)
        
        btn_exit = tk.Button(btn_frame, text="✖ Sair", font=("Arial", 14),
                            bg="#e74c3c", fg="#ffffff", padx=30, pady=10,
                            command=self.root.quit, cursor="hand2",
                            activebackground="#c0392b", relief="flat")
        btn_exit.pack(pady=10)
    
    def start_quiz(self):
        """Inicia o quiz"""
        self.cursor.execute('SELECT COUNT(*) FROM perguntas')
        if self.cursor.fetchone()[0] < 10:
            messagebox.showwarning("Atenção", "É necessário ter pelo menos 10 perguntas no banco!")
            return
        
        # Seleciona 10 perguntas aleatórias
        self.cursor.execute('SELECT * FROM perguntas ORDER BY RANDOM() LIMIT 10')
        self.quiz_questions = self.cursor.fetchall()
        self.current_question_index = 0
        self.score = 0
        
        self.show_question()
    
    def show_question(self):
        """Mostra uma pergunta"""
        self.clear_window()
        
        question = self.quiz_questions[self.current_question_index]
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#16213e", bd=2, relief="solid")
        header_frame.pack(fill="x", pady=(0, 20))
        
        progress_text = f"Pergunta {self.current_question_index + 1} de 10"
        progress_label = tk.Label(header_frame, text=progress_text, 
                                 font=("Arial", 14, "bold"), fg="#00d4ff", bg="#16213e")
        progress_label.pack(side="left", padx=20, pady=10)
        
        score_label = tk.Label(header_frame, text=f"Pontuação: {self.score}", 
                              font=("Arial", 14, "bold"), fg="#2ecc71", bg="#16213e")
        score_label.pack(side="right", padx=20, pady=10)
        
        # Barra de progresso
        progress_bar = ttk.Progressbar(main_frame, length=800, mode='determinate')
        progress_bar['value'] = ((self.current_question_index + 1) / 10) * 100
        progress_bar.pack(pady=10)
        
        remaining = 10 - self.current_question_index - 1
        remaining_label = tk.Label(main_frame, text=f"{remaining} pergunta(s) restante(s)", 
                                  font=("Arial", 10), fg="#95a5a6", bg="#1a1a2e")
        remaining_label.pack()
        
        # Pergunta
        question_frame = tk.Frame(main_frame, bg="#16213e", bd=2, relief="solid")
        question_frame.pack(pady=20, fill="x")
        
        question_label = tk.Label(question_frame, text=question[1], 
                                 font=("Arial", 16, "bold"), fg="#ffffff", bg="#16213e",
                                 wraplength=800, justify="left")
        question_label.pack(padx=30, pady=30)
        
        # Opções embaralhadas
        options = [
            (1, question[2]),
            (2, question[3]),
            (3, question[4]),
            (4, question[5]),
            (5, question[6])
        ]
        random.shuffle(options)
        self.shuffled_options = options
        
        self.selected_answer.set(-1)
        
        # Radio buttons para opções
        options_frame = tk.Frame(main_frame, bg="#1a1a2e")
        options_frame.pack(pady=20, fill="x")
        
        letters = ['A', 'B', 'C', 'D', 'E']
        for i, (orig_idx, text) in enumerate(options):
            option_frame = tk.Frame(options_frame, bg="#2c3e50", bd=1, relief="solid")
            option_frame.pack(pady=5, fill="x", padx=20)
            
            rb = tk.Radiobutton(option_frame, text=f"  {letters[i]}) {text}", 
                               variable=self.selected_answer, value=i,
                               font=("Arial", 13), fg="#ffffff", bg="#2c3e50",
                               selectcolor="#34495e", activebackground="#34495e",
                               cursor="hand2", anchor="w", padx=10, pady=15)
            rb.pack(fill="x")
        
        # Botão confirmar
        btn_confirm = tk.Button(main_frame, text="✓ Confirmar Resposta", 
                               font=("Arial", 14, "bold"), bg="#2ecc71", fg="#ffffff",
                               padx=40, pady=15, command=self.check_answer,
                               cursor="hand2", activebackground="#27ae60", relief="flat")
        btn_confirm.pack(pady=20)
    
    def check_answer(self):
        """Verifica a resposta"""
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Atenção", "Selecione uma resposta!")
            return
        
        question = self.quiz_questions[self.current_question_index]
        selected_idx = self.selected_answer.get()
        original_idx = self.shuffled_options[selected_idx][0]
        
        is_correct = original_idx == question[7]
        
        if is_correct:
            self.score += 1
            messagebox.showinfo("✓ Correto!", "Parabéns! Você acertou!")
        else:
            correct_answer = question[question[7] + 1]
            messagebox.showerror("✗ Incorreto", f"A resposta correta era:\n{correct_answer}")
        
        self.current_question_index += 1
        
        if self.current_question_index < 10:
            self.show_question()
        else:
            self.show_result()
    
    def show_result(self):
        """Mostra o resultado final"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title = tk.Label(main_frame, text="🏆 Quiz Finalizado!", 
                        font=("Arial", 36, "bold"), fg="#00d4ff", bg="#1a1a2e")
        title.pack(pady=30)
        
        # Resultado
        result_frame = tk.Frame(main_frame, bg="#16213e", bd=2, relief="solid")
        result_frame.pack(pady=20, padx=50, fill="x")
        
        percentage = (self.score / 10) * 100
        score_label = tk.Label(result_frame, text=f"{self.score}/10", 
                              font=("Arial", 60, "bold"), fg="#2ecc71", bg="#16213e")
        score_label.pack(pady=20)
        
        percent_label = tk.Label(result_frame, text=f"{percentage:.0f}% de acertos", 
                                font=("Arial", 20), fg="#ffffff", bg="#16213e")
        percent_label.pack(pady=10)
        
        # Mensagem
        if percentage == 100:
            message = "🎉 PERFEITO! Você domina Python!"
            color = "#2ecc71"
        elif percentage >= 70:
            message = "👏 MUITO BEM! Bom conhecimento!"
            color = "#3498db"
        elif percentage >= 50:
            message = "👍 BOM TRABALHO! Continue estudando!"
            color = "#f39c12"
        else:
            message = "💪 CONTINUE PRATICANDO!"
            color = "#e74c3c"
        
        message_label = tk.Label(result_frame, text=message, 
                                font=("Arial", 18, "bold"), fg=color, bg="#16213e")
        message_label.pack(pady=20)
        
        # Botão voltar
        btn_home = tk.Button(main_frame, text="↺ Voltar ao Menu", 
                            font=("Arial", 16, "bold"), bg="#00d4ff", fg="#1a1a2e",
                            padx=40, pady=15, command=self.show_home_screen,
                            cursor="hand2", activebackground="#00a8cc", relief="flat")
        btn_home.pack(pady=30)
    
    def show_manage_screen(self):
        """Tela de gerenciamento"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        title = tk.Label(main_frame, text="⚙ Gerenciar Perguntas", 
                        font=("Arial", 24, "bold"), fg="#9b59b6", bg="#1a1a2e")
        title.pack(pady=20)
        
        # Botões de ação
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        btn_add = tk.Button(btn_frame, text="➕ Adicionar Pergunta", 
                           font=("Arial", 12, "bold"), bg="#2ecc71", fg="#ffffff",
                           padx=20, pady=10, command=self.show_add_question,
                           cursor="hand2", relief="flat")
        btn_add.pack(side="left", padx=5)
        
        btn_list = tk.Button(btn_frame, text="📋 Listar Perguntas", 
                            font=("Arial", 12, "bold"), bg="#3498db", fg="#ffffff",
                            padx=20, pady=10, command=self.show_list_questions,
                            cursor="hand2", relief="flat")
        btn_list.pack(side="left", padx=5)
        
        btn_back = tk.Button(btn_frame, text="← Voltar", 
                            font=("Arial", 12, "bold"), bg="#95a5a6", fg="#ffffff",
                            padx=20, pady=10, command=self.show_home_screen,
                            cursor="hand2", relief="flat")
        btn_back.pack(side="left", padx=5)
    
    def show_add_question(self):
        """Formulário para adicionar pergunta"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=40, pady=30)
        
        title = tk.Label(main_frame, text="➕ Adicionar Nova Pergunta", 
                        font=("Arial", 20, "bold"), fg="#2ecc71", bg="#1a1a2e")
        title.pack(pady=20)
        
        # Frame do formulário
        form_frame = tk.Frame(main_frame, bg="#16213e", bd=2, relief="solid")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Pergunta
        tk.Label(form_frame, text="Pergunta:", font=("Arial", 12, "bold"), 
                fg="#ffffff", bg="#16213e").pack(anchor="w", padx=20, pady=(20, 5))
        entry_question = tk.Entry(form_frame, font=("Arial", 12), width=70)
        entry_question.pack(padx=20, pady=(0, 15))
        
        # Opções
        entries = []
        for i in range(1, 6):
            tk.Label(form_frame, text=f"Opção {i}:", font=("Arial", 12, "bold"), 
                    fg="#ffffff", bg="#16213e").pack(anchor="w", padx=20, pady=(5, 5))
            entry = tk.Entry(form_frame, font=("Arial", 12), width=70)
            entry.pack(padx=20, pady=(0, 10))
            entries.append(entry)
        
        # Resposta correta
        tk.Label(form_frame, text="Resposta correta (1-5):", font=("Arial", 12, "bold"), 
                fg="#ffffff", bg="#16213e").pack(anchor="w", padx=20, pady=(5, 5))
        entry_correct = tk.Spinbox(form_frame, from_=1, to=5, font=("Arial", 12), width=10)
        entry_correct.pack(padx=20, pady=(0, 20))
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
        btn_frame.pack(pady=20)
        
        def save_question():
            question = entry_question.get().strip()
            options = [e.get().strip() for e in entries]
            correct = entry_correct.get()
            
            if not question or any(not opt for opt in options):
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            
            try:
                correct = int(correct)
                if not 1 <= correct <= 5:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "Resposta correta deve ser entre 1 e 5!")
                return
            
            self.cursor.execute('''
                INSERT INTO perguntas (pergunta, opcao1, opcao2, opcao3, opcao4, opcao5, correta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (question, options[0], options[1], options[2], options[3], options[4], correct))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Pergunta adicionada com sucesso!")
            self.show_manage_screen()
        
        btn_save = tk.Button(btn_frame, text="💾 Salvar", font=("Arial", 14, "bold"),
                            bg="#2ecc71", fg="#ffffff", padx=30, pady=10,
                            command=save_question, cursor="hand2", relief="flat")
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = tk.Button(btn_frame, text="✖ Cancelar", font=("Arial", 14, "bold"),
                              bg="#e74c3c", fg="#ffffff", padx=30, pady=10,
                              command=self.show_manage_screen, cursor="hand2", relief="flat")
        btn_cancel.pack(side="left", padx=10)
    
    def show_list_questions(self):
        """Lista todas as perguntas"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        title = tk.Label(main_frame, text="📋 Lista de Perguntas", 
                        font=("Arial", 20, "bold"), fg="#3498db", bg="#1a1a2e")
        title.pack(pady=20)
        
        # Área de texto com scroll
        text_area = scrolledtext.ScrolledText(main_frame, font=("Arial", 11), 
                                             bg="#16213e", fg="#ffffff", 
                                             wrap=tk.WORD, height=20)
        text_area.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.cursor.execute('SELECT * FROM perguntas')
        questions = self.cursor.fetchall()
        
        for i, q in enumerate(questions, 1):
            text_area.insert(tk.END, f"[{i}] {q[1]}\n")
            text_area.insert(tk.END, f"    Resposta correta: Opção {q[7]} - {q[q[7] + 1]}\n")
            text_area.insert(tk.END, "-" * 80 + "\n\n")
        
        text_area.insert(tk.END, f"\nTotal: {len(questions)} pergunta(s)")
        text_area.config(state="disabled")
        
        # Botão voltar
        btn_back = tk.Button(main_frame, text="← Voltar", font=("Arial", 14, "bold"),
                            bg="#95a5a6", fg="#ffffff", padx=40, pady=10,
                            command=self.show_manage_screen, cursor="hand2", relief="flat")
        btn_back.pack(pady=20)
    
    def __del__(self):
        """Fecha a conexão ao destruir o objeto"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Executar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()