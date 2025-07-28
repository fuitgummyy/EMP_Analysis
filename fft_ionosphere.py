import numpy as np
import pandas as pd
import cmath
from scipy import signal

#double exponential in the time domain
t_index = []
t = 0
for i in range(2**20): 
    t += 0.001
    t_index.append(t)
t_index = np.array(t_index)

signal_t = []
alpha = 1/0.01
beta = 1/0.4
for time in t_index:
    if (((time -20) *alpha) < 256):
        signal_t.append(10**6 * (np.exp((time -20) * alpha)/ (1 + np.exp((time -20) * (alpha +beta)))))
    else:
        signal_t.append(np.exp((-beta) * (time -20)))

    
#signal_t = signal.unit_impulse((2**20), idx=20000) #<- delta function in time domain


#setup
signal_f = np.fft.fft(signal_t)
n = signal_f.size
time_interval = 0.001 #time in microseconds
signal_f_freq = np.fft.fftfreq(n, d=time_interval)
STEC = 10 #Slant TEC (total electron content) 
   

#highpass
signal_f[:7500] = 0
signal_f[-7500:] = 0
signal_f_mag= np.abs(signal_f)


no_mag_phase = []
right_circular_phase = []
left_circular_phase = []
for freq in signal_f_freq:
    if freq == 0:
        no_mag_phase.append(freq)
        right_circular_phase.append(freq)
        left_circular_phase.append(freq)
        
    else:
        no_mag_phase.append(-8445*STEC/(2*cmath.pi * freq))
        right_circular_phase.append((-8445*STEC)/((freq) *(1 - 0.5*(17.5 * 0.5))/ freq))
        left_circular_phase.append((-8445*STEC)/((freq) *(1 +  0.5*(17.5 * 0.5))/ freq))

no_mag_phase = np.array(no_mag_phase)
right_circular_phase = np.array(right_circular_phase)
left_circular_phase = np.array(left_circular_phase)

#enforces Hermitian symmetry
def enforce_symmetry (input_signal):
    N = np.size(input_signal)
    for i in range (1,(N +1) //2):
        input_signal[N-i] = np.conjugate(input_signal[i])
    return input_signal

#calculations for phase shift caused by ionosphere
def phaseshift(phase):
    ionosphere_phase = np.exp(-1j * phase)
    out_of_ionosphere = signal_f * (ionosphere_phase)
    #signal_t_satellite = np.fft.ifft(iono_symmetry)
    #t_satellite_mag = np.abs(signal_t_satellite)
    iono_mag =  np.abs(out_of_ionosphere)
    return out_of_ionosphere


no_mag = np.fft.ifft(enforce_symmetry(phaseshift(no_mag_phase)))
right_circular = np.fft.ifft(enforce_symmetry(phaseshift(right_circular_phase)))
left_circular = np.fft.ifft(enforce_symmetry(phaseshift(left_circular_phase)))
both = right_circular + left_circular



#for debug purposes:
#debug_df = pd.DataFrame( data = {'no': (no_mag),
                                 #'right': (right_circular_phase),
                                 #'left': (left_circular_phase),
                                     #'t_satellite: (signal_t_satellite)
                                     #})

    
df = pd.DataFrame(data = {'no_mag_real':(no_mag.real),
                          'no_mag_imag':(no_mag.imag),
                          'right_real': (right_circular.real),
                          'right_imag':(right_circular.imag),
                          'left_real':(left_circular.real),
                          'left_imag':(left_circular.imag),
                          'both_real':(both.real),
                          'both_imag':(both.imag)
                          })

df.to_csv(path_or_buf="fft_case_01_satellite.dat", sep=" ", index = True, header=[ 'no_mag_real','no_mag_imag',  'right_real', 'right_imag', 'left_real','left_imag', 'both_real','both_imag' ], float_format='%.6e')


