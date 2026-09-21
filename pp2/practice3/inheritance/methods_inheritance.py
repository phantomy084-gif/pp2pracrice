class person:
    def __init__(self, fname , lname , age):
        self.fname = fname
        self.lname = lname
        self.age = age
    
    def prin(self):
        print(self.age, self.lname,self.fname)


class worker(person):
    def __init__(self, fname,lname,age):
        super().__init__(fname,lname,age)


x = worker("Mark","Walker",23)
print(x.lname,x.age)