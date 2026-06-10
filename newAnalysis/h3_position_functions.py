from numba import njit
import numpy as np

def get_centroid(cell_coords):
    z, y, x = cell_coords
    return x.mean(), y.mean(), z.mean()


@njit
def line_calcs(xl, yl, x, y):
    dis = []
    
    for xli, yli in zip(xl, yl):
        dis.append((x-xli)**2 + (y-yli)**2)
    
    min_dis = min(dis)
    dis_pos = dis.index(min_dis)
    if yl[dis_pos] - y > 0:
        return -min(dis) ** .5
    else:
        return min(dis) ** .5


def get_distance_to_line(line_frame, x, y):
     
    line_x = np.array(list(line_frame.x_pixel))
    line_y = np.array(list(line_frame.ypixel))
    
    mindis = line_calcs(line_x, line_y, x, y)
        
    return  mindis
