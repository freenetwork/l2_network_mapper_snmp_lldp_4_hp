#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       Author: freenetwork
#       e-mail: imfreenetwork@gmail.com
#       site: vk.com/freenetwork
from commands import *
import re

COMMUNITY = 'RGSU_Network_Read'
#       Состояние портов по документации
DEFAULT_STATE = {'1': 'disabled', '2': 'blocking', '3': 'listening', '4': 'learning', '5': 'forwarding', '6': 'broken'}
#       Определяем стиль написания линий для линка. Красный пунктир для заблокированного или выключенного порта.
STATE = {'1': '[color=white', '2': '[style=dashed, color=red', '3': '[color=black', '4': '[color=black', '5': '[color=black', '6': '[color=white'}

#       Список классов. Список свичей.
list_of_Switch = []

class Switch():
        def __init__(self):
                self.hostname = ''
                self.address = ''
                self.neighbors = []
                self.local_ports_for_neighbors = {}
                self.local_ports = {}
                self.local_ports_state = {}
                self.local_ports_2_remote_ports = {}

        def getPortState(self, search):
                for key, value in self.local_ports_for_neighbors.iteritems():
                        if search in value:
                                return self.local_ports_state[key]

        def getPortStateForDraw(self, search):
                for key, value in self.local_ports_for_neighbors.iteritems():
                        if search in value:
                                return STATE[self.local_ports_state[key]]

        def getPort(self, search):
                for key, value in self.local_ports_for_neighbors.iteritems():
                        if search in value:
                                return key

        def getPortNameOfIndex(self, key):
                if key in self.local_ports:
                        return self.local_ports[key]
                else:
                        return key
        def getRemotePort(self, key):
                return self.local_ports_2_remote_ports.get(key, [''])

print "Напишите имя файла с IP адресами: ",
filename = raw_input()
for line in open(filename) :
        sw = Switch()
        #       Определенны переменные для запроса. Возвращают данные согласно названию переменной.
        get_neighbors = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' 1.0.8802.1.1.2.1.4.1.1.9.0'
        get_hostname = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' iso.3.6.1.2.1.1.5.0'
        get_remote_ports_index_lldp = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' 1.0.8802.1.1.2.1.4.1.1.7.0'
        get_remote_ports_index_lldp_2_local_port = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' 1.0.8802.1.1.2.1.4.1.1.7.0.'
        get_remote_ports_name_lldp = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' 1.0.8802.1.1.2.1.4.1.1.8.0'
        get_list_self_ports_index = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' iso.0.8802.1.1.2.1.3.7.1.3'
        get_list_self_ports_name = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' iso.0.8802.1.1.2.1.3.7.1.4'
        get_list_local_ports_index_lldp = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' iso.0.8802.1.1.2.1.4.1.1.4.0'
        get_list_local_ports_state = 'snmpwalk -v2c -c '+COMMUNITY+' '+line.rstrip('\n')+' 1.3.6.1.2.1.17.2.15.1.3'


        text = getoutput(get_hostname)
        text = re.findall(r'"(.*?)"', text)
        if len(text) > 0:
                #       Передаем адрес свичу
                sw.hostname = text[0]
                sw.address = line.rstrip('\n')

                text = getoutput(get_neighbors)
                #       Получаем соседей свича
                neighbors = re.findall(r'"(.*?)"', text)
                #       Получаем порты соседей свича
                neighbors_ports = re.findall(r'1\.9\.0\.(.*?)\.[\d\.]', text)

                i = 0
                while i < len(neighbors):
                        if neighbors[i] == '':
                                i = i + 1
                                continue
                        else:
                #       Передаем соседей свича
                                sw.neighbors.append(neighbors[i])
                #       Передаем порты на которых находятся соседи. Порт ключ - соседи значение (массив)
                                sw.local_ports_for_neighbors.setdefault(neighbors_ports[i], []).append(neighbors[i])
                                i = i + 1

                #       Получаем список портов свича: индекс - имя
                text = getoutput(get_list_self_ports_name)
                #       Определяем индекс локального порта
                index = re.findall(r'iso\.0\.8802\.1\.1\.2\.1\.3\.7\.1\.4\.(.*?) =', text)
                #       Определяем имя удаленного хоста каждому опреденному выше порту
                name = re.findall(r'"(.*?)"', text)
                
                i = 0
                while i < len(index):
                #       Передаем список портов свича: индекс - имя
                        sw.local_ports[index[i]] = name[i]
                        i = i + 1

                text = getoutput(get_list_local_ports_state)
                index = re.findall(r'iso\.3\.6\.1\.2\.1\.17\.2\.15\.1\.3\.(.*?) =', text)
                state = re.findall(r'= INTEGER: (.)', text)
                i = 0
                while i < len(index):
                #       Передаем список портов свича: индекс - имя
                        sw.local_ports_state[index[i]] = state[i]
                        i = i + 1

                
                for key, value in sw.local_ports_for_neighbors.iteritems():
                        text = getoutput(get_remote_ports_index_lldp_2_local_port+key)
                        name = re.findall(r'"(.*?)"', text)
                        for each in name:
                                sw.local_ports_2_remote_ports.setdefault(key, []).append(each)
                
                #       Добавляем полученную топологию в список сети. Дальше анализируем связи для построения графа.
                # print sw.address
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.hostname
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.local_ports
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.local_ports_state
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.neighbors
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.local_ports_for_neighbors
                # print '-=-=-=-=-=-=-=-=-=-'
                # print sw.local_ports_2_remote_ports
                # print '-=-=-=-=-=-=-=-=-=-'
                list_of_Switch.append(sw)

#       Код для проверки полученных данных. 
# i = 0
# while i < len(list_of_Switch):

#         for each in list_of_Switch[i].neighbors:
#                 print each
##        Разбираем словарь ключ:значение (индекс порта: имя порта)
#         for key, value in list_of_Switch[i].local_ports.iteritems():
#                 print "%s-%s" % (key, value)
##        Разбираем словарь ключ:значение (ключ:массив) где ключ номер порта, а значение (массив) его соседи
#         for key, value in list_of_Switch[i].local_ports_for_neighbors.iteritems():
#                 print "%s" % (list_of_Switch[i].local_ports[key])
##        Выводим список соседей предыдущего ключа (порта)
#                 print value
##        Разбираем список локальных портов - для получения их состояния. Передаем каждый ключ методу класса для определения
##              читаемого имени - индекс: имя. Так же передаем каждое значение от ключа для определения состояния порта.
#         for key, value in list_of_Switch[i].local_ports_state.iteritems():
#                 print "%s-%s" % (list_of_Switch[i].getNamePortOfIndex(key), DEFAULT_STATE[value])
#         i = i + 1

# Список свичей, в отредактированном виде. Для построения графа.
list_of_Graph = []

###     Этот код проверка существования линка на массивах. Ниже тое самое но на словарях.
# Список линков в 1 направлении. Свич А - Свич Б
list_1_direction = []
# # Список линков в 2 направлении. Свич Б - Свич А
list_2_direction = []

def hasIndex(_key, _value):
        if _key+':'+_value in list_1_direction:
                return False
        elif _value+':'+_key in list_1_direction:
                return False
        elif _key+':'+_value in list_2_direction:
                return False
        elif _value+':'+_key in list_2_direction:
                return False
        else:
                list_1_direction.append(_key+':'+_value)
                list_2_direction.append(_value+':'+_key)
                return True
###

# #Список линков в 1 направлении. Свич А - Свич Б
# list_1_direction = {}
# # Список линков в 2 направлении. Свич Б - Свич А
# list_2_direction = {}

def getNeighborsPortState(_switch, _neighbor):
        i = 0
        while i < len(list_of_Switch):
                if list_of_Switch[i].hostname == _neighbor:
                        statePortAnotherSide = list_of_Switch[i].getPortState(_switch)
                        if statePortAnotherSide == '2':
                                return 'Blocked'
                        if statePortAnotherSide == '1':
                                return 'Disabled'
                        else:
                                return 'None'
                i = i + 1

# def hasIndex(_key, _value):
#         if list_1_direction.get(_key, 'Null') == _value:
#                 print _key+': '+_value
#                 return False
#         elif list_1_direction.get(_value, 'Null') == _key:
#                 print _key+': '+_value
#                 return False
#         elif list_2_direction.get(_key, 'Null') == _value:
#                 print _key+': '+_value
#                 return False
#         elif list_2_direction.get(_value, 'Null') == _key:
#                 print _key+': '+_value
#                 return False
#         else:
#                 list_1_direction[_key] = _value
#                 list_2_direction[_value] = _key
#                 return True
class Graph():
        def __init__(self):
                self.hostname = ''
                self.address = ''
                self.neighbors = []
                self.line = []
                self.lineLabel = []


i = 0
while i < len(list_of_Switch):
        graph = Graph()
        graph.hostname = list_of_Switch[i].hostname
        graph.address = list_of_Switch[i].address
        for each in list_of_Switch[i].neighbors:
                if re.match('CISCO', each) is not None:
                        continue
                elif re.match('Cisco', each) is not None:
                        continue
                elif hasIndex(graph.hostname, each) is True:
                        graph.neighbors.append(each)
                        lineLabel=', taillabel="'+list_of_Switch[i].getPortNameOfIndex(list_of_Switch[i].getPort(each))+'", headlabel="'+list_of_Switch[i].getRemotePort(list_of_Switch[i].getPort(each))[0]+'"'
                        graph.lineLabel.append(lineLabel)
                        if getNeighborsPortState(graph.hostname, each) == 'Blocked':
                                graph.line.append('[style=dashed, color=red')
                        elif getNeighborsPortState(graph.hostname, each) == 'Disabled':
                                graph.line.append('[color=white')
                        elif getNeighborsPortState(graph.hostname, each) == 'None':
                                graph.line.append(list_of_Switch[i].getPortStateForDraw(each))
                        else:
                                graph.line.append(list_of_Switch[i].getPortStateForDraw(each))
        list_of_Graph.append(graph)
        i = i + 1

print 'graph switches {'
# print 'overlap = false;'
# print 'label="Вильгельма Пика";'
# print 'node [shape=box, fontname="Times-Roman", fontsize=14, style=filled, color="#d3edea"]; splines="compound"'
print 'overlap=false; compound=true; esep=1; node [shape=box, fontname="Times-Roman", fontsize=14];'
for each in list_of_Graph:
        print '"'+each.hostname+'"'+' [ label="'+each.address+'\\n'+each.hostname+'" image="switch.png" labelloc=b color="#ffffff"];'

for each in list_of_Graph:
        hostname = each.hostname
        i = 0
        while i < len(each.neighbors):
                print '"'+hostname+'" -- "'+each.neighbors[i]+'"'+each.line[i]+each.lineLabel[i]+' fontcolor="red" ];'
                i = i + 1
print '}'

#Результат выполнения скрипта пишем в файл sheme.dot
#Затем работает graphviz
#sfdp -x -Goverlap=scale  -Tpng sheme.dot -o sheme.png
#       По окружности. График окружность.
#circo -x -Goverlap=scale  -Tpng sheme.dot -o sheme.png
#       По окружности. Ноды равноудаленны.
#circo -x -Tpng .dot -o sheme.png
