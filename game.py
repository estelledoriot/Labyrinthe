"""
Gestion des scènes du jeu
"""

from enum import Enum

import pygame

from button import Button
from countdown import Countdown
from filled_surface import FilledSurface
from object import Object
from pikachu import Pikachu
from text import Text

Stage = Enum("Stage", ["RUNNING", "END", "TERMINATE"])


class Game:
    """Une partie de labyrinthe"""

    def __init__(self, width: int, height: int) -> None:
        # décors
        self.background: pygame.Color = pygame.Color(255, 255, 255)
        self.labyrinthe: Object = Object(
            "images/laby.png", (width // 2, height // 2), width - 38
        )
        self.opaque_surface: FilledSurface = FilledSurface(
            pygame.Color(230, 230, 230, 200)
        )

        # game elements
        self.pikachu: Pikachu = Pikachu((30, 425), 23, 2)
        self.pokeball: Object = Object("images/pokeball.png", (510, 120), 20)
        self.countdown: Countdown = Countdown(30, (width - 80, 60))
        self.game_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.game_elements.add(
            self.labyrinthe, self.pikachu, self.pokeball, self.countdown
        )

        # end elements
        self.end_message: Text = Text("", (width // 2, 150))
        self.restart_button: Button = Button(
            "Rejouer", (250, 80), (width // 2, 400)
        )
        self.end_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.end_elements.add(
            self.opaque_surface, self.end_message, self.restart_button
        )

        # sons
        self.collision_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/crunch.wav"
        )
        self.collision_sound.set_volume(0.25)
        self.end_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/gong.wav"
        )
        self.end_sound.set_volume(0.25)
        self.button_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.button_sound.set_volume(0.25)

        # stage
        self.stage: Stage = Stage.RUNNING

    @property
    def won(self) -> bool:
        """Vérifie si la partie est gagnée (le personnage touche la pokeball)"""
        return bool(pygame.sprite.collide_mask(self.pikachu, self.pokeball))

    @property
    def lost(self) -> bool:
        """Vérifie si la partie est perdue (le temps est écoulé)"""
        return self.countdown.time_finished

    def run_game(self) -> None:
        """Fait tourner le jeu"""
        # mise à jour des éléments du jeu
        self.game_elements.update()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.collision_sound.play()
            self.pikachu.goto_start()

        # fin du jeu
        if self.won or self.lost:
            self.stage = Stage.END
            self.end_sound.play()
            self.end_message.update_text(
                "Gagné !" if self.won else "Perdu ..."
            )

    def draw_game(self, screen: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        screen.fill(self.background)
        self.game_elements.draw(screen)

    def run_end(self) -> None:
        """Fait tourner l'écran de fin"""
        # mise à jour des éléments de l'écran de fin
        self.restart_button.update()

        # clic sur le bouton pour commencer une nouvelle partie
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.restart_button.touch_mouse():
                self.button_sound.play()
                self.stage = Stage.TERMINATE

    def draw_end(self, screen: pygame.Surface) -> None:
        """Affiche les éléments de l'écran de fin"""
        screen.fill(self.background)
        self.game_elements.draw(screen)
        self.end_elements.draw(screen)
