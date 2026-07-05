import math
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, InstructionGroup
from kivy.clock import Clock
from kivy.core.window import Window

class SolarSystemCanvas(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Simulation states
        self.is_paused = False
        self.click_count = 0
        self.cat_spawned = False
        
        # Engine tracking variables
        self.frame_time = 0.0
        self.cat_x_ratio = -0.15  # Use relative screen width tracking for mobile
        self.cat_frame = 0

        # Orbital data scaling parameters
        self.planets_data = {
            "mercury": {"or_scale": 0.08, "p_rad": 5,  "speed": 0.04,  "color": (0.62, 0.62, 0.62, 1)},
            "venus":   {"or_scale": 0.14, "p_rad": 8,  "speed": 0.015, "color": (0.89, 0.66, 0.34, 1)},
            "earth":   {"or_scale": 0.22, "p_rad": 9,  "speed": 0.01,  "color": (0.17, 0.51, 0.79, 1)},
            "mars":    {"or_rad_fixed": 0, "or_scale": 0.32, "p_rad": 7, "speed": 0.008, "color": (0.76, 0.27, 0.06, 1)}
        }
        self.angles = {name: 0.0 for name in self.planets_data}
        self.angles["moon"] = 0.0

        # Create UI Control layout overlay
        self.setup_ui()
        
        # Bind coordinate calculations to dynamic window resizes (handles screen rotation)
        self.bind(size=self.on_layout_resize)
        
        # Initialize background canvas structures
        self.stars_group = InstructionGroup()
        self.orbits_group = InstructionGroup()
        self.canvas.before.add(self.stars_group)
        self.canvas.before.add(self.orbits_group)

        # Main drawing loop execution handle (60 FPS target rate)
        Clock.schedule_interval(self.update_simulation, 1.0 / 60.0)

    def setup_ui(self):
        """Adds a responsive button scaling cleanly on fluid mobile layouts"""
        self.pause_btn = Button(
            text="Pause Simulation",
            font_size="16sp",  # Scale-independent pixels for high-DPI retina mobile screens
            size_hint=(0.5, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            background_color=(0.13, 0.13, 0.27, 1),
            color=(1, 1, 1, 1)
        )
        self.pause_btn.bind(on_release=self.handle_button_click)
        self.add_widget(self.pause_btn)

    def handle_button_click(self, instance):
        """Tracks input logs to capture screen interaction patterns"""
        self.click_count += 1
        if self.click_count == 3:
            self.cat_spawned = True
            
        self.is_paused = not self.is_paused
        self.pause_btn.text = "Resume Simulation" if self.is_paused else "Pause Simulation"

    def on_layout_resize(self, *args):
        """Recalculates display coordinate matrices during mobile screen rotations"""
        cx, cy = self.width / 2, self.height / 2
        min_dim = min(self.width, self.height)

        # Clear out structural vectors 
        self.stars_group.clear()
        self.orbits_group.clear()

        # Generate starry background landscape
        random.seed(101)
        self.stars_group.add(Color(1, 1, 1, 1))
        for _ in range(80):
            sx = random.randint(0, int(self.width))
            sy = random.randint(0, int(self.height))
            size = random.choice([1, 2, 3])
            self.stars_group.add(Ellipse(pos=(sx, sy), size=(size, size)))

        # Update static geometric orbit boundaries
        self.orbits_group.add(Color(0.1, 0.1, 0.23, 1))
        for data in self.planets_data.values():
            r = min_dim * data["or_scale"]
            self.orbits_group.add(Line(circle=(cx, cy, r), width=1))

    def update_simulation(self, dt):
        """The rendering loop processing mobile graphic frames"""
        cx, cy = self.width / 2, self.height / 2
        min_dim = min(self.width, self.height)
        
        # Flush the transient dynamic layers before plotting state frames
        self.canvas.clear()

        # --- SUN ENGINE ---
        self.canvas.add(Color(1, 0.65, 0, 1))
        self.canvas.add(Ellipse(pos=(cx - 25, cy - 25), size=(50, 50)))
        self.canvas.add(Color(1, 0.84, 0, 1))
        self.canvas.add(Ellipse(pos=(cx - 18, cy - 18), size=(36, 36)))

        # --- PLANET TRACKING SYSTEMS ---
        for name, data in self.planets_data.items():
            r = min_dim * data["or_scale"]
            px = cx + r * math.cos(self.angles[name])
            py = cy + r * math.sin(self.angles[name])

            # Draw Planet Sphere
            self.canvas.add(Color(*data["color"]))
            pr = data["p_rad"]
            self.canvas.add(Ellipse(pos=(px - pr, py - pr), size=(pr * 2, pr * 2)))

            if name == "earth":
                moon_r = min_dim * 0.025
                mx = px + moon_r * math.cos(self.angles["moon"])
                my = py + moon_r * math.sin(self.angles["moon"])
                self.canvas.add(Color(0.9, 0.9, 0.98, 1))
                self.canvas.add(Ellipse(pos=(mx - 2.5, my - 2.5), size=(5, 5)))
                if not self.is_paused:
                    self.angles["moon"] += 0.12

            if not self.is_paused:
                self.angles[name] += data["speed"]

        # --- SECRET EASTER EGG: CAT ---
        if self.cat_spawned:
            self.draw_space_cat(min_dim)

    def draw_space_cat(self, min_dim):
        """Draws the animated space cat using mobile hardware instructions"""
        cat_x = self.cat_x_ratio * self.width
        cat_y = self.height * 0.25
        
        bobbing = math.sin(self.cat_frame * 0.25) * 5
        y = cat_y + bobbing

        # Swing physics logic frameworks
        leg_swing_1 = math.sin(self.cat_frame * 0.3) * 20
        leg_swing_2 = -math.sin(self.cat_frame * 0.3) * 20
        tail_wave = math.sin(self.cat_frame * 0.15) * 12

        # 1. Plot Background Limbs
        self.draw_mobile_leg(cat_x + 15, y + 5, leg_swing_2, (0.53, 0.53, 0.6, 1))
        self.draw_mobile_leg(cat_x + 55, y + 5, leg_swing_1, (0.53, 0.53, 0.6, 1))

        # 2. Tail Mesh Assembly
        self.canvas.add(Color(0.83, 0.83, 0.83, 1))
        tail_points = [cat_x + 5, y + 15, cat_x - 10, y + 5 + tail_wave, cat_x - 15, y - 10 + tail_wave]
        self.canvas.add(Line(points=tail_points, width=3, cap="round"))

        # 3. Main Torso Base Chassis
        self.canvas.add(Color(0.83, 0.83, 0.83, 1))
        self.canvas.add(Ellipse(pos=(cat_x, y), size=(70, 32)))

        # 4. Plot Foreground Limbs
        self.draw_mobile_leg(cat_x + 20, y + 5, leg_swing_1, (0.83, 0.83, 0.83, 1))
        self.draw_mobile_leg(cat_x + 60, y + 5, leg_swing_2, (0.83, 0.83, 0.83, 1))

        # 5. Head Component Assembly
        hx, hy = cat_x + 52, y + 10
        self.canvas.add(Ellipse(pos=(hx, hy), size=(32, 30)))
        
        # Pointy Vector Space Ears
        self.canvas.add(Color(0.65, 0.65, 0.65, 1))
        self.canvas.add(Line(points=[hx + 4, hy + 24, hx + 2, hy + 38, hx + 14, hy + 26], close=True, width=1.5))
        self.canvas.add(Line(points=[hx + 18, hy + 26, hx + 28, hy + 38, hx + 26, hy + 24], close=True, width=1.5))

        # Neon Tracking Eye Matrix Sensors
        self.canvas.add(Color(0, 1, 0.8, 1))
        self.canvas.add(Ellipse(pos=(hx + 20, hy + 16), size=(4, 4)))

        # Move cat across relative tracking layout paths
        self.cat_x_ratio += 0.003
        if self.cat_x_ratio > 1.05:
            self.cat_x_ratio = -0.15
        self.cat_frame += 1

    def draw_mobile_leg(self, sx, sy, angle, color_tuple):
        """Converts polar transformations into clean system layouts on mobile viewports"""
        rad = math.radians(angle + 270) # 270 layout degrees maps downwards in Kivy space coordinates
        ex = sx + 22 * math.cos(rad)
        ey = sy + 22 * math.sin(rad)
        self.canvas.add(Color(*color_tuple))
        self.canvas.add(Line(points=[sx, sy, ex, ey], width=3.5, cap="round"))

class SolarSystemApp(App):
    def build(self):
        # Enforce dark space color background layout properties
        Window.clearcolor = (0.02, 0.02, 0.06, 1)
        return SolarSystemCanvas()

if __name__ == "__main__":
    SolarSystemApp().run()
