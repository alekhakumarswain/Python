import cv2
import numpy as np
import random
import time
import mediapipe as mp

# Game parameters
GRID_SIZE = 20
MIN_SPEED = 5
MAX_SPEED = 20
MIN_DISTANCE = 0.1  # Normalized distance thresholds
MAX_DISTANCE = 0.4

# Color definitions
BACKGROUND = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Get webcam dimensions
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculate grid dimensions
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

class SnakeGame:
    def __init__(self):
        self.reset()
        self.prev_hand_pos = None
        
    def reset(self):
        self.snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (0, 0)
        self.food = self.new_food()
        self.score = 0
        self.game_over = False

    def new_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                return food

    def update(self, direction):
        if self.game_over:
            return

        head = self.snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # Check collisions
        if (new_head in self.snake or 
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.new_food()
        else:
            self.snake.pop()

    def draw(self, frame, speed):
        frame[:] = BACKGROUND
        for segment in self.snake:
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            cv2.rectangle(frame, (x, y), (x+GRID_SIZE, y+GRID_SIZE), SNAKE_COLOR, -1)
        
        fx = self.food[0] * GRID_SIZE
        fy = self.food[1] * GRID_SIZE
        cv2.circle(frame, (fx+GRID_SIZE//2, fy+GRID_SIZE//2), GRID_SIZE//2, FOOD_COLOR, -1)

        cv2.putText(frame, f"Score: {self.score}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)
        cv2.putText(frame, f"Speed: {speed}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)
        if self.game_over:
            cv2.putText(frame, "Game Over! (R to restart)", (WIDTH//4, HEIGHT//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)

def process_hands(frame):
    direction = (0, 0)
    speed = MIN_SPEED
    hand_pos = None
    distance = 0
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Get wrist (0) and middle finger tip (12) positions
        wrist = hand_landmarks.landmark[0]
        middle_tip = hand_landmarks.landmark[12]
        
        # Calculate speed based on hand size
        distance = np.sqrt((wrist.x - middle_tip.x)**2 + (wrist.y - middle_tip.y)**2)
        speed = MIN_SPEED + int((distance - MIN_DISTANCE) / 
                (MAX_DISTANCE - MIN_DISTANCE) * (MAX_SPEED - MIN_SPEED))
        speed = max(MIN_SPEED, min(speed, MAX_SPEED))
        
        # Get hand position (palm center)
        hand_pos = (int(wrist.x * WIDTH), int(wrist.y * HEIGHT))
        
    return hand_pos, speed, distance, frame

def main():
    game = SnakeGame()
    last_update = time.time()
    current_speed = MIN_SPEED
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        
        hand_pos, speed, distance, processed_frame = process_hands(frame)
        current_speed = speed if hand_pos else current_speed
        
        if hand_pos:
            if game.prev_hand_pos:
                dx = hand_pos[0] - game.prev_hand_pos[0]
                dy = hand_pos[1] - game.prev_hand_pos[1]
                
                if abs(dx) > 20 or abs(dy) > 20:
                    if abs(dx) > abs(dy):
                        new_dir = (1 if dx > 0 else -1, 0)
                    else:
                        new_dir = (0, 1 if dy > 0 else -1)
                    
                    if (new_dir[0] != -game.direction[0] or 
                        new_dir[1] != -game.direction[1]):
                        game.direction = new_dir
            
            game.prev_hand_pos = hand_pos
        
        # Game update
        if time.time() - last_update > 1/current_speed:
            game.update(game.direction)
            last_update = time.time()
        
        # Draw game
        game_display = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        game.draw(game_display, current_speed)
        
        # Combine camera feed and game display
        combined = np.hstack([processed_frame, game_display])
        cv2.imshow("Hand Controlled Snake", combined)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            game.reset()
            current_speed = MIN_SPEED
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
