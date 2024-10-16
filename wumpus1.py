import pygame
import random

# Initialize Pygame
pygame.init()

# Set up game parameters
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4  # Default map size for easy mode
TILE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Load images
player_img = pygame.image.load('agent.png')
wumpus_img = pygame.image.load('wumpus.png')
pit_img = pygame.image.load('pit.png')
gold_img = pygame.image.load('gold.png')
bat_img = pygame.image.load('bat.png')

# Resize images
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
wumpus_img = pygame.transform.scale(wumpus_img, (TILE_SIZE, TILE_SIZE))
pit_img = pygame.transform.scale(pit_img, (TILE_SIZE, TILE_SIZE))
gold_img = pygame.transform.scale(gold_img, (TILE_SIZE, TILE_SIZE))
bat_img = pygame.transform.scale(bat_img, (TILE_SIZE, TILE_SIZE))

# Set up game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus Game")

# Environment constants
WUMPUS = "W"
GOLD = "G"
PIT = "P"
BAT = "B"
EMPTY = "."

# Directions
DIRECTIONS = {
    pygame.K_UP: (-1, 0),
    pygame.K_DOWN: (1, 0),
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1)
}

# Function to ask player for difficulty level
def choose_difficulty():
    choosing = True
    difficulty = "easy"
    
    while choosing:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        
        # Display option text
        easy_text = font.render("Press 1 for Easy Mode", True, WHITE)
        normal_text = font.render("Press 2 for Normal Mode", True, WHITE)
        
        # Render text on screen
        screen.blit(easy_text, (WIDTH // 3, HEIGHT // 3))
        screen.blit(normal_text, (WIDTH // 3, HEIGHT // 2))
        
        pygame.display.flip()
        
        # Get player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "easy"
                    choosing = False
                elif event.key == pygame.K_2:
                    difficulty = "normal"
                    choosing = False
    
    return difficulty

# Function to check if a position is valid for spawning
def is_safe_position(game_map, pos):
    row, col = pos
    # Check surrounding tiles for Wumpus or Pit
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if 0 <= row + dr < len(game_map) and 0 <= col + dc < len(game_map[0]):
                if game_map[row + dr][col + dc] in [WUMPUS, PIT]:
                    return False
    return True

# Create the game map
def create_map(difficulty="easy"):
    if difficulty == "easy":
        map_size, num_wumpus, num_gold, num_bats, num_pits = 16, 1, 1, 2, 3
    else:
        map_size, num_wumpus, num_gold, num_bats, num_pits = 64, 2, 2, 4, 9

    rows = int(map_size ** 0.5)
    cols = rows
    global TILE_SIZE
    TILE_SIZE = WIDTH // cols

    # Resize images based on new tile size
    global player_img, wumpus_img, pit_img, gold_img, bat_img
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
    wumpus_img = pygame.transform.scale(wumpus_img, (TILE_SIZE, TILE_SIZE))
    pit_img = pygame.transform.scale(pit_img, (TILE_SIZE, TILE_SIZE))
    gold_img = pygame.transform.scale(gold_img, (TILE_SIZE, TILE_SIZE))
    bat_img = pygame.transform.scale(bat_img, (TILE_SIZE, TILE_SIZE))

    # Create empty map
    game_map = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    # Place Wumpus, Gold, Pit, and Bat randomly
    place_elements(game_map, num_wumpus, WUMPUS)
    place_elements(game_map, num_gold, GOLD)
    place_elements(game_map, num_bats, BAT)
    place_elements(game_map, num_pits, PIT)

    # Ensure player spawns in a safe position
    player_pos = [0, 0]  # Starting position
    while not is_safe_position(game_map, player_pos):
        player_pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
    
    return game_map, player_pos

# Function to place elements randomly on the map
def place_elements(game_map, count, element):
    rows, cols = len(game_map), len(game_map[0])
    placed = 0
    while placed < count:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if game_map[r][c] == EMPTY:
            game_map[r][c] = element
            placed += 1

# Draw the map on the screen
def draw_map(screen, game_map, player_pos):
    rows, cols = len(game_map), len(game_map[0])
    for r in range(rows):
        for c in range(cols):
            pygame.draw.rect(screen, WHITE, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
            
            # Draw elements
            if game_map[r][c] == WUMPUS:
                screen.blit(wumpus_img, (c * TILE_SIZE, r * TILE_SIZE))
            elif game_map[r][c] == PIT:
                screen.blit(pit_img, (c * TILE_SIZE, r * TILE_SIZE))
            elif game_map[r][c] == GOLD:
                screen.blit(gold_img, (c * TILE_SIZE, r * TILE_SIZE))
            elif game_map[r][c] == BAT:
                screen.blit(bat_img, (c * TILE_SIZE, r * TILE_SIZE))
    
    # Draw player
    screen.blit(player_img, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE))

# Main game loop
def main():
    # Choose difficulty
    difficulty = choose_difficulty()
    
    # Create map and player position based on chosen difficulty
    game_map, player_pos = create_map(difficulty)
    
    # Set up arrows based on difficulty, ensuring 1:4 ratio with Wumpus
    num_wumpus = 1 if difficulty == "easy" else 2
    arrows = num_wumpus * 4  # Set arrows based on Wumpus count
    
    # Score tracking and game state
    score = 0
    gold_collected = 0  # Track collected gold
    total_gold = 1 if difficulty == "easy" else 2  # Total gold based on difficulty
    total_wumpus = num_wumpus  # Total Wumpus based on difficulty
    
    # Game loop
    running = True
    shooting_mode = False  # Add shooting mode flag
    while running:
        screen.fill(BLACK)
        draw_map(screen, game_map, player_pos)
        
        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in DIRECTIONS and not shooting_mode:
                    # Move player
                    move = DIRECTIONS[event.key]
                    new_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]
                    
                    # Check if the new position is valid
                    if 0 <= new_pos[0] < len(game_map) and 0 <= new_pos[1] < len(game_map[0]):
                        player_pos = new_pos
                        
                        # Check interactions
                        current_tile = game_map[player_pos[0]][player_pos[1]]
                        if current_tile == WUMPUS:
                            print("You've been killed by the Wumpus!")
                            score -= 1000
                            running = False
                        elif current_tile == PIT:
                            print("You fell into a pit!")
                            score -= 1000
                            running = False
                        elif current_tile == GOLD:
                            print("You found the gold!")
                            score += 1000
                            gold_collected += 1
                            game_map[player_pos[0]][player_pos[1]] = EMPTY  # Remove gold
                        elif current_tile == BAT:
                            print("A bat carried you to a random location!")
                            player_pos = teleport_player(game_map)  # Teleport player safely
                            score -= 1  # Small penalty for teleportation
                        else:
                            score -= 1  # Normal step penalty
                
                # Handle shooting mode
                elif event.key == pygame.K_x and arrows > 0 and not shooting_mode:
                    print("Press arrow key to shoot in a direction!")
                    shooting_mode = True  # Enable shooting mode
                
                elif event.key in DIRECTIONS and shooting_mode:
                    direction = DIRECTIONS[event.key]
                    arrows -= 1  # Decrease arrow count
                    shooting_mode = False  # Disable shooting mode
                    
                    # Shoot arrow in the selected direction
                    if shoot_arrow(game_map, player_pos, direction):
                        print("You killed the Wumpus!")
                        score += 500  # Award points for killing Wumpus
                        total_wumpus -= 1  # Decrease total Wumpus count
                    else:
                        print("Your arrow missed!")
                
                # Check for win condition
                if gold_collected == total_gold and total_wumpus == 0:
                    print("You win! All gold collected and Wumpus killed!")
                    running = False

                # Display score and arrows
                print(f"Current Score: {score}, Arrows Left: {arrows}")

        # Update display
        pygame.display.flip()

    # After the loop ends (i.e., when `running = False`), show game over screen
    if game_over():
        main()  # Restart the game
    else:
        pygame.quit()
        exit()

# Function to shoot arrow in a direction
def shoot_arrow(game_map, player_pos, direction):
    row, col = player_pos
    delta_row, delta_col = direction
    
    # Move in the selected direction and check each tile
    while 0 <= row < len(game_map) and 0 <= col < len(game_map[0]):
        row += delta_row
        col += delta_col
        
        # If Wumpus is found in the path, kill it
        if game_map[row][col] == WUMPUS:
            game_map[row][col] = EMPTY  # Remove Wumpus from the map
            return True  # Wumpus is killed
    
    return False  # Arrow missed the Wumpus

# Function to safely teleport the player
def teleport_player(game_map):
    rows, cols = len(game_map), len(game_map[0])
    while True:
        new_pos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        if is_safe_position(game_map, new_pos):
            return new_pos  # Return safe position

# Function to display Game Over message and ask if player wants to play again
def game_over():
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, RED)
    replay_text = font.render("Do you want to play again? (Y/N)", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
    screen.blit(replay_text, (WIDTH // 5, HEIGHT // 2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Player presses 'Y' to play again
                    return True
                elif event.key == pygame.K_n:  # Player presses 'N' to quit
                    pygame.quit()
                    exit()

# Run the game
if __name__ == "__main__":
    main()
