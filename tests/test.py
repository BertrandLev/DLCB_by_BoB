import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # Test distribution de Flory
# k = np.arange(1,50001)
# Mw = 28

# a1 = 0.001
# f1 = 100
# wk1 = f1*np.power(a1,2)*np.multiply(k,np.power(1-a1,k-1))

# a2 = 0.005
# f2 = 25
# wk2 = f2*np.power(a2,2)*np.multiply(k,np.power(1-a2,k-1))


# fig, ax = plt.subplots()
# ax.plot(k*Mw, wk1, label='Flory_1')
# ax.plot(k*Mw, wk2, label='Flory_2')
# ax.plot(k*Mw, wk1 + wk2, 'k--', label='Sum')
# ax.legend()
# ax.set_xscale('log')
# ax.grid()
# plt.show(block = True)

# Import du fichier
file_path = 'tests\GPCIR TOTAL-23-0259.xls'
data = pd.read_excel(file_path, sheet_name='Data')

print(data.head(20))