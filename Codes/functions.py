from neuron import h 
from neuron.units import mV, ms
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def simulate_v_t(array, tstop):
    all_v = [None] * len(array)
    for i in range(len(array)):
        all_v[i] = h.Vector().record(array[i]._ref_v)
    t = h.Vector().record(h._ref_t)
    h.load_file("stdrun.hoc")
    h.finitialize(-70 * mV)
    h.continuerun(tstop * ms)
    labels = array
    return all_v, t, labels

def plot_vt(array,t, labels):
    plt.figure()
    for i in range(len(array)):
        plt.plot(t, array[i], label = f'{labels[i]}')
    plt.title("3 connected neurons with noise (0.4) and current (2) clamp")
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (mV)")
    plt.legend()
    plt.show()
    
def current_clamp(location, delay, dur, amp):
    stim = h.IClamp(location)
    stim.delay = delay
    stim.dur = dur
    stim.amp = amp
    return stim

def gap_between(conductance, location_a, location_b):
    ga = h.gap(location_a)
    gb = h.gap(location_b)
    ga.g = conductance # 240 nS
    gb.g = conductance
    ga._ref_vgap = location_b._ref_v
    gb._ref_vgap = location_a._ref_v
    return ga, gb

def noise_clamp(location, delay, total_dur, noise_amp):
    stims = []
    for i in range(total_dur):
        noise = np.random.normal(scale=noise_amp)
        stim = current_clamp(location, delay+i, 1, noise)
        stims.append(stim)
    return stims

def phase_histograms(array,t, labels):
    all_peaks = []
    phase_times = []
    for i in range(len(array)):
        peaks, _ = find_peaks(array[i], height = -20)
        all_peaks.append(peaks)
        phase_times.append([t[all_peaks[i][j+1]] - t[all_peaks[i][j]] for j in range(len(all_peaks[i])-1)])
    # plot histogram of phase times for each location
    plt.figure()
    for i in range(len(array)):
        plt.hist(phase_times[i], bins = 10, alpha = 0.5,  label = f'{labels[i]}')
    plt.legend()
    plt.show()

def phase_difference(array,t, labels):
    # find the peaks of the two signals
    if len(array) != 2:
        raise ValueError("Only two signals are allowed")
    v1 = array[0]
    v2 = array[1]
    t_np = np.array(t)
    # find peak and peak timings for each v1 and v2
    peaks1, _ = find_peaks(v1, height = -20)
    peaks2, _ = find_peaks(v2, height = -20)
    peaks1, peaks2 = peaks1[0:], peaks2[0:]
    time_diff_1 = np.diff(t_np[peaks1])
    time_diff_2 = np.diff(t_np[peaks2])  
    # print(np.mean(time_diff_1), np.mean(time_diff_2))
    # calculate the difference in peaks only when it's less than np.mean(time_diff_1)
    peak_time_diff = []
    for i in range(1,min(len(peaks1), len(peaks2))):
        diff = t_np[peaks2[i]] - t_np[peaks1[i]] # location 1 be the source of peak
        if 0 < diff < np.mean(time_diff_1):
            peak_time_diff.append(diff)
    peak_phase_diff = peak_time_diff/np.mean(time_diff_1)
    # print(peak_phase_diff)
    if len(peak_phase_diff) < min(len(peaks1), len(peaks2))/2:
        ValueError("Not enough peaks to calculate phase difference")
        # return 0
    return peak_phase_diff # normalized phase difference 0-1