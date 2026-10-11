
import pygame
import random
import math
import array
from .target import Target

WHITE = (255, 255, 255)
RED = (220, 60, 60)
DARK_GRAY = (35, 35, 40)

DIFFICULTIES = {
    "Easy": {"lifespan": 120, "base_radius": 45, "min_radius": 18},
    "Medium": {"lifespan": 90, "base_radius": 40, "min_radius": 12},
    "Hard": {"lifespan": 60, "base_radius": 35, "min_radius": 8},
}


def make_tone(frequency, duration=0.12, volume=0.3):
    sample_rate = 22050
    samples = int(sample_rate * duration)
    buffer = array.array("h")

    for i in range(samples):
        fade = 1.0 - i / samples
        sample = int(
            32767 * volume * fade
            * math.sin(2 * math.pi * frequency * i / sample_rate)
        )
        buffer.append(sample)

    return pygame.mixer.Sound(buffer=buffer)


class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height
        self.margin = 60
        self.hud_height = 60
        self.round_seconds = 30
        self.font = pygame.font.SysFont("Arial", 26)
        self.large_font = pygame.font.SysFont("Arial", 40)
        self.difficulty = difficulty

        self.hit_sound = None
        self.miss_sound = None
        self.end_sound = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.hit_sound = make_tone(880)
            self.miss_sound = make_tone(220)
            self.end_sound = make_tone(440, duration=0.4)
        except pygame.error:
            print("Audio unavailable; continuing without sound.")

        self.reset()

    def play_sound(self, sound):
        if sound is not None:
            sound.play()

    def reset(self):
        self.time_left_frames = self.round_seconds * 60
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.game_over = False
        self.target = self._spawn_target()

    def _spawn_target(self):
        settings = DIFFICULTIES[self.difficulty]
        x = random.randint(self.margin, self.width - self.margin)
        y = random.randint(
            self.margin + self.hud_height,
            self.height - self.margin,
        )
        return Target(
            x,
            y,
            base_radius=settings["base_radius"],
            min_radius=settings["min_radius"],
            lifespan_frames=settings["lifespan"],
        )

    def handle_event(self, event):
        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        if self.target.contains_point(*pos):
            self.hits += 1
            self.score += 1
            self.play_sound(self.hit_sound)
            self.target = self._spawn_target()
        else:
            self.misses += 1
            self.play_sound(self.miss_sound)

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True
            self.play_sound(self.end_sound)
            return

        self.target.update()

        if self.target.expired():
            self.misses += 1
            self.play_sound(self.miss_sound)
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses
        return round(100 * self.hits / total, 1) if total else 0.0

    def render(self, screen):
        screen.fill(DARK_GRAY)

        if self.game_over:
            lines = [
                ("GAME OVER", self.large_font),
                (f"Final Score: {self.score}", self.font),
                (f"Accuracy: {self.accuracy()}%", self.font),
                ("1 - Easy    2 - Medium    3 - Hard", self.font),
                ("R - Replay    ESC - Exit", self.font),
            ]
            y = 130

            for message, font in lines:
                text = font.render(message, True, WHITE)
                screen.blit(
                    text,
                    text.get_rect(center=(self.width // 2, y)),
                )
                y += 55
            return

        radius = int(self.target.visual_radius())
        pygame.draw.circle(
            screen, RED, (self.target.x, self.target.y), radius
        )
        pygame.draw.circle(
            screen, WHITE, (self.target.x, self.target.y), radius, 2
        )

        screen.blit(
            self.font.render(f"Score: {self.score}", True, WHITE),
            (10, 10),
        )
        seconds_left = max(0, self.time_left_frames // 60)
        screen.blit(
            self.font.render(f"Time: {seconds_left}s", True, WHITE),
            (self.width - 140, 10),
        )
        screen.blit(
            self.font.render(
                f"Accuracy: {self.accuracy()}%", True, WHITE
            ),
            (self.width // 2 - 90, 10),
        )
