import numpy as np
import pandas as pd

class SoHUpdater:
    """
    Adaptive battery health updater.
    Learns gradual degradation using trip efficiency feedback.
    """

    def __init__(self, initial_soh=0.95, decay_rate=0.00005):
        self.soh = initial_soh
        self.decay_rate = decay_rate  # long-term aging factor

    def update(self, predicted_Wh_per_km, actual_Wh_per_km):
        # Error-based adjustment
        efficiency_ratio = predicted_Wh_per_km / (actual_Wh_per_km + 1e-6)
        delta = (1 - efficiency_ratio) * 0.002
        self.soh = np.clip(self.soh - self.decay_rate + delta, 0.6, 1.0)
        return self.soh

    def simulate_trip_update(self, df_trip):
        """Demonstration on a trip dataframe"""
        pred = df_trip["pred_energy"]
        act = df_trip["actual_energy"]
        soh_list = []
        for p, a in zip(pred, act):
            self.update(p, a)
            soh_list.append(self.soh)
        df_trip["updated_soh"] = soh_list
        return df_trip
