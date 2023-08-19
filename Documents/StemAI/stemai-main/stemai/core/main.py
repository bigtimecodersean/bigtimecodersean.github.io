#%%
try:
    from stemai.core import *
except:
    import os
    os.chdir('../../')
    from stemai.core import *


env = Env(
    fn=lambda x, t: (t % 3 < 2)
    if (t < 200 or t > 800)
    else (t % 4 < 2 if t < 400 or t > 600 else 1)
)

T = 1000

#--------------------------
#initializing empty final json data dictionary 
d3_visualization_data_final = {
    
    "nodes": [],     
    "links": [],    
    "max_timestamps": T, 
    "msgs_from_env": [],   
    "self_msgs": [], 
    "min_efes": [],  
    "mean_efes": [],  
    "nailed_it": [], 
    "nailed_it_trailing": [], 
    "num_cells": [], 
    "self_efficacies":  {}, 
    "stemnesses": {}, 
    "stresses": {}
}  

#--------------------------

DEDIFF_FACTOR = 0.1
CERTAIN_THRESHOLD = 0.9
MIN_STRESS = 0
MAX_STRESS = 50
SELF_STRESS_INCREMENT = 2
ALL_PENPAL_STRESS_INCREMENT = 0
STRESS_RELIEF = 0.2
B_MASS = 100000  # TODO: Why does this limit how undifferentiated cells can become?


stress_update = True
mass_update = True
onehot_b = True
logging = False
visualize_d3 = True

seed_cell = ConnectedAgent(
    is_seed_cell=True,
    stem_dim=2,
    logging=False,
    initial_action=0,
    stress_increment=SELF_STRESS_INCREMENT,
    max_stress=MAX_STRESS,
    penpal_stress_increment=ALL_PENPAL_STRESS_INCREMENT,
    stress_relief=STRESS_RELIEF,
    min_stress=MIN_STRESS,
)


all_agents = [seed_cell]
#%%

stem_data, _, d3_visualization_data_final = run_active_inference_loop(all_agents, env, T, d3_visualization_data_final)
#%%
stem_data.plot_msgs_from_env()

stem_data.plot_nailed_it(T)

stem_data.plot_stress()

stem_data.plot_stemness()

stem_data.plot_num_cells()

stem_data.plot_efes()

# %%

#----------Formatting Data for d3 Visualization------------------       

d3_visualization_data_final = stem_data.add_to_d3_visualization_final(d3_visualization_data_final, stem_data.msgs_from_env, stem_data.self_msgs, stem_data.nailed_it, stem_data.nailed_it_trailing, stem_data.num_cells, stem_data.min_efes, stem_data.mean_efes, stem_data.self_efficacies, stem_data.stemnesses, stem_data.stresses )
# print(f'/n visualization_data_final POST: {d3_visualization_data_final}')

# ------converting d3 dictionary data into JSON --------------------------    
import json 
d3_visualization_data_final_JSON = json.dumps(d3_visualization_data_final)

if visualize_d3:
    #----------Saving D3 Final JSON in d3_visualization------------
    stem_data.export_JSON_data(d3_visualization_data_final)
    #----------Running d3_visualization code-------
    stem_data.visualize_d3() 
#---------------------------------------------------


