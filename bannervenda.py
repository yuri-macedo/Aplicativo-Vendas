from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle

class BannerVenda(GridLayout):
    def __init__(self,**kwargs):
        super().__init__()
        self.rows = 1
        cliente = kwargs["cliente"]
        foto_cliente = kwargs["foto_cliente"]
        produto = kwargs["produto"]
        foto_produto = kwargs["foto_produto"]
        data = kwargs['data']
        preco = float(kwargs['preco'])
        unidade = kwargs['unidade']
        quantidade = float(kwargs["quantidade"])

        with self.canvas:
            Color(rgb=(0,0,0,1))
            self.rec=Rectangle(size=self.size,pos=self.pos)
        self.bind(size=self.atualizar_rec,pos=self.atualizar_rec)

        esquerda=FloatLayout()
        esquerda_imagem=Image(pos_hint={"right":1,"top":0.95},size_hint=(1,0.75),source=f"icones/fotos_clientes/{foto_cliente}")
        esquerda_texto=Label(pos_hint={"right":1,"top":0.2},size_hint=(1,0.2),text=cliente)
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_texto)
        
        meio=FloatLayout()
        meio_imagem = Image(pos_hint={"right": 1, "top": 0.95}, size_hint=(1, 0.75),
                                source=f"icones/fotos_produtos/{foto_produto}")
        meio_texto = Label(pos_hint={"right": 1, "top": 0.2}, size_hint=(1, 0.2), text=produto)
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_texto)
        
        direita=FloatLayout()
        direita_data=Label(pos_hint={"right": 1, "top": 0.9}, size_hint=(1, 0.33), text=f"Data: {data}")
        direita_preco=Label(pos_hint={"right": 1, "top": 0.65}, size_hint=(1, 0.33), text=f"Preço: R${preco:,.2f}")
        direita_quantidade=Label(pos_hint={"right": 1, "top": 0.4}, size_hint=(1, 0.33), text=f"Quantidade: {quantidade} {unidade}")
        direita.add_widget(direita_data)
        direita.add_widget(direita_preco)
        direita.add_widget(direita_quantidade)

        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self,*args):
        self.rec.size=self.size
        self.rec.pos=self.pos
