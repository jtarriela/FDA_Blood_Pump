# SBES Study FDA Round Robin
 
ANSYS Fluent 2020R1<br>
Files for Improved Delayed Detached Eddy Simulation. <br>
Note in residual notebook datasets:: Last 200 datapoints to be truncated

***
### FDA Conditions 1 <br>
2.5 L/min <br>
2500 RPM<br>

| Density | Viscosity| Hematocrit | Total Hemoglobin Concentration | Mass Flow Rate | Turbulent Intensity |
| --------------:|---------------:|---------------:|---------------:|---------------:| ---------------:|
| 1035 kg/m3 | 0.0035 Pa*s | 36% | 11.5 g/dL| 0.0431250 kg/s | 4% |

Surface Roughness: 0.6um
***
### Initialization 
Newtownian Fluid<br>
Steady State<br>
K-omega SST <br>
Steady State: 3500 iterations SS <br>
Transient Simulation: 600 Timesteps 
Hemolysis Equations: 200 iterations <br>
Mesh: 19M
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
x1 = sqrt(1/2)*0.03^2m <br>
y1 = -sqrt(1/2)*0.03^2m <br>
z1 = z0 = 0.006562m <br>
#### Quadrant 2 Line:
x0 = 0m <br>
y0 = 0m <br>
z0 = 0.006562m <br>
x1 = -sqrt(1/2)*0.03^2m or 0.0214 or 0.021213203435596427<br>
y1 = -sqrt(1/2)*0.03^2m <br>
z1 = z0 = 0.006562m <br>

#### Diffuser 1 Line:
x0 = 0.020m <br>
y0 = -0.02581m <br>
z0 = 0.006562m <br>
x1 = 0.020m<br>
y1 = -0.02986m<br>
z1 = z0 = 0.006562m <br>

#### Diffuser 2 Line:
x0 = 0.025m <br>
y0 = -0.02476m <br>
z0 = 0.006562m <br>
x1 = 0.025m<br>
y1 = -0.03061m<br>
z1 = z0 = 0.006562m <br>

#### Diffuser 3 Line:
x0 = 0.03m <br>
y0 = -0.02401m <br>
z0 = 0.006562m <br>
x1 = 0.03m<br>
y1 = -0.03151m<br>
z1 = z0 = 0.006562m <br>

#### Diffuser 4 Line:
x0 = 0.035m <br>
y0 = -0.02296m <br>
z0 = 0.006562m <br>
x1 = 0.035m
y1 = -0.03241m
z1 = z0 = 0.006562m <br>


#### Blade Passsage Plane:
z = 0.006562m
#### ZX Outlet Plane:
y = -0.027805m
***