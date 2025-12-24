import numpy as np
import matplotlib.pyplot as plt

directory = './comcot_run/A1'
time = (np.loadtxt(f'{directory}/time.dat'))/60
tsunami_amplitude = np.loadtxt(f'{directory}/ts_record0001.dat', usecols=0)

plt.figure(figsize=(10, 6))
plt.plot(time, tsunami_amplitude, label='DART 21413 ', color='b', linewidth=1.5)
plt.title('Tsunami Waveform Output (COMCOT)', fontsize=14, fontweight='bold')
plt.xlabel('Time (minutes)', fontsize=12) # Update unit if your data is in minutes/hours
plt.ylabel('Surface Elevation (m)', fontsize=12)
plt.xlim(120, 210)

plt.grid(True, linestyle='--', alpha=0.6)
plt.axhline(0, color='black', linewidth=0.8)
plt.legend()

plt.show()
