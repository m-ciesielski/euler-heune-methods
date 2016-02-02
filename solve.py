# -*- coding: utf-8 -*-

import argparse
from matplotlib import pyplot as plt
import numpy


def exact_result_value(x):
    return numpy.exp(float(x)) * float(x)


def x_y_function(x, y):
    return numpy.exp(x) + y - x


def equidistant_grid(a, b, h):
    n = int((b - a) / h)
    x = [a+(i * h) for i in range(0, n+1)]
    return x


def method_error(method_results, x):
    error_values = list()
    for i, x_i in enumerate(x):
        error_values.append(numpy.fabs(exact_result_value(x_i) - method_results[i]))

    return error_values


def heune_method(a, b, h):
    x = equidistant_grid(a, b, h)

    y = list()

    # Calculate x(a) and y(a) values
    y.append(exact_result_value(a))
    x_n = x[0]

    for x_i in x[1:]:
        y_n = y[-1]
        y.append(y_n + (h/2) * (x_y_function(x_n, y_n) + x_y_function(x_n + h, y_n + h*x_y_function(x_n, y_n))))
        x_n = x_i

    return y


def euler_method(a, b, h):
    x = equidistant_grid(a, b, h)

    y = list()

    # Calculate x(a) and y(a) values
    y.append(exact_result_value(a))
    x_n = x[0]

    for x_i in x[1:]:
        y_n = y[-1]
        y.append(y_n + h*(x_y_function(x_n, y_n)))
        x_n = x_i

    return y


def draw_plots(a, b, h):
    """
    Draws interpolation plot for given interpolation polynomial and nodes.
    """
    # TODO: calculate figure size dynamically
    figure = plt.figure(figsize=(10, 8), dpi=100)

    # Calculate equidistant grid
    eq_grid = equidistant_grid(a, b, h)

    # Plot exact solution
    y = [exact_result_value(x_i) for x_i in eq_grid]
    ax1 = figure.add_subplot(211)
    ax1.plot(eq_grid, y, label="Rozwiazanie dokladne")

    # Plot Euler method
    euler_results = euler_method(a, b, h)
    ax2 = figure.add_subplot(211)
    ax2.plot(eq_grid, euler_results, label="Metoda Eulera")

    # Plot Heune method
    heune_results = heune_method(a, b, h)
    ax3 = figure.add_subplot(211)
    ax3.plot(eq_grid, heune_results, label="Metoda Heune'a")

    # plt.legend(handles=[ax1_plot, ax2_plot, ax3_plot])

    # draw legend on top of plot area
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

    plt.grid(True)

    # Draw error plots

    euler_error_ax = figure.add_subplot(212)
    euler_error_ax.plot(eq_grid, method_error(euler_results, eq_grid), label="Blad metody Eulera")

    heune_error_ax = figure.add_subplot(212)
    heune_error_ax.plot(eq_grid, method_error(heune_results, eq_grid), label="Blad metody Heune'a")

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
           ncol=2, mode="expand", borderaxespad=0.)

    plt.grid(True)

    plt.show()


def parse_user_provided_float(label):
    val = None
    while True:
        try:
            val = float(input("Podaj {0}:".format(label)))
        except ValueError:
            print("Podaj poprawna wartosc dla zmiennej:  {0}.".format(label))
            continue
        else:
            break

    return val


def parseargs():
    parser = argparse.ArgumentParser(description='Metody Heune\'a i Eulera.')
    parser.add_argument('--step-length', type=float, help='Dlugosc kroku.')
    parser.add_argument('--start', type=float, help='Poczatek przedzialu wartosci X.')
    parser.add_argument('--end', type=float, help='Koniec przedzialu wartosci X.')
    parsed_args = parser.parse_args()

    if not parsed_args.start:
        parsed_args.start = parse_user_provided_float("wartosc a (poczatek przedzialu wartosci X)")

    if not parsed_args.end:
        parsed_args.end = parse_user_provided_float("wartosc b (koniec przedzialu wartosci X)")

    if not parsed_args.step_length:
        parsed_args.step_length = parse_user_provided_float("h (dlugosc kroku)")
        while parsed_args.step_length <= 0 or parsed_args.step_length > (parsed_args.end - parsed_args.start):
            print("Dlugosc kroku musi byc większa od zera i mniejsza niż dlugosc przedzialu.")
            parsed_args.step_length = parse_user_provided_float("h (dlugosc kroku)")

    return parsed_args


if __name__ == '__main__':
    args = parseargs()

    draw_plots(a=args.start, b=args.end, h=args.step_length)
