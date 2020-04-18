from timeit import default_timer
from random import choice, randint, uniform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from threading import Thread


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
    time = 0
    while sum(ok) != 4 and counter < num_iter and time < deadline:
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
        time = default_timer() - start
    return w0, w1, time


def genetic(a, b, c, d, y, chan=0.1):
    num_pop = 4
    chance = chan
    population = [[randint(0, int(y / 4)) for i in range(4)] for j in range(num_pop)]
    roots = [i[0] * a + i[1] * b + i[2] * c + i[3] * d for i in population]
    counter = 0
    while y not in roots:
        deltas = [1 / abs(i - y) for i in roots]
        chances = [i / sum(deltas) for i in deltas]
        for i in range(num_pop >> 1):
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
            gene = randint(0, 3)
            par1[gene], par2[gene] = par2[gene], par1[gene]
            for j in range(4):
                ran = uniform(0, 1)
                if ran < chance:
                    par1[j] += choice([-1, 1])
                ran = uniform(0, 1)
                if ran < chance:
                    par2[j] += choice([-1, 1])
            population[2 * i] = par1
            population[2 * i + 1] = par2
        roots = [j[0] * a + j[1] * b + j[2] * c + j[3] * d for j in population]
        counter += 1
    return population[roots.index(y)], counter


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
            w0, w1, time = perceptron(float(learn_speed.text), float(deadline.text), int(num_iter.text))
            result_2.text = "Result: w1={:.4f}, w2={:.4f}".\
                format(w0, w1)
            Popup(title="Time of calculating", title_align="center",
                  content=Label(text="{:.4f} ms".format(time * 1000)),
                  size_hint=(.5, .5)).open()

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

        def calc_3():
            result_3.text = "Result: ({}, {}, {}, {})".\
                format(*genetic(int(ins_a.text), int(ins_b.text), int(ins_c.text), int(ins_d.text), int(ins_y.text)))

        def press(instance):
            Thread(target=calc_3).start()

        gl3 = GridLayout(cols=2, size_hint=(1, .46))
        lab_3 = Label(text="Lab 3.3")
        ins_a = TextInput(text="Insert a here", multiline=False)
        # ins_a = TextInput(text="3", multiline=False)
        ins_a.bind(focus=clear_text)
        result_3 = Label(text="Result: ")
        ins_b = TextInput(text="Insert b here", multiline=False)
        # ins_b = TextInput(text="4", multiline=False)
        ins_b.bind(focus=clear_text)
        but_calc_3 = Button(text="Calculate", on_press=press)
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
    # TestApp().run()
    iters = []
    percents = (0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9)
    for i in percents:
        steps = 0
        for j in range(100):
            steps += genetic(3, 2, 1, 5, 39, i)[1]
        iters.append(steps / 100)
    it = iters.index(min(iters))
    print("Найшвидше виконується алгоритм з шансом мутації: {}".format(percents[it]))
    print("Кількість ітерацій за 100 спроб з шансом {}: {}".format(percents[it], iters[it]))
    print("Список кількості ітерацій залежно від шансу мутації " + str(dict(zip(percents[:9], iters[:9]))))
    print(str(dict(zip(percents[9:], iters[9:]))))