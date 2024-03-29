# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit

# # Creation des fonctions Flory
# def Flory(logM,tau):
#     M = np.power(10,logM)
#     return 2.3026*tau**2*np.multiply(np.power(M,2),np.exp(-M*tau))

# def Flory_multi(logM, *args):
#     if len(args) < 1:
#         raise ValueError("Number of parameter must be at least 1")    
#     elif len(args)%2 == 0:
#         raise ValueError("number of parameter should not be a factor of 2")
#     nb_Flory = len(args) // 2 + 1
#     if nb_Flory == 1:
#         return Flory(logM,args[0])
#     else :
#         Flory_sum = (1-np.sum([args[k] for k in range(0,nb_Flory-1)]))*Flory(logM,args[-1])
#         for i in range(0,nb_Flory-1):
#             Flory_sum += args[i]*Flory(logM,args[nb_Flory-1+i])
#         return Flory_sum

# def fit_N_Flory(logM,w,nb_Flory) -> tuple:
#     mz = np.ones(nb_Flory-1)*1/nb_Flory
#     tau = np.linspace(0.0003, 0.0005, nb_Flory)
#     p0 = list(mz) + list(tau)
#     bounds = (0,1)
#     params, pcov = curve_fit(Flory_multi, logM, w, p0 = p0, bounds=bounds)
#     return params 

# def plot_N_Flory(logM,w,nb_Flory,params) -> None:
#     fig, ax = plt.subplots()
#     if nb_Flory ==1:
#         ax.plot(logM, Flory(logM,params[0]), label=f'Flory')
#         print(f"Mn = {1/params[0]:.0f}")
#     else:
#         wlogM_tot = 0
#         for i in range(0,nb_Flory-1):
#             wlogM = params[i]*Flory(logM,params[nb_Flory-1+i])
#             ax.plot(logM, wlogM, label=f'Flory_{i+1}')
#             print(f"m_{i+1} = {params[i]:.3f}\nMn_{i+1} = {1/params[nb_Flory-1+i]:.0f}")
#             wlogM_tot = np.add(wlogM_tot,wlogM)
#         wlogM = (1-np.sum([params[k] for k in range(0,nb_Flory-1)]))*Flory(logM,params[-1])
#         ax.plot(logM, wlogM, label=f'Flory_{nb_Flory}')
#         print(f"m_{nb_Flory} = {(1-np.sum([params[k] for k in range(0,nb_Flory-1)])):.3f}\nMn_{nb_Flory} = {1/params[-1]:.0f}")
#         wlogM_tot = np.add(wlogM_tot,wlogM)
#         ax.plot(logM, wlogM_tot, 'r--', label=f'Flory_cumul')
#     ax.plot(logM, w, 'k-', label='MMD')
#     ax.set_xscale('linear')
#     ax.grid()
#     ax.legend()
#     ax.set_title(f"Fitting par {nb_Flory} Flory")
#     plt.show(block = True)
import sys    
print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)

from ..app.utils.Flory_fit import fit_N_Flory, plot_N_Flory
import numpy as np
import pandas as pd

# Import du fichier
file_path = 'tests\GPCIR TOTAL-23-0267.xls'
df_file = pd.read_excel(file_path, sheet_name='Data')
df_data = df_file[['LogM conventional ','Weight fraction / LogM ']]
df_data = df_data.rename(columns={'LogM conventional ':'LogM','Weight fraction / LogM ':'w'})
df_data = df_data.dropna()
df_data = df_data[df_data['LogM'] > 2.2]
df_data['M'] = np.power(10,df_data['LogM'].values)

# Interpolation des valeurs sur 1000 points
logM = np.linspace(np.min(df_data['LogM']),np.max(df_data['LogM']),1000)
w = np.interp(logM, df_data['LogM'].values[::-1], df_data['w'].values[::-1], )

# Lancement du fitting et affichage des résultats
for N in [1,2,3,4,5,6]:
    print(f"Fitting par {N} Flory")
    try:
        params = fit_N_Flory(logM, w, N)
        plot_N_Flory(logM,w,N,params)
    except Exception as e:
        print("Une erreur est survenue lors du fit:",e)