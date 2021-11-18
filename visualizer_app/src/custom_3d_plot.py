import open3d as o3d
import numpy  as np
from functools import partial

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)
print(o3d.utility.get_verbosity_level)

def custom_draw_geometry(pcd, pcd_frame):
    def background_c(vis):
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        return False

    xyz_colors = np.zeros((len(pcd_frame['X']), 3))

    def rotate_view(vis):
        ctr = vis.get_view_control()
        ctr.rotate(10.0, 0.0)
        return False
    # o3d.visualization.draw_geometries_with_animation_callback([pcd],
    #                                                           rotate_view)

    def rgb(vis):
        xyz_colors[:, 0] = pcd_frame['r']
        xyz_colors[:, 1] = pcd_frame['g']
        xyz_colors[:, 2] = pcd_frame['b']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('rgb')
        return True

    def ndvi(vis):
        # background_c(vis)
        xyz_colors[:, 0] = pcd_frame['r_NDVI']
        xyz_colors[:, 1] = pcd_frame['g_NDVI']
        xyz_colors[:, 2] = pcd_frame['b_NDVI']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('ndvi')
        return True

    def ndre(vis):
        xyz_colors[:, 0] = pcd_frame['r_NDRE']
        xyz_colors[:, 1] = pcd_frame['g_NDRE']
        xyz_colors[:, 2] = pcd_frame['b_NDRE']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('ndre')
        return True

    def savi(vis):
        xyz_colors[:, 0] = pcd_frame['r_SAVI']
        xyz_colors[:, 1] = pcd_frame['g_SAVI']
        xyz_colors[:, 2] = pcd_frame['b_SAVI']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('savi')
        return True

    def msavi(vis):
        xyz_colors[:, 0] = pcd_frame['r_MSAVI']
        xyz_colors[:, 1] = pcd_frame['g_MSAVI']
        xyz_colors[:, 2] = pcd_frame['b_MSAVI']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('msavi')
        return True

    def dvi(vis):
        xyz_colors[:, 0] = pcd_frame['r_DVI']
        xyz_colors[:, 1] = pcd_frame['g_DVI']
        xyz_colors[:, 2] = pcd_frame['b_DVI']
        pcd.colors = o3d.utility.Vector3dVector(xyz_colors)
        print('dvi')
        return True

    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    vis.get_render_option().background_color = np.asarray([0, 0, 0])
    vis.get_render_option().mesh_show_back_face = True

    vis.add_geometry(pcd)
    vis.register_key_callback(ord("P"), partial(rgb))
    vis.register_key_callback(ord("O"), partial(dvi))
    vis.register_key_callback(ord("I"), partial(ndvi))
    vis.register_key_callback(ord("U"), partial(ndre))
    vis.register_key_callback(ord("Y"), partial(savi))
    vis.register_key_callback(ord("T"), partial(msavi))
    
    # vis.get_view_control().set_front()
    vis.run()
    vis.destroy_window()
