import cv2
import time
import mediapipe as mp 
import numpy as np
from detectActions import detectAction, checkColor
from collections import deque


class clear_alert_cache():

    def check_clear(self,status):

        if self.len1 == 300:
            self.cache_clear.popleft()
            self.len1 -= 1

        self.cache_clear.append(status)            
        self.len1 += 1
        
        return all(self.cache_clear)

    def update_cache(self,clear_status):
        
        ret = []
        
        clear_seq_current = self.check_clear(clear_status)

        if clear_seq_current and (not self.prev_bent):
            ret.append('clear')

        self.prev_bent = clear_seq_current

        return ret

    def __init__(self):
        self.cache_clear = deque([])
        self.len1 = 0
        self.prev_bent = False



def mediapipe_results(frame, circles, color_change, color_num, pen_color, pen_size, mpHands, hands, mp_draw):

    flip = True 
    eraser_size = 100
    pen_color_changes = {0: "(255,0,0)", 1: "(0,255,0)", 2: "(0,0,255)", 3: "(0,0,0)"}

    frame = cv2.flip(frame, 1) if flip else frame
    h, w, c = frame.shape
    frame = cv2.resize(frame, (w*2, h*2))
    clear_dots = False

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
            action = detectAction(hand_landmarks, (h*2, w*2))
            color_num, color_change = checkColor(hand_landmarks, (h*2, w*2), color_change, color_num)
            pen_color = eval(pen_color_changes[color_num % 4]) if color_change else pen_color

            if action == 'Draw':
                index_pos = (int(hand_landmarks.landmark[4].x * w*2), int(hand_landmarks.landmark[4].y * h*2))
                cv2.circle(frame, index_pos, 20, (0,0,0), 2)
                circles.append([index_pos, eval(pen_color_changes[color_num % 4])])
            elif action == 'Erase':
                eraser_mid = (int(hand_landmarks.landmark[8].x * w*2), int(hand_landmarks.landmark[8].y * h*2))
                top_left = (eraser_mid[0] - eraser_size, eraser_mid[1] - eraser_size)
                bottom_right = (eraser_mid[0] + eraser_size, eraser_mid[1] + eraser_size)
                cv2.rectangle(frame, top_left, bottom_right, (0,0,255), 5)
                circles = [c for c in circles if not (top_left[0] < c[0][0] < bottom_right[0] and top_left[1] < c[0][1] < bottom_right[1])]
            elif action == 'Clear':
                clear_dots = True
            elif action == "pause":
                pos = (int(hand_landmarks.landmark[8].x * w*2), int(hand_landmarks.landmark[8].y * h*2))
                cv2.circle(frame, pos, 20, (0,0,255), 2)

    return frame, circles, pen_size, pen_color, color_change, color_num, clear_dots
