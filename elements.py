"""
Objets et personnages du jeu
"""

import pygame


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut se déplacer dans 4 directions
    centerx_depart, centery_depart: position initiale du personnage (centre)
    taille: taille du personnage à l'écran
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        centerx_depart: int,
        centery_depart: int,
        taille: int,
        vitesse: int,
    ) -> None:
        super().__init__()

        self.vitesse: int = vitesse

        self.image: pygame.Surface = pygame.image.load(
            "images/pika.png"
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, taille / self.image.get_width()
        )
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        self.depart: tuple[int, int] = centerx_depart, centery_depart
        self.rect: pygame.Rect = self.image.get_rect()
        self.revient_depart()

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        pygame.sprite.Sprite.update(self)

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
        self.rect.center = self.depart


class Objet(pygame.sprite.Sprite):
    """Objet du jeu
    filename: nom du fichier contenant l'objet
    centerx_depart, centery_depart: position initiale de l'objet (centre)
    largeur_objet: largeur de l'objet à l'écran
    """

    def __init__(
        self,
        filename: str,
        centerx_depart: int,
        centery_depart: int,
        largeur_objet: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, largeur_objet / self.image.get_width()
        )
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)
        self.rect: pygame.Rect = self.image.get_rect(
            center=(centerx_depart, centery_depart)
        )
