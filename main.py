import asyncio
import dotenv
from panoramisk import Manager
import threading
from aberturaDeTicket import abreChamado
from datetime import datetime

config = dotenv.dotenv_values('.env')

# Conexão no gerenciador com as informações que estão no .env
manager = Manager(loop=asyncio.get_event_loop(),
                host=config['HOST'],
                username=config['USERNAME'],
                secret=config['SECRET'])

# Esse gerenciador monitora eventos de Desligamento 'Shutdown'
@manager.register_event('Shutdown')
def alert(manager, message):
    abreChamado('Alerta: Monitoramento de Ramais', f'Shutdown Event:\n{message}')

# Esse gerenciador monitora todos os eventos
@manager.register_event('*')
def callback(manager, message):
    global timer
    global hour
    data = string_converter(message)
    hour = datetime.now().strftime("%H:%M:%S")
    try:
        # Filtra apenas os eventos de atendimento de ligação: ChannelStateDesc = Up
        if data['ChannelStateDesc'] == 'Up':
            # Cancela o timer
            timer.cancel()
            # Se estiver dentro do horário de trabalho da empresa inicia o timer
            if hour > '08:00:00' and hour < '18:00:00':
                timer = threading.Timer(1800, lambda: new_ticket()) # 1800
                timer.start()
            # Log dos eventos no terminal
            print('='*20)
            print(f'Hour - {hour}')
            for item in data:
                print(f'{item} - {data[item]}')
    except Exception:
        pass

def new_ticket():
    abreChamado('Alerta: Monitoramento de Ramais', 'Mais de 30 minutos sem ligação.')
    # Se estiver dentro do horário de trabalho da empresa inicia o timer
    hour = datetime.now().strftime("%H:%M:%S")
    if hour > '08:00:00' and hour < '18:00:00':
        timer = threading.Timer(1800, lambda: new_ticket()) # 1800
        timer.start()


# Essa função serve para transformar o log de eventos retornado pelo asterisk manager em um dicionário python
def string_converter(msg):
    # Atribui o log recebido a variagem message transformando o log em string
    message = str(msg)
    # Esse contador registra quantas vezes aparecem aspas simples na string
    count = 0
    # Essa lista guarda a posição na string das aspas simples, porém o objetivo é armazenar apenas as posições pares
    index_list = []
    # Verifica todos os caracteres na string
    for index, char in enumerate(message):
        # Se aparecer uma aspas simples adiciona mais um no contador
        if char == "'":
            count += 1
            # Verifica o resto da divisão do contador por 2, se for 0 significa que é um numero par
            if count%2==0 and count != 0:
                # Adiciona essa posição na lista
                index_list.append(index)
    # Esse loop adicionará uma virgula ao lado de cada aparição da aspas simples na string, essa virgula será o delimitador para realizar um split da string
    for index, item in enumerate(index_list):
        """
        Aqui deve ser somando index+item+1, porque:
        item: a posição da aspas simples na string;
        +1: pega uma posição depois dessa aspas na string;
        index: como a cada momento está sendo adiconado um novo caractere na string, no caso a virgula, pecisa do index da lista para não perder a posição,
        caso contrário a adicição da virgula não ficaria no local correto
        """
        pos = index+item+1
        message = message[:pos] + ',' + message[pos:]
    # Após isso é retidado todos os caracteres desnecessários, e feito o split da string pelo virgula adiconada anteriormente. Ao realizar o split a string vira uma lista
    msg_list = message.replace('<', '').replace('>', '').replace("'", '').split(',')
    msg_dict = {}
    # Esse loop transformará a mensagem que agora está como uma lista em um dicionário python
    for item in msg_list:
        # Cada aparição do caractere igual será o delimitador do que será a chave e o valor do dicionário
        if '=' in item:
            item_list = item.strip().split('=')
            msg_dict[item_list[0]] = item_list[1]
    # Retorna o dicionário
    return msg_dict

def main():
    global timer
    manager.connect()
    timer = threading.Timer(1800, lambda: new_ticket())
    try:
        manager.loop.run_forever()
    except KeyboardInterrupt:
        manager.loop.close()


if __name__ == '__main__':
    main()
