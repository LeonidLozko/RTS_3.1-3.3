from timeit import default_timer
from random import choice, randint, uniform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


def factorize(n):
    n = int(n)
    x = int(n ** 0.5) + 1
    while (int((x * x - n) ** 0.5)) ** 2 != (x * x - n):
        x += 1
    y = int((x * x - n) ** 0.5)
    a = x - y
    b = x + y
    return a, b


def perceptron(learn_speed, deadline, num_iter):
    dots = ((0, 6), (1, 5), (3, 3), (2, 4))
    p = 4
    w0 = 0
    w1 = 0
    ok = [False] * 4
    counter = 0
    start = default_timer()
    while sum(ok) != 4 and counter < num_iter and default_timer() - start < deadline:
        iteration = counter % 4
        if not ok[iteration]:
            y = w0 * dots[iteration][0] + w1 * dots[iteration][1]
            if (y > p and iteration < 2) or (y < p and iteration > 1):
                ok[iteration] = True
            else:
                delta = p + ((-1) ** (iteration > 1)) - y
                w0 = w0 + delta * dots[iteration][0] * learn_speed
                w1 = w1 + delta * dots[iteration][1] * learn_speed
                ok = [False] * 4
        counter += 1
    return w0, w1


def genetic(a, b, c, d, y):
    num_pop = 4
    population = [[randint(0, int(y / 4)) for i in range(4)] for j in range(num_pop)]

    def root(nums):
        return nums[0] * a + nums[1] * b + nums[2] * c + nums[3] * d

    def random_parents():
        p = uniform(0, 1)
        if p < chances[0]:
            par1 = population[0]
        elif p < chances[0] + chances[1]:
            par1 = population[1]
        elif p < chances[0] + chances[1] + chances[2]:
            par1 = population[2]
        else:
            par1 = population[3]
        par2 = par1
        while par2 == par1:
            p = uniform(0, 1)
            if p < chances[0]:
                par2 = population[0]
            elif p < chances[0] + chances[1]:
                par2 = population[1]
            elif p < chances[0] + chances[1] + chances[2]:
                par2 = population[2]
            else:
                par2 = population[3]
        return par1, par2
    roots = [root(i) for i in population]
    while roots[0] != y and roots[1] != y and roots[2] != y and roots[3] != y:
        deltas = [1 / abs(i - y) for i in roots]
        chances = [i / sum(deltas) for i in deltas]
        for i in range(num_pop >> 1):
            parents = random_parents()
            gene = randint(0, 3)
            parents[0][gene], parents[1][gene] = parents[1][gene], parents[0][gene]
            population[2 * i], population[2 * i + 1] = parents[0], parents[1]
        population[randint(0, 3)][randint(0, 3)] += choice([-1, 1])
        roots = [root(i) for i in population]
    if roots[0] == y:
        return population[0]
    elif roots[1] == y:
        return population[1]
    elif roots[2] == y:
        return population[2]
    else:
        return population[3]


class TestApp(App):
    def build(self):
        def calc_1(instance):
            result_1.text = "Result: x={}, y={}".format(*factorize(int(num_to_factorize.text)))

        def clear_text(instance, value):
            if value:
                instance.text = ""

        bl = BoxLayout(orientation='vertical', spacing=10)
        gl1 = GridLayout(cols=2, size_hint=(1, .27))
        lab_1 = Label(text="Lab 3.1")
        num_to_factorize = TextInput(text="Insert number here", multiline=False)
        num_to_factorize.bind(focus=clear_text)
        result_1 = Label(text="Result: ")
        but_calc_1 = Button(text="Calculate", on_press=calc_1)

        gl1.add_widget(lab_1)
        gl1.add_widget(num_to_factorize)
        gl1.add_widget(result_1)
        gl1.add_widget(Widget())
        gl1.add_widget(but_calc_1)

        def calc_2(instance):
            result_2.text = "Result: w1={}, w2={}".\
                format(*perceptron(float(learn_speed.text), float(deadline.text), int(num_iter.text)))

        gl2 = GridLayout(cols=2, size_hint=(1, .27))
        lab_2 = Label(text="Lab 3.2")
        learn_speed = TextInput(text="Insert learn speed here", multiline=False)
        learn_speed.bind(focus=clear_text)
        result_2 = Label(text="Result: ")
        deadline = TextInput(text="Insert deadline here", multiline=False)
        deadline.bind(focus=clear_text)
        but_calc_2 = Button(text="Calculate", on_press=calc_2)
        num_iter = TextInput(text="Insert number of iterations here", multiline=False)
        num_iter.bind(focus=clear_text)

        gl2.add_widget(lab_2)
        gl2.add_widget(learn_speed)
        gl2.add_widget(result_2)
        gl2.add_widget(deadline)
        gl2.add_widget(but_calc_2)
        gl2.add_widget(num_iter)

        def calc_3(instance):
            result_3.text = "Result: ({}, {}, {}, {})".\
                format(*genetic(int(ins_a.text), int(ins_b.text), int(ins_c.text), int(ins_d.text), int(ins_y.text)))

        gl3 = GridLayout(cols=2, size_hint=(1, .46))
        lab_3 = Label(text="Lab 3.3")
        ins_a = TextInput(text="Insert a here", multiline=False)
        # ins_a = TextInput(text="3", multiline=False)
        ins_a.bind(focus=clear_text)
        result_3 = Label(text="Result: ")
        ins_b = TextInput(text="Insert b here", multiline=False)
        # ins_b = TextInput(text="4", multiline=False)
        ins_b.bind(focus=clear_text)
        but_calc_3 = Button(text="Calculate", on_press=calc_3)
        ins_c = TextInput(text="Insert c here", multiline=False)
        # ins_c = TextInput(text="5", multiline=False)
        ins_c.bind(focus=clear_text)
        ins_y = TextInput(text="Insert y here", multiline=False)
        # ins_y = TextInput(text="39", multiline=False)
        ins_y.bind(focus=clear_text)
        ins_d = TextInput(text="Insert d here", multiline=False)
        # ins_d = TextInput(text="1", multiline=False)
        ins_d.bind(focus=clear_text)

        gl3.add_widget(lab_3)
        gl3.add_widget(ins_a)
        gl3.add_widget(result_3)
        gl3.add_widget(ins_b)
        gl3.add_widget(but_calc_3)
        gl3.add_widget(ins_c)
        gl3.add_widget(Widget())
        gl3.add_widget(ins_d)
        gl3.add_widget(Widget())
        gl3.add_widget(ins_y)

        bl.add_widget(gl1)
        bl.add_widget(gl2)
        bl.add_widget(gl3)
        return bl


if __name__ == "__main__":
    TestApp().run()
