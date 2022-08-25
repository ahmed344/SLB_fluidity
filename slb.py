import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class IntensityCurve():
    
    def __init__(self, t, x, It, Ix):
        
        self.t = t
        self.x = x
        self.It = It
        self.Ix = Ix

    # Intensity of the square center as a function of time
    def intensity_time(t, B, Io, Ib):
        return Io * np.exp(-B*t) + Ib

    # Fit an intensity curve on the data
    def curve_fitting(self, show=False):
        """Fit the intesity curve on the data.
        Parameter:
            t, x, It, Ix                 - as numpy arrays
        Returns: 
            B, Io_t, Ib_t, D, Io_x, Ib_x - of the intensity equations.
        """
        
        # Apply the fitting 
        (B, Io_t, Ib_t), _ = curve_fit(IntensityCurve.intensity_time, self.t, self.It,
                                       p0=(0.05, self.It.max()-self.It.min(), self.It.min()),
                                       bounds=([0.001, 0, 0],[1, self.It.max()*2, self.It.min()*3]))
        
        if show == True: print(f'Intensity equation of time:\nIo = {Io_t:.3f}\nIb = {Ib_t:.3f}\nB = {B:.3f}\n')
        
        # Intesity of the rectangle as a function of space from the edge
        def intensity_space(x, D, Io, Ib):
            return Io * np.exp(-x*np.sqrt(B/D)) + Ib
        
        (D, Io_x, Ib_x), _ = curve_fit(intensity_space, self.x, self.Ix,
                                       p0=(1, self.Ix.max()-self.Ix.min(), self.Ix.min()),
                                       bounds=([0.01, 0, 0],[100, self.Ix.max(), self.Ix.max()]))
        
        if show == True: print(f'Intensity equation of space:\nIo = {Io_x:.3f}\nIb = {Ib_x:.3f}\nD = {D:.3f}')
        
        # Display the results
        if show == True:
            plt.figure(figsize=(17,5))
            
            # Intensity time curve
            plt.subplot(121)
            plt.plot(self.t, self.It, label='Data')
            plt.plot(self.t, Io_t * np.exp(-B*self.t) + Ib_t, "r--",
                     label =f'Fitting:\n$I_o$={Io_t:.3f}\n$I_b$={Ib_t:.3f}\n$B$={B:.3f} $1/s$')
            plt.title('$I(t) = I_0 e^{(-Bt)} + I_{b}$', fontsize='xx-large')
            plt.xlabel('Time [S]', fontsize='large')
            plt.ylabel('I(t)', fontsize='large')
            plt.grid()
            plt.legend(fontsize='large')

            # Intensity space curve
            plt.subplot(122)
            plt.plot(self.x, self.Ix, label='Data')
            plt.plot(self.x, Io_x * np.exp(-self.x*np.sqrt(B/D)) + Ib_x, "r--",
                     label =f'Fitting:\n$I_o$={Io_x:.3f}\n$I_b$={Ib_x:.3f}\n$D$={D:.3f} $\mu m^2/s$')
            plt.title('$I(x) = I_0 e^{-x \sqrt{B/D}} + I_{b}$', fontsize='xx-large')
            plt.xlabel('Distance [ $\mu m^2$ ]', fontsize='large')
            plt.ylabel('I(x)', fontsize='large')
            plt.grid()
            plt.legend(fontsize='large');

        return B, Io_t, Ib_t, D, Io_x, Ib_x # B, Io, Ib, D of the intensity equations