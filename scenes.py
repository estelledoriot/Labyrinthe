"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from elements import Objet, Personnage
from texte import Bouton, Message


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self) -> None:
        ...

    def joue_tour(self) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de labyrinthe"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.fond: pygame.Color = pygame.Color(255, 255, 255)
        self.labyrinthe: Objet = Objet(
            "images/laby.png", largeur // 2, hauteur // 2, largeur - 38
        )
        self.pikachu: Personnage = Personnage(30, 425, 23, 2)
        self.pokeball: Objet = Objet("images/pokeball.png", 510, 120, 20)
        self.start: int = pygame.time.get_ticks()
        self.timer: Message = Message(
            str(self.temps_restant), "font/Avdira.otf", 40
        )

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()
        largeur, _ = pygame.display.get_window_size()
        couleur_timer = pygame.Color(235, 80, 63)
        fenetre.fill(self.fond)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.pikachu.image, self.pikachu.rect)
        fenetre.blit(self.pokeball.image, self.pokeball.rect)
        self.timer.affiche(couleur_timer, largeur - 80, 60)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de pikachu
        self.pikachu.update()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.pikachu.revient_depart()

        # mise à jour du timer
        self.timer.texte = str(self.temps_restant)

    def passe_suivant(self) -> bool:
        """Teste si la partie est terminée"""
        return self.gagne or self.perdu

    @property
    def gagne(self) -> bool:
        """Vérifie si la partie est gagnée (le personnage touche la pokeball)"""
        return bool(pygame.sprite.collide_mask(self.pikachu, self.pokeball))

    @property
    def perdu(self) -> bool:
        """Vérifie si la partie est perdue (le temps est écoulé)"""
        return self.temps_restant < 0

    @property
    def temps_restant(self) -> int:
        """Calcule le temps restant"""
        return 30 - (pygame.time.get_ticks() - self.start) // 1000


class Fin:
    """Scène de fin"""

    def __init__(self, victoire: bool) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.fond: pygame.Color = pygame.Color(255, 255, 255)
        self.labyrinthe: Objet = Objet(
            "images/laby.png", largeur // 2, hauteur // 2, largeur - 38
        )
        self.masque: pygame.Surface = pygame.Surface(
            (largeur, hauteur), flags=pygame.SRCALPHA
        )
        self.masque.fill(pygame.Color(230, 230, 230, 200))
        self.message_fin: Message = (
            Message("Gagné !", "font/Avdira.otf", 100)
            if victoire
            else Message("Perdu ...", "font/Avdira.otf", 100)
        )
        self.bouton_rejouer: Bouton = Bouton(
            Message("Rejouer", "font/Avdira.otf", 50)
        )

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        largeur, _ = pygame.display.get_window_size()

        fenetre.fill(self.fond)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.masque, (0, 0))
        couleur_message = pygame.Color(169, 70, 55)
        self.message_fin.affiche(couleur_message, largeur // 2, 150)
        couleur_rejouer = (
            pygame.Color(255, 255, 255)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(240, 240, 240)
        )
        couleur_fond = (
            pygame.Color(80, 80, 80)
            if self.bouton_rejouer.touche_souris()
            else pygame.Color(50, 50, 50)
        )
        self.bouton_rejouer.affiche(
            couleur_rejouer, couleur_fond, largeur // 2, 400
        )

    def joue_tour(self) -> None:
        """Rien"""

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.bouton_rejouer.est_clique()
