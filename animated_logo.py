import os
import time
import math
import sys
import shutil
import random

# Clear console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Particle class for sparkles
class Particle:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width - 1)
        self.y = random.randint(0, screen_height - 1)
        self.life = random.randint(20, 60)  # Lifetime in frames
        self.max_life = self.life
        self.char = random.choice(['·', '•', '*', '✦', '✧'])
        
    def update(self):
        self.life -= 1
        
    def is_alive(self):
        return self.life > 0
    
    def get_brightness(self):
        # Particle fades in and out smoothly
        progress = self.life / self.max_life
        if progress > 0.7:
            # Fade in
            return (1 - progress) / 0.3
        elif progress < 0.3:
            # Fade out
            return progress / 0.3
        else:
            # Full brightness
            return 1.0

# List of particles
particles = []
MAX_PARTICLES = 15  # Maximum number of particles on screen

# Logo parameters - simple design like the original
LOGO_RADIUS = 6  # Small radius - less detail
LOGO_THICKNESS = 1  # Ring thickness

def generate_circle_logo(char_aspect_ratio=2.0):
    """
    Generates circular logo accounting for character aspect ratio
    char_aspect_ratio: character height / width (usually ~2.0)
    """
    height = LOGO_RADIUS * 2 + 1
    width = int((LOGO_RADIUS * 2 + 1) * char_aspect_ratio)
    
    logo = []
    center_y = LOGO_RADIUS
    center_x = width / 2
    
    for y in range(height):
        line = []
        for x in range(width):
            # Distance to center accounting for aspect ratio
            dx = (x - center_x) / char_aspect_ratio
            dy = y - center_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Check if point is in the ring
            if LOGO_RADIUS - LOGO_THICKNESS <= dist <= LOGO_RADIUS + 0.5:
                line.append('█')
            else:
                line.append(' ')
        
        logo.append(''.join(line))
    
    return logo

# Auto-detect aspect ratio
# For most consoles, characters are ~2x taller than wide
CHAR_ASPECT_RATIO = 2.0  # Can be adjusted for your console
LOGO_TEMPLATE = generate_circle_logo(CHAR_ASPECT_RATIO)

# Colors for gradient and volume (ANSI escape codes)
def get_color(intensity):
    """Returns color based on intensity (0-1) - sharper gradient for volume"""
    # Base pink color like in the image
    base_r, base_g, base_b = 231, 172, 172
    
    # Apply intensity to create volume
    r = int(base_r * intensity)
    g = int(base_g * intensity)
    b = int(base_b * intensity)
    
    return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

def calculate_lighting(x, y, frame, max_x, max_y):
    """Calculates lighting for each pixel with rotating light source"""
    # Center of the shape
    cx, cy = max_x / 2, max_y / 2
    
    # Light source rotates around the shape
    light_angle = frame * 0.12  # Faster rotation
    light_x = cx + math.cos(light_angle) * 25
    light_y = cy + math.sin(light_angle) * 15
    light_z = 10 + math.sin(light_angle * 0.7) * 5  # Light source height
    
    # Distance from pixel to center (for volume creation)
    dist_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
    max_dist = math.sqrt(cx**2 + cy**2)
    
    # Normalized distance
    norm_dist = dist_to_center / max_dist if max_dist > 0 else 0
    
    # Sphere simulation - pixel protrudes outward
    # Using hemisphere formula: z = sqrt(r² - x² - y²)
    if norm_dist <= 1.0:
        sphere_z = math.sqrt(1 - norm_dist**2) * 8  # Height of "bulge"
    else:
        sphere_z = 0
    
    # Surface normal (vector showing surface direction)
    nx = (x - cx) / max_dist if max_dist > 0 else 0
    ny = (y - cy) / max_dist if max_dist > 0 else 0
    nz = sphere_z / 8  # Normalized Z component
    
    # Vector to light source
    lx = light_x - x
    ly = light_y - y
    lz = light_z - sphere_z
    
    # Normalize light vector
    light_dist = math.sqrt(lx**2 + ly**2 + lz**2)
    if light_dist > 0:
        lx /= light_dist
        ly /= light_dist
        lz /= light_dist
    
    # Dot product to calculate angle between normal and light
    dot = nx * lx + ny * ly + nz * lz
    
    # Ambient + Diffuse lighting
    ambient = 0.3  # Base lighting
    diffuse = max(0, dot) * 0.7  # Directional lighting
    
    # Specular highlight (shine)
    specular = max(0, dot) ** 10 * 0.4
    
    intensity = ambient + diffuse + specular
    
    return max(0.2, min(1.0, intensity))  # Limit range

def get_text_color(char_index, frame, total_chars):
    """Returns color for text with light animation and cycling typing effect"""
    # Cycling typing animation
    typing_speed = 2  # Frames per character
    cycle_length = (total_chars * typing_speed) + 30  # Full cycle: typing + pause
    frame_in_cycle = frame % cycle_length
    
    # Typing effect - show characters gradually
    visible_chars = min(total_chars, frame_in_cycle // typing_speed)
    
    if char_index >= visible_chars:
        return '\033[38;2;50;30;30m'  # Almost invisible
    
    # Light wave running across text
    wave = math.sin((frame * 0.1) - (char_index * 0.3))
    
    # Base pink + light wave
    base_intensity = 0.7
    wave_intensity = (wave + 1) * 0.15  # 0 to 0.3
    total_intensity = base_intensity + wave_intensity
    
    r = int(231 * total_intensity)
    g = int(172 * total_intensity)
    b = int(172 * total_intensity)
    
    return f'\033[38;2;{r};{g};{b}m'

def render_frame(frame):
    """Renders one animation frame"""
    clear_console()
    
    # Get console size
    term_size = shutil.get_terminal_size()
    term_width = term_size.columns
    term_height = term_size.lines
    
    max_y = len(LOGO_TEMPLATE)
    max_x = len(LOGO_TEMPLATE[0]) if max_y > 0 else 0
    
    # Center horizontally
    left_padding = max(0, (term_width - max_x) // 2)
    top_padding = 2
    
    # Create screen matrix for background with particles
    screen = [[' ' for _ in range(term_width)] for _ in range(term_height)]
    screen_colors = [[None for _ in range(term_width)] for _ in range(term_height)]
    
    # Update and draw particles
    global particles
    
    # Remove dead particles
    particles = [p for p in particles if p.is_alive()]
    
    # Add new particles
    if len(particles) < MAX_PARTICLES and random.random() < 0.3:
        particles.append(Particle(term_width, term_height))
    
    # Update and draw particles on screen
    for particle in particles:
        particle.update()
        if 0 <= particle.y < term_height and 0 <= particle.x < term_width:
            brightness = particle.get_brightness()
            # Gray color for particles
            gray = int(80 + brightness * 100)
            screen[particle.y][particle.x] = particle.char
            screen_colors[particle.y][particle.x] = f'\033[38;2;{gray};{gray};{gray}m'
    
    # Draw logo on top of background
    logo_start_y = top_padding
    for y, line in enumerate(LOGO_TEMPLATE):
        screen_y = logo_start_y + y
        if screen_y < term_height:
            for x, char in enumerate(line):
                screen_x = left_padding + x
                if screen_x < term_width:
                    if char == '█':
                        # Calculate lighting
                        intensity = calculate_lighting(x, y, frame, max_x, max_y)
                        screen[screen_y][screen_x] = '█'
                        screen_colors[screen_y][screen_x] = get_color(intensity)
    
    # Output screen
    for y in range(term_height - 4):  # Leave space for text
        line = ""
        for x in range(term_width):
            color = screen_colors[y][x]
            char = screen[y][x]
            if color:
                line += color + char + RESET
            else:
                line += char
        print(line)
    
    # Title with light animation and typing
    print()
    
    # Text for animation
    line1 = "╔════════════╗"
    line2 = "║   GENSYN   ║"
    line3 = "╚════════════╝"
    
    box_width = len(line1)
    box_padding = " " * max(0, (term_width - box_width) // 2)
    
    # Render each line with animation
    def render_text_line(text, frame_offset=0):
        output = box_padding
        for i, char in enumerate(text):
            color = get_text_color(i, frame + frame_offset, len(text))
            output += color + char + RESET
        return output
    
    print(render_text_line(line1, 0))
    print(render_text_line(line2, 5))
    print(render_text_line(line3, 10))

def main():
    """Main animation loop"""
    frame = 0
    
    try:
        print("\033[?25l")  # Hide cursor
        
        while True:
            render_frame(frame)
            frame += 1
            time.sleep(0.08)  # ~12 FPS - smooth animation
            
    except KeyboardInterrupt:
        print("\033[?25h")  # Show cursor
        clear_console()
        print("\n\n  Animation stopped. Goodbye! 👋\n")
        sys.exit(0)

if __name__ == "__main__":
    # Enable color support on Windows
    if sys.platform == 'win32':
        os.system('')  # Activate ANSI escape codes on Windows 10+
    
    main()
