class student:
    def __init__(self, fname , lname , id):
        self.fname= fname
        self.lname = lname
        self.id = id
    
    def printst(self):
        print(self.id, self.fname)
x = student("Mark","Colins",223)
x.printst()