from manim import *
import numpy as np
from scipy.optimize import minimize
import random
import math


class SimulatedAnnealing(Scene):
    
    def construct(self):
        # Função polinomial de grau 4 com alguns mínimos locais: f(x) = x^4 - 4x^3 + 6x^2
        def func1(x):
            return (x+10)*(x+6)*(x+5)*(x+1)*(x-7)*(x-10)/10000

        # Gerar o gráfico da função polinomial
        axes = Axes(
            x_range=[-11, 11],
            y_range=[-12, 23],
            axis_config={"color": BLUE},
        )

        # Função polinomial no gráfico
        def graph_function(x):
            return func1(x)

        # Plotando a função polinomial no gráfico 2D
        graph = axes.plot(graph_function, color=WHITE)

        # Desenhando o gráfico
        self.play(Create(axes), Create(graph))
        
        title = Text("Simulated Annealing", font_size=36, color=WHITE)
        title.to_edge(UP).shift(UP*0.5)  # Ajustando a posição para não cobrir a função
        self.play(Write(title))
        
        # Exibir a função na tela
        func_tex = MathTex("f(x) = \\frac{(x+10)(x+6)(x+5)(x+1)(x-7)(x-10)}{10000}", color=WHITE)
        func_tex.to_corner(UP + LEFT)
        self.play(Write(func_tex))

        # Ponto inicial aleatório (não no mínimo)
        start_x = random.uniform(-10, 10)
        point = Dot(color=RED).move_to(axes.c2p(start_x, func1(start_x)))

        # Mostrar o ponto inicial
        self.play(FadeIn(point))

        # Função de Simulated Annealing (com simplicidade)

    # Função de resfriamento
        def resfr(t, alpha):
            t = alpha * t
            return t

        # Função de vizinhança
        def viz(x, dk, a):
            x = x + dk * a
            return x

        # Função Simulated Annealing
        def SA(F, x0, t0, dx, alpha, n1, n2):
            points = []  # Lista para armazenar todos os pontos visitados
            bests = []  # Lista para armazenar o melhor ponto encontrado até o momento
            rng = np.random.default_rng()
            x = x0
            t = t0
            best = x

            for i in range(n1):
                for j in range(n2):
                    a = rng.random() * 2 - 1  # Valor aleatório para a direção
                    x1 = viz(x, dx, a)  # Calcula o novo valor de x
                    delta = F(x1) - F(x)  # Diferença de valores da função
                    if x1 > -11 and x1 < 11:  # Verifica se x está dentro dos limites
                        if delta < 0:
                            x = x1  # Aceita a solução se for melhor
                        else:  
                            b = rng.random()  # Probabilidade de aceitar piores soluções
                            temp = b - np.exp(-delta/t)
                            if temp < 0:
                                x = x1

                        if F(x) < F(best):  # Atualiza o melhor ponto encontrado
                            best = x

                        points.append(x)  # Armazena o ponto atual
                        bests.append(best)  # Armazena o melhor ponto encontrado
                
                t = resfr(t, alpha)  # Resfria a temperatura

            return points

        points = SA(func1, x0 = -11, t0 = 60, dx = 1, alpha = 0.75, n1 = 20, n2 = 50)

        for point_x in points:
            point_target = axes.c2p(point_x, func1(point_x))
            self.play(point.animate.move_to(point_target), run_time=0.1)

        # Exibir o valor da função no ponto final
        final_x = points[-1]
        final_y = func1(final_x)
        final_point = axes.c2p(final_x, final_y)

        # Exibir o valor da função abaixo do ponto final
        value_text = Tex(f"f({final_x:.2f}) = {final_y:.2f}", color=WHITE)
        value_text.next_to(final_point, DOWN)  # Colocando abaixo do ponto
        self.play(Write(value_text))

        # Finalizar
        self.wait(2)