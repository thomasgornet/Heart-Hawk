#import pyttsx3
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd

#engine = pyttsx3.init()

    

def analyze_hrv(sdnn, rmssd, pnn50):
    """
    Analyzes HRV data based on SDNN, RMSSD, and pNN50 values.
    Returns a health assessment and recommendations.
    """
    # HRV Health Interpretation
    interpretation = ""

    # SDNN Analysis
    if sdnn > 100:
        interpretation += "Your SDNN is very high, indicating excellent overall HRV and strong autonomic balance. Keep maintaining a healthy lifestyle.\n"
    elif 50 <= sdnn <= 100:
        interpretation += "Your SDNN is within a healthy range, indicating good overall heart rate variability. This suggests a well-functioning nervous system.\n"
    else:
        interpretation += "Your SDNN is low, which may indicate high stress levels, fatigue, or a potential health concern. Consider improving sleep, relaxation techniques, and aerobic exercise.\n"

    # RMSSD Analysis
    if rmssd > 100:
        interpretation += "Your RMSSD is abnormally high, which could indicate overtraining or extreme parasympathetic dominance. Consider monitoring fatigue levels.\n"
    elif 30 <= rmssd <= 100:
        interpretation += "Your RMSSD is in a good range, suggesting healthy short-term HRV and good recovery ability.\n"
    else:
        interpretation += "Your RMSSD is low, which may indicate stress, poor recovery, or insufficient parasympathetic activity. Deep breathing and meditation could help.\n"

    # pNN50 Analysis
    if pnn50 > 40:
        interpretation += "Your pNN50 is very high, which could indicate bradycardia (slow heart rate) or excessive parasympathetic activity. This may not be a concern unless you feel fatigued.\n"
    elif 10 <= pnn50 <= 40:
        interpretation += "Your pNN50 is in a healthy range, reflecting a good balance between sympathetic and parasympathetic nervous system activity.\n"
    else:
        interpretation += "Your pNN50 is low, indicating reduced HRV. This may be a sign of stress, dehydration, or lack of recovery. Consider lifestyle adjustments to improve resilience.\n"


    return interpretation
# Load pulse signal
pulse_signal = pd.read_csv("./data.csv").iloc[:, 0].values

# Define the correct sampling rate
sampling_rate = 20  # 500 samples per second (2 ms per sample)
time = np.arange(len(pulse_signal)) / sampling_rate  # Convert indices to seconds

# Detect peaks with tuned parameters
peaks, properties = find_peaks(
    pulse_signal, height=np.mean(pulse_signal), distance=sampling_rate//2, prominence=0.8
)

# Calculate RR Intervals in milliseconds (convert detected time differences)
rr_intervals = np.diff(time[peaks]) * 1000  # Convert seconds to milliseconds

# print("RR Intervals (ms):", rr_intervals)
print(f"BPM =  { int(60_000 / np.mean(rr_intervals))}")

# Compute HRV metrics
sdnn = np.std(rr_intervals, ddof=1)  # Standard deviation of RR intervals
rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2))  # RMSSD calculation

# pNN50 - Percentage of adjacent RR intervals differing by more than 50ms
nn50_count = np.sum(np.abs(np.diff(rr_intervals)) > 50)
pnn50 = (nn50_count / len(rr_intervals)) * 100

result = analyze_hrv(sdnn, rmssd, pnn50)
print(f"Sdnn -> {int(sdnn)}, rmssd -> {int(rmssd)} , pnn50 -> {int(pnn50)}")
print("HRV Analysis Report:")
print(result)

# Plot pulse signal with detected peaks
plt.figure(figsize=(12, 5))
plt.plot(time, pulse_signal, label="Pulse Signal", color='blue')
plt.plot(time[peaks], pulse_signal[peaks], "ro", label="Detected Peaks")
plt.xlabel("Time (s)")
plt.ylabel("Pulse Value")
plt.legend()
plt.title("Pulse Signal with Correctly Detected Peaks")
plt.show()






from scipy.signal import welch

# Compute Power Spectral Density (PSD) using Welch's method
freqs, psd = welch(rr_intervals, fs=1000/np.mean(rr_intervals), nperseg=len(rr_intervals)//2)

# Define frequency bands (Hz)
lf_band = (0.04, 0.15)  # Low Frequency (LF)
hf_band = (0.15, 0.4)   # High Frequency (HF)

# Integrate power in LF and HF bands
lf_power = np.trapezoid(psd[(freqs >= lf_band[0]) & (freqs < lf_band[1])], freqs[(freqs >= lf_band[0]) & (freqs < lf_band[1])])
hf_power = np.trapezoid(psd[(freqs >= hf_band[0]) & (freqs < hf_band[1])], freqs[(freqs >= hf_band[0]) & (freqs < hf_band[1])])

# Calculate LF/HF ratio
lf_hf_ratio = lf_power / hf_power if hf_power != 0 else np.nan

# Display Frequency-Domain HRV Metrics
hrv_freq_metrics_df = pd.DataFrame({
    "Metric": ["LF Power", "HF Power", "LF/HF Ratio"],
    "Value": [lf_power, hf_power, lf_hf_ratio]
})
from IPython.display import display
display(hrv_freq_metrics_df)

if (lf_hf_ratio > 2): print("You have sympathetic dominance. The sympathetic nervous system increases the heart rate. This could indicate stress")
elif (lf_hf_ratio > 1.5): print("You have a healthy balance between sympathetic and parasympathetic dominance")
elif (lf_hf_ratio < 1): print("You have parasympathetic dominance. You could be fatigued, or tired a lot")
else: print("You do not not have an unhealthy balance of Parasympathetic or Sympathetic, however you tend to have a little bit of Parasympathetic dominance.")




# Plot the Power Spectral Density (PSD)
plt.figure(figsize=(10, 5))
plt.semilogy(freqs, psd, label="Power Spectral Density")
plt.axvspan(lf_band[0], lf_band[1], color='red', alpha=0.3, label="LF Band (0.04-0.15 Hz)")
plt.axvspan(hf_band[0], hf_band[1], color='blue', alpha=0.3, label="HF Band (0.15-0.4 Hz)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")
plt.title("Power Spectral Density of HRV")
plt.legend()
plt.show()
