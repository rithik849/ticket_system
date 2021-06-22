

class LogFileIO:

    def append(self, msg):
        try:
            with open("log.txt", "a+") as file:
                file.write(msg+"\n")
        except ValueError as e:
            print(e)

    def read(self):
        content = ""
        try:
            with open("log.txt", "r") as file:
                content = file.readlines()
        except ValueError as e:
            print(e)
        return content
