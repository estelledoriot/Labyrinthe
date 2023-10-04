"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from button import Button
from countdown import Countdown
from object import Object
from pikachu import Pikachu
from text import Text


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
        self.labyrinthe: Object = Object(
            "images/laby.png", (largeur // 2, hauteur // 2), largeur - 38
        )
        self.pikachu: Pikachu = Pikachu((30, 425), 23, 2)
        self.pokeball: Object = Object("images/pokeball.png", (510, 120), 20)
        self.countdown: Countdown = Countdown(30, (largeur - 80, 60))
        self.son: pygame.mixer.Sound = pygame.mixer.Sound("sounds/crunch.wav")
        self.son.set_volume(0.25)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()
        fenetre.fill(self.fond)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.pikachu.image, self.pikachu.rect)
        fenetre.blit(self.pokeball.image, self.pokeball.rect)
        fenetre.blit(self.countdown.image, self.countdown.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de pikachu
        self.pikachu.update()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.son.play()
            self.pikachu.goto_start()

        # mise à jour du timer
        self.countdown.update()

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
        return self.countdown.temps_restant <= 0


class Fin:
    """Scène de fin"""

    def __init__(self, victoire: bool) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.fond: pygame.Color = pygame.Color(255, 255, 255)
        self.labyrinthe: Object = Object(
            "images/laby.png", (largeur // 2, hauteur // 2), largeur - 38
        )
        self.masque: pygame.Surface = pygame.Surface(
            (largeur, hauteur), flags=pygame.SRCALPHA
        )
        self.masque.fill(pygame.Color(230, 230, 230, 200))

        self.message_fin: Text = (
            Text("Gagné !", (largeur // 2, 150))
            if victoire
            else Text("Perdu ...", (largeur // 2, 150))
        )
        self.bouton_rejouer: Button = Button(
            "Rejouer", (250, 80), (largeur // 2, 400)
        )

        self.son_fin: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/gong.wav"
        )
        self.son_fin.set_volume(0.25)
        self.son_fin.play()

        self.son_bouton: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.son_bouton.set_volume(0.25)
        self.next: bool = False

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()
        fenetre.fill(self.fond)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.masque, (0, 0))
        fenetre.blit(self.message_fin.image, self.message_fin.rect)
        fenetre.blit(self.bouton_rejouer.image, self.bouton_rejouer.rect)

    def joue_tour(self) -> None:
        """Rien"""
        self.bouton_rejouer.update()
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.bouton_rejouer.touch_mouse():
                self.son_bouton.play()
                self.next = True

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.next
