Preforms a Fourier Transform on a signal mimicking an electromagnetic pulse (a double exponential) and simulates its interaction with the ionosphere and magnetic field. 

# How to run:

I use Gnuplot to display the dataset. If you do not have Gnuplot, install it with
`sudo apt install gnuplot`

1.**Clone this repo**
`git clone git@github.com:fuitgummyy/EMP_Analysis.git`
Make sure you are in the right directory using:
`cd EMP_Analysis`


2. **The code uses the Scipy, Numpy, Pandas, and Cmath libraries. If you do not have these libraries on your computer, run this code in your terminal:**
`sudo apt install python3-scipy`
`sudo apt install python3-numpy`
`sudo apt install python3-pandas`
`sudo apt install python3-cmath`

3: **Run 'fft_ionosphere.py' to recieve your data file** 
`python3 fft_ionosphere.py`

4: **Open Gnuplot and paste the following into the Gnuplot terminal to plot your data:**
`load "gnuplot_outofiono.txt"`
