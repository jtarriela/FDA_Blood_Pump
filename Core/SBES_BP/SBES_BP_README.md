# SBES Study FDA Round Robin
 
ANSYS Fluent 2020R1<br>
Files for Stress Blended Eddy Simulation. <br>
Note in residual notebook datasets:: Last 200 datapoints to be truncated

***
### FDA Conditions 1 <br>
2.5 L/min <br>
2500 RPM<br>
Density: 1056 kg/m3<br>
Viscosity: 0.0034 Pa*s<br>
Surface Roughness: 0.6um
***
### Initialization 
Newtownian Fluid<br>
Steady State<br>
K-omega SST <br>
Steady State: 3500 iterations SS <br>
Transient Simulation: 600 Timesteps 
Hemolysis Equations: 200 iterations <br>
Mesh: 24M, 48M
Moving Reference Frame <br> 
***
### Timestep Calculations
Seconds per revolution: 0.024 second <br> 
Seconds per blade pass: 0.006 second <br> 
Timestep per blade pass: 600.0 dimensionless<br> 
***
### Boundary Conditions
UDS Flux at walls = 0 <br>
UDS Flux at mesh interface = 0 <br> 
UDS Flux at outlet = 0 <br>
UDS Scalar Value at inlet = 0 <br>
***
### Surfaces
#### Quadrant 1 Line:
x0 = 0m <br>
y0 = 0m <br>
z0 = 0.006562m <br>
x1 = 0.03m <br>
y1 = -0.03m <br>
z1 = z0 = 0.006562m <br>
#### Quadrant 2 Line:
x0 = 0m <br>
y0 = 0m <br>
z0 = 0.006562m <br>
x1 = -0.03m <br>
y1 = -0.03m <br>
z1 = z0 = 0.006562m <br>
#### Blade Passsage Plane:
z = 0.006562m
#### ZX Outlet Plane:
y = -0.027805m
***
#### Steady State Observations & Conclusions:
Initial SS simulation 24M mesh:
* L0/delta ratio revealed that area trailing rotors not sufficiently resolved (L0<5) for LES switch.
* Global courant number > 1 :: Timestep = 5E-6 sec <br> <br>

Initial SS simulation 48M mesh: 
* Resolution is improved. Learnings from Ahmed body applied. Switched to URANS for further analysis of L0 ratio.  
* Global courant number > 1 :: Timestep = 3e-6E- sec
* y+<1 :: 0.9120703
#### URANS Observations & Conclusions:
Initial URANS simulation 48M mesh:
* L0/delta ratio revealed that mesh sufficiently resolved in rotor areas
#### Changes for SBES:
* Enable UDS equations
* Shear Stress eqn validation
* 
***

