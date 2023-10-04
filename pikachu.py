"""
classe Pikachu
"""

import pygame


class Pikachu(pygame.sprite.Sprite):
    """Personnage du jeu (pikachu)
    Peut se déplacer dans 4 directions
    start_center: position initiale du personnage (centre)
    width: taille du personnage à l'écran
    speed: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        start_center: tuple[int, int],
        width: int,
        speed: int,
    ) -> None:
        super().__init__()

        # image
        self.image: pygame.Surface = pygame.image.load(
            "images/pika.png"
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, width / self.image.get_width()
        )
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        # position
        self.start_position: tuple[int, int] = start_center
        self.rect: pygame.Rect = self.image.get_rect()
        self.goto_start()

        # vitesse
        self.speed: int = speed

    def goto_start(self) -> None:
        """Replace le personnage à son point de départ"""
        self.rect.center = self.start_position

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        elif pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
