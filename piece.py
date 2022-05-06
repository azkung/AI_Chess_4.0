
class piece:

    def __init__(self, name):
        self.name = name
        self.moved = False
        self.lastMoved = -1
    
    def __int__(self):
        return int(self.name)

    def __eq__(self, other):
        return self.name == other