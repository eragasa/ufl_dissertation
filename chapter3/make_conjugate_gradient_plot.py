import math
from collections import OrderedDict
import numpy as np
import pandas as pd

def kurasawe(x):
    return kurasawe_f1(x), kurasawe_f2(x)

def kurasawe_f1(x):
    n = len(x)

    f1 = 0
    for i in range(n-1):
        f1 += -10*math.exp(-0.2*(x[i]**2+x[i+1]**2)**0.5)
    return f1

def kurasawe_f2(x):
    n = len(x)

    f2 = 0
    for i in range(n):
        f2 += abs(x[i])**0.8+5*math.sin(x[0]**3)

    return f2

def costfunction(x,weights,obj_functions):
    assert len(weights) == len(obj_functions)

    m = len(weights)

    C = 0
    for i in range(m):
        C += weights[i] * obj_functions[i]

    return C

if __name__ == "__main__":
    from scipy.stats import uniform

    n_design_variables = 3
    n_obj_functions = 2
    n_simulations = 100000

    x_sampler = [uniform(-5,10) for i in range(n_design_variables)]

    column_names = ['id'] \
            + ['x{}'.format(i+1) for i in range(n_design_variables)] \
            + ['f{}'.format(i+1) for i in range(n_obj_functions)]
    data = []
    for i in range(n_simulations):
        x = [u.rvs() for u in x_sampler]
        f1,f2 = kurasawe(x)
        row = [i] + x + [f1,f2]
        data.append([i] + x + [f1,f2])

    df = pd.DataFrame(data,
                 columns=column_names)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1,)
    ax.scatter(df['f1'],df['f2'],c='black',marker=".",s=1)
    #ax.set_xlim(-20,-14)
    #ax.set_ylim(-12,2)
    plt.show()
    fig.savefig('pareto_mc_sampling.eps',dps=1200)
