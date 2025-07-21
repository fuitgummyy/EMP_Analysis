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

    
#removes DC term  of dataset   
signal_f = signal_f[1:]
signal_f_freq = signal_f_freq[1:] 

signal_f[:2500] = 0
signal_f[-2500:] = 0
signal_f_mag= np.abs(signal_f)
#minimum freq for highpass


#calculations for phase shift caused by ionosphere
change_in_phase = -8445*STEC/(2*cmath.pi * signal_f_freq)
ionosphere_phase = np.exp(-1j * change_in_phase)
out_of_ionosphere = signal_f * (ionosphere_phase)
signal_t_satellite = np.fft.ifft(out_of_ionosphere)
t_satellite_mag = np.abs(signal_t_satellite)
iono_mag =  np.abs(out_of_ionosphere)

#magnetic field
right_circular = 8445*STEC/(2*cmath.pi * signal_t_satellite) *(1 - 0.5*(17.5 * 0.5)/signal_t_satellite)
left_circular = 8445*STEC/(2*cmath.pi * signal_f_freq) *(1 +  0.5*(17.5 * 0.5)/signal_f_freq)
    
    #for debug purposes:
#debug_df = pd.DataFrame( data = {'signal_t': (signal_t)
                                 #'change_in_phase': (change_in_phase)})
                                     #'out_of_ionosphere': (out_of_ionosphere),
                                     #'t_satellite: (signal_t_satellite)
                                     #})

    
df = pd.DataFrame(data = {'real': (right_circular.real),
                          'imag':(right_circular.imag),
                         'mag': (t_satellite_mag),
                          #'complex':(signal_t_satellite.real + signal_t_satellite.imag*0j)
                          })

df.to_csv(path_or_buf="fft_case_01_satellite.dat", sep=" ", index = True, header=[ 'real', 'imag', 'mag' ], float_format='%.6e')

