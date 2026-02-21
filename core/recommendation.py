import json

with open("data/crops.json") as f:
    crops_data = json.load(f)

def calculate_ai_score(soil_type, suitability):

    recommendations = []

    for crop, data in crops_data.items():

        soil_match = 1 if soil_type in data["soil"] else 0
        profit_score = data["avg_profit"] / 150000
        demand_score = data["market_demand"] / 10

        final_score = (
            (suitability/100) * 0.4 +
            profit_score * 0.3 +
            demand_score * 0.2 +
            soil_match * 0.1
        )

        final_score = min(final_score, 1.0)

        recommendations.append((crop, round(final_score * 100, 2)))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations