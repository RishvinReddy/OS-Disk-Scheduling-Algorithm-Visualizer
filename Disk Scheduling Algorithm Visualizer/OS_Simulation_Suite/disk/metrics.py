import numpy as np

def calculate_metrics(seek_sequence):
    if len(seek_sequence) < 2:
        return {"Total Seek": 0, "Average Seek": 0.0, "Variance": 0.0}
    
    seek_times = [abs(seek_sequence[i] - seek_sequence[i-1]) for i in range(1, len(seek_sequence))]
    total_seek = sum(seek_times)
    avg_seek = total_seek / len(seek_times)
    variance = np.var(seek_times) if seek_times else 0.0
    
    return {
        "Total Seek": int(total_seek),
        "Average Seek": round(avg_seek, 2),
        "Variance": round(variance, 2)
    }
