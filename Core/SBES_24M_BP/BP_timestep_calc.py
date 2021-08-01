from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

case={'rpm': Q_(2500,'rpm'),
      'blades': 4,
      'timestep': Q_(5E-5,'sec')}

rps = case['rpm'].to('rps') #revolutions per second
sec_per_rev = 1/rps * Q_(1,'revolutions')
sec_per_rev = sec_per_rev.to('sec')
sec_per_blade_pass = sec_per_rev / case['blades']

step_per_blade_pass = sec_per_blade_pass / case['timestep']

print(f'For Specified Timestep: {case["timestep"]} \n'
      f'Seconds per revolution: {sec_per_rev} \n'
      f'Seconds per blade pass: {sec_per_blade_pass} \n'
      f'Time steps per blade pass: {step_per_blade_pass} \n'
      f'Time steps per rotation: {step_per_blade_pass*4}\n\n'
      f'ETA per Revolution 48M Mesh: {round(step_per_blade_pass*4/35/Q_(24,"1/day"),3)} or {round(step_per_blade_pass*4/35/Q_(1,"1/hr"),3)}\n'
      f'ETA per Revolution 24M Mesh: {round(step_per_blade_pass*4/57/Q_(24,"1/day"),3)} or {round(step_per_blade_pass*4/57/Q_(1,"1/hr"),3)}\n')

#### Temporal analysis study #####
deg = [.1, .25, .5, 1, 2.5, 5, 10]


for i in enumerate(deg):
      case['deg travel'] = Q_(i[1],'degrees')
      # print(case['deg per second'])`
      sec_per_deg = sec_per_rev / Q_(360,'degrees')
      time_to_travel_x_deg = case['deg travel'] * sec_per_deg

      print(f'Timestep for {case["deg travel"]} of travel: {round(time_to_travel_x_deg,7)}')









