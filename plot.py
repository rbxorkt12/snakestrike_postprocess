import numpy as np
import matplotlib.pyplot as plt
import os
from os.path import join
from util import get_pointnum, scale_checker, scale_proj


def plot3d_frame(whole_points, frame, scale, path, line_opt=False):
    flg = plt.figure()
    ax = flg.gca(projection='3d')
    time_points = whole_points[frame]
    plt.suptitle(f'3d position')
    if time_points is None:
        plt.savefig(path)
    else:
        X, Y, Z = [], [], []
        for point in time_points.values():
            X.append(point.x)
            Y.append(point.y)
            Z.append(point.z)
            if line_opt is True:
                lines = point.get_lines()
                for draw in lines:
                    X1, Y1, Z1 = zip(draw.point_1.position(), draw.point_2.position())
                    X1, Y1, Z1 = list(X1), list(Y1), list(Z1)
                    plt.plot(X1, Y1, Z1, 'b-')
        color = list(range(0, get_pointnum(whole_points)))
        ax.scatter(X, Y, Z, c=color)
        for i, txt in enumerate(color):
            ax.text(X[i], Y[i], Z[i], txt)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim3d(*scale[0])
        ax.set_ylim3d(*scale[1])
        ax.set_zlim3d(*scale[2])
        plt.savefig(path)
    plt.close()


def plot2d_frame(whole_points, frame, scale, path, plane, line_opt=False):
    flg = plt.figure()
    ax = flg.gca()
    time_points = whole_points[frame]
    plt.suptitle(f'2d position in {plane} plane')
    if time_points is None:
        plt.savefig(path)
    else:
        cord1, cord2 = [], []
        for _, point in time_points.items():
            if plane == 'X':
                cord1_num, cord2_num = point.projX()
                if line_opt is True:
                    lines = point.get_lines()
                    for draw in lines:
                        line1_num, line2_num = zip(draw.point_1.projX(), draw.point_2.projX())
                        line1_num, line2_num = list(line1_num), list(line2_num)
                        plt.plot(line1_num, line2_num, 'b-')
            elif plane == 'Y':
                cord1_num, cord2_num = point.projY()
                if line_opt is True:
                    lines = point.get_lines()
                    for draw in lines:
                        line1_num, line2_num = zip(draw.point_1.projY(), draw.point_2.projY())
                        line1_num, line2_num = list(line1_num), list(line2_num)
                        plt.plot(line1_num, line2_num, 'b-')
            elif plane == 'Z':
                cord1_num, cord2_num = point.projZ()
                if line_opt is True:
                    lines = point.get_lines()
                    for draw in lines:
                        line1_num, line2_num = zip(draw.point_1.projZ(), draw.point_2.projZ())
                        line1_num, line2_num = list(line1_num), list(line2_num)
                        plt.plot(line1_num, line2_num, 'b-')
            else:
                cord1_num, cord2_num = point.proj_plane(plane)
                if line_opt is True:
                    lines = point.get_lines()
                    for draw in lines:
                        line1_num, line2_num = zip(draw.point_1.proj_plane(plane), draw.point_2.proj_plane(plane))
                        line1_num, line2_num = list(line1_num), list(line2_num)
                        plt.plot(line1_num, line2_num, 'b-')
            cord1.append(cord1_num)
            cord2.append(cord2_num)
        color = list(range(0, get_pointnum(whole_points)))
        ax.scatter(cord1, cord2, c=color)
        ax.grid(True)
        for i, txt in enumerate(color):
            ax.text(cord1[i], cord2[i], txt)
        ax.set_xlabel('cord1')
        ax.set_ylabel('cord2')
        if plane == 'X':
            cord1_index, cord2_index = 1, 2
            ax.set_xlim(*scale[cord1_index])
            ax.set_ylim(*scale[cord2_index])
        elif plane == 'Y':
            cord1_index, cord2_index = 0, 2
            ax.set_xlim(*scale[cord1_index])
            ax.set_ylim(*scale[cord2_index])
        elif plane == 'Z':
            cord1_index, cord2_index = 0, 1
            ax.set_xlim(*scale[cord1_index])
            ax.set_ylim(*scale[cord2_index])
        else:
            scale = scale_proj(scale, proj=plane)
            ax.set_xlim(scale[0])
            ax.set_ylim(scale[1])
        plt.savefig(path)
    plt.close()


def plot_save(frame_num, whole_points, path, proj=None, line_opt=False):
    plt.ioff()
    os.makedirs(path, exist_ok=True)
    scale = scale_checker(whole_points)
    for i in range(frame_num):
        if proj is None:
            plot3d_frame(whole_points, frame=i, scale=scale, path=join(path, f'{i}.jpg'), line_opt=line_opt)
        elif proj in ['X', 'Y', 'Z']:
            plot2d_frame(whole_points, frame=i, scale=scale, path=join(path, f'{i}.jpg'), plane=proj, line_opt=line_opt)
        else:  # project to plane
            plot2d_frame(whole_points, frame=i, scale=scale, path=join(path, f'{i}.jpg'), plane=proj, line_opt=line_opt)
