from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

#
# case={'rpm': Q_(3500,'rpm'),
#       'blades': 4,
#       'timestep': Q_(1.5E-5,'sec')}


def spec_ts(case):
      rps = case['rpm'].to('rps') #revolutions per second
      sec_per_rev = 1/rps * Q_(1,'revolutions')
      sec_per_rev = sec_per_rev.to('sec')
      sec_per_blade_pass = sec_per_rev / case['blades']

      step_per_blade_pass = sec_per_blade_pass / case['timestep']

      print(f'For Specified Timestep: {case["timestep"]} \n'
            f'Seconds per revolution: {sec_per_rev} \n'
            f'Seconds per blade pass: {sec_per_blade_pass} \n'
            f'Time steps per blade pass: {step_per_blade_pass} \n'
            f'Time steps per rotation: {step_per_blade_pass*4}\n\n')


def ts_given_deg(case,deg):
      rps = case['rpm'].to('rps')  # revolutions per second
      sec_per_rev = 1 / rps * Q_(1, 'revolutions')
      sec_per_rev = sec_per_rev.to('sec')
      sec_per_blade_pass = sec_per_rev / case['blades']
      step_per_blade_pass = sec_per_blade_pass / case['timestep']
      for i in enumerate(deg):
            deg = [.1, .25, .5, 1, 2.5, 5, 10]
            case['deg travel'] = Q_(i[1],'degrees')
            # print(case['deg per second'])`
            sec_per_deg = sec_per_rev / Q_(360,'degrees')
            time_to_travel_x_deg = case['deg travel'] * sec_per_deg

            print(f'Timestep for {case["deg travel"]} of travel: {round(time_to_travel_x_deg,7)} at {case["rpm"]}')


if __name__ == "__main__":
      case = {'rpm': Q_(3500, 'rpm'),
              'blades': 4,
              'timestep': Q_(1E-5, 'sec')}
      deg = [1, 2, 3]
      ts_given_deg(case,deg)

      case['rpm']=Q_(2500, 'rpm')
      case['timestep']=Q_(6.67e-05, 'sec')
      ts_given_deg(case,deg)
      spec_ts(case)

      case['rpm'] = Q_(3500, 'rpm')
      case['timestep']=Q_(4.76e-05, 'sec')

      spec_ts(case)

      # print(f'Timestep for {case["deg travel"]} of travel: {round(time_to_travel_x_deg,7)}')









