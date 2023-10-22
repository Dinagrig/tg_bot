import Students

student1 = Student('Bellaahh', 12, 'math', 11)  # создание двух подопытных
student2 = Student('Jakobe', 20, 'GYM', 7)

student1.says_hello()  # взаимодействие между двумя подопытными
student2.hit(student1)
student2.hit(student1)

student_h1 = Student_hooligan('Edvard', 17, 'Bellaahh', 11)  # создание новых подопытных
student_d1 = Student_dead_inside('Bellaahhhh', 13, 'pedofiles', 7)
student_n1 = Student_nerd('Alice', 15, 'to be a nerd', 9)
student_p1 = Student_girls_girl('Jessikaahh', 16, 'Male teachers', 10)

student_h1.says_hello()  # проведение опытов, приветствие и взаимодействие подопытных
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