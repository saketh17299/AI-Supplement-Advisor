from typing import List, Dict

# Example deterministic rules for supplements
SUPPLEMENT_RULES = {
    "creatine": {
        "contraindications": ["kidney disease"],
        "interactions": [],
        "max_daily_dose_g": 5
    },
    "vitamin d3": {
        "contraindications": ["hypercalcemia"],
        "interactions": [],
        "max_daily_dose_IU": 4000
    },
    "magnesium": {
        "contraindications": ["renal failure"],
        "interactions": [],
        "max_daily_dose_mg": 350
    }
}

def apply_rules(supplements: List[Dict], user_profile: Dict) -> List[Dict]:
    flagged_supplements = []
    for sup in supplements:
        name = sup.get("name", "").lower()
        rule = SUPPLEMENT_RULES.get(name)
        sup_copy = sup.copy()

        if not rule:
            flagged_supplements.append(sup_copy)
            continue

        # Check contraindications
        contraindications = rule.get("contraindications", [])
        user_conditions = user_profile.get("conditions", [])
        intersect = [c for c in user_conditions if c.lower() in contraindications]
        if intersect:
            sup_copy["flag"] = f"⚠️ Contraindicated due to: {', '.join(intersect)}"
        else:
            sup_copy["flag"] = "✅ Safe based on rules"

        # Adjust max dose
        if "max_daily_dose_g" in rule and "dose_g" in sup_copy:
            sup_copy["dose_g"] = min(sup_copy["dose_g"], rule["max_daily_dose_g"])
        if "max_daily_dose_mg" in rule and "dose_mg" in sup_copy:
            sup_copy["dose_mg"] = min(sup_copy["dose_mg"], rule["max_daily_dose_mg"])
        if "max_daily_dose_IU" in rule and "dose_IU" in sup_copy:
            sup_copy["dose_IU"] = min(sup_copy["dose_IU"], rule["max_daily_dose_IU"])

        flagged_supplements.append(sup_copy)
    return flagged_supplements
