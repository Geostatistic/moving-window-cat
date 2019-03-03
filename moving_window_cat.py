import sgems
import numpy as np
import math
from collections import Counter

# Most comom element on a list finder
def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

#Transform i,j,k in n
def ijk_in_n(grid, i, j, k):
    dims = sgems.get_dims(grid)
    n = k*dims[0]*dims[1]+j*dims[0]+i
    return n

#Crestes a list with indices of the neighbors valid blocks
def neighb_value(grid, indice, dim_window, geomodel):

        dims_f = sgems.get_dims(grid)
        last_n = dims_f[0]*dims_f[1]*dims_f[2]
        last_ijk = sgems.get_ijk(grid, last_n-1)
        ijk = sgems.get_ijk(grid, indice)
        geo_model = sgems.get_property(grid, geomodel)

        neighborhood = []
        for i in range(ijk[0]-(dim_window[0]),ijk[0]+(dim_window[0]+1)):
            for j in range(ijk[1]-(dim_window[1]),ijk[1]+(dim_window[1]+1)):
                for k in range(ijk[2]-(dim_window[1]),ijk[2]+(dim_window[1]+1)):
                    ijk_blk = [i,j,k]
                    neighborhood.append(ijk_blk)

        #print neighborhood

        valid_neighb = []
        for i in neighborhood:
            if 0 <= i[0] <=last_ijk[0] and 0 <= i[1] <=last_ijk[1] and 0 <= i[2] <=last_ijk[2]:
                valid_neighb.append(i)

        #print valid_neighb

        neighb_n = []
        for i in valid_neighb:
            neighb_n.append(ijk_in_n(grid,i[0],i[1],i[2]))

       #print neighb_n

        cat_value = []
        for i in neighb_n:
                if not math.isnan(geo_model[i]):
                    cat_value.append(int(geo_model[i]))

        #print cat_value, type(cat_value[0])

        return Most_Common(cat_value)

# variable creation function
def create_variable(grid, name, list):
    lst_props_grid = sgems.get_property_list(grid)
    prop_final_data_name = name

    if (prop_final_data_name in lst_props_grid):
        flag = 0
        i = 1
        while (flag == 0):
            test_name = prop_final_data_name + '-' + str(i)
            if (test_name not in lst_props_grid):
                flag = 1
                prop_final_data_name = test_name
            i = i + 1

    sgems.set_property(grid, prop_final_data_name, list)

class moving_window_cat:
    def __init__(self):
        pass

    def initialize(self, params):
        self.params = params
        return True

    def execute(self):

        grid = self.params['grid']['value']
        prop = self.params['prop']['value']

        dimx = int(self.params['x_dim']['value'])
        dimy = int(self.params['y_dim']['value'])
        dimz = int(self.params['z_dim']['value'])
        dim_window = [dimx, dimy,dimz]

        geo_model = sgems.get_property(grid, prop)

        geo_model_smooth = []
        for i in xrange(len(geo_model)):
            if math.isnan(geo_model[i]):
                geo_model_smooth.append(float('nan'))
            else:
                geo_model_smooth.append(neighb_value(grid,i,[dimx,dimy,dimz],prop))

        create_variable(grid, 'Geomodel_smooth', geo_model_smooth)

        return True

    def finalize(self):
        return True

    def name(self):
        return "moving_window_cat"

################################################################################
def get_plugins():
    return ["moving_window_cat"]