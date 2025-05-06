# Classes Exercise
# Ben Phan
# 08/02/2025

class Cat:
    def __init__(self):
        self.name = ""
        self.color = ""
        self.weight = 0

    def about(self):
        print("The cats name is", self.name, ". He is", self.color, "and his weight is", self.weight)

    def meow(self):
        print(self.name,": Meeeeeooooow")


class Monster:
    def __init__(self):
        self.name = ""
        self.health = 0

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(self.name,"has died")


def main():
    cat1 = Cat()

    cat1.name = "Haru"
    cat1.color = "White"
    cat1.weight = 5

    monst1 = Monster()
    monst1.name = "Oni"
    monst1.health = 50

    cat1.about()
    cat1.meow()

    print("The monster name is",monst1.name)

    for i in range(10):
        monst1.decrease_health(5)
        print(monst1.health)


main()