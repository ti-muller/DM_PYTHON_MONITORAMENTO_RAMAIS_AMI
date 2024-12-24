#### Bibliotecas ####
import requests
import json
from requests.auth import HTTPBasicAuth

# Variáveis de conexão
FAppToken = 'MB0ewfGXpSpJ7tJQZ5hjhgGUgrHerPRsucF42RaG'
viTicket_Itil = 56
FBaseURL = "http://192.168.2.252/glpi/apirest.php"
# Informações de autenticação básica
usuario = 'bot.chamado'
senha = '!@#Chamado123'

# Faz post no GLPI para pegar session_Token
def abrir_conexao():
    try:
        # URL do endpoint
        url = 'http://192.168.2.252/glpi/apirest.php/initSession'

        # Configurando a autenticação básica
        auth = HTTPBasicAuth(usuario, senha)

        params = {'app_token': FAppToken}


        # Realizando a requisição POST
        response = requests.post(url, auth=auth,params=params)

        # Verificando o status da resposta
        response.raise_for_status()

        # Extraindo o campo session_token do JSON de resposta
        json_response = response.json()
        session_token = json_response.get('session_token', None)

        return session_token
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

#Fecha a sessão pelo session_token
def fechar_conexao(session_token):
    try:
        # URL do endpoint para encerrar a sessão
        url = 'http://192.168.2.252/glpi/apirest.php/killSession'

        # Configurando a autenticação básica
        auth = HTTPBasicAuth(usuario, senha)

        # Parâmetros da requisição POST
        params = {'session_token': session_token}

        # Realizando a requisição POST
        response = requests.post(url, auth=auth, params=params)

        # Verificando o status da resposta
        response.raise_for_status()

        # Verificando o resultado do POST (assumindo que a API retorna 'true' ou 'false')
        resultado = response.json()

        if resultado:
            print("Sessão encerrada com sucesso. Token: ",session_token)
        else:
            print(f"Resposta inesperada: {resultado}")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

# Abre uma nova solicitação
def abreChamado(nome,descricao):
    try:
        # Obtendo o session_token
        session_token = abrir_conexao()

        # URL do endpoint para abrir um chamado
        url = 'http://192.168.2.252/glpi/apirest.php/ticket'

        # Configurando a autenticação básica
        auth = HTTPBasicAuth(usuario, senha)

        # Configurando parâmetros e corpo da requisição
        params = {'app_token': FAppToken, 'session_token': session_token}
        body = {
            "input": {
                "name": nome,
                "content": descricao,
                "priority": 1,
		        "impact": 4,
                "status": 1,
                "urgency": 5,
                "itilcategories_id": viTicket_Itil
            }
        }

        # Realizando a requisição POST
        response = requests.post(url,json=body ,auth=auth,params=params)

        # Verificando o status da resposta
        response.raise_for_status()

        # Extraindo o campo session_token do JSON de resposta
        json_response = response.json()
        id = json_response.get('id', None)
        print('ID Chamado: ', id)
        return id
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
