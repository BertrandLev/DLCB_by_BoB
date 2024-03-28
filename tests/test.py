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
df_data = df_data[df_data['LogM'] > 2.69897]
df_data['M'] = np.power(10,df_data['LogM'].values)

# Range de masse molaire
Mpe = 28.0
kmin = int(np.divide(500,Mpe))
kmax = int(np.divide(np.max(df_data['M'].values),Mpe))
k = np.logspace(np.log10(kmin),np.log10(kmax+1),5000)

# Interpolation
M = k*Mpe
w = np.interp(M, df_data['M'].values[::-1], df_data['w'].values[::-1], )

# Creation 
def Flory(k,f,a):
    return f*a**2*np.multiply(np.power(k,2),np.exp(-k*a))

def Flory3(k,f1,f2,f3,a1,a2,a3):
    return f1*np.power(a1,2)*np.multiply(k, np.power(1-a1,k-1)) + f2*np.power(a2,2)*np.multiply(k, np.power(1-a2,k-1)) + f3*np.power(a3,2)*np.multiply(k, np.power(1-a3,k-1))

def Flory_multi(k, *args):
    if len(args) < 2:
        raise ValueError("Number of parameter must be at least 2")    
    elif len(args)%2:
        raise ValueError("number of parameter should be a factor of 2")
    nb_Flory = len(args) // 2
    Flory_sum = Flory(k,1,args[1])
    if nb_Flory > 1:
        for i in range(1,nb_Flory):
            Flory_sum += Flory(k,args[2*i],args[2*i+1])
    print(args[0])
    print(args[1])
    
    return args[0]*Flory_sum

# p0 = [1, 0.0006] #, 1, 0.0004]
# bounds = (0,[np.inf, 1]) #, 10, 1])
# [l, a1], pcov = curve_fit(Flory_multi, k, w, p0 = p0, bounds=bounds)
# print(np.linalg.cond(pcov))
# wk1 = 1*np.power(a1,2)*np.multiply(k,np.power(1-a1,k-1))
# # wk2 = f2*np.power(a2,2)*np.multiply(k,np.power(1-a2,k-1))
# # wk3 = f3*np.power(a3,2)*np.multiply(k,np.power(1-a3,k-1))
# wktot = l*(wk1)
# # Plot
# fig, ax = plt.subplots()
# ax.plot(M, wk1, 'r', label='Flory_1')
# # ax.plot(M, wk2, 'b', label='Flory_2')
# # ax.plot(M, wk3, 'g', label='Flory_3')
# ax.plot(M, wktot, 'k-', label='Sum')
# ax.plot(M, w, '--', label='MMD')
# ax.set_xscale('log')
# ax.grid()
# ax.legend()
# plt.show(block = True)

# p0 = [1000, 1000, 1000, 0.0002, 0.0004, 0.0006]
# bounds = (0,[np.inf,np.inf,np.inf,1,1,1])
# [f1,f2,f3,a1,a2,a3], res_cov = curve_fit(Flory3, k, w, p0 = p0, bounds=bounds)
# print([f1,Mpe/a1,f2,Mpe/a2,f3,Mpe/a3])
# # Distributions de Flory
# wk1 = f1*np.power(a1,2)*np.multiply(k,np.power(1-a1,k-1))
# wk2 = f2*np.power(a2,2)*np.multiply(k,np.power(1-a2,k-1))
# wk3 = f3*np.power(a3,2)*np.multiply(k,np.power(1-a3,k-1))
# wktot = (wk1 + wk2 + wk3)
# Plot
# fig, ax = plt.subplots()
# ax.plot(M, wk1, 'r', label='Flory_1')
# ax.plot(M, wk2, 'b', label='Flory_2')
# ax.plot(M, wk3, 'g', label='Flory_3')
# ax.plot(M, wktot, 'k-', label='Sum')
# ax.plot(M, w, '--', label='MMD')
# ax.set_xscale('log')
# ax.grid()
# ax.legend()
# plt.show(block = True)

p0 = [1000,0.0004]
bounds = (0,[np.inf,1])
[f,a], pcov = curve_fit(Flory, np.log(k), w, p0 = p0, bounds=bounds)
wk = Flory(k,f,a)
print(np.linalg.cond(pcov))
# Plot
fig, ax = plt.subplots()
ax.plot(M, wk, 'r', label='Flory')
ax.plot(M, w, '--', label='MMD')
ax.set_xscale('log')
ax.grid()
ax.legend()
plt.show(block = True)

