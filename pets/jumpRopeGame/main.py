import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time

pygame.init()

# Set up display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

# Load assets
background = displayio.OnDiskBitmap("background.bmp")
bg_sprite = displayio.TileGrid(background, pixel_shader=background.pixel_shader)
splash.append(bg_sprite)

player_sheet = displayio.OnDiskBitmap("player_sheet.bmp")
rope_sheet = displayio.OnDiskBitmap("rope_sheet.bmp")

# Tile sizes
tile_width = 32
tile_height = 32

# Player sprite
player_sprite = displayio.TileGrid(
    player_sheet,
    pixel_shader=player_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)
splash.append(player_sprite)

# Rope sprite
rope_sprite = displayio.TileGrid(
    rope_sheet,
    pixel_shader=rope_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    x=(display.width - tile_width) // 2,
    y=(display.height - tile_height) // 2
)
splash.append(rope_sprite)

# Game variables
frame = 0
rope_frame = 0
jumping = False
game_over = False
score = 0
rope_speed = 0.2  # Speed of the rope animation

def reset_game():
    global score, jumping, game_over, rope_speed
    score = 0
    jumping = False
    game_over = False
    rope_speed = 0.2
    player_sprite[0] = 0  # Reset to idle frame

# Main game loop
last_rope_update = time.monotonic()
last_jump_time = None
jump_window = 0.5  # Time window to jump correctly

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game_over:
                if not jumping:
                    jumping = True
                    player_sprite[0] = 2  # Jump animation frame
                    last_jump_time = time.monotonic()
            elif event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # Update rope animation
        if time.monotonic() - last_rope_update > rope_speed:
            rope_frame = (rope_frame + 1) % (rope_sheet.width // tile_width)
            rope_sprite[0] = rope_frame
            last_rope_update = time.monotonic()

            # Check if jump is in sync
            if rope_frame == 0:  # Assume frame 0 is the critical frame
                if jumping and last_jump_time and time.monotonic() - last_jump_time <= jump_window:
                    score += 1
                    rope_speed *= 0.98  # Gradually increase difficulty
                else:
                    game_over = True
                    player_sprite[0] = 3  # Trip animation frame

        # Reset player to idle if jumping is complete
        if jumping and time.monotonic() - last_jump_time > 0.3:
            jumping = False
            player_sprite[0] = 0  # Idle animation frame

    time.sleep(0.05)
