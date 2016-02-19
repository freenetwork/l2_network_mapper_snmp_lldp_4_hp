# l2_network_mapper_snmp_lldp_4_hp
A dynamic network topology map provides an interactive, visualization of the connections between network elements (WHILE ONLY HP SWITCHES)
- The script for the construction of L2 network topology graphically (HP Switches). With graphviz tools
- Скрипт для построения L2 топологии компьютерной сети (коммутаторы HP) в графическом виде. С помощью утилиты graphviz 

##HOW USE
user@linux:$ chmod +x crowl.py</br>
user@linux:$ ./crowl.py > sheme.dot</br>
user@linux:$ circo -x -Goverlap=scale  -Tpng sheme.dot -o sheme.png</br>
>OR </br>
>user@linux:$ sfdp -x -Goverlap=scale  -Tpng sheme.dot -o sheme.png</br>
>OR </br>
>user@linux:$ circo -x -Tpng sheme.dot -o sheme.png</br>
>OR </br>
>user@linux:$ dot -Tpng sheme.dot -o sheme.png</br>

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

# Features</br>
Recursively discovery HP devices via SNMP(LLDP)</br>
List self and neighbors name ports</br>
List blocked path (red line dashed)</br>
