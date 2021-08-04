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

hemolysis experiments conducted at density 1035 kgm3 <br>
PIV experiments conducted at density 1600-1750kg/m3 - newtownian blood analouge
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
#### Steady State Observations & Conclusions:
Initial SS simulation 24M mesh:
* L0/delta ratio revealed that area trailing rotors not sufficiently resolved (L0<5) for LES switch.
* Global courant number > 1 :: Timestep = 1E-5 sec <br> <br>

Initial SS simulation 48M mesh: 
* Resolution is improved. Learnings from Ahmed body applied. Switched to URANS for further analysis of L0 ratio.  
* Global courant number > 1 :: Timestep = 5e-6E sec or 
* y+<1 :: 0.9120703
#### URANS Observations & Conclusions:
Initial URANS simulation 48M mesh:
* L0/delta ratio revealed that mesh sufficiently resolved in rotor areas
#### Changes for SBES:
* Enable UDS equations
* Shear Stress eqn validation
###
| Mesh Size | Iteration/hr (72 cores) | 
| --------------:|---------------:|
| 24M | 57 |
| 38M | _ |
| 48M | 35 |

| Mesh Size | Iteration/hr (120 cores) | 
| --------------:|---------------:|
| 24M | 75 |
| 38M | _ |
| 48M | 36 |

	
| Timestep Size | Timesteps per Blade Revolution | Timestep per Rotation |e
| --------------:|---------------:|---------------:|
| 5E-5s | 300 | 1200 |
| 1E-5s | 600 | 2400 |
| 5E-6s | 1200 | 4800 |
| 1E-6s | 2200 | 9500 |

sample for 5 rev every blade pass

***
#### SBES Results 5 Rev
Avg static P at inlet (MFWA/MWA): -2.703585e+04 Pa <br>
Avg Damage index outlet MWA GW: 2.723866e-07 <br>
Avg DI outlet MWA EDS: 1.432285e-08
