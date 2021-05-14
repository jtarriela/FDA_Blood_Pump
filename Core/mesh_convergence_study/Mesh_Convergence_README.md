# Mesh Convergence Study FDA Round Robin
 
ANSYS Fluent 2020R1<br>
Files for mesh convergence study. <br>
Note in residual notebook datasets:: Last 200 datapoints to be truncated

***
### FDA Conditions 1 <br>
2.5 L/min <br>
2500 RPM<br>
Density: 1056 kg/m3<br>
Viscosity: 0.0034 Pa*s<br>
Surface Roughness: 0.6um
***
### General Settings 
Newtownian Fluid<br>
Steady State<br>
K-omega SST <br>
Flow Equations: 5000 iterations <br>
Hemolysis Equations: 200 iterations <br>
Mesh: 8,148,886, 10,972,801, 13,710,866  cells <br>
Moving Reference Frame <br> 
***
### Boundary Conditions
UDS Flux at walls = 0 <br>
UDS Flux at mesh interface = 0 <br> 
UDS Flux at outlet = 0 <br>
UDS Scalar Value at inlet = 0 <br>
***
##### Velocity Inlet Fluent Equation (Conditions_1.xlsx):<br>
Turbulent Intensity: 4% <br>
Hydraulic Diameter: 0.012 <br> <br>
Profile: <br>
780264109329.81[m^-4 s^-1]*(sqrt(Position.y**2+(Position.z-0.294[m])**2))**5-11253314468.816[m^-3 s^-1]*(sqrt(Position.y**2+(Position.z-0.294[m])**2))**4+51995094.410294[m^-2 s^-1]*(sqrt(Position.y**2+(Position.z-0.294[m])**2))**3-100228.08532706[m^-1 s^-1]*(sqrt(Position.y**2+(Position.z-0.294[m])**2))**2+64.857019836389[s^-1]*(sqrt(Position.y**2+(Position.z-0.294[m])**2))+0.54721263111368[m s^-1]) <br>
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
The medium appears to converge more tightly and oscillate at a greater frequency than the coarse and fine meshes with respect to pressure and mass flux. <br>
* Simple moving average would be useful in averaging out oscillations for residual and quantity monitors. 
  A sliding window would be useful in cutting off iteration points of no interest. 
  Currently thinking that iterations 1000-5000 are appropriate for analysis.
* Oscillations would be reduced by manually controlling relaxation factors.

Velocity slice data needs to be compared with respect to experimental data to make better conclusions on the accuracy of simulations.<br>
Currently the study is inconclusive as the residual monitors must be averaged out, velocity data must be compared with simulations.
