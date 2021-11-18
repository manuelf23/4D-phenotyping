import pandas as pd
import numpy as np
import open3d as o3d
import math
import cv2
import matplotlib.cm as cm
import matplotlib
import glob
# from lidar_utils import *
from sklearn import linear_model, datasets
from sklearn.linear_model import LinearRegression
from copy import deepcopy
from custom_exceptions import EmptyMultispectralDataError
class PcdModel():
    def __init__(self, pcd, x_center=0, y_center=0, nb_neighbors=15, std_ratio=0.1, rotation_plane_mtx=False, rot_ini=0, path_rgb_fusion_img=False, path_to_3d_2d_keypoints=None, method=None):
        self.__x_center = x_center
        self.__y_center = y_center
        self.__nb_neighbors = nb_neighbors
        self.__std_ratio = std_ratio
        self.__rot_ini = rot_ini
        self.__rotation_plane_mtx = rotation_plane_mtx
        self.__pcd = self.filter_and_promediate_pcd(pcd)
        self.__list_pcds = []
        self.norm = matplotlib.colors.Normalize(vmin=0, vmax=100, clip=True)
        self.mapper = cm.ScalarMappable(norm=self.norm, cmap=cm.jet)
        self.__intensity_r_list = []
        self.__intensity_g_list = []
        self.__intensity_b_list = []
        # self.__pcd = self.__pcd.apply(self.intensity_color, axis=1)
        # self.__pcd = self.__pcd.apply(self.intensity_color_umbral, axis=1)
        
        # self.intensity_color()
        
        if path_rgb_fusion_img is not False and path_to_3d_2d_keypoints is not None:
            self.__dim = (640, 480)
            self.__ffusion = True
            self.__regression_model = None
            self.__img_fusion = None
            self.__img_fusion_copy = None
            self.__img_fusion_NDVI = None
            self.__img_fusion_NDVI_copy = None
            self.__img_fusion_NDRE = None
            self.__img_fusion_NDRE_copy = None
            self.__img_fusion_SAVI = None
            self.__img_fusion_SAVI_copy = None
            self.__img_fusion_MSAVI = None
            self.__img_fusion_MSAVI_copy = None
            self.__img_fusion_DVI = None
            self.__img_fusion_DVI_copy = None
            self.__r_list = []
            self.__g_list = []
            self.__b_list = []
            self.__r_list_NDVI = []
            self.__g_list_NDVI = []
            self.__b_list_NDVI = []
            self.__r_list_NDRE = []
            self.__g_list_NDRE = []
            self.__b_list_NDRE = []
            self.__r_list_SAVI = []
            self.__g_list_SAVI = []
            self.__b_list_SAVI = []
            self.__r_list_MSAVI = []
            self.__g_list_MSAVI = []
            self.__b_list_MSAVI = []
            self.__r_list_DVI = []
            self.__g_list_DVI = []
            self.__b_list_DVI = []

            self.__ndvi_array = None

            self.__path_to_3d_2d_keypoints = path_to_3d_2d_keypoints
            self.set_fusion_model(self.__path_to_3d_2d_keypoints, method)
            self.__pcd = self.fusion_3d_2d(path_rgb_fusion_img, self.__pcd)
        else:
            self.__ffusion = False

        self.__pcd = self.calibrate_xy_plane(self.__pcd)
        self.__pcd = self.rotate_pcd(self.__pcd, self.__rot_ini)

        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['r']
        xyz_colors[:, 1] = self.__pcd['g']
        xyz_colors[:, 2] = self.__pcd['b']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        pcd_down = o3d_pcd
        # pcd_down = o3d_pcd.voxel_down_sample(voxel_size=0.001)
        # o3d.geometry.PointCloud.estimate_normals(
        #     pcd_down,
        #     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1,
        #                                                         max_nn=30))
        self.__list_pcds.append(pcd_down)

    def set_fusion_model(self, path_to_3d_2d_keypoints, method):
        pcd = pd.read_csv(path_to_3d_2d_keypoints)
        if method == 'linear':
            self.__regression_model = LinearRegression()
        elif method == 'ransac':
            self.__regression_model = linear_model.RANSACRegressor()
        else:
            raise Exception(ValueError('method is diferent of linear or ransac'))
        self.__regression_model.fit(
            pcd[['x', 'y', 'z', 'HC']].values, pcd[['u', 'v', 'HC']].values)

    def color_fusion(self, pcd):
        index = int(pcd['index'])
        idx = self.__regression_model.predict([[pcd['X'], pcd['Y'], pcd['Z'], 1]])
        u = np.clip(int(idx[0][1]), 0, self.__dim[0] - 1)
        v = np.clip(int(idx[0][0]), 0, self.__dim[1] - 1)
        try:
            pcd['ndvi'] = self.__ndvi_array[u][v][0]
        except TypeError:
            print("There is not multispectral pcd data in .pickle format")
            raise EmptyMultispectralDataError(
                "There is not multispectral pcd data in .pickle format")
        self.__img_fusion_copy[u][v] = (0, 0, 200)
        self.__img_fusion_NDVI_copy[u][v] = (0, 0, 200)
        self.__img_fusion_NDRE_copy[u][v] = (0, 0, 200)
        self.__img_fusion_SAVI_copy[u][v] = (0, 0, 200)
        self.__img_fusion_MSAVI_copy[u][v] = (0, 0, 200)
        self.__img_fusion_DVI_copy[u][v] = (0, 0, 200)
        self.__r_list.append(self.__img_fusion[u][v][2]/255.0)
        self.__g_list.append(self.__img_fusion[u][v][1]/255.0)
        self.__b_list.append(self.__img_fusion[u][v][0]/255.0)
        self.__r_list_NDVI.append(self.__img_fusion_NDVI[u][v][2]/255.0)
        self.__g_list_NDVI.append(self.__img_fusion_NDVI[u][v][1]/255.0)
        self.__b_list_NDVI.append(self.__img_fusion_NDVI[u][v][0]/255.0)

        self.__r_list_NDRE.append(self.__img_fusion_NDRE[u][v][2]/255.0)
        self.__g_list_NDRE.append(self.__img_fusion_NDRE[u][v][1]/255.0)
        self.__b_list_NDRE.append(self.__img_fusion_NDRE[u][v][0]/255.0)

        self.__r_list_SAVI.append(self.__img_fusion_SAVI[u][v][2]/255.0)
        self.__g_list_SAVI.append(self.__img_fusion_SAVI[u][v][1]/255.0)
        self.__b_list_SAVI.append(self.__img_fusion_SAVI[u][v][0]/255.0)

        self.__r_list_MSAVI.append(self.__img_fusion_MSAVI[u][v][2]/255.0)
        self.__g_list_MSAVI.append(self.__img_fusion_MSAVI[u][v][1]/255.0)
        self.__b_list_MSAVI.append(self.__img_fusion_MSAVI[u][v][0]/255.0)

        self.__r_list_DVI.append(self.__img_fusion_DVI[u][v][2]/255.0)
        self.__g_list_DVI.append(self.__img_fusion_DVI[u][v][1]/255.0)
        self.__b_list_DVI.append(self.__img_fusion_DVI[u][v][0]/255.0)
        return pcd
        # print(self.__img_fusion_NDVI[u][v][0])

    def fusion_3d_2d(self, path_image_folder, pcd_frame):
        if self.__ffusion:
            self.__r_list.clear()
            self.__g_list.clear()
            self.__b_list.clear()

            self.__r_list_NDVI.clear()
            self.__g_list_NDVI.clear()
            self.__b_list_NDVI.clear()

            self.__r_list_NDRE.clear()
            self.__g_list_NDRE.clear()
            self.__b_list_NDRE.clear()

            self.__r_list_SAVI.clear()
            self.__g_list_SAVI.clear()
            self.__b_list_SAVI.clear()

            self.__r_list_MSAVI.clear()
            self.__g_list_MSAVI.clear()
            self.__b_list_MSAVI.clear()

            self.__r_list_DVI.clear()
            self.__g_list_DVI.clear()
            self.__b_list_DVI.clear()
            image_files = glob.glob(
                path_image_folder + '*.JPG') + glob.glob(path_image_folder + '*.jpg')
            # print('PATH:', image_files)
            for image_name in image_files:
                if 'RGB' in image_name:
                    image = cv2.imread(image_name)
                    dim = (640, 480)
                    # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
                    # self.__img_fusion = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                    self.__img_fusion = image
                    self.__img_fusion_copy = deepcopy(self.__img_fusion)
                elif 'NDVI' in image_name and not 'GNDVI' in image_name:
                    self.__img_fusion_NDVI = cv2.imread(image_name, 1)
                    self.__img_fusion_NDVI_copy = deepcopy(
                        self.__img_fusion_NDVI)
                    self.__ndvi_array = np.load(image_name.split(
                        '.')[0] + '.pickle', allow_pickle=True)
                elif 'NDRE' in image_name:
                    self.__img_fusion_NDRE = cv2.imread(image_name)
                    self.__img_fusion_NDRE_copy = deepcopy(
                        self.__img_fusion_NDRE)
                elif 'MSAVI' in image_name:
                    self.__img_fusion_MSAVI = cv2.imread(image_name)
                    self.__img_fusion_MSAVI_copy = deepcopy(
                        self.__img_fusion_MSAVI)
                elif 'SAVI' in image_name and not 'MSAVI' in image_name:
                    self.__img_fusion_SAVI = cv2.imread(image_name)
                    self.__img_fusion_SAVI_copy = deepcopy(
                        self.__img_fusion_SAVI)
                elif 'DVI' in image_name and not 'NDVI' in image_name and not 'GNDVI' in image_name:
                    self.__img_fusion_DVI = cv2.imread(image_name)
                    self.__img_fusion_DVI_copy = deepcopy(
                        self.__img_fusion_DVI)


            # pcd_frame = read_pcd(path_pcd, self.__y_center), self.__x_center)
            # pcd_frame = filter_and_promediate_pcd(
            #     pcd_frame, nb_neighbors=15, std_ratio=0.1)
            
            pcd_frame = pcd_frame.reset_index(drop=True)
            pcd_frame.reset_index(inplace=True)
            pcd_frame = pcd_frame.apply(self.color_fusion, axis=1)
            pcd_frame['r'] = self.__r_list
            pcd_frame['g'] = self.__g_list
            pcd_frame['b'] = self.__b_list
            pcd_frame['r_NDVI'] = self.__r_list_NDVI
            pcd_frame['g_NDVI'] = self.__g_list_NDVI
            pcd_frame['b_NDVI'] = self.__b_list_NDVI
            pcd_frame['r_NDRE'] = self.__r_list_NDRE
            pcd_frame['g_NDRE'] = self.__g_list_NDRE
            pcd_frame['b_NDRE'] = self.__b_list_NDRE
            pcd_frame['r_SAVI'] = self.__r_list_SAVI
            pcd_frame['g_SAVI'] = self.__g_list_SAVI
            pcd_frame['b_SAVI'] = self.__b_list_SAVI
            pcd_frame['r_MSAVI'] = self.__r_list_MSAVI
            pcd_frame['g_MSAVI'] = self.__g_list_MSAVI
            pcd_frame['b_MSAVI'] = self.__b_list_MSAVI
            pcd_frame['r_DVI'] = self.__r_list_DVI
            pcd_frame['g_DVI'] = self.__g_list_DVI
            pcd_frame['b_DVI'] = self.__b_list_DVI
            pcd_frame = pcd_frame.drop(columns=['index'])
            # cv2.imshow('NDVI', self.__img_fusion_NDVI_copy)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


            # o3d.visualization.draw_geometries(
            #     [get_o3d_pcd_rgb(pcd_frame)])
            # print(path_image)
            # cv2.imshow('rgb', self.__img_fusion_copy)
            # if cv2.waitKey(0) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            
            
            return pcd_frame
        else:
            raise Exception(NameError(
                'Set the fusion model first with set_fusion_model(self, path_to_3d_2d_keypoints, method)'))
    
    def get_list_pcds(self):
        return self.__list_pcds

    def filter_and_promediate_pcd(self, pcd):
        pcd = pcd.groupby(['azimuth', 'laser_id']).mean()
        pcd = pcd.reset_index()
        
        xyz = np.zeros((len(pcd['X']), 3))
        xyz[:, 0] = pcd['X']
        xyz[:, 1] = pcd['Y']
        xyz[:, 2] = pcd['Z']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        # o3d_pcd.paint_uniform_color([0.1, 0.706, 0.1])
        cl, ind = o3d_pcd.remove_statistical_outlier(
            nb_neighbors=self.__nb_neighbors, std_ratio=self.__std_ratio)
        xyz = np.asarray(cl.points)
        # print(xyz.shape)
        pcd_dict = {'X':xyz[:, 0], 'Y':xyz[:, 1], 'Z': xyz[:, 2]}
        pcd2 = pcd.loc[ind]
        pcd = pd.DataFrame(pcd_dict)
        return pcd2

    def set_outlier_filter_parameters(self, nb_neighbors, std_ratio):
        self.__nb_neighbors = nb_neighbors
        self.__std_ratio = std_ratio

    def get_pcd_model(self):
        return self.__pcd

    def get_o3d_pcd(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        return o3d_pcd

    def get_o3d_pcd_rgb(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['r']
        xyz_colors[:, 1] = self.__pcd['g']
        xyz_colors[:, 2] = self.__pcd['b']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd

    def get_o3d_pcd_NDVI(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['r_NDVI']
        xyz_colors[:, 1] = self.__pcd['g_NDVI']
        xyz_colors[:, 2] = self.__pcd['b_NDVI']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd

    def get_o3d_pcd_NDRE(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['r_NDRE']
        xyz_colors[:, 1] = self.__pcd['g_NDRE']
        xyz_colors[:, 2] = self.__pcd['b_NDRE']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd
    
    def calibrate_xy_plane(self, pcd):
        if self.__rotation_plane_mtx is False:
            return pcd
        
        pcd[['X', 'Y', 'Z']] = self.__rotation_plane_mtx.dot(pcd[['X', 'Y', 'Z']].T).T
        return pcd
       
    def rotate_pcd(self, pcd, rot_grade):
        RD = math.radians(rot_grade)
        RMATRIX = np.matrix([[math.cos(RD), -math.sin(RD), 0],
                         [math.sin(RD), math.cos(RD), 0],
                         [0, 0, 1]])
        # pcd[['X', 'Y', 'Z']] = RMATRIX.dot(pcd[['X', 'Y', 'Z']].T).T
        pcd['X'] += self.__x_center
        pcd['Y'] += self.__y_center
        pcd[['X', 'Y', 'Z']] = RMATRIX.dot(pcd[['X', 'Y', 'Z']].T).T
        return pcd

    def add_pcd(self, new_pcd, rot_grade, path_rgb_fusion_img=None):
        pcd = self.filter_and_promediate_pcd(new_pcd)
        
        if path_rgb_fusion_img is not None:
            pcd = self.fusion_3d_2d(path_rgb_fusion_img, pcd)
        
        pcd = self.calibrate_xy_plane(pcd)
        pcd = self.rotate_pcd(pcd, rot_grade)

        xyz = np.zeros((len(pcd['X']), 3))
        xyz_colors = np.zeros((len(pcd['X']), 3))
        xyz[:, 0] = pcd['X']
        xyz[:, 1] = pcd['Y']
        xyz[:, 2] = pcd['Z']
        xyz_colors[:, 0] = pcd['r']
        xyz_colors[:, 1] = pcd['g']
        xyz_colors[:, 2] = pcd['b']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        pcd_down = o3d_pcd
        # pcd_down = o3d_pcd.voxel_down_sample(voxel_size=0.001)
        # o3d.geometry.PointCloud.estimate_normals(
        #     pcd_down,
        #     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1,
        #                                                       max_nn=30))

        self.__list_pcds.append(pcd_down)


        self.__pcd = pd.concat([self.__pcd, pcd])

    def intensity_color(self, pcd):

        i_rgb = self.mapper.to_rgba(pcd['intensity'])
        pcd['intensity_r'] = i_rgb[0]
        pcd['intensity_g'] = i_rgb[1]
        pcd['intensity_b'] = i_rgb[2]
        return pcd
    
    def intensity_color_umbral(self, pcd):
        if pcd['intensity'] <= 20:
            inte = 0
        else:
            inte = 100
        i_rgb = self.mapper.to_rgba(inte)
        pcd['intensity_umbral'] = inte
        pcd['intensity_r_umbral'] = i_rgb[0]
        pcd['intensity_g_umbral'] = i_rgb[1]
        pcd['intensity_b_umbral'] = i_rgb[2]
        return pcd

    def get_o3d_pcd_intensity_rgb(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['intensity_r']
        xyz_colors[:, 1] = self.__pcd['intensity_g']
        xyz_colors[:, 2] = self.__pcd['intensity_b']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd

    def get_o3d_pcd_intensity_rgb_umbral(self):
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['intensity_r_umbral']
        xyz_colors[:, 1] = self.__pcd['intensity_g_umbral']
        xyz_colors[:, 2] = self.__pcd['intensity_b_umbral']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd

    def get_o3d_pcd_rgb_umbral(self):
        self.__pcd = self.__pcd.apply(self.get_color_umbral, axis=1)
        xyz = np.zeros((len(self.__pcd['X']), 3))
        xyz_colors = np.zeros((len(self.__pcd['X']), 3))
        xyz[:, 0] = self.__pcd['X']
        xyz[:, 1] = self.__pcd['Y']
        xyz[:, 2] = self.__pcd['Z']
        xyz_colors[:, 0] = self.__pcd['umbral_r']
        xyz_colors[:, 1] = self.__pcd['umbral_g']
        xyz_colors[:, 2] = self.__pcd['umbral_b']

        o3d_pcd = o3d.geometry.PointCloud()
        o3d_pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d_pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        return o3d_pcd

    def get_color_umbral(self, pcd):
        val_med = [pcd['r'], pcd['g'], pcd['b']]
        val_med.sort()
        val_med = val_med[1]
        
        tresh = 0.10
        if val_med - tresh <= pcd['r'] <= val_med + tresh and \
                val_med - tresh <= pcd['g'] <= val_med + tresh and \
                val_med - tresh <= pcd['b'] <= val_med + tresh:

            if pcd['r'] <= 0.30 and\
                    pcd['g'] <= 0.30 and\
                    pcd['b'] <= 0.30:

                pcd['color_umbral'] = 0
            else:
                pcd['color_umbral'] = 100

        else:
            # print(pcd['r'], pcd['g'], pcd['b'])
            pcd['color_umbral'] = 50

        umb_rgb = self.mapper.to_rgba(pcd['color_umbral'])
        pcd['umbral_r'] = umb_rgb[0]
        pcd['umbral_g'] = umb_rgb[1]
        pcd['umbral_b'] = umb_rgb[2]

        return pcd

    def get_ndvi_mean(self):
        print(len(self.__pcd['ndvi']))
        return self.__pcd['ndvi'].mean()
