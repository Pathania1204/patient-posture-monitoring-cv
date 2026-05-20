import cv2

GREEN  = (0, 200, 0)
RED    = (0, 0, 220)
WHITE  = (255, 255, 255)
YELLOW = (0, 255, 255)
FONT   = cv2.FONT_HERSHEY_SIMPLEX

# Only show these angles on screen — skip asymmetry raw values
DISPLAY_ANGLES = {
    "left_knee":   "L Knee",
    "right_knee":  "R Knee",
    "spine":       "Spine",
    "shoulder":    "L Shoulder",
    "right_shoulder": "R Shoulder",
}

def draw_angles(frame, angles):
    h, w = frame.shape[:2]
    font_scale = w / 1000
    thickness  = max(2, int(w / 500))

    y        = int(h * 0.06)
    line_gap = int(h * 0.055)

    for key, label in DISPLAY_ANGLES.items():
        val = angles.get(key)
        if val is None:
            continue
        text = f"{label}: {val}"
        cv2.putText(frame, text, (20, y), FONT, font_scale, WHITE, thickness)
        y += line_gap

    # Show asymmetry separately at bottom left if detected
    knee_asym = angles.get("knee_asymmetry")
    shoulder_asym = angles.get("shoulder_asymmetry")

    if knee_asym is not None:
        cv2.putText(frame, f"Knee Asymmetry: {knee_asym}",
                    (20, y), FONT, font_scale * 0.85, YELLOW, thickness)
        y += line_gap

    if shoulder_asym is not None:
        cv2.putText(frame, f"Shoulder Asymmetry: {shoulder_asym}",
                    (20, y), FONT, font_scale * 0.85, YELLOW, thickness)

    return frame

def draw_status(frame, analysis):
    h, w = frame.shape[:2]
    font_scale = w / 1000
    thickness  = max(2, int(w / 500))
    color      = GREEN if analysis["status"] == "Good" else RED

    box_height = 50 + (len(analysis["issues"]) * 32)
    cv2.rectangle(frame, (0, h - box_height - 10), (w // 2, h), (0, 0, 0), -1)

    cv2.putText(frame, analysis["status"],
                (20, h - box_height + 20),
                FONT, font_scale * 1.2, color, thickness + 1)

    y = h - box_height + 52
    for issue in analysis["issues"]:
        cv2.putText(frame, f"- {issue}", (20, y),
                    FONT, font_scale * 0.8, RED, thickness)
        y += 32

    return frame