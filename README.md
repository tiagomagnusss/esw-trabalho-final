# esw-trabalho-final
Trabalho final para a disciplina de Engenharia de Software - INF - UFRGS - 2021/2

# Instruções de instalação

Para desenvolver o projeto, foi utilizado o framework [Django](https://djangoproject.com/), que é baseado na linguagem Python. As instruções a seguir assumem que o desenvolvedor utilizará uma máquina com Windows 10.

Para edição de código, recomenda-se utilizar o [Visual Studio Code](https://code.visualstudio.com/), que é gratuito e possui extensões para Python e Django.

Para começar, devemos primeiramente instalar o interpretador Python. Para o projeto, utilizaremos a versão 3.10.3, que está disponível no [site oficial](https://www.python.org/downloads/) para download. A instalação deve ser a padrão, lembrando apenas de marcar a caixa **Add Python 3.10 to PATH**, para que possamos rodar os comandos no terminal depois. A seguir, será necessário reiniciar o computador para que o PATH seja atualizado.

Os comandos a seguir devem ser rodados na raíz do repositório. Recomenda-se que seja utilizado o terminal integrado do VS Code, que é baseado no Powershell.

Para criar o ambiente virtual: `py -m venv .`
Para entrar no ambiente virtual: `Scripts\Activate.ps1`

Uma vez lá dentro, podemos instalar as bibliotecas necessárias para rodar o projeto: `py -m pip install Django colorama`

Com isso, temos acesso ao terminal do Django e podemos trabalhar no projeto :)

# Trabalhando no projeto

> **Importante! Sempre devemos trabalhar dentro do ambiente virtual! Então use o comando de entrar no ambiente sempre que for começar a trabalhar!**

A partir da raíz, vamos entrar no diretório do projeto com `cd escambox`. A partir dai, podemos rodar `py manage.py runserver`. Para aplicar as migrações do banco de dados, utilizamos `py manage.py migrate`.

Pronto! A partir daí o aplicativo estará disponível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 

# Referências

[Documentação oficial do Django](https://docs.djangoproject.com/pt-br/4.0/) (parcialmente traduzida para pt-BR)