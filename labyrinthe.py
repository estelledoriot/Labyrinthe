"""Jeu de labyrinthe
    - déplace le personnage en utilisant les flèches directionnelles
    - attrape la pokeball pour gagner
    - si tu touches les murs, tu retournes au point de départ
"""

# TODO: ajout sons
# TODO: ajout fps
# TODO: vérifier Protocol

from typing import Protocol

import pygame


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut se déplacer dans 4 directions
    x_depart, y_depart: position initiale du personnage
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(self, x_depart: int, y_depart: int, vitesse: int) -> None:
        self.vitesse: int = vitesse

        self.image: pygame.Surface = pygame.image.load("pika.png")
        self.image = pygame.transform.scale_by(
            self.image, 23 / self.image.get_width()
        )

        self.x_depart: int = x_depart
        self.y_depart: int = y_depart
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = self.x_depart
        self.rect.y = self.y_depart

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
        self.rect.x = self.x_depart
        self.rect.y = self.y_depart


class Objet(pygame.sprite.Sprite):
    """Objet à attrapper
    x_depart, y_depart: position initiale de l'objet
    """

    def __init__(self, x_depart: int, y_depart: int) -> None:
        self.image: pygame.Surface = pygame.image.load("pokeball.png")
        self.image = pygame.transform.scale_by(
            self.image, 20 / self.image.get_width()
        )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x_depart
        self.rect.y = y_depart


class Fond(pygame.sprite.Sprite):
    """Fond d'écran
    filename: nom du fichier contenant l'image de fond
    x_center, y_center: position du centre de l'image
    rescale: s'il faut redimensionner l'image ou non
    """

    def __init__(
        self,
        filename: str,
        x_center: int,
        y_center: int,
        rescale: bool = False,
    ) -> None:
        self.image: pygame.Surface = pygame.image.load(filename)
        if rescale:
            self.image = pygame.transform.scale_by(
                self.image, 550 / self.image.get_width()
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = x_center, y_center


class Message:
    """Message
    texte: texte à afficher
    nom_police: nom du fichier de police pour afficher le message
    taille: taille du texte
    """

    def __init__(self, texte: str, nom_police: str, taille: int) -> None:
        self.police: pygame.font.Font = pygame.font.Font(nom_police, taille)
        self.texte: str = texte
        self.surface: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.surface.get_rect()

    def genere_surface(
        self, couleur: pygame.Color, x_center: int, y_center: int
    ):
        """Génère le message"""
        self.surface = self.police.render(self.texte, True, couleur)
        self.rect = self.surface.get_rect(center=(x_center, y_center))

    def affiche(
        self,
        fenetre: pygame.Surface,
        couleur: pygame.Color,
        x_center: int,
        y_center: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        self.genere_surface(couleur, x_center, y_center)
        fenetre.blit(self.surface, self.rect)


class Bouton:
    """Bouton
    message: texte du bouton
    """

    def __init__(self, message: Message) -> None:
        self.message: Message = message
        self.bouton: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    def affiche(
        self,
        fenetre: pygame.Surface,
        couleur: pygame.Color,
        couleur_fond: pygame.Color,
        x_center: int,
        y_center: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        self.message.genere_surface(couleur, x_center, y_center)
        self.bouton = self.message.rect.inflate(15, 15)
        self.bouton.center = (x_center, y_center)
        pygame.draw.rect(fenetre, couleur_fond, self.bouton, border_radius=20)
        self.message.affiche(fenetre, couleur, x_center, y_center)

    def touche_souris(self) -> bool:
        """Détermine si la souris touche le bouton"""
        return self.bouton.collidepoint(pygame.mouse.get_pos())

    def est_clique(self) -> bool:
        """Détermine si on clique sur le bouton"""
        return self.touche_souris() and any(
            evenement.type == pygame.MOUSEBUTTONDOWN
            for evenement in pygame.event.get()
        )


class Scene(Protocol):
    """Scène du jeu"""

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche les léléments de la scène"""
        ...

    def passe_suivant(self) -> bool:
        """Vérifie s'il faut passer à la scène suivante"""
        ...


class Partie:
    """Partie de labyrinthe"""

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.labyrinthe: Fond = Fond("laby.png", largeur // 2, hauteur // 2)
        self.pikachu: Personnage = Personnage(20, 415, 1)
        self.pokeball: Objet = Objet(510, 110)

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
        self.pikachu.deplace_personnage()

        # collision avec le labyrinthe
        if pygame.sprite.collide_mask(self.pikachu, self.labyrinthe):
            self.pikachu.revient_depart()

        # collision avec la pokeball
        return bool(pygame.sprite.collide_mask(self.pikachu, self.pokeball))


class Fin:
    """Scène de fin"""

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.fond_fin: Fond = Fond(
            "fireworks.jpg", largeur // 2, hauteur // 2, True
        )
        self.message_gagne: Message = Message("Gagné !", "Avdira.otf", 100)
        self.rejouer: Bouton = Bouton(Message("Rejouer", "Avdira.otf", 50))
        self.hauteur: int = hauteur

    def affiche_scene(self, fenetre: pygame.Surface) -> None:
        """Affiche la scène de fin"""
        blanc = pygame.Color(255, 255, 255)
        jaune = pygame.Color(255, 255, 0)
        noir = pygame.Color(0, 0, 0)

        fenetre.blit(self.fond_fin.image, self.fond_fin.rect)
        self.message_gagne.affiche(fenetre, blanc, self.hauteur // 2, 150)
        couleur = jaune if self.rejouer.touche_souris() else blanc
        self.rejouer.affiche(fenetre, couleur, noir, self.hauteur // 2, 400)

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.rejouer.est_clique()


class Fenetre:
    """Jeu"""

    def __init__(self) -> None:
        pygame.init()

        # fenêtre
        self.largeur: int = 550
        self.hauteur: int = 550
        self.fenetre: pygame.Surface = pygame.display.set_mode(
            (self.largeur, self.hauteur)
        )
        pygame.display.set_caption("Labyrinthe")
        pygame.display.set_icon(pygame.image.load("pika.png"))

        # état
        self.en_cours: bool = True
        self.scene: Scene = Partie(self.largeur, self.hauteur)

    def scene_suivante(self):
        """Passe à la scène suivante"""
        if self.en_cours:
            self.scene = Fin(self.largeur, self.hauteur)
            self.en_cours = False
        else:
            self.scene = Partie(self.largeur, self.hauteur)
            self.en_cours = True

    def jouer(self) -> None:
        """Lance le jeu"""
        while True:
            if self.scene.passe_suivant():
                self.scene_suivante()

            # quitter
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return

            # affichage
            self.scene.affiche_scene(self.fenetre)
            pygame.display.flip()


if __name__ == "__main__":
    jeu = Fenetre()
    jeu.jouer()
    pygame.quit()
