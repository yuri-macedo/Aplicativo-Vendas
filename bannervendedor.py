import requests
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle
from botoes import ImageButton,LabelButton
from kivy.app import App
from functools import partial

class BannerVendedor(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__()
        id_vendedor_equipe = kwargs["id_vendedor_equipe"]
        requisicao=requests.get(f'https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_equipe}"')
        requisicao_dic=list(requisicao.json().values())[0]
        avatar=requisicao_dic["avatar"]
        total_vendas=requisicao_dic["total_vendas"]

        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.atualizar_rec, pos=self.atualizar_rec)

        meu_app=App.get_running_app()
        imagem = ImageButton(pos_hint={"right": 0.4, "top": 0.9}, size_hint=(0.3, 0.8),
                                source=f"icones/fotos_perfil/{avatar}",
                             on_release=partial(meu_app.carregar_outro_vendedor_page,requisicao_dic))
        label_id = LabelButton(pos_hint={"right": 0.9, "top": 0.9}, size_hint=(0.5, 0.5),
                             text=f"ID Vendedor: {id_vendedor_equipe}",
                             on_release=partial(meu_app.carregar_outro_vendedor_page,requisicao_dic))
        label_total_vendas = LabelButton(pos_hint={"right": 0.9, "top": 0.6}, size_hint=(0.5, 0.5),
                               text=f"Total de Vendas: R${float(total_vendas):,.2f}",
                             on_release=partial(meu_app.carregar_outro_vendedor_page,requisicao_dic))

        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total_vendas)



    def atualizar_rec(self,*args):
        self.rec.size=self.size
        self.rec.pos=self.pos
