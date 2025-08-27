
#IMPROVED CODE#

import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from numpy.polynomial import Polynomial
from datetime import datetime

# =======================
# CONFIGURATION
# =======================
PORT = 'COM10'  # Adjust your port
BAUD = 115200
NUM_ACQUISITIONS = 3  # number of spectra to average
SAVE_DIR = Path("calibration_data")
SAVE_DIR.mkdir(exist_ok=True)

# Known LED wavelengths for wavelength calibration
LED_WAVELENGTHS = {
    "Violet": 405,
    "Blue": 470,
    "Green": 525,
    "Yellow": 590,
    "Red": 630,
    "FarRed": 730
}

# =======================
# SERIAL FUNCTIONS
# =======================
def read_spectrum(ser):
    """Read one spectrum from the spectrometer."""
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line.count(',') == 287:  # 288 pixels = 287 commas
            try:
                return np.array([int(val) for val in line.split(',')])
            except ValueError:
                continue

def average_spectra(ser, n=NUM_ACQUISITIONS):
    """Take n spectra and return the average."""
    spectra = []
    for _ in range(n):
        ser.write(b's\n')  # trigger acquisition
        spectrum = read_spectrum(ser)
        spectra.append(spectrum)
    return np.mean(spectra, axis=0)

# =======================
# PLOTTING
# =======================
def plot_spectrum(intensities, label=None):
    """Interactive plot for spectrum."""
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(intensities, color='royalblue')
    ax.set_title(f"Spectrum - {label}" if label else "Spectrum")
    ax.set_xlabel("Pixel Index")
    ax.set_ylabel("Intensity")
    ax.grid(True)
    plt.show()
    plt.pause(0.001)

# =======================
# CALIBRATION ROUTINE
# =======================
def calibrate():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)

    # Optionally capture dark spectrum
    input("Place the spectrometer in the dark (cover sensor), then press Enter to capture dark spectrum...")
    dark_spectrum = average_spectra(ser)
    np.save(SAVE_DIR / "dark_spectrum.npy", dark_spectrum)
    print("✅ Dark spectrum saved.")

    pixel_points = []
    wavelength_points = []

    print("\n=== Wavelength Calibration ===")
    print("Turn ON one LED at a time when prompted.\n")

    for color, wavelength in LED_WAVELENGTHS.items():
        ans = input(f"Do you want to calibrate {color} LED (~{wavelength} nm)? (y/n): ").strip().lower()
        if ans != "y":
            continue

        input(f"--> Please turn ON the {color} LED, then press Enter to capture...")

        # Take multiple acquisitions
        intensities = average_spectra(ser)
        # Dark correction
        intensities_corrected = intensities - dark_spectrum
        intensities_corrected[intensities_corrected < 0] = 0  # avoid negatives

        # Save raw spectrum with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        np.save(SAVE_DIR / f"spectrum_{color}_{timestamp}.npy", intensities_corrected)

        # Plot
        plot_spectrum(intensities_corrected, label=color)

        # Find peak pixel
        peak_pixel = np.argmax(intensities_corrected)
        peak_intensity = intensities_corrected[peak_pixel]
        print(f"[{color}] Peak Pixel: {peak_pixel}, Intensity: {peak_intensity}, Wavelength ≈ {wavelength} nm")

        # Store calibration points
        pixel_points.append(peak_pixel)
        wavelength_points.append(wavelength)

    ser.close()

    if len(pixel_points) < 2:
        print("❌ Not enough calibration points collected. At least 2 are required.")
        return

    # Polynomial fit: pixel → wavelength
    poly_degree = min(3, len(pixel_points)-1)  # cubic if enough points
    poly = Polynomial.fit(pixel_points, wavelength_points, poly_degree)

    # Save calibration polynomial
    calib_file = SAVE_DIR / "wavelength_poly.json"
    with open(calib_file, "w") as f:
        json.dump({
            "coefficients": [float(c) for c in poly.convert().coef],
            "degree": int(poly_degree),
            "pixel_points": [int(x) for x in pixel_points],
            "wavelength_points": [float(x) for x in wavelength_points],
            "dark_spectrum_file": str(SAVE_DIR / "dark_spectrum.npy"),
            "timestamp": datetime.now().isoformat()
        }, f, indent=4)
        

    print(f"\n✅ Calibration complete. Polynomial saved to {calib_file}")

if __name__ == "__main__":
    calibrate()
