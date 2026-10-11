
import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Target Aim Trainer - Pygame Version")

clock = pygame.time.Clock()
FPS = 60


def main():
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if engine.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        engine.difficulty = "Easy"
                        engine.reset()
                    elif event.key == pygame.K_2:
                        engine.difficulty = "Medium"
                        engine.reset()
                    elif event.key == pygame.K_3:
                        engine.difficulty = "Hard"
                        engine.reset()
                    elif event.key == pygame.K_r:
                        engine.reset()
                continue

            engine.handle_event(event)

        if not running:
            break

        engine.update()
        engine.render(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
