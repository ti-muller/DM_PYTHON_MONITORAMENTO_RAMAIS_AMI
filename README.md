# Script de Monitoramento de Chamadas Asterisk Manager Interface (AMI)


Este script usa o protocolo Asterisk Manager Interface (AMI) para se conectar 192.168.2.30 e monitorar eventos de chamadas. Ele é projetado para detectar quando não há chamadas em um período de tempo determinado (atualmente definido como 30 minutos) e abrir um ticket para notificar os administradores. Além disso também estará verificando eventos específicos ocasionados por problemas.


## Recursos

* Conecta ao Asterisk usando o protocolo AMI
* Monitora eventos de chamadas, incluindo VarSet, Shutdown, EndpointDetail, EndpointList, EndpointListComplete, ChannelTalkingStop, Alarm, AlarmClear, Error, FailedACL, Reload, SpanAlarm e SpanAlarmClear
* Abre um ticket quando não há chamadas detectadas em 30 minutos
* Registra eventos em um arquivo para fins de depuração e auditoria

## Requisitos:
```
pip install panoramisk
```
```
pip install python-dotenv
```
```
pip install asyncio
```

## Conexão: Arquivo .ENV
[Base de conhecimento 882](http://server-chamados/glpi/front/knowbaseitem.form.php?id=882)
## Documentação

docs.asterisk.org/Configuration/Interfaces/Asterisk-Manager-Interface-AMI/AMI-Libraries-and-Frameworks/
https://panoramisk.readthedocs.io/en/latest/