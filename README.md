# 🌟 Gensyn Animated 3D Logo

A stunning animated 3D logo renderer for the terminal console with dynamic lighting, particle effects, and smooth animations.

![Gensyn Logo Animation](demo.gif)

## ✨ Features

- **3D Volume Effect** - Realistic sphere lighting simulation with normal mapping
- **Dynamic Lighting** - Rotating light source that orbits around the logo
- **Particle System** - Animated sparkles that appear and fade smoothly in the background
- **Typing Animation** - Text appears character by character with cycling effect
- **Light Wave Effect** - Smooth light waves flow across the text
- **Auto-Centering** - Automatically centers logo based on terminal size
- **Aspect Ratio Correction** - Generates perfectly circular logo regardless of console font

## 🎬 What It Does

The program creates a beautiful animated circular logo in your terminal with:
- Smooth 3D lighting that rotates around the logo
- Ambient sparkles in the background
- Animated text with typing effect
- Real-time rendering at ~12 FPS

## 🚀 Requirements

- Python 3.6+
- Windows 10+ (for full color support) or Unix-like system
- Terminal with ANSI color support

## 📦 Installation

1. Clone or download this repository
2. No additional dependencies required - uses only Python standard library!

## 🎮 Usage

Simply run the script:

```bash
python animated_logo.py
```

Press `Ctrl+C` to stop the animation.

## ⚙️ Customization

You can easily customize the logo by modifying these parameters at the top of `animated_logo.py`:

```python
LOGO_RADIUS = 6          # Logo size (radius in characters)
LOGO_THICKNESS = 1       # Thickness of the circle ring
MAX_PARTICLES = 15       # Maximum number of sparkles on screen
CHAR_ASPECT_RATIO = 2.0  # Adjust for your terminal's character aspect ratio
```

### Adjusting Circle Shape

If the circle appears squashed or stretched on your monitor:
- If **too wide** → decrease `CHAR_ASPECT_RATIO` (try 1.8 or 1.6)
- If **too tall** → increase `CHAR_ASPECT_RATIO` (try 2.2 or 2.4)

### Animation Speed

Adjust the lighting rotation speed:
```python
light_angle = frame * 0.12  # In calculate_lighting() function
```

Adjust the frame rate:
```python
time.sleep(0.08)  # In main() function - lower = faster
```

## 🎨 Technical Details

### 3D Lighting System
- **Ambient lighting** - Base illumination (30%)
- **Diffuse lighting** - Directional light based on surface normal (70%)
- **Specular highlights** - Shiny reflections for realistic effect
- **Sphere mapping** - Uses hemisphere formula: `z = sqrt(r² - x² - y²)`

### Particle System
- Particles spawn randomly across the screen
- Each particle has a lifetime of 20-60 frames
- Smooth fade-in and fade-out using brightness curves
- 5 different particle characters: `·`, `•`, `*`, `✦`, `✧`

### Text Animation
- Cycling typing effect with configurable speed
- Light wave travels across text using sine function
- Character-by-character color gradient

## 🎯 How It Works

1. **Logo Generation** - Creates circular logo using distance formula with aspect ratio correction
2. **3D Lighting Calculation** - Computes surface normals and dot product with light vector
3. **Particle Management** - Spawns, updates, and renders background particles
4. **Screen Buffering** - Builds complete frame in memory before rendering
5. **ANSI Color Output** - Uses RGB escape codes for 16.7 million colors

## 🖼️ Color Palette

- **Logo Base Color**: `RGB(231, 172, 172)` - Soft pink
- **Particles**: Dynamic gray scale `RGB(80-180, 80-180, 80-180)`
- **Background**: Pure black

## 📝 License

Free to use and modify. Created for the Gensyn project.

## 🙏 Credits

Created with ❤️ using Python and mathematics.

---

**Tip**: For the best visual experience, use a terminal with:
- Dark background
- Unicode font support
- True color (24-bit) support
- Monospace font like Consolas, Courier New, or Fira Code
