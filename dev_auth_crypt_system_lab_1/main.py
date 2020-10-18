#Интерфейс для работы со скриптом

from rsa import *
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox as mb
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style
from tkinter import *

"""
    Создание формы tkinter
"""
class Main(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.init_main()

    def init_main(self):
        self.centerWindow()


    def centerWindow(self):
        w = 475
        h = 350
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

"""
    Выбор директории для сохранения ключей
"""
def opening_folder():
    try:
        mb.showinfo("Информация", "Создайте директорию и выберете её, в ней будут сохранены сгенерированные ключи!")
        dir_path = askdirectory()
        os.chdir(dir_path)
        p = generate_prime_number()
        q = generate_prime_number()
        e, d, n = generate(p, q, key_size=int(key_size_text.get()))
        export(e, d, n)
        mb.showinfo("Информация", "Открытый и закрытый ключи созданы и успешно сохранены в файлы public.key и private.key в выбранную директорию!")
        show_public_key.configure(state='active')
        show_private_key .configure(state='active')
        text.configure(state='normal')
        encrypt_text.configure(state='active')
        clear.configure(state='active')
    except OSError:
        mb.showerror("Ошибка", "Директория не выбрана!")
    except ValueError:
        mb.showerror("Ошибка", "В поле 'Длина ключа' должно быть целое число")
    

def information_key_size():
    mb.showinfo("Информация", "По умолчанию - 128 бит. \n 31 декабря 2013 года браузеры Mozilla перестали поддерживать сертификаты удостоверяющих центров с ключами RSA меньше 2048 бит))0)0)")

def show_info_public_key():
    with open("public.key","r") as fp:
        mb.showinfo("Открытый ключ", fp.read())

def show_info_private_key():
    with open("private.key","r") as fp:
        mb.showinfo("Закрытый ключ", fp.read())

def encryption_text():
    try:
        mb.showinfo("Информация", "Выберите открытый ключ того, кому хотите передать сообщение (в случае если от Боба Алисе, то выберите открытый ключ Алисы)!")
        public_key = askopenfilename()
        with open(public_key,'r') as fp:
            _,e,n = fp.readline(),int(fp.readline()),int(fp.readline())
        message = text.get("1.0", END)
        cipher_text = encrypt(message, e, n)
        text.delete(1.0, END)
        text.insert("1.0", cipher_text)
        text.configure(state='disabled')
        encrypt_text.configure(state='disabled')
        decrypt_text.configure(state='active')
        mb.showinfo("Успех", "Сообщение успешно зашифровано и отображается в поле!")
    except OSError:
        mb.showerror("Ошибка", "Директория не выбрана!")

def decryption_text():
    try:
        mb.showinfo("Информация", "Выберите закрытый ключ того, кому передавалось сообщение (в случае если от Боба Алисе, то выберите закрытый ключ Алисы)!")
        private_key = askopenfilename()
        with open(private_key,'r') as fp:
            _,d,n = fp.readline(),int(fp.readline()),int(fp.readline())
        message_encrypt = [int(i) for i in text.get("1.0", END).strip().split(' ')]
        plain_text = decrypt(message_encrypt, d, n)
        text.configure(state='normal')
        text.delete(1.0, END)
        text.insert("1.0", plain_text)
        encrypt_text.configure(state='active')
        decrypt_text.configure(state='disabled')
        mb.showinfo("Успех", "Сообщение успешно расшифровано и отображается в поле!")
    except OSError:
        mb.showerror("Ошибка", "Директория не выбрана!")

def clear_text():
    text.delete(1.0, END)
    text.configure(state='disabled') 
    encrypt_text.configure(state='disabled')
    decrypt_text.configure(state='disabled')
    clear.configure(state='disabled')
    show_public_key.configure(state='disabled')
    show_private_key .configure(state='disabled')
    mb.showinfo("Информация", "Поля очищены, данные сброшены, сгенерируйте ключи повторно!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.title("Алгоритм RSA")
    root.resizable(False, False)

    #опции для позиционирования элементов
    opts = { 'ipadx': 10, 'ipady': 2, 'sticky': 'nswe' }

    frame1 = Frame(relief=RAISED, borderwidth=1)

    label_key_size = tk.Label(root, text='Длина ключа, бит', font='Arial 10 bold')
    label_key_size.grid(row = 1, column = 1, **opts)

    key_size_text = tk.Entry(root, font='Arial 10')
    key_size_text.insert(0, '128')
    key_size_text.grid(row = 1, column = 2, **opts)

    info_key_size = tk.Button(root)
    info_key_size.configure(text='Инфо', font='Arial 10', command=information_key_size)
    info_key_size.grid(row = 1, column = 3, **opts)

    frame1.grid(row = 2, column = 1, columnspan = 3, **opts)

    label_keys = tk.Label(root, text='Генерация ключей', font='Arial 10 bold')
    label_keys.grid(row = 3, column = 1, **opts)

    generate_keys = tk.Button(root)
    generate_keys.configure(text='Сгенерировать ключи в директорию', font='Arial 10', command=opening_folder)
    generate_keys.grid(row = 3, column = 2, columnspan = 3, **opts)

    frame2 = Frame(relief=RAISED, borderwidth=1)
    frame2.grid(row = 4, column = 1, columnspan = 3, **opts)

    label_show_keys = tk.Label(root, text='Просмотр ключей', font='Arial 10 bold')
    label_show_keys.grid(row = 5, column = 1, **opts)

    show_public_key = tk.Button(root)
    show_public_key.configure(text='Показать открытый ключ', font='Arial 10', command=show_info_public_key)
    show_public_key.configure(state='disabled')
    show_public_key.grid(row = 5, column = 2)

    show_private_key = tk.Button(root)
    show_private_key.configure(text='Показать закрытый ключ', font='Arial 10', command=show_info_private_key)
    show_private_key .configure(state='disabled')
    show_private_key.grid(row = 5, column = 3)

    frame3 = Frame(relief=RAISED, borderwidth=1)
    frame3.grid(row = 6, column = 1, columnspan = 3, **opts)

    label_keys = tk.Label(root, text='Сообщение', font='Arial 10 bold')
    label_keys.grid(row = 7, column = 1, columnspan = 3, **opts)

    text = tk.Text(root)
    text.configure(width=25, height=11)
    text.configure(state='disabled')
    text.grid(row = 8, column = 1, columnspan = 3, **opts)
    
    encrypt_text = tk.Button(root)
    encrypt_text.configure(text='Зашифровать', font='Arial 10', command=encryption_text)
    encrypt_text.configure(state='disabled')
    encrypt_text.grid(row = 9, column = 1,  **opts)

    decrypt_text = tk.Button(root)
    decrypt_text.configure(text='Расшифровать', font='Arial 10', command=decryption_text)
    decrypt_text.configure(state='disabled')
    decrypt_text.grid(row = 9, column = 2, **opts)

    clear = tk.Button(root)
    clear.configure(text='Рестарт', font='Arial 10', command=clear_text)
    clear.configure(state='disabled')
    clear.grid(row = 9, column = 3, **opts)

    root.mainloop()