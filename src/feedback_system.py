import numpy as np

class RangeFeedback:
    """
    Context-aware feedback system to reduce range anxiety.
    Combines predicted confidence range with trip context.
    """

    def __init__(self):
        pass

    def generate_message(self, range_safe, range_expected, range_optimistic,
                         traffic_index, hvac_on, soh, soc):
        buffer = range_optimistic - range_safe
        conf_level = "High" if buffer < 25 else "Moderate" if buffer < 60 else "Low"

        # Base message
        msg = f"Confidence: {conf_level}. Expected range ≈ {range_expected:.1f} km."

        # Context adjustments
        if soh < 0.8:
            msg += " Battery health slightly reduced. Consider avoiding rapid acceleration."
        if traffic_index > 0.7:
            msg += " Heavy traffic expected — range may reduce by 5–10 km."
        if hvac_on:
            msg += " HVAC active — additional energy load detected."
        if soc < 25:
            msg += " Low charge! Plan next charging stop within 20 km."

        if conf_level == "High" and soc > 40:
            msg += " ✅ You’re well within safe limits for this trip."

        return msg
