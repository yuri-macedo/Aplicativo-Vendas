
<h1 align="center"> Aplicativo Vendas </h1>

<p align="center">
    •<a href="#Descrição">  Descrição </a>
    •<a href="#Funcionalidades">  Funcionalidades </a>
</p>
 	
 <h2 id="Descrição">
     Descrição
 </h2>
 
 <p style="text-align:justify" >
     Esse projeto tem o objetivo de construir um aplicativo de vendas de produtos de fornecedores para redes de supermercados, utilizando python, a biblioteca Kivy, o banco de dados firebase e a API do Google para realizar login. 
 </p>

 <h2 id="Funcionalidades">
     Funcionalidades
 </h2>
 
 Esse projeto possui as seguintes funcionalidades: 
 
 <h3>
     Criar Conta
 </h3>
 
 Foi utilizada a API do Google para a criação de conta e realização de Login. As informações do perfil do usuário no aplicativo são salvas no banco de dados firebase
 
<h1 align="center">
    <img src="/Gifs/Criarconta.gif">
</h1>

 <h3>
     Login
 </h3>
 
 A realização do Login ocorre através da API do Google e as informações do usuário são carregadas com base nas informações do mesmo na firebase.
 
<h1 align="center">
    <img src="/Gifs/Login.gif">
</h1>

 <h3>
     Adicionar Venda
 </h3>
 
 As vendas são cadastradas no banco de dados firebase para cada usuário.
 
<h1 align="center">
    <img src="/Gifs/Adicionarvenda.gif">
</h1>

 <h3>
     Lista de Vendas
 </h3>
 
 Tanto a lista de vendas quanto o total de vendas são informações possíveis de consultar no banco de dados Firebase para cada usuário.
 
<h1 align="center">
    <img src="/Gifs/Vendasdousuario.gif">
</h1>

 <h3>
     Editar Foto de Perfil
 </h3>
 
 A foto de perfil pode ser alterada entre as opções disponíveis e a informação é atualizada no banco de dados firebase.
 
<h1 align="center">
    <img src="/Gifs/Fotoperfil.gif">
</h1>

<h3>
     Acompanhar Vendedores
 </h3>
 
 É possível adicionar um vendedor pelo atributo de ID do mesmo, adicionando-o a sua equipe.
 
<h1 align="center">
    <img src="/Gifs/Adicionarvendedores.gif">
</h1>

<h3>
     Listar Vendedores
 </h3>
 
 A lista de vendedores é obtida com base na equipe de vendedores que você adicionou, sendo possível ver informações sobre o total de vendas e as vendas desses vendedores através da consulta ao banco de dados firebase.
 
<h1 align="center">
    <img src="/Gifs/Listavendedores.gif">
</h1>

<h3>
     Ver Todas as Vendas
 </h3>
 
 A lista de todas as vendas é obtida ao obter ao consultar o banco de dados firebase e iterar a lista de vendedores e a lista de vendas de cada vendedor.
 
<h1 align="center">
    <img src="/Gifs/Todasvendas.gif">
</h1>
