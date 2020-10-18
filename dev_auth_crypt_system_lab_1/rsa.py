import random


LIMIT_PRIME = 1000000000000

"""
    Функция для генерации случайного простого числа
    Самого большого простого числа не существует, поэтому ограничимся LIMIT_PRIME = триллиону для более быстрых подсчётов
    Можно было взять, конечно, самое наибольшее известное простое 2 ** 82589933 - 1, но оно содержит 24.862.048 десятичных цифр)0)))
    return:
        num - случайное простое число
"""
def generate_prime_number(limit = LIMIT_PRIME):
    num = 0
    while True:
        num = random.randint(0, limit)
        if isPrime(num):
            break
    return num

"""
    Функция для проверки того является ли число простым
    Простое число - это такое число, которое делится только на себя и на 1
    Перебираем число n начиная с 2, пока не найдем делитель числа number
    У любого составного числа есть делитель не равный 1, не превосходящий квадратного корня из числа
    Чиcло number является простым, если алгоритм закончился по причине того, 
    что проверяемый делитель стал больше, чем корень из number.
    return:
        True: для простых числе
        False: для составных
"""
def isPrime(number):
    n = 2
    while n * n <= number and number % n != 0:
        n += 1
    return n * n > number


"""
    Функция для генерации числа n, открытого и закрытого ключа
"""
def generate(p, q, key_size=128):
    #key_size - размер ключа (по умолчанию - 128 бит)
    n = p * q
    euler_func = (p - 1) * (q - 1) #функция Эйлера
    e = generate_public_key(euler_func, key_size)
    d = generate_private_key(e, euler_func)
    return e, d, n


"""
    Функция для генерации открытого ключа
"""
def generate_public_key(euler_func, key_size):
    #генерируем случайное число длиной key_size бит (например, для 128: начиная от 2**127 (170141183460469231731687303715884105728) до 2*128 - 1 (340282366920938463463374607431768211455) )
    e = random.randint(2 ** (key_size - 1), 2**key_size - 1)
    #ищем наибольший общий делитель числа e и функции Эйлера
    g = gcd(e, euler_func)
    #наша цель - достичь того, чтобы НОД был равен 1
    while g != 1:
        e = random.randint(2 ** (key_size - 1), 2**key_size - 1)
        g = gcd(e, euler_func)
    return e

"""
    Рекурсивная функция для нахождения наибольшего общего делителя
"""
def gcd(e, euler_func):
    if e == 0:
        return euler_func
    return gcd(euler_func % e, e)

"""
    Функция для генерации закрытого ключа
    gcdex - расширенный алгоритм евклидова расстояния
"""
def generate_private_key(e, euler_func):
    #euler_func - обратный к элементу e, то есть e^-1
    d = gcdex(e, euler_func)[1]
    d = d % euler_func
    if d < 0 :
        d += euler_func
    return d

"""
    Рекурсивная реализация расширенного алгоритма евклидова расстояния
    Цель - подобрать такие числа x и y, чтобы ax + by = d
    return:
        d - наибольший общий делитель a и b
        x и y - такие числа, что ax + by = d
"""
def gcdex(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = gcdex(b % a, a)
    return (g, x - (b // a) * y, y)


"""
    Функция для шифрования текста
    plain_text: открытый текст
    (e, n): открытый ключ
"""
def encrypt(plain_text, e, n):
    cipher_text = [] #список для хранения шифротекста
    for char in plain_text:
        #возведение каждого символа, переведённого в его эквивалент ASCII, в степень по модулю n 
        cipher_text.append(pow(ord(char), e, n))
    return cipher_text

"""
    Функция для дешифрования текста
    cipher_text: зашифрованный текст
    (d, n): закрытый ключ
    return: открытый текст
"""
def decrypt(cipher_text, d, n):
    plain_text = []
    try: 
        for char in cipher_text:
            #обратная операция: возведение каждого числа в степень по модулю n, и его перевод в эквивалент ASCII
            plain_text.append(chr(pow(char, d, n)))
        return "".join(plain_text)
    except TypeError as e:
         print(e)

"""
    Функция для экспорта ключей в файлы
    public.key - открытый ключ
    private.key - закрытый ключ
"""
def export(e, d, n):
    with open("public.key","w") as fp:
        fp.write(f"RSA PUBLIC KEY:\n{e}\n{n}\nEND")
    with open("private.key","w") as fp:
        fp.write(f"RSA PRIVATE KEY:\n{d}\n{n}\nEND")
    