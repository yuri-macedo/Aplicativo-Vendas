from kivy.app import App
from kivy.lang import Builder
from paginas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial
from myfirebase import MyFirebase
from bannervendedor import BannerVendedor
from datetime import date

GUI = Builder.load_file("main.kv")

class MainApp(App):
    cliente = None
    produto = None
    data = None
    unidade = None

    def build(self):
        self.firebase=MyFirebase()
        return GUI
    def on_start(self):
        self.carregar_info_usuario()

        #Obter Lista de Fotos de Perfil
        fotos=os.listdir("icones/fotos_perfil")
        foto_perfil_page=self.root.ids["fotoperfilpage"]
        lista_fotos_perfil=foto_perfil_page.ids["id_lista_fotos_perfil"]
        for foto in fotos:
            imagem=ImageButton(source=f"icones/fotos_perfil/{foto}",on_release=partial(self.mudar_foto_perfil,foto))
            lista_fotos_perfil.add_widget(imagem)

        #Obter Lista de Clientes
        arquivos=os.listdir("icones/fotos_clientes")
        pagina_adicionar_venda=self.root.ids["adicionarvendaspage"]
        lista_clientes=pagina_adicionar_venda.ids["id_lista_clientes"]
        for cliente in arquivos:
            Imagem=ImageButton(source=f"icones/fotos_clientes/{cliente}",
                               on_release=partial(self.selecionar_cliente,cliente))
            Label=LabelButton(text=cliente.replace(".png","").capitalize(),
                              on_release=partial(self.selecionar_cliente,cliente))
            lista_clientes.add_widget(Imagem)
            lista_clientes.add_widget(Label)

        # Obter Lista de Produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionar_venda = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionar_venda.ids["id_lista_produtos"]
        for produto in arquivos:
            Imagem = ImageButton(source=f"icones/fotos_produtos/{produto}",
                               on_release=partial(self.selecionar_produto,produto))
            Label = LabelButton(text=produto.replace(".png", "").capitalize(),
                               on_release=partial(self.selecionar_produto,produto))
            lista_produtos.add_widget(Imagem)
            lista_produtos.add_widget(Label)

        #Obter Data
        data=pagina_adicionar_venda.ids["id_data"]
        data.text=date.today().strftime("%d/%m/%Y")
        self.data=data.text

    def carregar_info_usuario(self):
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, token_id = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.token_id = token_id
            # Obter informações do úsuario
            requisicao = requests.get(
                f'https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.token_id}').json()
            avatar = requisicao["avatar"]
            self.avatar=avatar

            # Obter Foto Perfil
            foto_perfil = self.root.ids["id_foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            #Obter ID Usuário
            id_vendedor_valor=requisicao["id_vendedor"]
            self.id_vendedor=id_vendedor_valor

            ajustespage=self.root.ids["ajustespage"]
            id_vendedor=ajustespage.ids["id_vendedor"]
            id_vendedor.text=f"Seu ID Único: {id_vendedor_valor}"

            #Obter o Total de Vendas do Vendedor
            total_vendas_valor = requisicao["total_vendas"]
            self.total_vendas=float(total_vendas_valor)

            homepage = self.root.ids["homepage"]
            id_total_vendas = homepage.ids["id_total_vendas"]
            id_total_vendas.text = f"[color=#000000]Total Vendas:[/color] R$ {float(total_vendas_valor):,.2f}"

            # Obter Lista de Vendas
            try:
                vendas = requisicao["vendas"]
                self.vendas=vendas
                pagina_homepage = self.root.ids["homepage"]
                lista_vendas = pagina_homepage.ids["id_lista_vendas"]
                for indice in vendas:
                    venda = vendas[indice]
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda['data'], preco=venda['preco'],
                                         unidade=venda['unidade'], quantidade=venda["quantidade"])

                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                print(excecao)
                pass

            # Obter Lista de Vendedores
            listar_vendedores_page = self.root.ids["listarvendedorespage"]
            id_lista_vendedores=listar_vendedores_page.ids["id_lista_vendedores"]
            equipe=requisicao["equipe"]
            self.equipe=equipe

            lista_equipe = equipe.split(",")
            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe!="":
                    banner_vendedor=BannerVendedor(id_vendedor_equipe=id_vendedor_equipe)
                    id_lista_vendedores.add_widget(banner_vendedor)

            self.mudar_tela("homepage")
        except:
            print("error")
            pass
    def mudar_tela(self,id_tela):
        manager=self.root.ids["screen_manager"]
        manager.current=id_tela

    def mudar_foto_perfil(self,foto,*args):
        foto_perfil = self.root.ids["id_foto_perfil"]
        foto_perfil.source=f"icones/fotos_perfil/{foto}"
        self.avatar=foto

        requisicao = requests.patch(f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.token_id}",
                                    data=f'{{"avatar":"{foto}"}}')

    def adicionar_vendedor(self,id_vendedor_adicionado):
        link= f'https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        requisicao=requests.get(link).json()

        pagina_adicionar_vendedor = self.root.ids["adicionarvendedorpage"]
        mensagem_adicionar_vendedor = pagina_adicionar_vendedor.ids["id_mensagem_outro_vendedor"]
        if requisicao=={}:
            mensagem_adicionar_vendedor.text="Vendedor não existe"
        else:
            if id_vendedor_adicionado in self.equipe.split(","):
                mensagem_adicionar_vendedor.text = "Vendedor já está na equipe"
            elif id_vendedor_adicionado==self.id_vendedor:
                mensagem_adicionar_vendedor.text = "Não pode se adicionar a equipe"
            else:
                self.equipe+=f",{id_vendedor_adicionado}"
                info=f'{{"equipe":"{self.equipe}"}}'
                requisicao = requests.patch(
                    f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.token_id}",data=info)

                listar_vendedores_page = self.root.ids["listarvendedorespage"]
                id_lista_vendedores = listar_vendedores_page.ids["id_lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor_equipe=id_vendedor_adicionado)
                id_lista_vendedores.add_widget(banner_vendedor)


                mensagem_adicionar_vendedor.text = "Vendedor adicinado"

    def selecionar_cliente(self,cliente,*args):
        #Pintar todos de branco
        pagina_adidionar_vendas=self.root.ids["adicionarvendaspage"]
        lista_clientes=pagina_adidionar_vendas.ids["id_lista_clientes"]

        for item in list(lista_clientes.children):
            item.color=(1,1,1,1)

            #Pintar o selecionado de azul
            try:
                if cliente.replace(".png","").capitalize()==item.text:
                    self.cliente=cliente
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass
        # Pintar o texto "Selecionar Cliente" de branco
        pagina_adidionar_vendas.ids["id_label_cliente"].color = (1, 1, 1, 1)

    def selecionar_produto(self,produto,*args):
        #Pintar todos de branco
        pagina_adidionar_vendas=self.root.ids["adicionarvendaspage"]
        lista_produto=pagina_adidionar_vendas.ids["id_lista_produtos"]

        for item in list(lista_produto.children):
            item.color=(1,1,1,1)

            #Pintar o selecionado de azul
            try:
                if produto.replace(".png","").capitalize()==item.text:
                    self.produto=produto
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass
        #Pintar o texto "Selecionar Produto" de branco
        pagina_adidionar_vendas.ids["id_label_produto"].color = (1, 1, 1, 1)

    def selecionar_unidade(self,id_unidade):
        pagina_adidionar_vendas = self.root.ids["adicionarvendaspage"]

        # Pintar todos de branco
        pagina_adidionar_vendas.ids["id_kg"].color = (1, 1, 1, 1)
        pagina_adidionar_vendas.ids["id_unidades"].color = (1, 1, 1, 1)
        pagina_adidionar_vendas.ids["id_litros"].color = (1, 1, 1, 1)

        # Pintar o selecionado de azul
        pagina_adidionar_vendas.ids[id_unidade].color = (0, 207/255, 219/255, 1)
        self.unidade=id_unidade.replace("id_","")

    def adicionar_produto(self):
        pagina_adidionar_vendas = self.root.ids["adicionarvendaspage"]
        cliente = None
        produto = None

        foto_cliente = self.cliente
        foto_produto = self.produto
        unidade = self.unidade
        data = self.data
        preco = pagina_adidionar_vendas.ids["id_preco_total"].text
        quantidade = pagina_adidionar_vendas.ids["id_quantidade"].text

        if foto_cliente:
            cliente = self.cliente.replace(".png", "")
        else:
            pagina_adidionar_vendas.ids["id_label_cliente"].color=(1,0,0,1)

        if foto_produto:
            produto = self.produto.replace(".png", "")
        else:
            pagina_adidionar_vendas.ids["id_label_produto"].color=(1,0,0,1)

        if not unidade:
            pagina_adidionar_vendas.ids["id_kg"].color = (1,0,0,1)
            pagina_adidionar_vendas.ids["id_unidades"].color = (1,0,0,1)
            pagina_adidionar_vendas.ids["id_litros"].color = (1,0,0,1)

        if not preco:
            pagina_adidionar_vendas.ids["id_label_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco=float(preco)
            except:
                pagina_adidionar_vendas.ids["id_label_preco"].color = (1, 0, 0, 1)

        if not quantidade:
            pagina_adidionar_vendas.ids["id_label_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade=float(quantidade)
            except:
                pagina_adidionar_vendas.ids["id_label_quantidade"].color = (1, 0, 0, 1)

        if cliente and produto and foto_cliente and foto_produto and unidade and type(preco)==float and type(quantidade)==float and data:
            link = f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.token_id}"
            info = f'{{"cliente":"{cliente}","foto_cliente":"{foto_cliente}","produto":"{produto}","foto_produto":"{foto_produto}","unidade":"{unidade}","data":"{data}","preco":"{preco}","quantidade":"{quantidade}"}}'
            requests.post(f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.token_id}", data=info)

            pagina_homepage=self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["id_lista_vendas"]
            banner = BannerVenda(cliente=cliente, foto_cliente=foto_cliente,
                                 produto=produto, foto_produto=foto_produto,
                                 data=data, preco=preco,
                                 unidade=unidade, quantidade=quantidade)
            lista_vendas.add_widget(banner)
            self.mudar_tela("homepage")

            link = f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.token_id}"
            self.total_vendas+=preco
            info=f'{{"total_vendas":"{self.total_vendas}"}}'
            requests.patch(link,data=info)

            homepage = self.root.ids["homepage"]
            id_total_vendas = homepage.ids["id_total_vendas"]
            id_total_vendas.text = f"[color=#000000]Total Vendas:[/color] R$ {float(self.total_vendas):,.2f}"


        self.cliente = None
        self.produto = None
        self.unidade = None
        cliente = None
        produto = None

    def carregar_todas_vendas_page(self):
        # Limpar a Lista de Banners
        pagina_todas_vendas = self.root.ids["todasvendaspage"]
        lista_vendas = pagina_todas_vendas.ids["id_lista_vendas"]
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)
        # Obter Foto Perfil
        foto_perfil = self.root.ids["id_foto_perfil"]
        foto_perfil.source = "icones/fotos_perfil/hash.png"

        # Obter Lista de Vendas
        total_vendas = 0

        requisicao = requests.get('https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"').json()


        for id_local_usuario in requisicao:
            try:
                vendas = requisicao[id_local_usuario]["vendas"]
                for indice in vendas:

                    venda = vendas[indice]
                    total_vendas += float(venda['preco'])
                    banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                         produto=venda["produto"], foto_produto=venda["foto_produto"],
                                         data=venda['data'], preco=venda['preco'],
                                         unidade=venda['unidade'], quantidade=venda["quantidade"])


                    lista_vendas.add_widget(banner)
            except Exception as excecao:
                print(excecao)
                pass


        # Obter o Total de Vendas da Empresa
        id_total_vendas = pagina_todas_vendas.ids["id_total_vendas"]
        id_total_vendas.text = f"[color=#000000]Total Vendas:[/color] R$ {float(total_vendas):,.2f}"
        self.mudar_tela("todasvendaspage")

    def sair_e_alterar_imagem(self,id_page):
        self.root.ids["id_foto_perfil"].source=f"icones/fotos_perfil/{self.avatar}"
        self.mudar_tela(id_page)

    def carregar_outro_vendedor_page(self,info_outro_vendedor,*args):
        avatar=info_outro_vendedor["avatar"]

        # Limpar a Lista de Banners
        pagina_outro_vendedor = self.root.ids["outrovendedorpage"]
        lista_vendas = pagina_outro_vendedor.ids["id_lista_vendas"]
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)

        # Obter Foto Perfil
        foto_perfil = self.root.ids["id_foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # Obter Lista de Vendas
        total_vendas = 0
        try:
            vendas = info_outro_vendedor["vendas"]
            for indice in vendas:
                venda = vendas[indice]
                total_vendas += float(venda['preco'])
                banner = BannerVenda(cliente=venda["cliente"], foto_cliente=venda["foto_cliente"],
                                     produto=venda["produto"], foto_produto=venda["foto_produto"],
                                     data=venda['data'], preco=venda['preco'],
                                     unidade=venda['unidade'], quantidade=venda["quantidade"])

                lista_vendas.add_widget(banner)
        except Exception as excecao:
            print(excecao)
            pass

        # Obter o Total de Vendas do Vendedor
        id_total_vendas = pagina_outro_vendedor.ids["id_total_vendas"]
        id_total_vendas.text = f"[color=#000000]Total Vendas:[/color] R$ {float(total_vendas):,.2f}"

        self.mudar_tela("outrovendedorpage")













MainApp().run()
