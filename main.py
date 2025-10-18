# main.py
from src.feedback_system import RangeFeedback
from src.soh_updater import SoHUpdater

feedback = RangeFeedback()
soh_model = SoHUpdater(initial_soh=0.9)

# Example test integration (you can later replace these with live model values)
sample = {
    "range_safe": 240,
    "range_expected": 275,
    "range_optimistic": 310,
    "traffic_index": 0.6,
    "hvac_on": 1,
    "soh": soh_model.soh,
    "soc": 65
}

msg = feedback.generate_message(**sample)
print(msg)
