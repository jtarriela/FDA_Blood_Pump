import pandas as pd

def import_quad_dict():
    condition_list = ['C1','C4','C5']
    sim_type = ['KW','SBES','IDDES']
    quadrant_list = ['Q1','Q2']
    quad_temp = {}
    quad_ascii = {}
    key_list = []
    url_head = r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/case_comparison/quadrant_data/'

    for count, condition in enumerate(condition_list):
        for sim in sim_type:
            str2 = condition + '_' + sim
            key_list.append(str2)
            for quadrant in quadrant_list:

                str1 = condition + '_' + sim + '-' + quadrant

                df = pd.read_csv(url_head+str1)
                # print(df.head())
                quad_temp[quadrant] = df.sort_values(['bin_centres'])
            quad_ascii[str2] = quad_temp.copy()


    return quad_ascii

def import_diff_dict():
    condition_list_diff = ['C1','C5']
    sim_type = ['KW','SBES','IDDES']
    diff_list = ['D1','D2','D3','D4']
    diff_temp = {}
    diff_ascii = {}
    url_head_diff = r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/case_comparison/diffuser_data/'

    for count, condition in enumerate(condition_list_diff):
        for sim in sim_type:
            for diff in diff_list:

                str1 = condition + '_' + sim + '-' + diff
                # print(url_head_diff+str1)
                df = pd.read_csv(url_head_diff+str1)
                diff_temp[diff] = df.sort_values(['y-coordinate_bin_mean'])
            str2 = condition + '_' + sim
            diff_ascii[str2] = diff_temp.copy()

    return diff_ascii

def import_experimental_dict(str):
    url = r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/'
    condition = str+r'_Experimental'
    folder_1 = str+r'_sampling_coordinates/'
    folder_2 = str+r'_Experimental_Slice_Data/'


    if condition == "C1_Experimental" or condition == "C5_Experimental":
        loader_list = ['D1','D2','D3','D4','Q1','Q2']
    elif condition == "C4_Experimental":
        loader_list = ['Q1', 'Q2']

    dict = {}

    for cond in loader_list:
        full_url = url+folder_1+folder_2+str+'_'+cond+r'.csv'
        print(full_url)
        df = pd.read_csv(full_url)
        dict[cond] = df

    return dict









if __name__ == "__main__":
    # quad_ascii = import_quad_dict()
    diff_ascii = import_diff_dict()

    # condition_list_exp = ['C1', 'C4', 'C5']
    # C1_Experimental = import_experimental_dict('C1')
