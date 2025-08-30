# import serial
# import time
# import matplotlib.pyplot as plt
# import numpy as np

# PORT = 'COM10'  # Update if needed
# BAUD_RATE = 115200

# def send_parameters(ser, delay_time, integration_cycles):
#     param_str = f"{delay_time} {integration_cycles}\n"
#     ser.write(param_str.encode('utf-8'))
#     print(f"Sent: {param_str.strip()}")
#     time.sleep(0.5)

#     # Send 's' to begin spectrum capture
#     ser.write(b's\n')
#     print("Sent 's' to begin capture")

# def read_spectrum(ser):
#     while True:
#         line = ser.readline().decode('utf-8', errors='ignore').strip()

#         if line and ',' in line:
#             try:
#                 values = [int(val) for val in line.split(',')]
#                 if len(values) == 288:
#                     return np.array(values)
#             except ValueError:
#                 continue
#         else:
#             print(f"[ARDUINO MSG] {line}")

# def main():
#     ser = serial.Serial(PORT, BAUD_RATE, timeout=2)
#     time.sleep(2)  # Let Arduino initialize

#     try:
#         while True:
#             user_input = input("Enter delayTime and integrationCycles (e.g. 1 85), or 'q' to quit: ")
#             if user_input.lower() == 'q':
#                 break

#             try:
#                 delay_time, integration_cycles = map(int, user_input.strip().split())
#             except ValueError:
#                 print("Invalid format. Use: number number")
#                 continue

#             send_parameters(ser, delay_time, integration_cycles)
#             spectrum = read_spectrum(ser)

#             # Summary
#             print(f"Min: {spectrum.min()} | Max: {spectrum.max()} | Mean: {spectrum.mean():.2f}")

#             # Plot
#             plt.figure()
#             plt.plot(spectrum, color='royalblue')
#             plt.title("C12880MA Spectrum")
#             plt.xlabel("Pixel")
#             plt.ylabel("Intensity")
#             plt.grid(True)
#             plt.show()

#     except KeyboardInterrupt:
#         print("User exited.")
#     finally:
#         ser.close()
#         print("Serial port closed.")

# if __name__ == "__main__":
#     main()



# import serial
# import time
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.colors import Normalize
# from matplotlib.cm import get_cmap

# PORT = 'COM10'  # Update as needed
# BAUD = 115200

# def read_spectrum(ser):
#     while True:
#         line = ser.readline().decode('utf-8', errors='ignore').strip()
#         if line.startswith("Optimal Integration Cycles:"):
#             print(line)
#             continue
#         elif line.count(',') == 287:
#             try:
#                 spectrum = [int(val) for val in line.split(',')]
#                 print("[✓] Spectrum received.")
#                 return np.array(spectrum)
#             except ValueError:
#                 continue
#         else:
#             print(f"[INFO] {line}")

# def plot_spectrum(wavelengths, intensities):
#     plt.figure(figsize=(10, 5))

#     # Standard Plot
#     plt.subplot(2, 1, 1)
#     plt.plot(wavelengths, intensities, color='royalblue')
#     plt.title("Wavelength vs Intensity")
#     plt.xlabel("Wavelength (nm)")
#     plt.ylabel("Intensity")
#     plt.grid(True)

#     # Colored Spectrum Strip
#     plt.subplot(2, 1, 2)
#     norm = Normalize(vmin=min(intensities), vmax=max(intensities))
#     cmap = get_cmap('plasma')  # You can also try 'turbo', 'rainbow', etc.

#     for i in range(len(wavelengths)-1):
#         plt.axvspan(wavelengths[i], wavelengths[i+1],
#                     color=cmap(norm(intensities[i])), linewidth=0)

#     plt.xlim(wavelengths[0], wavelengths[-1])
#     plt.title("Simulated Spectrum Visualization")
#     plt.xlabel("Wavelength (nm)")
#     plt.yticks([])
#     plt.tight_layout()
#     plt.show()

# def main():
#     ser = serial.Serial(PORT, BAUD, timeout=2)
#     time.sleep(2)

#     print("Sending 's' to start optimized integration and capture...")
#     ser.write(b's\n')

#     intensities = read_spectrum(ser)
#     wavelengths = np.linspace(340, 850, 288)

#     print(f"[Summary] Min: {intensities.min()} | Max: {intensities.max()} | Mean: {intensities.mean():.2f}")
#     plot_spectrum(wavelengths, intensities)

#     ser.close()
#     print("Serial port closed.")

# if __name__ == "__main__":
#     main()



# WORKING CODE FROM SPECTROMETER2.PY

# import serial
# import time
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.colors import Normalize
# from matplotlib.cm import get_cmap
# import os
# from datetime import datetime

# PORT = 'COM10'  # Update as needed
# BAUD = 115200

# def read_spectrum(ser):
#     while True:
#         line = ser.readline().decode('utf-8', errors='ignore').strip()
#         if line.startswith("Optimal Integration Cycles:"):
#             print(line)
#             continue
#         elif line.count(',') == 287:
#             try:
#                 spectrum = [int(val) for val in line.split(',')]
#                 print("[✓] Spectrum received.")
#                 return np.array(spectrum)
#             except ValueError:
#                 continue
#         else:
#             print(f"[INFO] {line}")

# def plot_spectrum(wavelengths, intensities):
#     plt.figure(figsize=(10, 5))

#     # Standard Plot
#     plt.subplot(2, 1, 1)
#     plt.plot(wavelengths, intensities, color='royalblue')
#     plt.title("Wavelength vs Intensity")
#     plt.xlabel("Wavelength (nm)")
#     plt.ylabel("Intensity")
#     plt.grid(True)

#     # Colored Spectrum Strip
#     plt.subplot(2, 1, 2)
#     norm = Normalize(vmin=min(intensities), vmax=max(intensities))
#     cmap = get_cmap('plasma')  # Try 'turbo', 'rainbow', etc.

#     for i in range(len(wavelengths)-1):
#         plt.axvspan(wavelengths[i], wavelengths[i+1],
#                     color=cmap(norm(intensities[i])), linewidth=0)

#     plt.xlim(wavelengths[0], wavelengths[-1])
#     plt.title("Simulated Spectrum Visualization")
#     plt.xlabel("Wavelength (nm)")
#     plt.yticks([])
#     plt.tight_layout()
#     plt.show()

# def save_spectrum(wavelengths, intensities):
#     # Save folder on Desktop
#     desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#     save_dir = os.path.join(desktop_path, "Spectra_Logs")
#     os.makedirs(save_dir, exist_ok=True)

#     # Timestamp for filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = os.path.join(save_dir, f"spectrum_{timestamp}.csv")

#     # Save as 2-column CSV (wavelength, intensity)
#     data = np.column_stack((wavelengths, intensities))
#     # np.savetxt(filename, data, delimiter=",", header="Wavelength,Intensity", comments='')
#     np.savetxt(filename, data, delimiter=",", header="Wavelength,Intensity", comments='', fmt=["%.2f", "%d"])


#     print(f"[Saved] Spectrum stored as {filename}")

# def main():
#     ser = serial.Serial(PORT, BAUD, timeout=2)
#     time.sleep(2)

#     print("Sending 's' to start optimized integration and capture...")
#     ser.write(b's\n')

#     intensities = read_spectrum(ser)
#     wavelengths = np.linspace(340, 850, 288)

#     # Print summary
#     print(f"[Summary] Min: {intensities.min()} | Max: {intensities.max()} | Mean: {intensities.mean():.2f}")

#     # Find and print peak wavelength
#     peak_idx = np.argmax(intensities)
#     peak_wavelength = wavelengths[peak_idx]
#     peak_value = intensities[peak_idx]
#     print(f"[Peak] Highest intensity at {peak_wavelength:.2f} nm (Intensity = {peak_value})")

#     # Save spectrum
#     save_spectrum(wavelengths, intensities)

#     # Plot
#     plot_spectrum(wavelengths, intensities)

#     ser.close()
#     print("Serial port closed.")

# if __name__ == "__main__":
#     main()


import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap
import os
import json
from datetime import datetime
from numpy.polynomial import Polynomial

# ---- Settings ----
PORT = 'COM10'
BAUD = 115200
NUM_PIXELS = 288
NUM_ACQUISITIONS = 3  # Number of spectra to average per capture

# ---- Load calibration ----
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
calib_file = os.path.join(desktop_path, "Calibration_Data", "wavelength_poly.json")
with open(calib_file, "r") as f:
    calib_data = json.load(f)
poly_coeffs = calib_data["coefficients"]
poly = Polynomial(poly_coeffs)
wavelengths = poly(np.arange(NUM_PIXELS))
print(f"[Calibration] Loaded polynomial mapping from {calib_file}")

# -------------------- Functions --------------------
def read_spectrum(ser):
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line.count(',') == 287:
            try:
                return np.array([int(val) for val in line.split(',')])
            except ValueError:
                continue

def average_spectra(ser, n=NUM_ACQUISITIONS):
    spectra = []
    for i in range(n):
        ser.write(b's\n')
        spectrum = read_spectrum(ser)
        spectra.append(spectrum)
        time.sleep(0.1)  # small delay between acquisitions
    return np.mean(spectra, axis=0)

def plot_spectrum(wavelengths, intensities):
    plt.figure(figsize=(10, 5))
    plt.subplot(2,1,1)
    plt.plot(wavelengths, intensities, color='royalblue')
    plt.title("Wavelength vs Intensity")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.grid(True)
    plt.subplot(2,1,2)
    norm = Normalize(vmin=min(intensities), vmax=max(intensities))
    cmap = get_cmap('plasma')
    for i in range(len(wavelengths)-1):
        plt.axvspan(wavelengths[i], wavelengths[i+1], color=cmap(norm(intensities[i])), linewidth=0)
    plt.xlim(wavelengths[0], wavelengths[-1])
    plt.title("Simulated Spectrum Visualization")
    plt.xlabel("Wavelength (nm)")
    plt.yticks([])
    plt.tight_layout()
    plt.show()

def save_spectrum(wavelengths, intensities):
    save_dir = os.path.join(desktop_path, "Spectra_Logs")
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"spectrum_{timestamp}.csv")
    data = np.column_stack((wavelengths, intensities))
    np.savetxt(filename, data, delimiter=",", header="Wavelength,Intensity", comments='', fmt=["%.2f", "%d"])
    print(f"[Saved] Spectrum stored as {filename}")

def centroid_peak(wavelengths, intensities):
    total = intensities.sum()
    if total == 0:
        return wavelengths[np.argmax(intensities)]
    return (wavelengths * intensities).sum() / total

# -------------------- Main --------------------
def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)
    print(f"Capturing {NUM_ACQUISITIONS} spectra to average...")

    averaged_intensities = average_spectra(ser, NUM_ACQUISITIONS)

    peak_wavelength = centroid_peak(wavelengths, averaged_intensities)
    peak_idx = np.argmax(averaged_intensities)
    peak_value = averaged_intensities[peak_idx]

    print(f"[Summary] Min: {averaged_intensities.min()} | Max: {averaged_intensities.max()} | Mean: {averaged_intensities.mean():.2f}")
    print(f"[Peak] Centroid peak: {peak_wavelength:.2f} nm")
    print(f"[Raw max pixel] Pixel {peak_idx} at {wavelengths[peak_idx]:.2f} nm, Intensity = {peak_value}")

    save_spectrum(wavelengths, averaged_intensities)
    plot_spectrum(wavelengths, averaged_intensities)

    ser.close()
    print("Serial port closed.")

if __name__ == "__main__":
    main()


# import serial
# import time
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.colors import Normalize
# from matplotlib.cm import get_cmap

# PORT = 'COM10'  # Update as needed
# BAUD = 115200

# def read_spectrum(ser):
#     while True:
#         line = ser.readline().decode('utf-8', errors='ignore').strip()
#         if line.startswith("Optimal Integration Cycles:"):
#             print(line)
#             continue
#         elif line.count(',') == 287:
#             try:
#                 spectrum = [int(val) for val in line.split(',')]
#                 print("[✓] Spectrum received.")
#                 return np.array(spectrum)
#             except ValueError:
#                 continue
#         else:
#             print(f"[INFO] {line}")

# def plot_spectrum(wavelengths, intensities):
#     plt.figure(figsize=(10, 5))

#     # Standard Plot
#     plt.subplot(2, 1, 1)
#     plt.plot(wavelengths, intensities, color='royalblue')
#     plt.title("Wavelength vs Intensity")
#     plt.xlabel("Wavelength (nm)")
#     plt.ylabel("Intensity")
#     plt.grid(True)

#     # Colored Spectrum Strip
#     plt.subplot(2, 1, 2)
#     vmax = 1000  # Adjust this based on your sensor's max expected intensity
#     norm = Normalize(vmin=0, vmax=vmax)
#     cmap = get_cmap('magma')  # Good perceptual colormap for low intensities

#     for i in range(len(wavelengths)-1):
#         plt.axvspan(wavelengths[i], wavelengths[i+1],
#                     color=cmap(norm(intensities[i])), linewidth=0)

#     plt.xlim(wavelengths[0], wavelengths[-1])
#     plt.title("Simulated Spectrum Visualization")
#     plt.xlabel("Wavelength (nm)")
#     plt.yticks([])
#     plt.tight_layout()
#     plt.show()

# def main():
#     ser = serial.Serial(PORT, BAUD, timeout=2)
#     time.sleep(2)

#     print("Sending 's' to start optimized integration and capture...")
#     ser.write(b's\n')

#     intensities = read_spectrum(ser)
#     wavelengths = np.linspace(340, 850, 288)

#     # Print all intensity values
#     print("\n[Pixel Intensities]")
#     for i, intensity in enumerate(intensities):
#         print(f"Pixel {i:03d}: {intensity}")
#     print()

#     # Summary statistics
#     print(f"[Summary] Min: {intensities.min()} | Max: {intensities.max()} | Mean: {intensities.mean():.2f}")

#     # Plot the spectrum
#     plot_spectrum(wavelengths, intensities)

#     ser.close()
#     print("Serial port closed.")

# if __name__ == "__main__":
#     main()

