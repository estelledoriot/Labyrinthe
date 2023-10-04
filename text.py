"""
classe Text
"""

import pygame


class Text:
    """Texte
    text: texte à afficher
    position: position du texte
    """

    def __init__(self, text: str, position: tuple[int, int]) -> None:
        self.font: pygame.font.Font = pygame.font.Font("font/Avdira.otf", 50)
        self.text: str = text
        self.color: pygame.Color = pygame.Color(169, 70, 55)
        self.image: pygame.Surface = self.font.render(
            self.text, True, self.color
        )
        self.position: tuple[int, int] = position
        self.rect: pygame.Rect = self.image.get_rect(center=position)

    def update_text(self, text: str):
        """Génère le message"""
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.position)
