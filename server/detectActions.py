import os
from math import sqrt


def are_fingers_close(thumb, finger_1, finger_2, finger_3, finger_4):
    fingers = [thumb, finger_1, finger_2, finger_3, finger_4]
    max_distance = 250 # maximum distance to check closeness
    
    # Compare each finger with every other finger
    for i in range(len(fingers)):
        for j in range(i + 1, len(fingers)):
            # Calculate the Euclidean distance between fingers[i] and fingers[j]
            distance = ((fingers[i][0] - fingers[j][0]) ** 2 + (fingers[i][1] - fingers[j][1]) ** 2) ** 0.5
            # print("Distance : ", distance)
            if distance > max_distance:
                return False  # Return False if any two fingers are further apart than max_distance
    
    return True  # Return True if all fingers are within max_distance of each other


def detectAction(hand_landmarks, image_shape):
    """
    Detects the user's action (Erasing, Drawing, or Unknown) based on hand landmarks and image shape.
    """
    if clear(hand_landmarks,image_shape):
        return "Clear"
    if isErasing(hand_landmarks, image_shape):
        return "Erase"
    if isDrawing(hand_landmarks, image_shape):
        return "Draw"
    return "unknown"

def calcDistance(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def clear(hand_landmarks,image_shape):
    
    h, w = image_shape
    thumb = (int(hand_landmarks.landmark[4].x * w*2), int(hand_landmarks.landmark[4].y * h*2))
    finger_1 = (int(hand_landmarks.landmark[8].x * w*2), int(hand_landmarks.landmark[8].y * h*2))
    finger_2 = (int(hand_landmarks.landmark[12].x * w*2), int(hand_landmarks.landmark[12].y * h*2))
    finger_3 = (int(hand_landmarks.landmark[16].x * w*2), int(hand_landmarks.landmark[16].y * h*2))
    finger_4 = (int(hand_landmarks.landmark[20].x * w*2), int(hand_landmarks.landmark[20].y * h*2))
    
    return are_fingers_close(thumb, finger_1, finger_2, finger_3, finger_4)
    
def isErasing(hand_landmarks, image_shape):
    """
    Checks if the erasing conditions are met.
    """
    h, w = image_shape
    index_tip = (hand_landmarks.landmark[8].x * w, hand_landmarks.landmark[8].y * h)
    middle_tip = (hand_landmarks.landmark[12].x * w, hand_landmarks.landmark[12].y * h)
    index_mcp = (hand_landmarks.landmark[5].x * w, hand_landmarks.landmark[5].y * h)
    
    return calcDistance(index_tip, middle_tip) < calcDistance(index_tip, index_mcp) // 3

# def isDrawing(hand_landmarks, image_shape):
#     """
#     Checks if the drawing conditions are met.
#     """
#     w = image_shape[1]
#     thumb_tip_x = hand_landmarks.landmark[4].x * w
#     index_mcp_x = hand_landmarks.landmark[2].x * w

#     return thumb_tip_x > index_mcp_x

def isDrawing(hand_landmarks, image_shape):
    """
    Checks if the drawing conditions are met, considering both x and y positions, and calculating the distance
    between the thumb tip and the index finger tip.
    """
    w = image_shape[1]  # Image width
    h = image_shape[0]  # Image height
    thumb_tip_x = hand_landmarks.landmark[4].x * w
    thumb_tip_y = hand_landmarks.landmark[4].y * h
    index_tip_x = hand_landmarks.landmark[8].x * w
    index_tip_y = hand_landmarks.landmark[8].y * h
    threshold = (1/20) * w  # Define the threshold for "very close"
    
    # Calculate the Euclidean distance between the thumb tip and the index tip
    distance = ((thumb_tip_x - index_tip_x) ** 2 + (thumb_tip_y - index_tip_y) ** 2) ** 0.5

    # Check if the distance is within the threshold
    return distance <= threshold

def checkColor(hand_landmarks, image_shape, color_change, color_num):
    """
    Checks for a change in pen color.
    """
    h, w = image_shape
    index_tip_y = hand_landmarks.landmark[8].y * h
    index_mcp_y = hand_landmarks.landmark[5].y * h
    wrist_y = hand_landmarks.landmark[0].y * h

    curr_result = wrist_y > index_tip_y > index_mcp_y
    return (color_num + 1, True) if curr_result != color_change else (color_num, False)