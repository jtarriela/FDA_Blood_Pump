import re
import statistics
import matplotlib.pyplot as plt
import numpy as np



def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line.rstrip()))
    return list_of_results

def p_average(string_list):
    # takes list of floats in string formant -- takes average and returns float
    temp_list = []
    for index, string in enumerate(string_list):
        float_number = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", string)
        # temp_list.append(float(float_number[0]))
        if float(float_number[0]) < 305:
            temp_list.append(float(float_number[0]))
        else:
            pass
    list_mean = statistics.mean(temp_list)
    return list_mean

def parsed_list(string_list):
    temp_list = []
    for index, string in enumerate(string_list):
        float_number = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", string)
        temp_list.append(float(float_number[0]))
        # temp_list.append(float(float_number[0]))
    return temp_list


if __name__ == "__main__":
    test_list = search_string_in_file(r"C:\Users\Joseph Tarriela\Downloads\Pressure Files\Pressure-C1-SBES.trn", "static_phead_mmhg  ")
    value = p_average(test_list)
    parsed_list_1=parsed_list(test_list)

    for i in range(len(parsed_list_1)):
        parsed_list_1[i] = parsed_list_1[i]-6.5
    mean_parsed_list = np.mean(parsed_list_1)
    print("Variance: {}".format(np.var(parsed_list_1)),
          '\nMean: {}'.format(mean_parsed_list))


    x_val = range(0,len(parsed_list_1))

    fig, ax = plt.subplots()
    ax.plot(x_val, parsed_list_1, 'o-', label='Instantaneous Pressure Rise')
    y_avg = [mean_parsed_list] * len(x_val)
    ax.plot(x_val, y_avg, color='red', lw=6, ls='--', label="Average Pressure Rise")
    plt.xlabel("Data Point")
    plt.ylabel("Pressure Head (mmHg)")

    plt.legend(loc=0)
    plt.show()