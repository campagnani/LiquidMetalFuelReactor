import numpy as np
import openmc
import openmc.deplete
import matplotlib.pyplot as plt


results = openmc.deplete.Results('depletion_results.h5')


time, massaU235  = results.get_mass(mat='1', mass_units='g', nuc='U235')
time, massaU238  = results.get_mass(mat='1', mass_units='g', nuc='U238')
time, massaPu239 = results.get_mass(mat='1', mass_units='g', nuc='Pu239')
time, keff  = results.get_keff()

################################################################################################################################
# ESPECTRO DE ENERGIA

# Criando a figura e o eixo principal
fig, ax1 = plt.subplots()

#Estilo de cores
plt.style.use('seaborn-v0_8-paper')

# Escala logarítimica
#plt.xscale('log')
#plt.yscale('log')

ax1.plot(time, massaU235, color='xkcd:yellow', linestyle='-', linewidth=1,marker='^', markersize=5, label='U235')
ax1.plot(time, massaU238, color='xkcd:green', linestyle='-', linewidth=1,marker='^', markersize=5, label='U238')
ax1.plot(time, massaPu239, color='xkcd:red', linestyle='-', linewidth=1,marker='^', markersize=5, label='U235')
#ax1.plot(time, keff, color='xkcd:blue', linestyle='-', linewidth=1,marker='^', markersize=5, label='keff')

# Títulos e legenda
plt.title('Mass in fuction of time', fontsize=24)
plt.ylabel('Mass (g)', fontsize=20)
plt.xlabel('Time (s))', fontsize=20)
plt.legend(fontsize=20, loc='upper left')

# Gridlines 
plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.2, color='gray')
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.2, color='gray') # which='major'
plt.tick_params(axis='both', which='major', labelsize=16)



plt.tight_layout()
plt.show()