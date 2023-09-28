"""
Gestion des scènes du jeu
"""

from typing import Protocol

import pygame

from bouton import Bouton
from countdown import Countdown
from objet import Objet
from personnage import Personnage
from texte import Texte


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
        self.countdown: Countdown = Countdown(30)
        self.son: pygame.mixer.Sound = pygame.mixer.Sound("sounds/crunch.wav")
        self.son.set_volume(0.25)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()
        fenetre.fill(self.fond)
        fenetre.blit(self.labyrinthe.image, self.labyrinthe.rect)
        fenetre.blit(self.pikachu.image, self.pikachu.rect)
        fenetre.blit(self.pokeball.image, self.pokeball.rect)
        self.countdown.draw()

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de pikachu
        self.pikachu.update()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.son.play()
            self.pikachu.revient_depart()

        # mise à jour du timer
        self.countdown.update_etiquette()

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
        return self.countdown.temps_restant < 0


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

        self.message_fin: Texte = (
            Texte("Gagné !", "font/Avdira.otf", 100)
            if victoire
            else Texte("Perdu ...", "font/Avdira.otf", 100)
        )
        self.bouton_rejouer: Bouton = Bouton(
            Texte("Rejouer", "font/Avdira.otf", 50)
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
        if self.passe_suivant():
            self.son_bouton.play()

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.bouton_rejouer.est_clique()
