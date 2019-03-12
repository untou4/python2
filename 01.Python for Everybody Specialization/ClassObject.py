class PartyAnimal:
    x = 0
    name = ""

    def __init__(self,name):
        self.name = name
        print(self.name,'constructed')

    def party(self):
        self.x += 1
        print(self.name, "party count",self.x)

    def __del__(self):
        print(self.name,'destructed')

class FootballFan(PartyAnimal):
    points = 0
    def touchdown(self):
        self.points = self.points + 7
        self.party()
        print(self.name,"points",self.points)

j = FootballFan("Jim")
j.party()
j.touchdown()

