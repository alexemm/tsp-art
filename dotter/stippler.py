from random import choices, seed
from typing import List, Tuple

import numpy as np


def get_probability_matrix(arr):
    return (255. - arr) / (255. - arr).sum()


def determine_datapoint_from_int(i, arr, prev_shape):
    x = int(i % prev_shape[1])
    y = int(i / prev_shape[1])
    return x, y


def choose_k_points(prob_arr_2d, k, prev_shape):
    chosen_data_values = np.random.choice(range(prob_arr_2d.size), size=k, p=prob_arr_2d.flatten(), replace=False)
    chosen_data_points = [determine_datapoint_from_int(i, prob_arr_2d, prev_shape) for i in chosen_data_values]
    return chosen_data_points, chosen_data_values


def choose_next_point(prob_arr_2d, prev_shape):
    chosen_data_values = choices(range(prob_arr_2d.size), k=1, weights=prob_arr_2d.flatten())
    chosen_data_points = [determine_datapoint_from_int(i, prob_arr_2d, prev_shape) for i in chosen_data_values]
    return chosen_data_points


def create_dotted_array(chosen_points, arr):
    dotted_arr = np.zeros(arr.shape) + 255
    for point in chosen_points:
        try:
            dotted_arr[point[1], point[0]] = 0
        except IndexError:
            print(point)
            print('exit')
            exit()
    return dotted_arr


def find_closest_point(p, w):
    distance_to_w = lambda x_1, y_1: np.sqrt((x_1 - w[0])**2 + (y_1 - w[1])**2)
    min_distance = distance_to_w(p[0][0], p[0][1])
    closest_point = 0
    for i, point in enumerate(p):
        if min_distance == 0:
            break
        curr_distance = distance_to_w(point[0], point[1])
        if curr_distance < min_distance:
            closest_point = i
            min_distance = curr_distance
    return closest_point


def tractor_beam(arr, k, iterations=10):
    prob_matr = get_probability_matrix(arr)
    prev_shape = prob_matr.shape
    prob_matr = prob_matr.flatten()
    p, values = choose_k_points(prob_matr, k, prev_shape)
    n = np.zeros(len(p))
    #prob_matr[values] = 0.
    #prob_matr = prob_matr.reshape(prev_shape)
    #print(prob_matr)
    for iteration in range(iterations):
        # 1. Select tractor beam point
        w = choose_next_point(prob_matr, prev_shape)[0]
        # 2. Find closest point to tractor beam point
        i = find_closest_point(p, w)
        #print("P"+str(p[i]))
        #print("W"+str(w))
        # 3.
        n[i] += 1
        p[i] = int(round(1./(n[i] + 1.) * w[0] + n[i]/float(n[i] + 1.) * p[i][0])), \
               int(round(1./(n[i] + 1.) * w[1] + n[i]/float(n[i] + 1.) * p[i][1]))

        if iteration % 100 == 0 or iterations/2 == iteration:
            print(iteration)
    return create_dotted_array(p, arr)
