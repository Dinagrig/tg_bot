class Student:

    def __init__(self, name, age, fav_sub, grade):    # анкета" для студента, чтобы их создавать
        self.name = name
        self.age = age
        self.fav_sub = fav_sub
        self.grade = grade
        self.is_hooligan = False
        self.is_suffering = False
        self.is_dead_inside = False

    def says_hello(self):    # действие приветствия
        print(f'{self.name} не рад(a) тебя видеть, катись отсюда.')

    def hit(self, other):    # действиe удара

        if other.is_suffering:
            print(f'{other.name} скоро впадет в депрессию - осторожно!')
            other.is_dead_inside = True

        if self.is_hooligan:
            print(f'такими темпами {self.name} далеко не пойдет..')
            print(f'{self.name} снова ведет себя как некультурная обезьяна..')
        else:
            print(f'{self.name} ведет себя как некультурная обезьяна')

        print(f'{other.name} получил(а) по роже')

        self.is_hooligan = True
        other.is_suffering = True


class Student_hooligan(Student):    # создание подклассов
    def __init__(self, name, age, fav_sub, grade):    # пренос на них данных и супер-класса
        super().__init__(name, age, fav_sub, grade)
        self.is_hooligan = True
        self.is_stupid_sigma = False

    def argue(self, other):    # добавление новых функций для подклассовых подопытных
        if other.is_dead_inside:
            print(f'{self.name}: {other.name}, ты че, нарываешься?')
            print(f'{other.name}: И-извини, я нет, не трогай меня пожалуйстаааа..')
            print(f'{self.name}: Вали отсюда быстрее, пока ноги не переломал')
            print(f'{other.name}уходит, грустно заправляя волосы за ухо и шаркая ногами.*')
        elif other.is_nerd:
            print(f'{self.name}: {other.name}, ты че, нарываешься?')
            print(f'{other.name}: И-извини, я нет, не трогай меня пожалуйстаааа..')
            print(f'{self.name}: Вали отсюда быстрее, пока ноги не переломал')
            print(f'{other.name} уходит, торопливо подбирая охапку книг.*')

    def sigma(self, other):
        if other.flirted:
            print(f'Фу, {other.name}, т чм, нт. Я люблю {self.fav_sub}.')
            self.is_stupid_sigma = True
            other.is_suffering = True
            print(f'{other.name} жоско отшита.')

    def vape(self):
        print(f'{self.name} жоско повейпил.')


class Student_dead_inside(Student):
    def __init__(self, name, age, fav_sub, grade):
        super().__init__(name, age, fav_sub, grade)
        self.is_dead_inside = True
        self.is_suffering = True

    def suffer(self):
        print(f'{self.name}: Блин, я никому не нужен, меня никто не любит, зачем мама меня родила..'
              ' Блин, почему им всем везет, а меня буллят.'
              ' Блин, я ни на что не способен, почему я вообще живу..')


class Student_nerd(Student):
    def __init__(self, name, age, fav_sub, grade):
        super().__init__(name, age, fav_sub, grade)
        self.is_nerd = True

    def nerd(self, other):
        if other.is_hooligan or other.is_popular:
            print('Фер, вапфета, фкола - это не мефто для кувения. '
                  'Повалуйфта, фию ве фекунду убевите эвектвонную сигалету!')
            print(f'{other.name} задохнулся(ась).*')


class Student_girls_girl(Student):
    def __init__(self, name, age, fav_sub, grade):
        super().__init__(name, age, fav_sub, grade)
        self.is_popular = True
        self.flirted = False

    def flirt(self, other):
        if other.is_hooligan:
            print(f'{self.name}: Блинб, {other.name}, ты такой крутой, го встр.')
            self.flirted = True

    def vape(self):
        print(f'{self.name} жоско повейпила.')

    def sad(self):
        print(f'{self.name}: Блин, почему меня отшили, я вообще-то крутая. Все мужики козлы!'
              ' Почему я не могу нормально спокойно жить?..')



if __name__ == '__main__':
    student1 = Student('Bellaahh', 12, 'math', 11)    # создание двух подопытных
    student2 = Student('Jakobe', 20, 'GYM', 7)

    student1.says_hello()    # взаимодействие между двумя подопытными
    student2.hit(student1)
    student2.hit(student1)


    student_h1 = Student_hooligan('Edvard', 17, 'Bellaahh', 11)    # создание новых подопытных
    student_d1 = Student_dead_inside('Bellaahhhh', 13, 'pedofiles', 7)
    student_n1 = Student_nerd('Alice', 15, 'to be a nerd', 9)
    student_p1 = Student_girls_girl('Jessikaahh', 16, 'Male teachers', 10)

    student_h1.says_hello()    # проведение опытов, приветствие и взаимодействие подопытных
    student_p1.says_hello()
    student_n1.says_hello()
    student_d1.says_hello()

    student_h1.argue(student_d1)
    student_h1.hit(student_n1)

    student_p1.vape()
    student_h1.vape()
    student_n1.nerd(student_p1)
    student_n1.nerd(student_h1)

    student_p1.flirt(student_h1)
    student_h1.sigma(student_p1)

    student_d1.suffer()
    student_p1.sad()
