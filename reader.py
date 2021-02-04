import numpy as np
import csv
from numpy import linalg as LA
from util import get_pointnum


class line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def length(self):
        x_distance = self.point_1.x - self.point_2.x
        y_distance = self.point_1.y - self.point_2.y
        z_distance = self.point_1.z - self.point_2.z
        return LA.norm([x_distance, y_distance, z_distance])

    def vector(self):
        x_diff = self.point_1.x - self.point_2.x
        y_diff = self.point_1.y - self.point_2.y
        z_diff = self.point_1.z - self.point_2.z
        return x_diff,y_diff,z_diff

    def angle(self, target_line):  # return cos value
        my_vector = self.vector()
        target_vector = target_line.vector()
        return np.dot(my_vector, target_vector) / (LA.norm(my_vector) * LA.norm(target_vector))


class point:
    def __init__(self, x, y, z, index):
        self.index = index
        self.x = x
        self.y = y
        self.z = z
        self.lines = []

    def position(self):
        return [self.x, self.y, self.z]

    def projZ(self):
        return self.x, self.y

    def projX(self):
        return self.y, self.z

    def projY(self):
        return self.x, self.z

    def proj_plane(self, vector):
        cord1 = np.dot([self.x, self.y, self.z], vector[:, 0])
        cord2 = np.dot([self.x, self.y, self.z], vector[:, 1])
        return cord1, cord2

    def add_line(self, line):
        self.lines.append(line)

    def get_lines(self):
        return self.lines


def line_setting_read(path):
    line_setting = {}
    with open(path, 'r') as f:
        for text in f:
            origin, targets = text.split(":")
            targets = list(map(int, targets.split(',')))
            origin = int(origin)
            line_setting[origin] = targets
    return line_setting


def csv2pointdic(path, line_opt=False, linesetting_path=None):
    data = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 4:
                data.append(row[0].split(','))
    for row in data:
        del row[0]
        del row[-1]
    whole_points = {}
    for time, row in enumerate(data):
        time_points = {}
        for point_num, position in enumerate(row):
            try:
                x, y, z = position.split('|')
                x, y, z = float(x), float(y), float(z)
                time_points[point_num] = point(x, y, z, index=point_num)
            except Exception as e:
                print("There is frame that cannot be triangulated in video")
                time_points = None
                break
        whole_points[time] = time_points
    if line_opt is True and linesetting_path is not None:
        setting = line_setting_read(linesetting_path)
        for origin in setting.keys():
            if origin >= get_pointnum(whole_points):
                raise IndexError
            for target in setting[origin]:
                for frame in whole_points.values():
                    frame[origin].add_line(line(frame[origin], frame[target]))
                    frame[target].add_line(line(frame[target], frame[origin]))

    return whole_points
