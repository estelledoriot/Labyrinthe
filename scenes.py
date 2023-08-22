"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from elements import Objet, Personnage
from texte import Bouton, Message


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de labyrinthe"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.labyrinthe: Objet = Objet(
            "laby.png", largeur // 2, hauteur // 2, largeur - 38
        )
        self.pikachu: Personnage = Personnage(30, 425, 23, 2)
        self.pokeball: Objet = Objet("pokeball.png", 510, 120, 20)

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        blanc = pygame.Color(255, 255, 255)
        fenetre.fill(blanc)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.pikachu.image, self.pikachu.rect)
        fenetre.blit(self.pokeball.image, self.pokeball.rect)

    def passe_suivant(self) -> bool:
        """Joue un tour du jeu et renvoie si la partie est terminée"""
        # déplacements de pikachu
        self.pikachu.update()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.pikachu.revient_depart()

        # collision avec la pokeball
        return bool(pygame.sprite.collide_mask(self.pikachu, self.pokeball))


class Fin:
    """Scène de fin"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.fond_fin: Objet = Objet(
            "fireworks.jpg", largeur // 2, hauteur // 2, largeur
        )
        self.message_gagne: Message = Message("Gagné !", "Avdira.otf", 100)
        self.rejouer: Bouton = Bouton(Message("Rejouer", "Avdira.otf", 50))

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche la scène de fin"""
        blanc = pygame.Color(255, 255, 255)
        jaune = pygame.Color(255, 255, 0)
        noir = pygame.Color(0, 0, 0)
        _, hauteur = pygame.display.get_window_size()

        fenetre.blit(self.fond_fin.image, self.fond_fin.rect)
        self.message_gagne.affiche(blanc, hauteur // 2, 150)
        couleur = jaune if self.rejouer.touche_souris() else blanc
        self.rejouer.affiche(couleur, noir, hauteur // 2, 400)

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.rejouer.est_clique()
