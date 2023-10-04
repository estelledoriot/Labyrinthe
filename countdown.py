"""
classe Countdown
"""

import pygame


class Countdown(pygame.sprite.Sprite):
    """compte à rebours
    total_time: temps total pour jouer
    position: position du timer"""

    def __init__(self, total_time: int, position: tuple[int, int]) -> None:
        super().__init__()
        self.start_time: int = pygame.time.get_ticks()
        self.total_time: int = total_time

        self.font: pygame.font.Font = pygame.font.Font("font/Avdira.otf", 40)
        self.couleur_timer = pygame.Color(235, 80, 63)
        self.image: pygame.Surface = self.font.render(
            str(self.temps_restant), True, self.couleur_timer
        )
        self.position = position
        self.rect = self.image.get_rect(center=self.position)

    @property
    def temps_restant(self) -> int:
        """Calcule le temps restant"""
        return (
            self.total_time
            - (pygame.time.get_ticks() - self.start_time) // 1000
        )

    def update(self) -> None:
        """Mise à jour de la valeur du compte à rebours"""
        self.image = self.font.render(
            str(self.temps_restant), True, self.couleur_timer
        )
        self.rect = self.image.get_rect(center=self.position)
