def SA(F, x0, t0, dx, alpha, n1, n2):
    points = []
    bests = []
    rng = np.random.default_rng()
    x = x0
    t = t0
    best = x
    for i in range(n1):
        for j in range(n2):
            a = rng.random() * 2 - 1
            x1 = viz(x, dx, a)
            delta = F(x1) - F(x)
            if x1 > -11 and x1 < 11:
                if delta < 0:
                    x = x1 
                else:  
                    b = rng.random()
                    temp = b - np.exp(-delta/t)
                    if temp < 0:
                        x = x1
                if F(x) < F(best):
                    best = x
                points.append(x)
                bests.append(best)
        t = resfr(t, alpha)
    return points