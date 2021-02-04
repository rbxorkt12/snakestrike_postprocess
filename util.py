import numpy as np
from sklearn.decomposition import PCA


def get_pointnum(whole_points):
    return len(whole_points[0].keys())


def get_framenum(whole_points):
    return len(whole_points.keys())


def scale_checker(whole_points):
    max_x, max_y, max_z = -np.inf, -np.inf, -np.inf
    min_x, min_y, min_z = np.inf, np.inf, np.inf
    for _, time_points in whole_points.items():
        if time_points is None:
            continue
        for _, point in time_points.items():
            if point.x < min_x:
                min_x = point.x
            elif point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            elif point.y > max_y:
                max_y = point.y
            if point.z < min_z:
                min_z = point.z
            elif point.z > max_z:
                max_z = point.z
    return [[min_x - 50, max_x + 50], [min_y - 50, max_y + 50], [min_z - 50, max_z + 50]]


def scale_proj(scale, proj):
    scale_1pc = [np.dot([scale[0][0], scale[1][0], scale[2][0]], proj[:, 0]),
                 np.dot([scale[0][1], scale[1][1], scale[2][1]], proj[:, 0])]
    if scale_1pc[0] > scale_1pc[1]:
        scale_1pc[0], scale_1pc[1] = scale_1pc[1], scale_1pc[0]
    scale_2pc = [np.dot([scale[0][0], scale[1][0], scale[2][0]], proj[:, 1]),
                 np.dot([scale[0][1], scale[1][1], scale[2][1]], proj[:, 1])]
    if scale_2pc[0] > scale_2pc[1]:
        scale_2pc[0], scale_2pc[1] = scale_2pc[1], scale_2pc[0]
    scale = (scale_1pc, scale_2pc)
    return scale


def get_pca(whole_points):
    x = []
    for _, stamp in whole_points.items():
        if stamp is None:
            continue
        for _, point in stamp.items():
            x.append(point.position())
    pca = PCA(n_components=2)
    pca.fit(x)
    pc_vector = pca.components_.T
    pc_ratio = pca.explained_variance_ratio_
    return pc_vector, pc_ratio
