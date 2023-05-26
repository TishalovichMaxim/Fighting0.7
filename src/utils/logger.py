from datetime import datetime

class Logger:
    def __init__(self, owner) -> None:
        self.owner = owner

    def log(self, message):
        print()
        print(self.owner + ": " + message)
        
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        print("Time: ", t)

        print()