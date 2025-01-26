import os
import json
import numpy as np

from .graph_generation import EnvelopeGameNetwork, read_graph

def perform_simulation(output_dir: str, graph_dir: str, type: int=1, step: int=0):
    # Load arguments
    OUTPUT_DIR = output_dir
    GRAPH_FILE = graph_dir
    
    # Load constants
    code_dir = os.path.dirname(os.path.realpath(__file__))
    constants = json.load(open(f"{code_dir}/constants.json"))['base-constants']
    
    N = constants['N']
    T = constants['T']
    a = constants['a']
    cl = constants['cl']
    ch = constants['ch']
    b = constants['b']
    d1 = constants['d1']
    d2 = constants['d2']
    beta = constants['beta']
    mu = constants['mu']
    
    # Load graph
    G = read_graph(GRAPH_FILE)
    
    # Perform simulation
    if type == 1:
        p_options = [0.1, 0.4, 0.8]
        rez_num = 1
    
        for p in p_options:
            simulation_r = EnvelopeGameNetwork(N, G, T, p, a, cl, ch, b, d1, d2, 0, beta, mu)
            simulation_r.perform_simulation()
            
            np.save(os.path.join(OUTPUT_DIR, f"sim1_rr_looking_p{rez_num}"), simulation_r.get_f_look())
            np.save(os.path.join(OUTPUT_DIR, f"sim1_rr_exit_p{rez_num}"), simulation_r.get_f_exit())
            np.save(os.path.join(OUTPUT_DIR, f"sim1_rr_coop_p{rez_num}"), simulation_r.get_f_coop())

            rez_num += 1
            
    elif type == 2:
        total = step * step
        p_vector = np.linspace(0, 1, step)
        lmbd_vector = np.linspace(0, 1, step)
        frequencies = np.zeros((step, step))
        exits = np.zeros((step, step))
        coops = np.zeros((step, step))
        count = 0
        
        print(p_vector, lmbd_vector)
        
        for i in range(step):
            for j in range(step):
                simulation = EnvelopeGameNetwork(N, G, T, p_vector[i], a, cl, ch, b, d1, d2, lmbd_vector[j], beta, mu)
                simulation.perform_simulation()
                
                frequencies[i][j] = np.mean(simulation.get_f_look())
                exits[i][j] = np.mean(simulation.get_f_exit())
                coops[i][j] = np.mean(simulation.get_f_coop())
                
                print("Progress:", count, "out of", total)
                count += 1

        np.save(os.path.join(OUTPUT_DIR, 'sim2-frequencies'), frequencies)
        np.save(os.path.join(OUTPUT_DIR, 'sim2-exits'), exits)
        np.save(os.path.join(OUTPUT_DIR, 'sim2-coops'), coops)