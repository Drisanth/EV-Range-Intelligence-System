import numpy as np
import pandas as pd

def generate_synthetic_ev_data(n_samples=10000, seed=42):
    np.random.seed(seed)
    df = pd.DataFrame()
    
    # Time-related features
    df['timestamp'] = pd.date_range(start='2024-01-01', periods=n_samples, freq='5min')
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Basic driving behavior
    df['avg_speed_kmph'] = np.clip(np.random.normal(45, 15, n_samples), 5, 110)
    df['trip_distance_km'] = np.clip(np.random.normal(12, 8, n_samples), 1, 60)
    df['elevation_gain_m'] = np.clip(np.random.normal(50, 40, n_samples), 0, 400)
    df['traffic_index'] = np.clip(np.random.normal(0.5, 0.2, n_samples), 0, 1)
    
    # Environmental features
    df['ambient_temp_c'] = np.clip(np.random.normal(25, 7, n_samples), -5, 40)
    df['rain_flag'] = np.random.choice([0,1], size=n_samples, p=[0.8,0.2])
    
    # Vehicle-specific
    df['battery_age_years'] = np.clip(np.random.normal(2, 1.5, n_samples), 0, 8)
    df['tyre_pressure_psi'] = np.clip(np.random.normal(36, 1.5, n_samples), 30, 40)
    df['hvac_on'] = np.where((df['ambient_temp_c'] > 28) | (df['ambient_temp_c'] < 12), 1, 0)
    df['payload_kg'] = np.clip(np.random.normal(150, 50, n_samples), 50, 400)
    df['soc_start'] = np.clip(np.random.normal(80, 10, n_samples), 20, 100)
    
    # Derived SoH (State of Health)
    df['soh'] = np.clip(1 - (df['battery_age_years'] * 0.05 + np.random.normal(0,0.02,n_samples)), 0.7, 1.0)
    
    # --- Energy consumption model (true function) ---
    base_consumption = 130  # Wh/km baseline
    df['energy_wh_per_km'] = (
        base_consumption
        + 0.6 * (df['avg_speed_kmph'] - 50)**2 / 100  # aerodynamic drag
        + 8 * df['traffic_index']                     # stop-go traffic
        + 0.8 * df['hvac_on'] * abs(df['ambient_temp_c'] - 22)
        + 0.05 * df['payload_kg']
        + 2 * (36 - df['tyre_pressure_psi'])
        + 0.05 * df['elevation_gain_m']
        + 15 * (1 - df['soh'])
        + np.random.normal(0, 5, n_samples)           # noise
    )
    
    # Clamp values
    df['energy_wh_per_km'] = np.clip(df['energy_wh_per_km'], 90, 350)
    
    # Range estimation (for reference)
    battery_capacity_kwh = 60  # typical mid-size EV
    df['usable_kwh'] = battery_capacity_kwh * df['soh']
    df['predicted_range_km'] = (df['usable_kwh'] * 1000 * df['soc_start']/100) / df['energy_wh_per_km']
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_ev_data()
    print(df.head())
    df.to_csv("data/synthetic_ev_data.csv", index=False)
