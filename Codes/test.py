from neuron import h 
from neuron.units import mV, ms
from functions import *
import matplotlib.pyplot as plt
import numpy as np
from numpy import correlate


import math
# Code inspired by https://github.com/ModelDBRepository/114047 
h.load_file("stdrun.hoc")
if h.load_file("Grant Proposal\Codes/cella.hoc") and h.load_file("Grant Proposal\Codes/cellb.hoc") and h.load_file("Grant Proposal\Codes/cellc.hoc"):
    print("Morphologies loaded")
    # each neuron has 1 soma, 1a, 2a, 3a 0-8, 4a 0-9
if h.nrn_load_dll("Grant Proposal\Codes\MOD_files/nrnmech.dll"):
    print("Mod files loaded")

# ps = h.PlotShape(True)  # False tells h.PlotShape not to use NEURON's gui
# input("Press enter to proceed")
level = 1.6
for sec in h.allsec():
    # print(sec)
    sec.insert('hh')
    # sec.gnabar_hh = 0.12*level
    # sec.gkbar_hh = 0.036*level
    # pass

# h.somaa.insert('hh')
# h.somab.insert('hh')

tstop = 50
# noise_clamp in all sections
# for sec in h.allsec():
#     noise_stim = []
#     stim = noise_clamp(sec(0.5),0,tstop,0.5)
#     noise_stim.append(stim)
    
# plot_vt([h.somaa(0.5),h.somab(0.5)],100)
gap1, gap2 = gap_between(1e1, h.dend4a[8](1), h.dend4b[8](1))
# gap3, gap4 = gap_between(1e1, h.dend4b[9](1), h.dend4c[9](1))
# smallgap1, smallgap2 = gap_between(1e2, h.somaa(0.5),h.somab(0.5))
# clampa = current_clamp_advance(h.somaa(0.5),0,100,3)

# noise_amp = 0.5
# noisea = noise_clamp(h.somaa(0.5),0,tstop,noise_amp)
# noiseb = noise_clamp(h.somab(0.5),0,tstop, noise_amp)
# # clampb = current_clamp(h.somab(0.5),0,20,1)



  
# plot_vt(all_v,t,labels)
# # phase_histograms(all_v, t, labels)
# phase_diff = phase_difference(all_v, t, labels)
# print(np.median(phase_diff))
# # # plot histogram showing the mean and stdev of phase_diff
# plt.hist(phase_diff)
# plt.xlabel('Phase difference (ms)')
# plt.ylabel('Frequency')
# plt.show()
# find time duration of 2nd peak in all_v[0]

# clampa = current_clamp(h.somaa(0.5),0,tstop,2)
# all_v,t, labels = simulate_v_t([h.somaa(0.5)],tstop)  
# plt.figure()
# plt.plot(t,all_v[0])
# peaks, _ = find_peaks(all_v[0], height = -20)
# arrays = []
# for i in range(-2,5):
#     time_delay = t[peaks[1]]+i
#     clampb = current_clamp(h.dend4a[8](1),time_delay,5,2)
#     clampa = current_clamp(h.somaa(0.5),0,tstop,2)
#     all_v1,t1, labels = simulate_v_t([h.somaa(0.5)],tstop)
#     plt.plot(t1,all_v1[0], label = f'{i}')
# plt.legend()
# plt.show()

clampa = current_clamp(h.somaa(0.5),0,tstop,2)
all_v,t, labels = simulate_v_t([h.somaa(0.5)],tstop)  
plt.figure()
plt.plot(t,all_v[0])
peaks, _ = find_peaks(all_v[0], height = -20)
arrays = []
second_peak_times = []
third_peak_times = []
i_values = list(range(-2,10,2))
for i in i_values:
    time_delay = t[peaks[1]]+i
    clampb = current_clamp(h.dend4a[8](1),time_delay,5,2)
    clampa = current_clamp(h.somaa(0.5),0,tstop,2)
    all_v1,t1, labels = simulate_v_t([h.somaa(0.5)],tstop)
    plt.plot(t1,all_v1[0], label = f'{i}')
    peaks1, _ = find_peaks(all_v1[0], height = -20)
    if len(peaks1) >= 3:
        second_peak_times.append(t1[peaks1[1]])
        third_peak_times.append(t1[peaks1[2]])
    else:
        second_peak_times.append(None)
        third_peak_times.append(None)
plt.legend()
plt.show()
# calculate time difference between 2nd and 3rd peaks
time_diff_2nd_3rd = np.array(third_peak_times) - np.array(second_peak_times)

# calculate percentage change of other time differences
percentage_change = (time_diff_2nd_3rd - time_diff_2nd_3rd[0]) / time_diff_2nd_3rd[0] * 100

# plot percentage change against i
plt.figure()
plt.plot(i_values, percentage_change)
plt.xlabel('i')
plt.ylabel('Percentage change in time difference')
plt.show()

