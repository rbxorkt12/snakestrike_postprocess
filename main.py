import argparse
from reader import csv2pointdic
from util import get_framenum
from plot import plot_save
from video import images2video, horizontal_concat_videos, vertical_concat_videos
from export import export_analysis
from os.path import join


def main(project_path, line_opt):
    whole_points = csv2pointdic(join(project_path, 'triangulate.csv'), line_opt=line_opt)
    frame_num = get_framenum(whole_points)
    plot_save(frame_num, whole_points, join(project_path, 'proj_x'), proj='X', line_opt=line_opt)
    images2video(join(project_path, 'proj_x'), join(project_path, 'x_visualize.avi'), 30)
    print('x visualize end')
    plot_save(frame_num, whole_points, join(project_path, 'proj_y'), proj='Y', line_opt=line_opt)
    images2video(join(project_path, 'proj_y'), join(project_path, 'y_visualize.avi'), 30)
    print('y visualize end')
    plot_save(frame_num, whole_points, join(project_path, 'proj_z'), proj='Z', line_opt=line_opt)
    images2video(join(project_path, 'proj_z'), join(project_path, 'z_visualize.avi'), 30)
    print('z visualize end')
    plot_save(frame_num, whole_points, join(project_path, '3d'), line_opt=line_opt)
    images2video(join(project_path, '3d'), join(project_path, '3d_visualize.avi'), 30)
    print('3d visualize end')
    horizontal_concat_videos([join(project_path, 'cam1.avi'), join(project_path, 'cam2.avi')],
                             join(project_path, 'camera.avi'))
    horizontal_concat_videos([join(project_path, 'x_visualize.avi'), join(project_path, 'y_visualize.avi'),
                              join(project_path, 'z_visualize.avi'),
                              join(project_path, '3d_visualize.avi')], join(project_path, 'visualize.avi'))
    vertical_concat_videos([join(project_path, 'camera.avi'), join(project_path, 'visualize.avi')],
                           join(project_path, 'output.avi'))
    export_analysis(whole_points, join(project_path, 'analysis'))


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(nargs='+', help='Example) index.html', dest='project')
    parser.add_argument('--line', '-l', nargs='*', help='Example) True', default=False, dest='line_opt')

    project = parser.parse_args().project
    line_opt = parser.parse_args().line_opt

    return project, line_opt


if __name__ == '__main__':
    project, line_opt = get_arguments()
    main(project, line_opt)
