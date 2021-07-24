# SBES Ahmed Body Test
 
ANSYS Fluent 2020R1<br>
Ahmed body test for SBES Hybrid model. <br>
Reference:<br>
https://www.researchgate.net/publication/324606594_Comparison_of_Three_Hybrid_Turbulence_Models_for_the_Flow_Around_a_Ahmed_Body <br>
https://link-springer-com.ezproxy.lib.usf.edu/content/pdf/10.1007/s00348-015-1996-5.pdf <br>
***
### Model Conditions <br>
25deg <br>
k-omega SST <br>
***
#### Body Conditions <br>
Lb = 1044mm <br>
Wb = 380mm <br>
Hb = 288mm <br>
***
#### Domain Conditions <br>
Upstream = 5*Lb <br>
Downstream = 10*Lb <br>
Height = 5*Lb <br>
Cross Section = 4.2*Lb <br>
***
#### Boundary Conditions <br>
Velocity Inlet = 40 m/s <br>
Pressure Outlet = 0 Pa Gauge <br>
No Slip on ahmed body <br>
No Slip domain L/R/T walls <br>
Slip Wall on ground:: inlet to X = Lb*3 <br>
No Slip on Ground:: after X = Lb*3<br>
***
#### Simulation Settings
Timestep dt = 5.1E-5s <br>
CFL = 1 in critical areas of flow <br>
Nondimensional Timestep dt*Vinf/Lb = 0.002 <br>
115 Convective Transit Times T*Vinf/Lb, T = 3s physical time <br>
Time averaging after 77 Transit Times

***
### Mesh 2<br>
Boundry Layer 15 cells
Expansion Rate 1.15

13.9M Cells 

2 BOI
* Wake 15mm cells<br>
* Immediate area around body 6mm 
* Face size on walls 4mm


Target y+ = 1



Spatial Resolution l0

temporal resolution
***
### Meshing Notes and Procedure Post SS<br>
Refine y+ mesh adaption to Y+ <=1 <br>
Journal code adds integral length scale, l0 to delta ratio, and timestep CFF & surface generation. <br>
* 5 cells for l0 resolves 80% of k
* 10-12 cells resolves 90% of k 
* - l0_to_delta_ratio contour plot to see
* time_scale contour plot to see smallest time scales to be used for CFL<=1. 
* - Timestep= 1E-5
***
Notes <br>
- 
- Not completely resolving mesh area around the slant edges<br>
- Temporal resolution appears to be fully resolved.<br>
- Error in Q-criterion iso surface may be due to not completely solving the flow field.<br>
**  rerunning first 20 timesteps with 5000 iterations rather than 1000 iterations.


- Scratch script parsing velocity line data
-- what is that line graph called where the scatter plots are aligned
  
- Create categorical scatter plot 
-
***
Changes <br>
- Found that previous run did not have BCD for momentum discretization
- switched to SIMPLEC && under-relaxation for pressure & mom = 0.8
- SHOULD CHANGE:: Pressure outlet to avg pressure out. did not change for this run


