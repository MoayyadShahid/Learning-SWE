import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

training_set = pd.read_csv("salary_data.csv")

x_train = training_set["YearsExperience"].values
y_train = training_set["Salary"].values

def cost_function(x, y, w, b):
    m = len(x)
    cost_sum = 0

    for i in range(m):
        f = w * x[i] + b
        cost = (f - y[i]) ** 2
        cost_sum += cost
    
    cost_sum = (1 / (2 * m)) * cost_sum
    return cost_sum


def gradient_function(x, y, w, b):
    m = len(x)
    dc_dw = 0
    dc_db = 0

    for i in range(m):
        f = w * x[i] + b
        dc_dw = (f - y[i]) * x[i]
        dc_db = f - y[i]
    
    dc_dw = (1 / m) * dc_dw
    dc_db = (1 / m) * dc_db

    return dc_dw, dc_db


def gradient_descent(x, y, alpha, iterations):
    w = 0
    b = 0

    for i in range(iterations):
        dc_dw, dc_db = gradient_function(x, y, w, b)

        w = w - alpha * dc_dw
        b = b - alpha * dc_db

        print(f"Iteration {i}: Cost {cost_function(x, y, w, b)}")

    return w, b



learning_rate = 0.01
iterations = 10000
final_w, final_b = gradient_descent(x_train, y_train, learning_rate, iterations)

print(f"final slope (w): {final_w}, final intercept (b): {final_b}")


plt.scatter(x_train, y_train, label='Data Points')

x_vals = np.linspace(min(x_train), max(x_train), 100)
y_vals = final_w * x_vals + final_b 
plt.plot(x_vals, y_vals, color='red', label='regression line')

plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.show()
