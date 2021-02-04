import pandas as pd
from os.path import join
from util import get_pointnum


def export_analysis(whole_points,path):
    point_num = get_pointnum(whole_points)
    for i in range(point_num):
        result = []
        for frame in whole_points.values():
            columns = []
            frame_result = []
            p = frame[i]
            x,y,z = p.position()
            columns.extend(['x','y','z'])
            frame_result.extend([x,y,z])
            lines = p.get_lines()
            frame_result.append(len(lines))
            columns.append('# of connected lines')
            for j in range(len(lines)):
                dest=lines[j].point_2.index
                columns.append('{}th line destination point'.format(j))
                frame_result.append(dest)
                for k in range(j+1,len(lines)):
                    angle=lines[j].angle(lines[k])
                    columns.append('{0}th line and {1}th line cos'.format(j,k))
                    frame_result.append(angle)
            result.append(frame_result)
        output = pd.DataFrame(result,columns=columns)
        output.to_csv(join(path,f'{i}th_point_result.csv'))
