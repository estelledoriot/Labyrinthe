"""
Objets, Fonds et personnages du jeu
"""

import pygame


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut se déplacer dans 4 directions
    centerx_depart, centery_depart: position initiale du personnage (centre)
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self, centerx_depart: int, centery_depart: int, vitesse: int
    ) -> None:
        super().__init__()

        self.vitesse: int = vitesse

        self.image: pygame.Surface = pygame.image.load("pika.png")
        self.image = pygame.transform.scale_by(
            self.image, 23 / self.image.get_width()
        )

        self.centerx_depart: int = centerx_depart
        self.centery_depart: int = centery_depart
        self.rect: pygame.Rect = self.image.get_rect()
        self.revient_depart()

    def deplace_personnage(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.vitesse
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= self.vitesse
        elif pressed[pygame.K_UP]:
            self.rect.y -= self.vitesse
        elif pressed[pygame.K_DOWN]:
            self.rect.y += self.vitesse

    def revient_depart(self) -> None:
        """Replace le personnage à son point de départ"""
        self.rect.center = self.centerx_depart, self.centery_depart


class Objet(pygame.sprite.Sprite):
    """Objet à attrapper
    centerx_depart, centery_depart: position initiale de l'objet (centre)
    """

    def __init__(self, centerx_depart: int, centery_depart: int) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load("pokeball.png")
        self.image = pygame.transform.scale_by(
            self.image, 20 / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = centerx_depart, centery_depart


class Fond(pygame.sprite.Sprite):
    """Fond d'écran
    filename: nom du fichier contenant l'image de fond
    largeur: largeur de la fenêtre
    hauteur: hauteur de la fenêtre
    rescale: s'il faut redimensionner l'image ou non
    """

    def __init__(
        self,
        filename: str,
        largeur: int,
        hauteur: int,
        rescale: bool = False,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(filename)
        if rescale:
            self.image = pygame.transform.scale_by(
                self.image, largeur / self.image.get_width()
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = largeur // 2, hauteur // 2
