import math


# points
p_O = [0, 0]
p_A = [0, 168]
p_B = [84, 168]
p_C = [84, 126]
p_D = [84, 210]
p_E = [168, 210]
p_F = [168, 84]
p_G = [210, 84]
p_H = [210, 0]

# walls
w_a = [p_O, p_A, "O-A"]
w_b = [p_A, p_B, "A-B"]
w_c = [p_C, p_D, "C-D"]
w_d = [p_D, p_E, "D-E"]
w_e = [p_E, p_F, "E-F"]
w_f = [p_F, p_G, "F-G"]
w_g = [p_G, p_H, "G-H"]
w_h = [p_H, p_O, "H-O"]

list_wall = [w_a, w_b, w_c, w_d, w_e, w_f, w_g, w_h]

def find_mm(angle_list):
    min = 370
    max = -370
    for item in angle_list:
        if item > 0 and item < min:
            min = item
        elif item < 0 and item > max:
            max = item
    print(min, max)
    if max == -370:
        max = 0
        for item in angle_list:
            if item > max:
                max = item
    elif min == 370:
        min = 0
        for item in angle_list:
            if item < min:
                min = item
    return min, max

def find_point_index(point_list, angle_list, min, max):
    min_index = angle_list.index(min)
    max_index = angle_list.index(max)
    print(min_index, max_index)
    if abs(max_index - min_index) == 1:
        return point_list[max_index], point_list[min_index]
    elif (max_index == 2 and min_index == 4) or (max_index == 2 and min_index == 4):
        return point_list[max_index], point_list[min_index]
    elif (max_index == 0 and min_index == 8) or (max_index == 8 and min_index == 0):
        return point_list[max_index], point_list[min_index]
    else:
        angle_list[max_index] = -370
        min, max = find_mm(angle_list)
        return find_point_index(point_list, angle_list, min, max)

def find_walls(x, y, theta):


    possible_w = list()
    max_angle = 0
    point_list = [p_O, p_A, p_B, p_C, p_D, p_E, p_F, p_G, p_H]
    angle_list = list()
    for item in point_list:
        angle = math.atan2(item[1] - y, item[0] - x)
        angle = math.degrees(angle) % 360
        angle_list.append(angle)
        if angle > max_angle:
            max_angle = angle
    res = 360 - max_angle
    print(angle_list)
    for i in range(len(angle_list)):
        angle_list[i] -=theta
    print(angle_list)
    min, max = find_mm(angle_list)
    p1 ,p2 = find_point_index(point_list, angle_list, min, max)
    return p1 ,p2


def decide_walls():

    pass


if __name__ == "__main__":

    print(find_walls(90, 90, 270))
