# SBES Study FDA Round Robin
 
ANSYS Fluent 2021R1<br>
Files for Stress Blended Eddy Simulation. <br>

***
### FDA Condition 5 <br>
6.0 L/min <br>
3500 RPM<br>

| Density | Viscosity| Hematocrit | Total Hemoglobin Concentration | Mass Flow Rate | Turbulent Intensity |
| --------------:|---------------:|---------------:|---------------:|---------------:| ---------------:|
| 1035 kg/m3 | 0.0035 Pa*s | 36% | 11.5 g/dL| 0.1035 kg/s | 7% |

Surface Roughness: 0.6um
***
### Initialization 
Newtownian Fluid<br>
Steady State (MRF) <br>
K-omega SST <br>
Steady State: 3500 iterations SS <br>
Steady Hemolysis initialization <br>
Coupled scalar transient simulation <br>

***
### Timestep Calculations

Timestep:: 3/280,000s or 1.0714E-5s

| Timestep Size | Timesteps per Blade Pass | Timestep per Rotation |
| --------------:|---------------:|---------------:|
| 5E-5s | 120 | 480 |
| 2.5E-5s | 240 | 960 |
| 1.5E-6s | 400 | 1600 |
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
