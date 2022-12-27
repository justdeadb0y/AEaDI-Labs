
# -*- coding: utf-8 -*-
class Node:   # Создаём класс Узел, чтобы в дальнейшем сформировать дерево, метод __init__ нужен для заполнения полей во время инициализации, а не через новую функцию set_value например
    def __init__(self, probability, char, leftnode=None, rightnode=None): 
        #self представляет экземпляр класса. Используя "self", мы можем получить доступ к атрибутам и методам класса в python. Он связывает атрибуты с заданными аргументами. 
        
        self.probability = probability  # Частота / вероятность
        self.char = char  # Символ
        self.left = leftnode # левый узел
        self.right = rightnode # правый узел
        self.code = '' # Для выбора пути по дереву 0 либо 1

codes = dict() # Создаём словарик для кодов символов
    
    # функция показывающая разнизу в битах
def difference_between(data, encoded):
    bef_comp = 8 * len(data) # переменная отвечающая за кол-во бит до сжатия, для этого длину умножаем на 8
    af_comp = 0 # изначально ставим значение 0, так как потом будем прибавлять
    chars = encoded.keys() # возьмём из списка символы
    for char in chars:     # проходимся пока такие символы найдены
        count = data.count(char) # обратимся к методу count, который посчитает нам сколько раз встречался определённый символ в исходных данных
        af_comp += count * len(encoded[char]) # кол-во бит после сжатия формируется путём прибавления к нему же числа (частоты в исходных данных * длину кода, полученного после функции)  
    print ("bits before compression: ", bef_comp) # Вывод на экран
    print ("bits after compression : ", af_comp) 
        
        # Создаём функцию вывода закодированных данных
def encoded_output(data, encoded): 
    encoded_out = [] # создадим пустой массив
    for char in data: # проходим по исходным данным 
        encoded_out.append(encoded[char]) # заносим в пустой массив коды символов в соответсвии с символами из data
    outstring = ''.join([str(i) for i in encoded_out]) # методом join мы работаем с путой строкой '', и заносим , некое переопределние типа, до этого были int, мы делаем str()
    return outstring
        
    # Теперь напишем функцию, которая будет находить частоту встречающегося символа

def calc_probs(inptdata): # На вход функции мы будем потдавать данные, которые мы считали из файла 
    chars = dict() # создаём словарик под численное кол-во частоты
    for elem in inptdata: # проходимся поэлементно по данным
        if chars.get(elem) == None: # через .get обращаемся к нашему словарю и сравниваем встречался ли символ до этого
            chars[elem] = 1 # если нет, значит он новый => его частота 1
        else:
            chars[elem] += 1 # иначе операцией += вычисляем новое значение
    return chars # итогом функции послужит возвращение словарика chars 
    # Теперь напишем функцию, которая будет подсчитывать код узла
def calc_codes(node, value=''): # на вход передаём узел и пустое значение
    newvalue = value + str(node.code) # так будет формироваться новое значение путём конкатенации value и строки из кода узла
    if (node.left): # if node.left == true , то есть 1
        calc_codes(node.left, newvalue) # вызывается та же функция в которой мы сейчас, но уже передаются новые параметры
    if (node.right): # if node.right == true то есть 1
        calc_codes(node.right, newvalue) 
    if(not node.left and not node.right): # Если ((не (0/1 на левом узле)) и (не (0/1 на правом узле))) == true, то есть 1 это когда node.left and node.right оба равны 0 ((не 0) = 1) * ((не 0) = 1) == 1
        codes[node.char] = newvalue # Тогда мы заносим в словарик кодов для опр символов новое значение "код" символа состоящий из 0 и 1
    return codes # В результате функция вернёт словарик который мы объявляли до этого, но уже заполненный
        # напишем функцию кодирования
def huffman_encoding(data): # функция кодирования параметром выступает полученные данные из файла / задали в коде 
    dictionary_probability = calc_probs(data) # присвоим переменной наш словарик chars, который мы получили в результате работы функции calc_probs, он будет иметь поля keys(символы) и values(частота)
    chars = dictionary_probability.keys() # Теперь наш словарик будет состоять из символов
    probabilities = dictionary_probability.values() # Значения частоты символов, встречаемых в данных 
        # теперь для наглядности выведем их на экран, чтобы если пример небольшой можно было убедиться в корректности выполнения функций
    print("chars: ", chars)
    print("probs: ", probabilities)
        # Объявим массив под узлы дерева
    array_nodes = []
        
        #Заполним массив так, чтобы переделать символы и их вероятности в узлы дерева хаффмана
    for char in chars:
        array_nodes.append(Node(dictionary_probability.get(char), char))
        #Создадим цикл в ходе которого отсортируем узлы в порядке возрастания в зависимости от их вероятности, так же как это было в статье на хабре
    while len(array_nodes) > 1:
            # Для следующего метода sorted, нам потребуется вторым аргументом задать функцию, по которой будет происходить сортировка, изучить key = lambda var: var.smth
        array_nodes = sorted(array_nodes, key=lambda tmp: tmp.probability)
            # Выберем 2 узла с наименьшей частотой
        right = array_nodes[0]
        left = array_nodes[1]
            
        left.code = 0
        right.code = 1
            # теперь нужно создать новый узел, путём комбинации выбранных узлов
            # Для этого обратимся к классу которому передадим новые аргументы
        newnode = Node(left.probability+right.probability, left.char+right.char, left, right)
        array_nodes.remove(left) # поскольку array_nodes - массив, можем воспользоваться методом remove, чтобы удалить использованные узлы
        array_nodes.remove(right)
        array_nodes.append(newnode) # методом append, добавляются новые элементы в массив

    encoding = calc_codes(array_nodes[0])
    print("chars with their codes", encoding)
    difference_between(data, encoding) # вызываем функцию для вывода разницы в битах между исходной и зашифрованной информацией 
    encoded_out = encoded_output(data, encoding) # вызываем функцию encoded_output(data, encoding)
    return encoded_out, array_nodes[0] # Возвращаем закодированную строку и вершину дерева хаффмана, чтобы использовать это для раскодирования данных, без этого сделать это невы

def huffmanDecoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.char == None and huffman_tree.right.char == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.char)
            huffman_tree = tree_head
        
    string = ''.join([str(item) for item in decoded_output])
    return string  

efile = open("example.txt", "r") # Открываем файл с примерным текстом
data = efile.read() #Читаем файл
encoding, tree = huffman_encoding(data)
redactfile = open("encodeddata.txt", "w")
redactfile.write(encoding)
decodefile = open("decode.txt", "w")
decodefile.write(huffmanDecoding(encoding,tree))

