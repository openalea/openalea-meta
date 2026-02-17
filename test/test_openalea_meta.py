
'''
very simple test of the different pkgs just to have more than only import
'''

import numpy
import weakref # used in openalea.grapheditor test
import networkx as nx # used in openalea.grapheditor test

import openalea.plantgl.all as pgl
from openalea.mtg.io import *
from openalea.lpy import *
from openalea.core.node import *
from openalea.widgets.plantgl import PlantGL
from openalea.plantgl.scenegraph import Material # for spice test
from openalea.oapylab import tools # test scipack
from openalea.oalab.service.mimedata import encode, decode
from openalea.oalab.testing.mimedata import SampleCustomData
from openalea.grapheditor.all import  Observed
from openalea.visualea.helpwidget import *
from openalea.weberpenn.mtg_client import *
from openalea.weberpenn.tree_client import Quaking_Aspen
from openalea.rsml.continuous import discrete_to_continuous, continuous_to_discrete
from openalea.ratp.skyvault import Skyvault
from openalea.caribu.caribu import green_leaf_PAR, radiosity
from openalea.astk.sky_irradiance import clear_sky_irradiances
from openalea.adel.adel import Adel
from openalea.spice.common.convert import pgl_to_spice, spice_add_pgl
from openalea.spice.simulator import Simulator
from openalea.hydroroot.main import hydroroot
import openalea.phenomenal.calibration as phm_calib
from openalea.hydroshoot import exchange


# Test plantgl
def test_turtle_gc_gen():
    # copied from plantgl test
    p = pgl.PglTurtle()
    p.startGC()
    p.F(10)
    p.push()
    p.left(10)
    p.F(10)
    p.pop()
    p.push()
    p.right(10)
    p.pop()
    p.F(10)
    p.stopGC()
    assert len(p.getScene()) == 2

# test lpy
def test_axiom():
    l = Lsystem()
    l.setCode('''
module AA
Axiom: AA
''')
    print('Axiom:',l.axiom)
    assert (len(l.axiom) == 1)

# test mtg
def test0():
    # simple set of two successives axes
    s = '/I1<I2<I3<I4+I5<I6'
    g = multiscale_edit(s)
    assert len(g) == 7
    assert g.nb_vertices(scale=1)==6

# test core
def test_funcnode():
    """ Test Node creation"""
    inputs = (dict(name='x', interface=None, value=None), )
    outputs = (dict(name='y', interface=None), )

    def func(*input_values):
        return (input_values, )

    n = FuncNode(inputs, outputs, func)

    n.add_input(name='a', inteface=None, value=0)
    assert n.get_nb_input() == 2
    assert n.get_nb_output() == 1

    # Test IO and acess by key or index
    n.set_input(0, 1)
    n.eval()
    print((n.get_output('y')))
    assert n.get_output('y') == (1, 0)

    n.set_input('a', 'BB')
    n.eval()
    assert n.get_output(0) == (1, 'BB')

# test oawidgets
def test_scene():
    scene = pgl.Scene()
    c = pgl.NurbsCurve2D(
        [(0, 0, 1), (0.5, 1, 1), (1, 2, 1), (0.5, 3, 1), (0, 4, 1), (0, 4, 1)]
    )
    scene.add(pgl.Sphere(5))
    scene.add(c)
    scene.add(pgl.Text("test"))

    p = PlantGL(scene)
    assert p is not None

# test scipack pylab
def test_build_dict():
    d = tools.build_dict(['a'])
    assert d['a'] == 'a'
    assert 'None' not in list(d.keys())

    d = tools.build_dict(['a'], add_none=True)
    assert d['None'] == None

# test Oalab
def test_codec():
    mimetype = 'custom/data'
    initial = SampleCustomData(1, 'b')
    mimetype, raw_data = encode(initial, mimetype_in=mimetype, mimetype_out=mimetype)
    final, kwds = decode(raw_data, mimetype_in=mimetype, mimetype_out=mimetype)

    assert initial.num == final.num
    assert initial.letter == final.letter

# test grapheditor
class NxObservedVertex(Observed):

    def __init__(self, graph, identifier):
        Observed.__init__(self)
        self.identifier = identifier
        self.g = weakref.ref(graph)

    def notify_position(self, pos):
        self.notify_listeners(("metadata_changed", "position", pos))

    def notify_update(self, **kwargs):
        for k, v in kwargs.items():
            self.notify_listeners(("metadata_changed", k, v))

        pos = self.g().nodes[self]["position"]
        self.notify_position(pos)

    def __setitem__(self, key, value):
        self.g().nodes[self][key] = value
        self.notify_update()

    def __getitem__(self, key):
        return self.g().nodes[self][key]

def test_grapheditor():
    vtx = NxObservedVertex(nx.Graph(), 0)

# test visualea
text1 = "This is a simple docstring"
def test_rst2alea():
    res = rst2alea(text1)

# test weberpenn
def default_mtg():
    g = MTG()
    root = g.add_component(g.root)

    axis0 = [0, 0, 2, 0, 1, 0, 1, 0]
    axis1 = [1, 0, 2, 0]
    axis2 = [0, 0]

    def add_axis(vid, axis):
        stack = []
        for nb_ramif in axis:
            for i in range(nb_ramif):
                v = g.add_child(vid, edge_type='+')
                stack.append(v)
            vid = g.add_child(vid, edge_type='<')
        return stack

    order1 = add_axis(root, axis0)
    order2 = []
    for vid in order1:
        order2.extend(add_axis(vid, axis1))
    for vid in order2:
        add_axis(vid, axis2)

    fat_mtg(g)

    return g

def test2():
    g = default_mtg()
    param = Quaking_Aspen()
    wp = Weber_MTG(param, g)
    wp.run()
    assert wp

# test rsml
def simple_tree():
    """ create a simple tree """
    from openalea.mtg import MTG
    g = MTG()
    p = g.add_component(g.root, edge_type='/')  # plant

    # primary axe
    a1 = g.add_component(p, edge_type='/')  # the axe
    s11 = g.add_component(a1, position=(1, 1, 0), edge_type='/')  # segment 1
    s12 = g.add_child(s11, position=(1, 2, 0), edge_type='<')  # segment 2
    s13 = g.add_child(s12, position=(1, 3, 0), edge_type='<')  # segment 3
    s14 = g.add_child(s13, position=(1, 4, 0), edge_type='<')  # segment 4

    # 1st lateral axe
    a2 = g.add_child(a1, edge_type='/')  # the axe
    s21 = g.add_component(a2, position=(0, 2, 0), edge_type='/')  # segment 1
    s21 = g.add_child(s12, s21, edge_type='+')  # attach on parent segment
    s22 = g.add_child(s21, position=(0, 3, 0), edge_type='<')  # segment 2

    # 2nd lateral axe
    a3 = g.add_child(a1, edge_type='/')  # the axe
    s31 = g.add_component(a3, position=(2, 3, 0), edge_type='/')  # segment 1
    s31 = g.add_child(s13, s31, edge_type='+')  # attach on parent segment

    return g

def test_discrete_to_continuous():

    def test_tree(g0):
        gc = discrete_to_continuous(g0.copy())
        gd = continuous_to_discrete(gc.copy())

        assert len(g0.vertices(scale=3)) == len(gd.vertices(scale=3)), 'not the same number of segment'

    test_tree(simple_tree())  # test simple tree

# test openalea.ratp
def test_initialise():
    sky = Skyvault.initialise()
    assert sky.ndir == 46
    expected_hmoy = numpy.array([0.16109389, 0.16109389, 0.16109389, 0.16109389, 0.16109389,
                                 0.16109389, 0.16109389, 0.16109389, 0.16109389, 0.16109389,
                                 0.1886701, 0.1886701, 0.1886701, 0.1886701, 0.1886701,
                                 0.46373397, 0.46373397, 0.46373397, 0.46373397, 0.46373397,
                                 0.54244834, 0.54244834, 0.54244834, 0.54244834, 0.54244834,
                                 0.54244834, 0.54244834, 0.54244834, 0.54244834, 0.54244834,
                                 0.82746059, 0.82746059, 0.82746059, 0.82746059, 0.82746059,
                                 0.91839224, 0.91839224, 0.91839224, 0.91839224, 0.91839224,
                                 1.20706975, 1.20706975, 1.20706975, 1.20706975, 1.20706975,
                                 1.57079637])

    numpy.testing.assert_allclose(sky.hmoy, expected_hmoy, atol=1e-4)
    sky = Skyvault.initialise(hmoy=90, azmoy=0, omega=2 * numpy.pi, pc=1)
    assert sky.ndir == 1
    numpy.testing.assert_allclose(sky.hmoy, numpy.radians(90))

# test caribu
def test_default_light_in_radiosity():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    pts2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # default light
    res = radiosity(triangles, mats)

    assert 'area' in res

# test astk
def test_clear_sky_irradiances():
    df = clear_sky_irradiances()
    assert len(df) == 15
    df2 = clear_sky_irradiances(with_pvlib=False)
    assert len(df2) == 15
    numpy.testing.assert_allclose(df.ghi, df2.ghi, atol=55)

# test adel
def test_instantiate():
    adel = Adel()
    assert len(adel.leaves[0].xydb) == 6
    assert adel.stand.plant_density == 250
    assert adel.convUnit == 0.01
    assert adel.nplants == 1
    assert adel.domain_area == 1.0 / adel.stand.plant_density
    assert adel.positions[0] == (0, 0, 0)

# test spice
def test_plantgl_to_spice():
    sim = Simulator()
    assert sim.scene.nVertices() == 0
    pgl_sc = pgl.Scene([pgl.Shape(pgl.Sphere(5), Material(transparency=0.6)), pgl.Text("test")])
    pgl_to_spice(pgl_sc, sim)
    assert sim.scene.nVertices() > 0

    # With Adding sensors
    pgl_sc = pgl.Scene([pgl.Shape(pgl.Sphere(5), Material(transparency=0.6)), pgl.Text("test")])
    pgl_to_spice(pgl_sc, sim, sensors=True, setup=True)
    assert sim.scene.nVertices() > 0

    # Test adding PGL scene directly
    spice_add_pgl(sim, pgl_sc)
    assert sim.scene.nVertices() > 0

    spice_add_pgl(sim, pgl_sc, sensors=True, setup=True)
    assert sim.scene.nVertices() > 0

# test hydroroot
def data():
    length = [0., 0.03, 0.05, 0.16], [0., 0., 0.01, 0.13]
    axial = ([0., 0.03, 0.06, 0.09, 0.12, 0.15, 0.18],
        [2.9e-4, 34.8e-4, 147.4e-4, 200.3e-4, 292.6e-4, 262.5e-4, 511.1e-4])
    radial = ([0., 0.015, 0.03, 0.045, 0.06, 0.075, 0.09, 0.105, 0.135, 0.15, 0.16],
        [300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300])

    return length, axial, radial

def test_flux1():
    length, axial, radial = data()
    g, surface, volume, Keq, Jv_global = hydroroot(primary_length=0.09,
                                               order_decrease_factor=0.7,
                                               length_data=length,
                                               axial_conductivity_data=axial,
                                               radial_conductivity_data=radial,
                                               seed=2)

# test phenomenal
lemnatec2 = {
    "angle_factor": 1.000196048985029,
    "cameras_parameters": {
        "side": {
            "_focal_length_x": 4673.858469128553,
            "_focal_length_y": 4671.176406737264,
            "_height_image": 2454,
            "_pos_x": 7.416535279860737,
            "_pos_y": -5446.349857591031,
            "_pos_z": 0.0,
            "_rot_x": -1.563436412611411,
            "_rot_y": -0.0034441048748163894,
            "_rot_z": -0.0013892635134205022,
            "_width_image": 2056
        },
        "top": {
            "_focal_length_x": 3786.9976615441783,
            "_focal_length_y": 3774.298507266704,
            "_height_image": 2056,
            "_pos_x": 13.351850903226996,
            "_pos_y": 2.2518764959739954,
            "_pos_z": 2661.0739077404382,
            "_rot_x": 3.140604378068007,
            "_rot_y": 0.0013393974482163173,
            "_rot_z": 0.003890406092895482,
            "_width_image": 2454
        }
    },
    "clockwise": True,
    "reference_camera": "side",
    "targets_parameters": {
        "target_1": {
            "_pos_x": 173.8113353568984,
            "_pos_y": -117.1160724826211,
            "_pos_z": 289.41396894009847,
            "_rot_x": 1.322954720666246,
            "_rot_y": 0.03259785478254251,
            "_rot_z": 0.8717478672441068
        },
        "target_2": {
            "_pos_x": -158.92264324949636,
            "_pos_y": 142.91039605963402,
            "_pos_z": 263.4924154812679,
            "_rot_x": 1.2812023189269341,
            "_rot_y": -0.045830612887471034,
            "_rot_z": -2.3541476545144135
        }
    }
}

def test_find_points():

    image_points = {'side': [(478, 1969), (1550, 1976)],
                    'top': [(473, 255), (1951, 258)]}
    # accelerate test
    guess = [(700, 700, -700), (-700, 700, -700)]
    calib = phm_calib.CalibrationSolver.from_dict(lemnatec2)
    pts = calib.find_points(image_points, guess, niter=2)
    expected = [[-710.670687,  732.762684, -936.617387],
                [694.774179,  736.698475, -945.038652]]
    numpy.testing.assert_allclose(pts, expected, rtol=1e-2)

# test hydroshoot
def test_leaf_na_is_as_expected():
    obtained_result = exchange.leaf_Na(age_gdd=1000., ppfd_10=38.64, a_n=-0.0008, b_n=3.3, a_m=6.471, b_m=56.635)
