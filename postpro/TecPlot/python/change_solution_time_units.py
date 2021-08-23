import datetime
import tecplot as tp
tp.session.connect()
with tp.session.suspend():
    for z in tp.active_frame().dataset.zones():
        if z.strand > 0:
            solution_time = z.solution_time

            #
            # Modify the units here
            # example: seconds to hours
            #
            solution_time /= 3600
            
            # Two methods can be used:
            #   Add Zone Auxiliary Data with the new values. This doesn't modify the original data and
            #   has more flexibility since you can use string values. For example you want to format
            #   the string to represent hh:mm:ss format
            z.aux_data["SolutionTime"] = str(datetime.timedelta(hours=solution_time))
            
            #  Or you can modify the value in place. This is limited to numeric values
            z.solution_time = solution_time
    #
    # If you added Zone Auxiliary Data, this will display the text (assuming FieldMap #1 has transient data)
    #
    tp.active_frame().add_text("&(AUXZONE[ACTIVEOFFSET=1]:SolutionTime)", position=(50,50))

