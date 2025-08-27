
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

PORT = 'COM10'  # Update as needed
BAUD = 115200

def read_spectrum(ser):
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line.startswith("Optimal Integration Cycles:"):
            print(line)
            continue
        elif line.count(',') == 287:
            try:
                spectrum = [int(val) for val in line.split(',')]
                print("[✓] Spectrum received.")
                return np.array(spectrum)
            except ValueError:
                continue
        else:
            print(f"[INFO] {line}")

def plot_spectrum(wavelengths, intensities):
    plt.figure(figsize=(10, 5))

    # Standard Plot
    plt.subplot(2, 1, 1)
    plt.plot(wavelengths, intensities, color='royalblue')
    plt.title("Wavelength vs Intensity")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.grid(True)

    # Colored Spectrum Strip
    plt.subplot(2, 1, 2)
    norm = Normalize(vmin=min(intensities), vmax=max(intensities))
    cmap = get_cmap('plasma')  # You can also try 'turbo', 'rainbow', etc.

    for i in range(len(wavelengths)-1):
        plt.axvspan(wavelengths[i], wavelengths[i+1],
                    color=cmap(norm(intensities[i])), linewidth=0)

    plt.xlim(wavelengths[0], wavelengths[-1])
    plt.title("Simulated Spectrum Visualization")
    plt.xlabel("Wavelength (nm)")
    plt.yticks([])
    plt.tight_layout()
    plt.show()

def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)

    print("Sending 's' to start optimized integration and capture...")
    ser.write(b's\n')

    intensities = read_spectrum(ser)
    wavelengths = np.linspace(340, 850, 288)

    print(f"[Summary] Min: {intensities.min()} | Max: {intensities.max()} | Mean: {intensities.mean():.2f}")
    plot_spectrum(wavelengths, intensities)

    ser.close()
    print("Serial port closed.")

if __name__ == "__main__":
    main()



