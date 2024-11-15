import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng()

# Função exemplo Aula
def func1(x):
    return (x+10)*(x+6)*(x+5)*(x+1)*(x-7)*(x-10)/10000

# Função de Italo (comentada)
# def func2(x):
#     if x < -1 or x > 1:
#         y = 0
#     else:
#         y = (np.cos(50*x) + np.sin(20*x))
#     return y
# fv = np.vectorize(func)

xx = np.linspace(-11, 11, 500)
plt.plot(xx, func1(xx))

dx = 1  # Distância máxima da vizinhança
t0 = 60  # Temperatura inicial
alpha = 0.75  # Constante de redução da Temperatura
x0 = -11  # X inicial
n1 = 20  # Número de temperaturas
n2 = 50  # Número de iterações em cada temperatura

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
    sols = []  # Lista para armazenar todos os pontos visitados
    bests = []  # Lista para armazenar o melhor ponto encontrado até o momento

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

                sols.append(x)  # Armazena o ponto atual
                bests.append(best)  # Armazena o melhor ponto encontrado
        
        t = resfr(t, alpha)  # Resfria a temperatura

    return sols, bests

# Função para plotar os resultados
def plotter(F, sol, best):
    plt.plot(xx, F(xx), c='blue')  # Função no gráfico
    plt.scatter(sol, [F(y) for y in sol], c='gray', label='Pontos Visitados')  # Pontos visitados
    plt.scatter(best, [F(y) for y in best], c='red', label='Melhores Pontos')  # Melhores pontos

# Rodar o algoritmo Simulated Annealing
sol, best = SA(func1, x0, t0, dx, alpha, n1, n2)

# Plotar os resultados
plotter(func1, sol, best)

# Exibir o gráfico
plt.legend()
plt.show()

# Exibir as listas de soluções e melhores pontos
print("Soluções Visitadas:", sol)
print("Melhores Pontos Encontrados:", best)