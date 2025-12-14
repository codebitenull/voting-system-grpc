"""
Aplicação GUI para Sistema de Votação Eletrónica
Integra os serviços de Registo (AR) e Votação (AV)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Adiciona path para importar os clientes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.voter_client import VoterRegistrationClient
from src.voting_client import VotingClient


class VotingApp:
    """Aplicação principal de votação eletrónica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votação Eletrónica")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Clientes gRPC
        self.voter_client = VoterRegistrationClient()
        self.voting_client = VotingClient()
        
        # Dados da sessão
        self.voting_credential = None
        self.candidates = []
        
        # Conecta aos serviços
        self.connect_services()
        
        # Cria interface
        self.create_widgets()
        
        # Protocolo de fecho
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def connect_services(self):
        """Conecta aos serviços gRPC"""
        try:
            self.voter_client.connect()
            self.voting_client.connect()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", 
                f"Não foi possível conectar aos serviços:\n{str(e)}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        
        # Título principal
        title = tk.Label(
            self.root,
            text="🗳️ SISTEMA DE VOTAÇÃO ELETRÓNICA",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        )
        title.pack(fill=tk.X)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba 1: Registo
        self.tab_registration = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_registration, text="📋 Registo")
        self.create_registration_tab()
        
        # Aba 2: Votação
        self.tab_voting = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_voting, text="🗳️ Votação")
        self.create_voting_tab()
        
        # Aba 3: Resultados
        self.tab_results = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_results, text="📊 Resultados")
        self.create_results_tab()
        
        # Rodapé
        footer = tk.Label(
            self.root,
            text="Integração de Sistemas | 2025-2026",
            font=("Arial", 9),
            fg="gray"
        )
        footer.pack(pady=5)
    
    def create_registration_tab(self):
        """Cria aba de registo"""
        
        frame = ttk.Frame(self.tab_registration, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Instruções
        instructions = tk.Label(
            frame,
            text="Insira o seu número de Cartão de Cidadão para obter credencial de voto",
            font=("Arial", 10),
            wraplength=500,
            justify=tk.LEFT
        )
        instructions.pack(pady=(0, 20))
        
        # Campo CC
        cc_frame = ttk.Frame(frame)
        cc_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(cc_frame, text="Cartão de Cidadão:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.cc_entry = ttk.Entry(cc_frame, font=("Arial", 12), width=30)
        self.cc_entry.pack(fill=tk.X, pady=5)
        self.cc_entry.insert(0, "123456789")  # Valor de teste
        
        # Botão registar
        register_btn = tk.Button(
            frame,
            text="Obter Credencial de Voto",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.register_voter,
            pady=10
        )
        register_btn.pack(pady=20, fill=tk.X)
        
        # Área de resultado
        result_frame = ttk.LabelFrame(frame, text="Resultado do Registo", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.registration_result = tk.Text(
            result_frame,
            height=8,
            font=("Courier", 10),
            wrap=tk.WORD,
            bg="#ecf0f1",
            relief=tk.FLAT
        )
        self.registration_result.pack(fill=tk.BOTH, expand=True)
        self.registration_result.config(state=tk.DISABLED)
    
    def create_voting_tab(self):
        """Cria aba de votação"""
        
        frame = ttk.Frame(self.tab_voting, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Instruções
        instructions = tk.Label(
            frame,
            text="Selecione um candidato e submeta o seu voto",
            font=("Arial", 10),
            wraplength=500
        )
        instructions.pack(pady=(0, 20))
        
        # Credencial atual
        cred_frame = ttk.LabelFrame(frame, text="Credencial de Voto", padding=10)
        cred_frame.pack(fill=tk.X, pady=10)
        
        self.credential_label = tk.Label(
            cred_frame,
            text="Nenhuma credencial obtida",
            font=("Courier", 10),
            fg="red"
        )
        self.credential_label.pack()
        
        # Candidatos
        candidates_frame = ttk.LabelFrame(frame, text="Candidatos", padding=10)
        candidates_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botão carregar candidatos
        load_btn = tk.Button(
            candidates_frame,
            text="🔄 Carregar Lista de Candidatos",
            command=self.load_candidates,
            bg="#3498db",
            fg="white",
            cursor="hand2"
        )
        load_btn.pack(pady=5)
        
        # Lista de candidatos (Radiobuttons)
        self.candidates_frame = ttk.Frame(candidates_frame)
        self.candidates_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.selected_candidate = tk.IntVar()
        
        # Botão votar
        vote_btn = tk.Button(
            frame,
            text="🗳️ SUBMETER VOTO",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.submit_vote,
            pady=10
        )
        vote_btn.pack(pady=10, fill=tk.X)
    
    def create_results_tab(self):
        """Cria aba de resultados"""
        
        frame = ttk.Frame(self.tab_results, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(
            frame,
            text="Resultados da Votação",
            font=("Arial", 12, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Botão atualizar
        refresh_btn = tk.Button(
            frame,
            text="🔄 Atualizar Resultados",
            command=self.load_results,
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            pady=8
        )
        refresh_btn.pack(pady=10, fill=tk.X)
        
        # Tabela de resultados
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para mostrar resultados
        columns = ("ID", "Candidato", "Votos")
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=10
        )
        
        # Configurar colunas
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("Candidato", text="Candidato")
        self.results_tree.heading("Votos", text="Votos")
        
        self.results_tree.column("ID", width=50, anchor=tk.CENTER)
        self.results_tree.column("Candidato", width=300)
        self.results_tree.column("Votos", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def register_voter(self):
        """Processa registo do eleitor"""
        cc_number = self.cc_entry.get().strip()
        
        if not cc_number:
            messagebox.showwarning("Aviso", "Insira o número do Cartão de Cidadão")
            return
        
        # Chama serviço de registo
        is_eligible, credential = self.voter_client.issue_voting_credential(cc_number)
        
        # Atualiza interface
        self.registration_result.config(state=tk.NORMAL)
        self.registration_result.delete(1.0, tk.END)
        
        if is_eligible:
            self.voting_credential = credential
            result_text = f"""
✓ REGISTO BEM SUCEDIDO

Eleitor elegível!
Credencial de voto emitida:

    {credential}

Pode agora dirigir-se ao separador
'Votação' para exercer o seu direito
de voto.
            """
            self.registration_result.insert(1.0, result_text)
            self.credential_label.config(
                text=f"✓ {credential}",
                fg="green"
            )
            
            # Muda para aba de votação
            self.notebook.select(self.tab_voting)
            
        else:
            result_text = f"""
✗ REGISTO FALHADO

Credencial inválida recebida:

    {credential}

Tente novamente ou contacte o
suporte técnico.
            """
            self.registration_result.insert(1.0, result_text)
        
        self.registration_result.config(state=tk.DISABLED)
    
    def load_candidates(self):
        """Carrega lista de candidatos"""
        candidates = self.voting_client.get_candidates()
        
        if not candidates:
            messagebox.showerror("Erro", "Não foi possível obter lista de candidatos")
            return
        
        self.candidates = candidates
        
        # Limpa frame
        for widget in self.candidates_frame.winfo_children():
            widget.destroy()
        
        # Cria radiobuttons para cada candidato
        for cid, name in candidates:
            rb = ttk.Radiobutton(
                self.candidates_frame,
                text=f"[{cid}] {name}",
                variable=self.selected_candidate,
                value=cid
            )
            rb.pack(anchor=tk.W, pady=5, padx=20)
        
        # Seleciona primeiro por defeito
        if candidates:
            self.selected_candidate.set(candidates[0][0])
        
        messagebox.showinfo("Sucesso", f"{len(candidates)} candidatos carregados")
    
    def submit_vote(self):
        """Submete voto"""
        
        # Verifica credencial
        if not self.voting_credential:
            messagebox.showwarning(
                "Aviso",
                "Precisa primeiro obter uma credencial de voto no separador 'Registo'"
            )
            self.notebook.select(self.tab_registration)
            return
        
        # Verifica se carregou candidatos
        if not self.candidates:
            messagebox.showwarning("Aviso", "Carregue primeiro a lista de candidatos")
            return
        
        candidate_id = self.selected_candidate.get()
        
        # Confirmação
        candidate_name = next((name for cid, name in self.candidates if cid == candidate_id), "Desconhecido")
        
        confirm = messagebox.askyesno(
            "Confirmar Voto",
            f"Confirma o seu voto em:\n\n{candidate_name}\n\nEsta ação não pode ser revertida."
        )
        
        if not confirm:
            return
        
        # Submete voto
        success, message = self.voting_client.vote(self.voting_credential, candidate_id)
        
        if success:
            messagebox.showinfo("Sucesso", f"✓ Voto registado com sucesso!\n\n{message}")
            # Limpa credencial (não pode votar novamente)
            self.voting_credential = None
            self.credential_label.config(text="Credencial já utilizada", fg="orange")
        else:
            messagebox.showerror("Erro", f"✗ Falha ao registar voto:\n\n{message}")
    
    def load_results(self):
        """Carrega resultados da votação"""
        results = self.voting_client.get_results()
        
        # Limpa tabela
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Preenche com resultados
        total_votes = 0
        for cid, name, votes in results:
            self.results_tree.insert("", tk.END, values=(cid, name, votes))
            total_votes += votes
        
        messagebox.showinfo("Resultados", f"Total de votos contabilizados: {total_votes}")
    
    def on_closing(self):
        """Callback ao fechar aplicação"""
        # Desconecta clientes
        self.voter_client.disconnect()
        self.voting_client.disconnect()
        # Fecha janela
        self.root.destroy()


def main():
    """Função principal"""
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
