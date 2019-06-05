import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-matplotlibs-3d-plot
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation

class Annotation3D(Annotation):
    '''Annotate the point xyz with text s

    code from:
    https://stackoverflow.com/questions/10374930/matplotlib-annotating-a-3d-scatter-plot
    '''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''

    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)

# https://stackoverflow.com/questions/44881885/python-draw-parallelepiped
def plot_cube(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='grey')
    faces.set_facecolor((0,0,1,0.1))
    ax.add_collection3d(faces)
    # Plot the points themselves to force the scaling of the axes
    ax.scatter(points[:,0], points[:,1], points[:,2], s=0)

    ax.quiver(0.0, 0.0, 0.0, 1,0,0, length=1.0,
        arrow_length_ratio = 0.1, linewidth=2, colors='black',normalize=False)
    ax.text(0.5,0.0,0.09, r'$a_1$', fontsize=12)
    ax.quiver(0.0, 0.0, 0.0, 0,1,0,
        arrow_length_ratio = 0.1, linewidth=2, colors='black',normalize=False)
    ax.text(0.0,0.5,0.05, r'$a_2$', fontsize=12)
    ax.quiver(0.0, 0.0, 0.0, 0,0,1,
        arrow_length_ratio = 0.1, linewidth=2, colors='black',normalize=False)
    ax.text(0.0,0.05,0.5, r'$a_3$', fontsize=12)


    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.view_init(azim=29, elev=16)

    fig.tight_layout()
    fig.set_size_inches(4,4)
    plt.show()
    fig.savefig('unit_cell.jpg',dpi=1200)




cube_definition = [
    (0,0,0), (0,1,0), (1,0,0), (0,0,1)
]
plot_cube(cube_definition)
