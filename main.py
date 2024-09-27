import asterisk.manager
from time import time
import sys
from aberturaDeTicket import abreChamado
import logging
from datetime import datetime
import os

manager = asterisk.manager.Manager()
logging.basicConfig(filename=os.path.join(os.getcwd(), 'monitoramento_ramais.log'), level=logging.DEBUG, format='%(asctime)s - %(message)s')

def handle_call(event, manager):
    global now, last_call, hour_now
    # Sempre que houver uma ligação atendida reiniciará o tempo da ultima chamada
    for key, value in event.headers.items():
        if key == 'ChannelStateDesc' and value == 'Up':
            print(event.headers)
            print('-='*20)
            last_call = time()
    # Caso não haja ligações em um período de 30 minutos abrirá um chamado
    if (now - last_call) > 1800 and hour_now > '08:00:00' and hour_now < '18:00:00':
        last_call = time()
        print('ALERTA: Monitoramento Ramais. Mais de 30 minutos sem registro de ligação.')
        logging.info('ALERTA: Monitoramento Ramais. Mais de 30 minutos sem registro de ligação.')
        abreChamado('ALERTA: Monitoramento Ramais', 'Mais de 30 minutos sem registro de ligação.')

def handle_event(event, manager):
    global now, last_ticket
    # Caso algum dos eventos seja ativado um novo chamado é aberto a cada 30 minutos
    if (now - last_ticket) > 1800:
        # Abre um novo ticket com os detalhes do evento
        print(f'ALERTA: Monitoramento Ramais\n{event.headers}')
        logging.info(f'ALERTA: Monitoramento Ramais\n{event.headers}')
        abreChamado('ALERTA: Monitoramento Ramais', str(event.headers))
        # Atualiza o tempo do último ticket
        last_ticket = time()

try:
    try:
        now = last_ticket = last_call = time()
        # Realiza a conexão com o Asterisk
        manager.connect('192.168.2.30')
        manager.login('interno_muller', 'mur@ca@l11')
        logging.info('Conexão estabelecida com o Asterisk')
        print('Conexão estabelecida com o Asterisk')

        # Registro de eventos
        manager.register_event('VarSet', handle_call)

        manager.register_event('Shutdown', handle_event)
        manager.register_event('EndpointDetail', handle_event)
        manager.register_event('EndpointList', handle_event)
        manager.register_event('EndpointListComplete', handle_event)
        manager.register_event('ChannelTalkingStop', handle_event)
        manager.register_event('Alarm', handle_event)
        manager.register_event('AlarmClear', handle_event)
        manager.register_event('Error', handle_event)
        manager.register_event('FailedACL', handle_event)
        manager.register_event('Reload', handle_event)
        manager.register_event('SpanAlarm', handle_event)
        manager.register_event('SpanAlarmClear', handle_event)
        logging.info('Iniciando registro de eventos')
        print('Iniciando registro de eventos')
        
        # Entra em um loop infinito para monitorar os eventos do Asterisk
        while True:
            hour_now = datetime.now().strftime("%H:%M:%S")
            # Atualiza o tempo atual
            now = time()

    except asterisk.manager.ManagerSocketException as e:
        print(f'Monitoramento Ramais: Erro ao conectar no gerenciador\n{e}')
        logging.error(f'Monitoramento Ramais: Erro ao conectar no gerenciador\n{e}')
        abreChamado(f'Monitoramento Ramais: Erro ao conectar no gerenciador', f'Error connecting to the Manager: {e}')
        sys.exit()
    except asterisk.manager.ManagerAuthException as e:
        print(f'Monitoramento Ramais: Erro na autentificação do gerenciador\n{e}')
        logging.error(f'Monitoramento Ramais: Erro na autentificação do gerenciador\n{e}')
        abreChamado(f'Monitoramento Ramais: Erro na autentificação do gerenciador', f'Error logging in to the Manager: {e}')
        sys.exit()
    except asterisk.manager.ManagerException as e:
        print(f'Monitoramento Ramais: Erro no gerenciador\n{e}')
        logging.error(f'Monitoramento Ramais: Erro no gerenciador\n{e}')
        abreChamado(f'Monitoramento Ramais: Erro no gerenciador', f'Error: {e}')
        sys.exit()
finally:
    logging.info('Conexão encerrada com o Asterisk')
    print('Conexão encerrada com o Asterisk')
    manager.close()
