def compute_severity(damage_type, crop_area, image_area):
    """
    Practical, insurance-aligned severity rules.
    Designed for MVP reliability, not visual cleverness.
    """

    # 1️⃣ Scratches are cosmetic → always minor
    if damage_type == "scratch":
        return "minor"

    area_ratio = crop_area / image_area

    # 2️⃣ Dents: size matters, but never severe
    if damage_type == "dent":
        if area_ratio < 0.04:
            return "minor"
        else:
            return "moderate"

    # 3️⃣ Glass & headlight: safety components
    if damage_type in ["broken_glass", "headlight_damage"]:
        if area_ratio < 0.02:
            return "moderate"
        else:
            return "severe"

    # 4️⃣ Bumper damage: structural
    if damage_type == "bumper_damage":
        if area_ratio < 0.03:
            return "moderate"
        else:
            return "severe"

    # 5️⃣ Safe fallback
    return "minor"
