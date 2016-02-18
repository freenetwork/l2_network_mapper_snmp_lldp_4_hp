# l2_network_mapper_snmp_lldp_4_hp
#RU
- Подготовка:</br>
a) Создайте файл где построчно будут указаны IP адреса свичей</br>
b) Убедитесь что протокол LLDP включен на каждом свиче</br>
c) Убедитесь что протокол SNMP включен на каждом свиче. Убидитесь что политики безопасности не запрещают SNMP для вашего IP адреса. И Вы знаете COMMUNITY STRING</br>

- Напоминание:</br>
Как включить SNMP?
>snmp-server community "YOU_SNMP_COMMUNITY" Operator</br>
>snmp-server community "YOU_SNMP_COMMUNITY" Operator Unrestricted</br>

# ENG
- Prepare:</br>
a) You need create file with ip addresses your switches</br>
b) You need enable lldp for every device in network</br>
c) You need enable snmp for every device in network</br>
  
- The note:</br>
Add these lines to the configuration of each of your HP devices to enable SNMP</br>
>snmp-server community "YOU_SNMP_COMMUNITY" Operator</br>
>snmp-server community "YOU_SNMP_COMMUNITY" Operator Unrestricted</br>
