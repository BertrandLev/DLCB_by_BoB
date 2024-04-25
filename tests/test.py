from app.utils.Flory_fit import fit_N_Flory, plot_N_Flory
from app.utils.GPC_data import GPC
import numpy as np
import pandas as pd
import subprocess
import os

# pyinstaller --onefile mon_scripts.py 

# Import du fichier
# file_path = 'tests\GPCIR TOTAL-23-0259.xls'
# file_path = 'tests\GPCIR TOTAL-23-0263.xls'
# file_path = 'tests\GPCIR TOTAL-23-0267.xls'
# data = GPC()
# data.import_file(file_path)

# print(data)

# Lancement du fitting et affichage des résultats
# for N in [1,2,3,4,5,6]:
#     print(f"Fitting par {N} Flory")
#     try:
#         params = fit_N_Flory(logM, w, N)
#         plot_N_Flory(logM,w,N,params)
#     except Exception as e:
#         print("Une erreur est survenue lors du fit:",e)

# Test de lancement de Bob
# Bob_folder = "app/data/"
# Bob_inputFile = "inputBob.dat"
# Bob_exe = os.path.join(Bob_folder,"bob2P5.exe")

# command = [Bob_exe,'-i', Bob_inputFile]

# subprocess.run(command, cwd = Bob_folder)

# Test deplacement de fichier

import sys
def nested_iteration(iterators_list):
    # Base case: if there are no more iterators, yield an empty tuple
    if not iterators_list:
        yield ()
    else:
        # Get the first iterator in the list
        current_iterator = iterators_list[0]
        
        # Recursively iterate over the remaining iterators
        for nested_result in nested_iteration(iterators_list[1:]):
            # Iterate over the elements of the current iterator
            for item in current_iterator:
                # Yield the combination of the current element and the nested result
                yield (item,) + nested_result

# Suppose you have a list of iterators
iterators = [iter(range(3)), iter(range(3, 6))]
# Use recursion to perform nested iteration
for result in nested_iteration(iterators):
    print(result)