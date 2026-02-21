def calculate_crop_risk(soil, temperature, suitability, expected_profit):

    risk_score = 0
    reasons = []

    if temperature < 18 or temperature > 38:
        risk_score += 30
        reasons.append("Unfavorable temperature")

    if suitability < 60:
        risk_score += 30
        reasons.append("Low soil suitability")

    if expected_profit < 40000:
        risk_score += 20
        reasons.append("Low expected profit")

    if soil not in ["Black Soil", "Alluvial Soil"]:
        risk_score += 20
        reasons.append("Soil may not be ideal")

    if risk_score < 30:
        level = "Low Risk"
    elif risk_score < 60:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return level, reasons