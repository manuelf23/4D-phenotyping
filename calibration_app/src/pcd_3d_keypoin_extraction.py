from lidar_utils import *
import glob
import pyransac3d as pyrsc
from matplotlib import pyplot as plt
from sklearn import linear_model, datasets
import numpy as np
import open3d as o3d



def get_3d_points_plane(fname, plot = True):
    y_limit = (0.7, 1.2)
    z_limit = (-0.4, 1.8)
    plane1 = pyrsc.Plane()
    line = pyrsc.Plane()
    pcd_frame = read_pcd(fname, y_limit, z_limit)
    
    o3d_pcd = get_o3d_pcd(pcd_frame)
    xyz_numpy = np.asarray(o3d_pcd.points)

    best_eq2, best_inliers = plane1.fit(xyz_numpy, 0.01)
    a3d = best_eq2[0]
    b3d = best_eq2[1]
    c3d = best_eq2[2]
    d3d = best_eq2[3]
    pcd_max = pcd_frame.loc[pcd_frame.groupby(['laser_id'])['Z'].idxmax()]
    pcd_min = pcd_frame.loc[pcd_frame.groupby(['laser_id'])['Z'].idxmin()]
 
    if plot:
        plt.scatter(pcd_max['X'], pcd_max['Z'], linewidths=1)
        plt.scatter(pcd_min['X'], pcd_min['Z'], linewidths=1)

    max_pcd_max = pcd_max.loc[pcd_max[
        'Z'].idxmax()]

    min_pcd_min = pcd_min.loc[pcd_min[
        'Z'].idxmin()]
    ul = pcd_max[(pcd_max.X < max_pcd_max['X'])]
    ur = pcd_max[(pcd_max.X > max_pcd_max['X'])]
    dl = pcd_min[(pcd_min.X < min_pcd_min['X'])]
    dr = pcd_min[(pcd_min.X > min_pcd_min['X'])]

    if plot:
        plt.scatter(ul['X'], ul['Z'], linewidths=1)
        plt.scatter(ur['X'], ur['Z'], linewidths=1)
        plt.scatter(dl['X'], dl['Z'], linewidths=1)
        plt.scatter(dr['X'], dr['Z'], linewidths=1)

    plt.show()
    if plot:
        plt.scatter(ul['X'], ul['Z'], linewidths=1)
        plt.scatter(ur['X'], ur['Z'], linewidths=1)
        plt.scatter(dl['X'], dl['Z'], linewidths=1)
        plt.scatter(dr['X'], dr['Z'], linewidths=1)
    xp_ul = np.zeros((len(ul['X']), 1))
    xp_ul[:, 0] = ul['X']
    yp_ul = np.zeros((len(ul['X']), 1))
    yp_ul[:, 0] = ul['Z']
    ransac_ul = linear_model.RANSACRegressor()
    ransac_ul.fit(xp_ul, yp_ul)

    m1 = ransac_ul.estimator_.coef_
    b1 = ransac_ul.estimator_.intercept_
    line_X = np.arange(xp_ul.min()-0.2,
                        xp_ul.max()+0.2, 0.001)[:, np.newaxis]
    line_y_ransac_ul = ransac_ul.predict(line_X)
    if plot:
        plt.plot(line_X, line_y_ransac_ul, color='red', linewidth=1, label='RANSAC regressor')

    xp_ur = np.zeros((len(ur['X']), 1))
    xp_ur[:, 0] = ur['X']
    yp_ur = np.zeros((len(ur['X']), 1))
    yp_ur[:, 0] = ur['Z']
    ransac_ur = linear_model.RANSACRegressor()
    ransac_ur.fit(xp_ur, yp_ur)

    m2 = ransac_ur.estimator_.coef_
    b2 = ransac_ur.estimator_.intercept_
    line_X = np.arange(xp_ur.min()-0.2,
                        xp_ur.max()+0.2, 0.001)[:, np.newaxis]
    line_y_ransac_ur = ransac_ur.predict(line_X)
    if plot:
        plt.plot(line_X, line_y_ransac_ur, color='red',
                linewidth=1, label='RANSAC regressor')

    xp_dl = np.zeros((len(dl['X']), 1))
    xp_dl[:, 0] = dl['X']
    yp_dl = np.zeros((len(dl['X']), 1))
    yp_dl[:, 0] = dl['Z']
    ransac_dl = linear_model.RANSACRegressor()
    ransac_dl.fit(xp_dl, yp_dl)

    m4 = ransac_dl.estimator_.coef_
    b4 = ransac_dl.estimator_.intercept_
    line_X = np.arange(xp_dl.min()-0.2,
                        xp_dl.max()+0.2, 0.001)[:, np.newaxis]
    line_y_ransac_dl = ransac_dl.predict(line_X)
    if plot:
        plt.title(fname.split('/')[-1])
        plt.plot(line_X, line_y_ransac_dl, color='red',linewidth=1, label='RANSAC regressor')

    xp_dr = np.zeros((len(dr['X']), 1))
    xp_dr[:, 0] = dr['X']
    yp_dr = np.zeros((len(dr['X']), 1))
    yp_dr[:, 0] = dr['Z']
    ransac_dr = linear_model.RANSACRegressor()
    ransac_dr.fit(xp_dr, yp_dr)
  
    m3 = ransac_dr.estimator_.coef_
    b3 = ransac_dr.estimator_.intercept_
    line_X = np.arange(xp_dr.min()-0.2,
                        xp_dr.max()+0.2, 0.001)[:, np.newaxis]
    line_y_ransac_dr = ransac_dr.predict(line_X)
    if plot:
        plt.plot(line_X, line_y_ransac_dr, color='red',linewidth=1, label='RANSAC regressor')

    kp_X = []
    kp_Z = []

    p1_x = (b2 - b1) / (m1 - m2)
    p1_z = ransac_ur.predict(p1_x)
    kp_X.append(p1_x[0,0])
    kp_Z.append(p1_z[0,0])

    p2_x = (b3 - b2) / (m2 - m3)
    p2_z = ransac_dr.predict(p2_x)
    kp_X.append(p2_x[0,0])
    kp_Z.append(p2_z[0,0])

    p3_x = (b4 - b3) / (m3 - m4)
    p3_z = ransac_dl.predict(p3_x)
    kp_X.append(p3_x[0,0])
    kp_Z.append(p3_z[0,0])

    p4_x = (b4 - b1) / (m1 - m4)
    p4_z = ransac_dl.predict(p4_x)
    kp_X.append(p4_x[0,0])
    kp_Z.append(p4_z[0,0])

    if plot:

        plt.scatter(kp_X, kp_Z, color='red',
                linewidth=2, label='K Points')

        plt.show()
    kp_Y = []
    p1_y = - (a3d*p1_x + c3d*p1_z + d3d)/b3d
    kp_Y.append(p1_y[0,0])
    p2_y = - (a3d*p2_x + c3d*p2_z + d3d)/b3d
    kp_Y.append(p2_y[0,0])
    p3_y = - (a3d*p3_x + c3d*p3_z + d3d)/b3d
    kp_Y.append(p3_y[0,0])
    p4_y = - (a3d*p4_x + c3d*p4_z + d3d)/b3d
    kp_Y.append(p4_y[0,0])
    
    o3d_pcd.paint_uniform_color([0.1, 0.706, 0.1])
    if plot:
        o3d.visualization.draw_geometries(
            [o3d_pcd])
    
    xyz_kp_points = np.zeros((len(kp_X), 3))
    xyz_kp_points[:, 0] = kp_X[:]
    xyz_kp_points[:, 1] = kp_Y[:]
    xyz_kp_points[:, 2] = kp_Z[:]

    o3d_kp = o3d.geometry.PointCloud()
    o3d_kp.points = o3d.utility.Vector3dVector(xyz_kp_points)
    o3d_kp.paint_uniform_color([1, 0, 0])

    
    if plot:
        o3d.visualization.draw_geometries(
        [o3d_kp])
        o3d.visualization.draw_geometries(
            [o3d_kp, o3d_pcd], window_name=fname.split('/')[-1])

    return kp_X, kp_Y, kp_Z