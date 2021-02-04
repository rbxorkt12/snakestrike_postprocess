from reader import csv2pointdic
from util import get_framenum
from plot import plot_save
from video import images2video, horizontal_concat_videos, vertical_concat_videos

whole_points = csv2pointdic('finger/realfinger.csv')
frame_num = get_framenum(whole_points)
plot_save(frame_num, whole_points, 'finger/proj_x', proj='X')
images2video('finger/proj_x', 'finger/xproj_visualize.avi', 30)
print('x visualize end')
plot_save(frame_num, whole_points, 'finger/proj_y', proj='Y')
images2video('finger/proj_y', 'finger/yproj_visualize.avi', 30)
print('y visualize end')
plot_save(frame_num, whole_points, 'finger/proj_z', proj='Z')
images2video('finger/proj_z', 'finger/zporj_visualize.avi', 30)
print('z visualize end')
plot_save(frame_num, whole_points, 'finger/3d')
images2video('finger/images', 'finger/3d_visualize.avi', 30)
print('3d visualize end')
horizontal_concat_videos(['finger/real_finger1.avi', 'finger/real_finger2.avi'], 'finger/camera.avi')
horizontal_concat_videos(['finger/xproj_visualize.avi', 'finger/yproj_visualize.avi', 'finger/zporj_visualize.avi',
                          'finger/3d_visualize.avi'], 'finger/visualize.avi')
vertical_concat_videos(['finger/camera.avi', 'finger/visualize.avi'], 'finger/output.avi')
