import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pygame
from pygame import mixer
import os
import pandas as pd
from dados import df

class QuizApp:
    def __init__(self):
        self.janela = ctk.CTk()
        self.configurar_janela()
        self.carregar_recursos()
        self.inicializar_variaveis()
        self.criar_interface()
        self.iniciar_quiz()
        
    def configurar_janela(self):
        """Configurações básicas da janela principal"""
        self.janela.title('Quiz Verde: Você sabe cuidar do planeta?')
        self.janela.geometry("550x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")
        
    def carregar_recursos(self):
        """Carrega recursos externos (sons e imagens)"""
        try:
            pygame.init()
            mixer.init()
            
            # Carrega arquivos de áudio
            base_dir = os.path.dirname(os.path.abspath(__file__))
            caminho_acerto = os.path.join(base_dir, "sons", "acertou", "aplauso.wav")
            caminho_erro = os.path.join(base_dir, "sons", "errou", "erro_curto.mp3")
            
            self.som_acerto = mixer.Sound(caminho_acerto) if os.path.exists(caminho_acerto) else None
            self.som_erro = mixer.Sound(caminho_erro) if os.path.exists(caminho_erro) else None
            
            if self.som_acerto: self.som_acerto.set_volume(0.7)
            if self.som_erro: self.som_erro.set_volume(0.7)
            
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
            self.som_acerto = self.som_erro = None
            
        try:
            # Carrega imagem da logo
            caminho_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            if os.path.exists(caminho_logo):
                self.logo_img = ctk.CTkImage(
                    light_image=Image.open(caminho_logo),
                    dark_image=Image.open(caminho_logo),
                    size=(120, 120))
            else:
                self.logo_img = None
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            self.logo_img = None
    
    def inicializar_variaveis(self):
        """Inicializa variáveis do jogo"""
        num_perguntas = min(10, len(df))
        self.perguntas = df.sample(n=num_perguntas, replace=True if len(df) < 10 else False).values.tolist()
        self.score = 0
        self.pergunta_atual = 0
        self.tempo_restante = 30
        self.timer_id = None
        
    def criar_interface(self):
        """Cria todos os elementos da interface gráfica"""
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.janela, corner_radius=15)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Logo
        if self.logo_img:
            self.logo_label = ctk.CTkLabel(self.frame_principal, image=self.logo_img, text="")
        else:
            self.logo_label = ctk.CTkLabel(self.frame_principal, text="Quiz Verde", font=("Arial", 24, "bold"))
        self.logo_label.pack(pady=10)
        
        # Painel de informações (pontuação e tempo)
        self.frame_contadores = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_contadores.pack(pady=5)
        
        self.label_pontuacao = ctk.CTkLabel(self.frame_contadores, text=f"Pontuação: {self.score}", font=("Arial", 14))
        self.label_pontuacao.pack(side="left", padx=10)
        
        self.label_tempo = ctk.CTkLabel(self.frame_contadores, text=f"Tempo: {self.tempo_restante}s", font=("Arial", 14))
        self.label_tempo.pack(side="right", padx=10)
        
        # Barra de progresso
        self.barra_progresso = ctk.CTkProgressBar(self.frame_principal, height=10)
        self.barra_progresso.pack(pady=10, padx=20, fill="x")
        self.barra_progresso.set(0)
        
        # Área da pergunta
        self.label_pergunta = ctk.CTkLabel(
            self.frame_principal, 
            text="", 
            wraplength=480,
            font=("Arial", 16, "bold"),
            justify="center")
        self.label_pergunta.pack(pady=20, padx=10)
        
        # Botões de resposta
        self.frame_botoes = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botoes.pack(pady=10, padx=10, fill="both", expand=True)
        
        estilo_botao = {
            "width": 320,
            "height": 50,
            "font": ("Arial", 14),
            "corner_radius": 10,
            "fg_color": "#2E7D32",
            "hover_color": "#1B5E20",
            "border_width": 2,
            "border_color": "#FFFFFF"
        }
        
        self.botao_opcao1 = ctk.CTkButton(self.frame_botoes, text="", **estilo_botao)
        self.botao_opcao1.pack(pady=8)
        
        self.botao_opcao2 = ctk.CTkButton(self.frame_botoes, text="", **estilo_botao)
        self.botao_opcao2.pack(pady=8)
        
        self.botao_opcao3 = ctk.CTkButton(self.frame_botoes, text="", **estilo_botao)
        self.botao_opcao3.pack(pady=8)
        
        # Botão de reinício
        self.botao_reiniciar = ctk.CTkButton(
            self.frame_principal, 
            text="Jogar Novamente", 
            width=220,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=self.reiniciar_quiz)
    
    def iniciar_quiz(self):
        """Inicia o fluxo do quiz"""
        if not hasattr(self, 'perguntas') or len(self.perguntas) == 0:
            messagebox.showerror("Erro", "Não há perguntas disponíveis!")
            return
            
        self.mostrar_pergunta()
        self.iniciar_temporizador()
    
    def iniciar_temporizador(self):
        """Configura e inicia o temporizador para cada pergunta"""
        if self.timer_id:
            self.janela.after_cancel(self.timer_id)
            
        self.tempo_restante = 30
        self.label_tempo.configure(text=f"Tempo: {self.tempo_restante}s", text_color="white")
        self.atualizar_temporizador()
    
    def atualizar_temporizador(self):
        """Atualiza o contador de tempo a cada segundo"""
        self.tempo_restante -= 1
        self.label_tempo.configure(text=f"Tempo: {self.tempo_restante}s")
        
        if self.tempo_restante <= 10:
            self.label_tempo.configure(text_color="red")
            
        if self.tempo_restante > 0:
            self.timer_id = self.janela.after(1000, self.atualizar_temporizador)
        else:
            self.tempo_esgotado()
    
    def tempo_esgotado(self):
        """Ações quando o tempo acaba"""
        if self.som_erro:
            self.som_erro.play()
                
        self.mostrar_feedback(False)
        messagebox.showinfo("Tempo Esgotado", "O tempo para responder acabou!")
        self.proxima_pergunta()
    
    def mostrar_pergunta(self):
        """Exibe a pergunta atual e suas opções"""
        pergunta = self.perguntas[self.pergunta_atual]
        self.label_pergunta.configure(text=pergunta[0])
        
        self.botao_opcao1.configure(text=pergunta[1], command=lambda: self.verificar_resposta(1))
        self.botao_opcao2.configure(text=pergunta[2], command=lambda: self.verificar_resposta(2))
        self.botao_opcao3.configure(text=pergunta[3], command=lambda: self.verificar_resposta(3))
        
        progresso = (self.pergunta_atual + 1) / len(self.perguntas)
        self.barra_progresso.set(progresso)
        
        self.iniciar_temporizador()
    
    def verificar_resposta(self, resposta):
        """Verifica se a resposta selecionada está correta"""
        if self.timer_id:
            self.janela.after_cancel(self.timer_id)
        
        if resposta == self.perguntas[self.pergunta_atual][4]:
            self.resposta_correta()
        else:
            self.resposta_errada()
        
        self.proxima_pergunta()
    
    def resposta_correta(self):
        """Ações para resposta correta"""
        self.score += 1
        self.label_pontuacao.configure(text=f"Pontuação: {self.score}")
        
        if self.som_acerto:
            self.som_acerto.play()
                
        self.mostrar_feedback(True)
    
    def resposta_errada(self):
        """Ações para resposta errada"""
        if self.som_erro:
            self.som_erro.play()
                
        self.mostrar_feedback(False)
        resposta_correta = self.perguntas[self.pergunta_atual][4]
        explicacao = self.perguntas[self.pergunta_atual][6] if len(self.perguntas[self.pergunta_atual]) > 6 else ""
        
        messagebox.showinfo(
            "Resposta Correta", 
            f"A resposta correta era: {self.perguntas[self.pergunta_atual][resposta_correta]}\n\n{explicacao}")
    
    def proxima_pergunta(self):
        """Avança para a próxima pergunta ou finaliza o quiz"""
        self.pergunta_atual += 1
        if self.pergunta_atual < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            self.finalizar_quiz()
    
    def finalizar_quiz(self):
        """Exibe resultados finais e opções"""
        messagebox.showinfo(
            "Fim do Quiz", 
            f"Quiz concluído!\nPontuação final: {self.score}/{len(self.perguntas)}")
        self.botao_reiniciar.pack(pady=20)
        self.desativar_botoes()
    
    def desativar_botoes(self):
        """Desativa os botões de resposta"""
        for botao in [self.botao_opcao1, self.botao_opcao2, self.botao_opcao3]:
            botao.configure(state="disabled")
    
    def ativar_botoes(self):
        """Ativa os botões de resposta"""
        for botao in [self.botao_opcao1, self.botao_opcao2, self.botao_opcao3]:
            botao.configure(state="normal")
    
    def reiniciar_quiz(self):
        """Reinicia o quiz para uma nova partida"""
        self.inicializar_variaveis()
        self.label_pontuacao.configure(text=f"Pontuação: {self.score}")
        self.botao_reiniciar.pack_forget()
        self.ativar_botoes()
        self.mostrar_pergunta()
    
    def mostrar_feedback(self, correto):
        """Exibe feedback visual para respostas"""
        feedback = ctk.CTkToplevel(self.janela)
        feedback.geometry("300x150")
        feedback.overrideredirect(True)
        feedback.attributes('-alpha', 0.9)
        
        janela_x = self.janela.winfo_x()
        janela_y = self.janela.winfo_y()
        feedback.geometry(f"+{janela_x+125}+{janela_y+250}")
        
        if correto:
            label = ctk.CTkLabel(feedback, text="✓ CORRETO", text_color="#4CAF50", font=("Arial", 24, "bold"))
        else:
            label = ctk.CTkLabel(feedback, text="✗ ERRADO", text_color="#F44336", font=("Arial", 24, "bold"))
        
        label.pack(expand=True, fill='both')
        feedback.after(800, lambda: feedback.destroy())

if __name__ == "__main__":
    try:
        app = QuizApp()
        app.janela.mainloop()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{e}")