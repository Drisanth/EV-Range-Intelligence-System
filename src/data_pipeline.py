import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(path="data/synthetic_ev_data.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df


def feature_engineering(df):
    """Add time, interaction, and normalized features."""
    df = df.copy()

    # --- Time features (cyclical) ---
    df['hour'] = df['timestamp'].dt.hour
    df['hour_sin'] = np.sin(2*np.pi*df['hour']/24)
    df['hour_cos'] = np.cos(2*np.pi*df['hour']/24)
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

    # --- Derived features ---
    df['temp_deviation'] = np.abs(df['ambient_temp_c'] - 22)
    df['hvac_temp_interaction'] = df['hvac_on'] * df['temp_deviation']
    df['traffic_speed_ratio'] = df['traffic_index'] / (df['avg_speed_kmph'] + 1e-3)
    df['pressure_deficit'] = 36 - df['tyre_pressure_psi']
    df['payload_to_soh'] = df['payload_kg'] * (1 - df['soh'])
    df['elevation_per_km'] = df['elevation_gain_m'] / df['trip_distance_km']

    # --- Select final features ---
    feature_cols = [
        'avg_speed_kmph','traffic_index','ambient_temp_c','hvac_on',
        'hvac_temp_interaction','payload_kg','tyre_pressure_psi','pressure_deficit',
        'soh','battery_age_years','rain_flag','elevation_per_km',
        'hour_sin','hour_cos','is_weekend'
    ]
    target_col = 'energy_wh_per_km'

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    return X, y, df


def split_and_scale(X, y, test_size=0.2, random_state=42):
    """Train/val split + scaling."""
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_val_scaled   = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns)

    return X_train_scaled, X_val_scaled, y_train, y_val, scaler


if __name__ == "__main__":
    df = load_data()
    X, y, df_all = feature_engineering(df)
    X_train, X_val, y_train, y_val, scaler = split_and_scale(X, y)
    print("Train shape:", X_train.shape)
