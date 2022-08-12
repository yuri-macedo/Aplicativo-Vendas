import requests
from kivy.app import App

class MyFirebase():
    API_KEY="AIzaSyBQzuC25S3YaybB7VbG6-WQ2DMnC8MNJ7o"


    def criar_conta(self,email,senha):
        link=f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info={"email":email,
              "password":senha,
              "returnSecureToken":True }
        requisicao=requests.post(link,data=info)
        requisicao_dic=requisicao.json()

        if requisicao.ok:
            idtoken=requisicao_dic["idToken"]
            refreshtoken=requisicao_dic["refreshToken"]
            local_id=requisicao_dic["localId"]

            meu_app=App.get_running_app()
            meu_app.idtoken=idtoken
            meu_app.local_id = local_id
            with open("refreshtoken.txt","w") as arquivo:
                arquivo.write(refreshtoken)


            req_id=requests.get(f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={meu_app.idtoken}")
            id_vendedor=req_id.json()
            print(id_vendedor)

            link=f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/{local_id}.json?auth={meu_app.idtoken}"
            info=f'{{"avatar":"foto1.png","equipe":"","total_vendas":"0","vendas":"","id_vendedor":"{id_vendedor}"}}'
            requests.patch(link,data=info)

            proximo_id_vendedor=int(id_vendedor)+1
            prox_id=f'{{"proximo_id_vendedor":"{proximo_id_vendedor}"}}'
            requests.patch(f"https://aplicativovendashash-f2533-default-rtdb.firebaseio.com/.json?auth={meu_app.idtoken}",data=prox_id)

            meu_app.carregar_info_usuario()
            meu_app.mudar_tela("homepage")


            print("Usuário Criado")
        else:
            mensagem_erro=requisicao_dic["error"]["message"]
            login_page=App.get_running_app().root.ids["loginpage"]
            mensagem_login_page=login_page.ids["id_mensagem_login"]
            mensagem_login_page.color=(1,0,0,1)
            mensagem_login_page.text=mensagem_erro
        print(requisicao_dic)

    def login(self,email,senha):
        link=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info={"email":email,
              "password":senha,
              "returnSecureToken":True }
        requisicao=requests.post(link,data=info)
        requisicao_dic=requisicao.json()

        if requisicao.ok:
            idtoken=requisicao_dic["idToken"]
            refreshtoken=requisicao_dic["refreshToken"]
            local_id=requisicao_dic["localId"]

            meu_app=App.get_running_app()
            meu_app.idtoken=idtoken
            meu_app.local_id = local_id
            with open("refreshtoken.txt","w") as arquivo:
                arquivo.write(refreshtoken)

            meu_app.carregar_info_usuario()
            meu_app.mudar_tela("homepage")
        else:
            mensagem_erro=requisicao_dic["error"]["message"]
            login_page=App.get_running_app().root.ids["loginpage"]
            mensagem_login_page=login_page.ids["id_mensagem_login"]
            mensagem_login_page.color=(1,0,0,1)
            mensagem_login_page.text=mensagem_erro
        print(requisicao_dic)

    def trocar_token(self,refresh_token):
        link=f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info={"grant_type":"refresh_token",
              "refresh_token":refresh_token}
        requisicao=requests.post(link,data=info)
        requisicao_dic=requisicao.json()
        local_id=requisicao_dic["user_id"]
        token_id=requisicao_dic["id_token"]
        return local_id,token_id
