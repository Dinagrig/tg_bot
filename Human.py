class Student:

    def __init__(self, name, age, fav_sub, grade):    # анкета" для студента, чтобы их создавать
        self.name = name
        self.age = age
        self.fav_sub = fav_sub
        self.grade = grade
        self.is_hooligan = False
        self.is_suffering = False
        self.is_prisoner = False
        self.is_dead = False

    def says_hello(self):    # действие приветствия
        print(f'{self.name} не рад(a) тебя видеть, катись отсюда.')

    def hit(self, other):    # действия удара) с возможностью убийста при повторном ударе))

        if self.is_hooligan:
            print(f'{self.name}, ты хочешь попасть в тюрьму?')
            self.is_prisoner = True

        if other.is_suffering:
            print(f'{other.name} скоро умрет - осторожно!')
            other.is_dead = True

        self.is_hooligan = True
        other.is_suffering = True


student1 = Student('Bellaahh', 12, 'math', 11)    #создание двух подопытных
student2 = Student('Jakobe', 20, 'GYM', 7)

student1.says_hello()    # взаимодействие между двумя подопытными
student2.hit(student1)
student2.hit(student1)

print(student1.is_dead)    # проверка
print(student2.is_prisoner)


