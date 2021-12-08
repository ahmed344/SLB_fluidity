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
            t, x, It, Ix - as numpy arrays
        Returns: 
            D, B, Io, Ib - of the intensity equations.
        """
        
        # Apply the fitting 
        (B, Io, Ib), _ = curve_fit(IntensityCurve.intensity_time, self.t, self.It, p0=(0, self.It.max(), self.It.max()/3))
        
        # Intesity of the rectangle as a function of space from the edge
        def intensity_space(x, D):
            return Io * np.exp(-x*np.sqrt(B/D)) + Ib
        
        D, _ = curve_fit(intensity_space, self.x, self.Ix, p0=1, bounds=[1e-100,np.inf])
        D = D[0]
        
        # Display the results
        if show == True:
            plt.figure(figsize=(17,5))
            
            # Intensity time curve
            plt.subplot(121)
            plt.plot(self.t, self.It, label='Data')
            plt.plot(self.t, Io * np.exp(-B*self.t) + Ib, "r--", label =f'fit: Io={Io:.3f}, Ib={Ib:.3f}, B={B:.3f}')
            plt.title('I(t)')
            plt.xlabel('Time [S]')
            plt.ylabel('I(t)')
            plt.grid()
            plt.legend()

            # Intensity space curve
            plt.subplot(122)
            plt.plot(self.x, self.Ix, label='Data')
            plt.plot(self.x, Io * np.exp(-self.x*np.sqrt(B/D)) + Ib, "r--", label =f'fit: D={D:.4f}')
            plt.title('I(x)');
            plt.xlabel('Distance [ $\mu m^2$ ]')
            plt.ylabel('I(x)')
            plt.grid()
            plt.legend();

        return B, Io, Ib, D # B, Io, Ib, D of the intensity equations