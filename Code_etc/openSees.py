import streamlit as st
import numpy as np

import openseespy.opensees as ops
import opsvis
import matplotlib.pyplot as plt
import vfo.vfo as vfo

def elem_prop():
    pass

### Input Data =====================================================>
class In:
    pass
In.joist_b = 50.0;  In.joist_h = 50;  In.joist_t = 2.3;  In.Lj = 150.0
In.yoke_b = 75;  In.yoke_h = 125;  In.yoke_t = 3.2;  In.Ly = 914
In.vertical_d = 60.5;  In.vertical_t = 2.6;  In.Lv = 914
In.horizontal_d = 42.7;  In.horizontal_t = 2.2;  In.Lh = 1725
In.bracing_d = 42.7;  In.bracing_t = 2.2

In.slab_X = 8;  In.slab_Y = 12;  In.height = 9.5  # Unit : m
In.dead_load = 10;  In.design_load = 12.5;  In.hx = 0.2;  In.hy = 0.2;  In.wind = 0.3  # kN/m2
### Input Data =====================================================>

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### ';  factor = 1e3
### openseespy =====================================================>
ops.wipe()  # 초기화
ops.model('basic', '-ndm', 3, '-ndf', 6)

xea = int(np.ceil(In.slab_X*factor/In.Lv) + 1);  yea = int(np.ceil(In.slab_Y*factor/In.Ly) + 1);  zea = int(np.ceil(In.height*factor/In.Lh) + 1)
xea,yea,zea

## 노드 생성  ----------------->
P = 1e3*In.design_load*In.Ly*In.Lv/1e6 
ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)
for i in range(1, xea+1):
    for j in range(1, yea+1):        
        for k in range(1, zea+1):
            ops.node(i + (j-1)*100 + (k-1)*10000, In.Lv*(i-1), In.Ly*(j-1), In.Lh*(k-1))
            if k == 1:
                ops.fix(i + (j-1)*100 + (k-1)*10000, 1, 1, 1, 1, 1, 1)  # for k=1  ## 경계 조건  ----------------->
            if k == zea:
                nodeTag = i + (j-1)*100 + (k-1)*10000
                # ops.timeSeries('Constant', nodeTag)
                # ops.pattern('Plain', nodeTag, nodeTag)
                ops.load(nodeTag, 0,0,-P, 0,0,0)  # for k=zea  ## 수직 하중  ----------------->
                # l = ops.nodeReaction(nodeTag)  # 하중 확인 용도


# opsvis.plot_loads_2d()
# st.pyplot(plt)    

## 좌표 변환  ----------------->
gTz = 1;  gTx = 2;  gTy = 3;  gTd = 4
ops.geomTransf('Linear', gTz, 1, 0, 0)
ops.geomTransf('Linear', gTx, 0, 1, 0)
ops.geomTransf('Linear', gTy, 0, 0, 1)
ops.geomTransf('Linear', gTd, 1, 1, 0)

## 요소 물성치  ----------------->
E = 200e3;  G = E/(2*(1 + 0.3))
d = In.vertical_d;  t = In.vertical_t
A = np.pi*(d**2 - (d-2*t)**2)/4
Iy = np.pi*(d**4 - (d-2*t)**4)/64;  Iz = Iy
J = np.pi*(d**4 - (d-2*t)**4)/32

## 요소 생성  ----------------->
nele = 0
for i in range(1, xea + 1):   # 수직재 z
    for j in range(1, yea + 1):
        for k in range(1, zea):
            nele = nele + 1
            ops.element('elasticBeamColumn', nele, i + 100*(j-1) + 10000*(k-1), i + 10000 + 100*(j-1) + 10000*(k-1), A, E, G, J, Iy, Iz, gTz)  # element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag)

for i in range(1, xea):   # 수평재 x
    for j in range(1, yea + 1):
        for k in range(1, zea):
            nele = nele + 1
            ops.element('elasticBeamColumn', nele, i + 10000 + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1), A, E, G, J, Iy, Iz, gTx)
for i in range(1, xea + 1):   # 수평재 y
    for j in range(1, yea):
        for k in range(1, zea):
            nele = nele + 1
            ops.element('elasticBeamColumn', nele, i + 10000 + 100*(j-1) + 10000*(k-1), i + 10100 + 100*(j-1) + 10000*(k-1), A, E, G, J, Iy, Iz, gTy)

for i in range(1, xea, 2):   # 가새재 d
    for j in range(1, yea + 1, 2):
        for k in range(1, zea, 2):
            nele = nele + 1
            ops.element('elasticBeamColumn', nele, i + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1), A, E, G, J, Iy, Iz, gTd)

fig_wi_he = [30., 20.]
fig_wi_he

vfo.createODB(model="TwoSpan_Bridge")
vfo.plot_model(filename='vfo.png')

import sys
sys.exit()
# fmt_model = {'linewidth': 1.5, 'color': 'blue', 'marker': '.', 'markersize': 5}
# opsvis.plot_model(node_labels=0, element_labels=0, fig_wi_he = fig_wi_he, local_axes=False, fmt_model=fmt_model, offset_nd_label=True, axis_off=True)
# st.pyplot(plt)

ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGeneral')
ops.test('NormDispIncr', 1.0e-6, 6, 2)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1)
ops.analysis('Static')
ops.analyze(1)




opsvis.plot_defo()

plt.title('3d 3-element cantilever beam')
st.pyplot(plt)


sfacN, sfacV, sfacM = 5.e-5, 5.e-5, 5.e-5

opsvis.section_force_diagram_3d('N', end_max_values=False, node_supports=False, alt_model_plot=2)
plt.title('Axial force distribution')
st.pyplot(plt)

# opsvis.section_force_diagram_3d('My', sfacV)
# plt.title('Shear force distribution')
# st.pyplot(plt)

# opsvis.section_force_diagram_3d('Mz', sfacM)
# plt.title('Bending moment distribution')
# st.pyplot(plt)


# ele_shapes = {}
# for i in range(1, nele+1):
#     ele_shapes[i] = ['circ', [d]]
# # ele_shapes = {1: ['circ', [d]],
# #               2: ['rect', [d, d]],
# #               3: ['I', [d, d, d/10., d/6.]]}
# opsvis.plot_extruded_shapes_3d(ele_shapes, fig_wi_he = fig_wi_he)  # green - local x-axis, red - local z-axis, blue - local y-axis.
# st.pyplot(plt)

import sys
sys.exit()

b = 0.2
h = 0.4

A, Iz, Iy, J = 0.04, 0.0010667, 0.0002667, 0.01172

E = 25.0e6
G = 9615384.6

# Lx, Ly, Lz = 4., 3., 5.
Lx, Ly, Lz = 4., 4., 4.

ops.node(1, 0., 0., 0.)
ops.node(2, 0., 0., Lz)
ops.node(3, Lx, 0., Lz)
ops.node(4, Lx, Ly, Lz)

ops.fix(1, 1, 1, 1, 1, 1, 1)

lmass = 200.

ops.mass(2, lmass, lmass, lmass, 0.001, 0.001, 0.001)
ops.mass(3, lmass, lmass, lmass, 0.001, 0.001, 0.001)
ops.mass(4, lmass, lmass, lmass, 0.001, 0.001, 0.001)

gTTagz = 1
gTTagx = 2
gTTagy = 3
gTTagd = 4

coordTransf = 'Linear'
ops.geomTransf(coordTransf, gTTagz, -1., 1., 0.)
ops.geomTransf(coordTransf, gTTagx, 0., -1., 1.)
ops.geomTransf(coordTransf, gTTagy, 1., 0., 1.)
# ops.geomTransf(coordTransf, gTTagz, 0., -1., 0.)
# ops.geomTransf(coordTransf, gTTagx, 0., -1., 0.)
# ops.geomTransf(coordTransf, gTTagy, 1., 0., 0.)

ops.element('elasticBeamColumn', 1, 1, 2, A, E, G, J, Iy, Iz, gTTagz)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, G, J, Iy, Iz, gTTagx)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, G, J, Iy, Iz, gTTagy)

opsvis.plot_model()
st.pyplot(plt)

# fig_wi_he = 22., 14.
fig_wi_he = 30., 20.

# ele_shapes = {1: ['circ', [h]],
ele_shapes = {1: ['rect', [b, h]],
              2: ['rect', [b, h]],
              3: ['I', [b, h, b/10., h/6.]]}
opsvis.plot_extruded_shapes_3d(ele_shapes, fig_wi_he=fig_wi_he)  # green - local x-axis, red - local z-axis, blue - local y-axis.

# plt.show()
st.pyplot(plt)

Ew = {}

Px = -4.e1
Py = -2.5e1
Pz = -3.e1

ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)
ops.load(4, Px, Py, Pz, 0., 0., 0.)

ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGeneral')
ops.test('NormDispIncr', 1.0e-6, 6, 2)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1)
ops.analysis('Static')
ops.analyze(1)

opsvis.plot_model()
# st.pyplot(plt)

sfac = 2.0e0

# - 1
nep = 9
opsvis.plot_defo(sfac, nep, az_el=(-68., 39.),
               fig_wi_he=fig_wi_he, endDispFlag=0)

plt.title('3d 3-element cantilever beam')

# - 2
opsvis.plot_defo(sfac, 19, az_el=(6., 30.), fig_wi_he=fig_wi_he)

plt.title('3d 3-element cantilever beam')

# - 3
nfreq = 6
eigValues = ops.eigen(nfreq)

modeNo = 6

sfac = 2.0e1
opsvis.plot_mode_shape(modeNo, sfac, 19, az_el=(106., 46.),
                     fig_wi_he=fig_wi_he)
plt.title(f'Mode {modeNo}')

sfacN = 1.e-2
sfacVy = 5.e-2
sfacVz = 1.e-2
sfacMy = 1.e-2
sfacMz = 1.e-2
sfacT = 1.e-2

# plt.figure()
opsvis.section_force_diagram_3d('N', sfacN)
plt.title('Axial force N')

opsvis.section_force_diagram_3d('Vy', sfacVy)
plt.title('Transverse force Vy')

opsvis.section_force_diagram_3d('Vz', sfacVz)
plt.title('Transverse force Vz')

opsvis.section_force_diagram_3d('My', sfacMy)
plt.title('Bending moments My')

opsvis.section_force_diagram_3d('Mz', sfacMz)
plt.title('Bending moments Mz')

opsvis.section_force_diagram_3d('T', sfacT)
plt.title('Torsional moment T')

exit()
