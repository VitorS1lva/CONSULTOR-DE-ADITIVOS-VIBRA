#UTF-8  LANG.: PT-BR
import sqlite3
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

#inicio do laço da aplicação
main_screen=Tk()

#funcionalidade dos botões da aplicação
class Funcs():
    def limpar_campos(self):
        self.add_entry_codigo.delete(0, END)
        self.add_entry_aditivo.delete(0, END)
        self.add_entry_deposito.delete(0, END)
        self.add_entry_estufa.delete(0, END)
        self.add_entry_transf.delete(0, END)
        self.add_entry_visc.delete(0, END)
        self.add_entry_peso.delete(0, END)
        self.add_entry_dens.delete(0, END)
    def conect_db(self):
        self.conect=sqlite3.connect('banco_aditivos.db')
        self.cursor=self.conect.cursor(); print('Conectando ao banco de dados')
    def desconect_db(self):
        self.conect.close()
    def montar_tabelas(self):
        self.conect_db()
        ### criar tabela de aditivos
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS tabela_aditivos (
                 cod INTEGER PRIMARY KEY,
                 aditivo CHAR(40) NOT NULL,
                 deposito CHAR(40),
                 estufa CHAR(40),
                 transferencia CHAR(40),
                 viscosidade CHAR(40),
                 peso INTEGER(20),
                 densidade INTEGER(20)
             );
         """)
        # validando informações no banco de dados
        self.conect.commit();
        print("Banco de dados criado")
        self.desconect_db()
    def var_insercoes(self):
        self.codigo=self.add_entry_codigo.get()
        self.aditivo = self.add_entry_aditivo.get()
        self.deposito = self.add_entry_deposito.get()
        self.estufa = self.add_entry_estufa.get()
        self.transf = self.add_entry_transf.get()
        self.visc = self.add_entry_visc.get()
        self.peso = self.add_entry_peso.get()
        self.dens = self.add_entry_dens.get()
    def add_dados_db(self):
        #self.codigo=self.add_entry_codigo.get()
        self.var_insercoes()
        #chamando o sqlite3
        self.conect_db()

        self.cursor.execute(""" INSERT INTO tabela_aditivos (aditivo, deposito, estufa, transferencia, viscosidade, peso, densidade)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.aditivo, self.deposito, self.estufa, self.transf,
                                             self.visc, self.peso, self.dens))
        self.conect.commit()
        self.desconect_db()
        self.busca_dados_db()
        self.limpar_campos()
    def busca_dados_db(self):
        self.listaAdv.delete(*self.listaAdv.get_children())
        self.conect_db()
        lista = self.cursor.execute(""" SELECT cod, aditivo, deposito, estufa, transferencia, viscosidade, peso, densidade 
            FROM tabela_aditivos ORDER BY aditivo ASC; """)
        for i in lista:
           self.listaAdv.insert("", END, values=i)
        self.desconect_db()
    def busca_registro(self):
        self.conect_db()
        self.listaAdv.delete(*self.listaAdv.get_children())

        self.add_entry_aditivo.insert(END, '%')
        nome = self.add_entry_aditivo.get()
        self.cursor.execute(""" SELECT cod, aditivo, deposito, estufa, transferencia, viscosidade, peso, densidade
                            FROM tabela_aditivos WHERE aditivo LIKE '%s' ORDER BY aditivo ASC""" % nome)
        buscanomeAdv=self.cursor.fetchall()
        for i in buscanomeAdv:
            self.listaAdv.insert("", END, values=i)
        self.limpar_campos()
        self.desconect_db()
    def ondoubleclick(self, event):
        self.limpar_campos()
        self.listaAdv.selection()

        for n in self.listaAdv.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.listaAdv.item(n, 'values')
            self.add_entry_codigo.insert(END, col1)
            self.add_entry_aditivo.insert(END, col2)
            self.add_entry_deposito.insert(END, col3)
            self.add_entry_estufa.insert(END, col4)
            self.add_entry_transf.insert(END, col5)
            self.add_entry_visc.insert(END, col6)
            self.add_entry_peso.insert(END, col7)
            self.add_entry_dens.insert(END, col8)
    def deleta_campos(self):
        self.var_insercoes()
        self.conect_db()
        self.cursor.execute("""DELETE FROM tabela_aditivos WHERE cod=?""", [self.codigo])
        self.conect.commit()
        self.desconect_db()
        self.limpar_campos()
        self.busca_dados_db()
    def alterar_campos(self):
        self.var_insercoes()
        self.conect_db()
        self.cursor.execute(""" UPDATE tabela_aditivos SET aditivo=?, deposito=?, estufa=?,
         transferencia=?, viscosidade=?, peso=?, densidade=?
         WHERE cod=? """, (self.aditivo, self.deposito, self.estufa, self.transf, self.visc, self.peso, self.dens, self.codigo))
        self.conect.commit()
        self.desconect_db()
        self.busca_dados_db()
        self.limpar_campos()

# estrutura da aplicação
class Application(Funcs):
    def __init__(self):
        self.main_screen=main_screen
        self.tela_principal_design()
        self.montar_tabelas()
        self.busca_dados_db()
        self.limpar_campos()
        self.deleta_campos()
        self.menu_bar()
        main_screen.mainloop()
    def tela_principal_design(self):
        self.main_screen.title("CONSULTOR ADITIVOS VIBRA")
        self.main_screen.geometry("650x500")
        self.main_screen.resizable(True, True)
        self.main_screen.configure(background='#004415')
        self.main_screen.iconbitmap('imagem_2022-04-30_110511930.ico')

        ## frame icone vibra
        im = Image.open('logovibra.png')
        ph = ImageTk.PhotoImage(im)
        self.icolabel=Label(self.main_screen, image=ph, compound=tkinter.CENTER)
        self.icolabel.image=ph
        self.icolabel.place(relx=0.53, rely=0.115, relwidth=0.45, relheight=0.32)

        #treeview
        self.listaAdv = ttk.Treeview(self.main_screen, columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6',
                                                                'col7', 'col8'))
        self.listaAdv.place(relx=0.05, rely=0.48, relwidth=0.94, relheight=0.45)
        self.listaAdv.heading("#0", tex='')
        self.listaAdv.heading("#1", tex='ID')
        self.listaAdv.heading("#2", tex='ADITIVO')
        self.listaAdv.heading("#3", tex='DEPÓSITO')
        self.listaAdv.heading("#4", tex='ESTUFA')
        self.listaAdv.heading("#5", tex='TRANSF.')
        self.listaAdv.heading("#6", tex='VISC.')
        self.listaAdv.heading("#7", tex='PESO')
        self.listaAdv.heading("#8", tex='DENSIDADE')
        self.listaAdv.column("#0", width=0)
        self.listaAdv.column("#1", width=1)
        self.listaAdv.column("#2", width=35)
        self.listaAdv.column("#3", width=35)
        self.listaAdv.column("#4", width=35)
        self.listaAdv.column("#5", width=30)
        self.listaAdv.column("#6", width=27)
        self.listaAdv.column("#7", width=20)
        self.listaAdv.column("#8", width=35)

        self.scrollistaadvver=Scrollbar(self.main_screen, orient='vertical')
        self.scrollistaadvver.place(relx=0.965, rely=0.48, relheight=0.45, relwidth=0.025)
        #self.scrollistaadvhor=Scrollbar(self.main_screen, orient='horizontal')
        #self.scrollistaadvhor.place(relx=0.05,rely= 0.905, relheight=0.02, relwidth=0.94)
        self.listaAdv.configure(yscroll=self.scrollistaadvver.set)
        #self.listaAdv.configure(xscroll=self.scrollistaadvhor.set)
        self.listaAdv.bind("<Double-1>", self.ondoubleclick) #referência do tipo de interação que estamos fazendo

        # frame e botoes de adição
        self.frame_botoes = Frame(self.main_screen, bg='#004415')
        self.frame_botoes.place(relx=0.01, rely=0.1, relwidth=0.5, relheight=0.35)
        self.label_principal=Label(self.main_screen,text='-ADICIONAR ADITIVOS-', bg='#004415', fg='white')
        self.label_principal.place(relx=0.045, rely=0.05, relwidth=0.5, relheight=0.05)
        self.botao_inserir = Button(self.frame_botoes, text='INSERIR', command=self.add_dados_db, bd=3, bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_inserir.place(relx=0.78, rely=0.05, relwidth=0.2, relheight=0.15)
        self.botao_excluir = Button(self.frame_botoes, text='EXCLUIR', command=self.deleta_campos, bd=3, bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_excluir.place(relx=0.78, rely=0.25, relwidth=0.2, relheight=0.15)
        self.botao_editar = Button(self.frame_botoes, text='EDITAR', command=self.alterar_campos, bd=3, bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_editar.place(relx=0.78, rely=0.435, relwidth=0.2, relheight=0.15)
        self.botao_limpar = Button(self.frame_botoes, text='LIMPAR', command=self.limpar_campos, bd=3, bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_limpar.place(relx=0.78, rely=0.635, relwidth=0.2, relheight=0.15)
        self.botao_pesquisar = Button(self.frame_botoes, text='PESQUISAR', command=self.busca_registro, bd=3,
                                      bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_pesquisar.place(relx=0.78, rely=0.81, relwidth=0.2, relheight=0.15)

        ## entrys, labels e dropdown boxes
        self.add_entry_codigo=Entry(self.frame_botoes, bg='#004415')
        self.add_entry_codigo.place(relx=0.35, rely=0.05, relwidth=0.20, relheight=0.1)

        self.aditivo_label_add=Label(self.frame_botoes, text='ADITIVO: ', background='#004415', foreground='white')
        self.aditivo_label_add.place(relx=0.06, rely=0.05, relheight=0.1, relwidth=0.3)
        self.add_entry_aditivo=Entry(self.frame_botoes)
        self.add_entry_aditivo.place(relx=0.29, rely=0.05, relwidth=0.47, relheight=0.1)

        self.deposito_label_add = Label(self.frame_botoes, text='DEPÓSITO:', background='#004415', foreground='white')
        self.deposito_label_add.place(relx=0.039, rely=0.17, relheight=0.1, relwidth=0.3)
        self.add_entry_deposito = Entry(self.frame_botoes)
        self.add_entry_deposito.place(relx=0.29, rely=0.17, relwidth=0.47, relheight=0.1)

        self.estufa_label_add = Label(self.frame_botoes, text='ESTUFA:', background='#004415', foreground='white')
        self.estufa_label_add.place(relx=0.058, rely=0.29, relheight=0.1, relwidth=0.3)
        self.add_entry_estufa = Entry(self.frame_botoes)
        self.add_entry_estufa.place(relx=0.29, rely=0.29, relwidth=0.47, relheight=0.1)

        self.transf_label_add = Label(self.frame_botoes, text='TRÂNSF.:', background='#004415', foreground='white')
        self.transf_label_add.place(relx=0.0496, rely=0.40, relheight=0.1, relwidth=0.3)
        self.add_entry_transf = Entry(self.frame_botoes)
        self.add_entry_transf.place(relx=0.29, rely=0.40, relwidth=0.47, relheight=0.1)

        self.visc_label_add = Label(self.frame_botoes, text='VISCOSIDADE:', background='#004415', foreground='white')
        self.visc_label_add.place(relx=0.014, rely=0.51, relheight=0.1, relwidth=0.3)
        self.add_entry_visc = Entry(self.frame_botoes)
        self.add_entry_visc.place(relx=0.29, rely=0.51, relwidth=0.47, relheight=0.1)

        self.peso_label_add = Label(self.frame_botoes, text='PESO:', background='#004415', foreground='white')
        self.peso_label_add.place(relx=0.0762, rely=0.62, relheight=0.1, relwidth=0.3)
        self.add_entry_peso = Entry(self.frame_botoes)
        self.add_entry_peso.place(relx=0.29, rely=0.62, relwidth=0.47, relheight=0.1)

        self.dens_label_add = Label(self.frame_botoes, text='DENSIDADE:', background='#004415', foreground='white')
        self.dens_label_add.place(relx=0.027, rely=0.73, relheight=0.1, relwidth=0.3)
        self.add_entry_dens = Entry(self.frame_botoes)
        self.add_entry_dens.place(relx=0.29, rely=0.73, relwidth=0.47, relheight=0.1)

        ''''#### frame de pesquisa
        self.frame_pesquisa = Frame(self.main_screen, bg='#004415')
        self.frame_pesquisa.place(relx=0.05, rely=0.1, relwidth=0.5, relheight=0.43)
        self.label_pesquisa=Label(self.frame_pesquisa, text='PESQUISE O ADITIVO', background='#004415', foreground='white')
        self.label_pesquisa.place(relx=0.163, rely=0.07, relwidth=0.356, relheight=0.1)
        self.botao_pesquisar=Button(self.frame_pesquisa, text='PESQUISAR', command=self.busca_registro, bd=3, bg='#0a3818', fg='white', font=('arial', 8, 'bold'))
        self.botao_pesquisar.place(relx=0.66, rely=0.18, relwidth=0.27, relheight=0.1)
        self.pesquisa_entry=Entry(self.frame_pesquisa)
        self.pesquisa_entry.place(relx=0.16, rely=0.18, relwidth=0.48, relheight=0.1)
            # LABELS DE CONSULTA
        self.label_aditivo=Label(self.frame_pesquisa, text='ADITIVO: ', background='#004415', foreground='white')
        self.label_aditivo.place(relx=0.14, rely=0.32, relwidth=0.15, relheight=0.1)
        self.entry_aditivo=Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_aditivo.place(relx=0.31 ,rely=0.32, relwidth=0.55, relheight=0.1)

        self.label_dep=Label(self.frame_pesquisa, text='DEPÓSITO: ', background='#004415', foreground='white')
        self.label_dep.place(relx=0.115, rely=0.45, relwidth=0.17, relheight=0.1)
        self.entry_dep = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_dep.place(relx=0.31, rely=0.45, relwidth=0.55, relheight=0.1)

        self.label_estufa=Label(self.frame_pesquisa, text='ESTUFA: ', background='#004415', foreground='white')
        self.label_estufa.place(relx=0.137, rely=0.58, relwidth=0.17, relheight=0.1)
        self.entry_estufa = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_estufa.place(relx=0.31, rely=0.58, relwidth=0.36, relheight=0.1)

        self.label_transf = Label(self.frame_pesquisa, text='TRANSFERÊNCIA: ', background='#004415', foreground='white')
        self.label_transf.place(relx=0.017, rely=0.70, relwidth=0.27, relheight=0.1)
        self.entry_transf = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_transf.place(relx=0.31, rely=0.70, relwidth=0.25, relheight=0.1)

        self.label_visc = Label(self.frame_pesquisa, text='VISCOSIDADE: ', background='#004415', foreground='white')
        self.label_visc.place(relx=0.065, rely=0.82, relwidth=0.22, relheight=0.1)
        self.entry_visc = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_visc.place(relx=0.31, rely=0.82, relwidth=0.55, relheight=0.1)

        self.label_peso = Label(self.frame_pesquisa, text='PESO: ', background='#004415', foreground='white')
        self.label_peso.place(relx=0.688, rely=0.58, relwidth=0.10, relheight=0.1)
        self.entry_peso = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_peso.place(relx=0.798, rely=0.58, relwidth=0.15, relheight=0.1)

        self.label_dens = Label(self.frame_pesquisa, text='DENSIDADE: ', background='#004415', foreground='white')
        self.label_dens.place(relx=0.58, rely=0.70, relwidth=0.22, relheight=0.1)
        self.entry_dens = Entry(self.frame_pesquisa, background='#004415', foreground='white')
        self.entry_dens.place(relx=0.798, rely=0.70, relwidth=0.15, relheight=0.1)'''
    def menu_bar(self):
        menubar=Menu(self.main_screen)
        self.main_screen.config(menu=menubar)
        filemenu=Menu(menubar)
        filemenu2=Menu(menubar)

        def Quit(): self.main_screen.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Sobre", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu2.add_command(label="Versão do programa = 1.0")
        filemenu2.add_command(label="Python, 3.10 (Libraries: TKinter, MySql")
        filemenu2.add_command(label="Código idealizado por: Vitor Roque (Op.3)")
        filemenu2.add_command(label="Código realizado por: Vitor Pereira(Software Developer)")

# mantendo loop da janela
Application()