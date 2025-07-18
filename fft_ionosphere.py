import numpy as np
import pandas as pd
import cmath

signal_t = np.loadtxt('/home/fuitgummyy/Documents/ICR/case_01.dat', dtype=float)

#setup
signal_f = np.fft.fft(signal_t)
n = signal_f.size
time_interval = 0.001 #time in microseconds
signal_f_freq = np.fft.fftfreq(n, d=time_interval)
#positive_freq = signal_f_freq [:524289]
#pos_signal_f = signal_f [:524289] 
signal_f_mag= np.abs(signal_f)
STEC = 10 #Slant TEC (total electron content) 

    
#removes DC term  of dataset   
signal_f = signal_f[1:]
signal_f_freq = signal_f_freq[1:] 

#minimum freq for highpass
safety_factor=0.8
f_min = 8445*STEC/(2*cmath.pi *(100* safety_factor))
f_min_sqrt = np.sqrt(f_min)

#calculations for phase shift caused by ionosphere
change_in_phase = 8445*STEC/(2*cmath.pi * signal_f_freq)
    #highpass = change_in_phase > f_min_sqrt
    #phase_highpass = change_in_phase * highpass
ionosphere_phase = np.exp(-1j * change_in_phase)
out_of_ionosphere = signal_f * ionosphere_phase
signal_t_satellite = np.fft.ifft(out_of_ionosphere)
    #signal_t_satellite = signal_t_satellite[:101857]
t_satellite_mag = np.abs(signal_t_satellite)

    
    #for debug purposes:
#debug_df = pd.DataFrame( data = {#'f_min': (f_min_sqrt),
                                     #'change_in_phase': (change_in_phase)})
                                     #'out_of_ionosphere': (out_of_ionosphere),
                                     #'t_satellite': (signal_t_satellite)})

    
df = pd.DataFrame(data = {'real': (signal_t_satellite.real),
                          'imag':(signal_t_satellite.imag),
                          'mag': (t_satellite_mag),
                          'complex':(signal_t_satellite.real + signal_t_satellite.imag*0j)
                          })

#print(f_min_sqrt)

df.to_csv(path_or_buf="fft_case_01_satellite.dat", sep=" ", index = True, header=['real', 'imag', 'mag', 'complex' ], float_format='%.6e')
