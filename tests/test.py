import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize, curve_fit

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
df_file = pd.read_excel(file_path, sheet_name='Data')
df_data = df_file[['LogM conventional ','Weight fraction / LogM ']]
df_data = df_data.rename(columns={'LogM conventional ':'LogM','Weight fraction / LogM ':'w'})
df_data = df_data.dropna()
df_data = df_data[df_data['LogM'] > 3]
df_data['M'] = np.power(10,df_data['LogM'].values)

# Range de masse molaire
Mpe = 28.0
kmin = int(np.divide(1000,Mpe))
kmax = int(np.divide(np.max(df_data['M'].values),Mpe))
k = np.logspace(np.log10(kmin),np.log10(kmax+1),5000)

# Interpolation
M = k*Mpe
w = np.interp(M, df_data['M'].values[::-1], df_data['w'].values[::-1], )

# Creation 
def Flory_2(k,f1,a1,f2,a2):
    return f1*np.power(a1,2)*np.multiply(k, np.power(1-a1,k-1)) + f2*np.power(a2,2)*np.multiply(k, np.power(1-a2,k-1))

def obj_funct(x,k):
    return np.sum(np.power(w-Flory_2(x,k),2))

# result = minimize(obj_funct, [4000,0.0003,4000,0.0005], args=(k,))
# print(result)
p0 = [4000,0.0003,4000,0.0005]
[f1,a1,f2,a2], res_cov = curve_fit(Flory_2, k, w, p0 = p0)
print([f1,a1,f2,a2])

# Distributions de Flory
# a1 = 0.0003
# f1 = 4000
wk1 = f1*np.power(a1,2)*np.multiply(k,np.power(1-a1,k-1))

# a2 = 0.0005
# f2 = 4000
wk2 = f2*np.power(a2,2)*np.multiply(k,np.power(1-a2,k-1))

wktot = wk1 + wk2

# Plot
fig, ax = plt.subplots()
ax.plot(M, wk1, 'r', label='Flory_1')
ax.plot(M, wk2, 'b', label='Flory_2')
ax.plot(M, wktot, 'k-', label='Sum')
ax.plot(M, w, '--', label='MMD')
ax.set_xscale('log')
ax.grid()
ax.legend()
plt.show(block = True)