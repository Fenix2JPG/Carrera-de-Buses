import pygame
from PIL import Image, ImageOps
import random
import time

# Initialize Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080 / 2
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Bus:
    def __init__(self, img, x=0, y=0, color=(255, 0, 0), scale=1) -> None:
        """
        Constructor de la clase Bus.
        Carga una imagen, cambia su color y escala, y define las coordenadas iniciales.
        
        :param img: Ruta de la imagen del autobús.
        :param x: Posición inicial en el eje X.
        :param y: Posición inicial en el eje Y.
        :param color: Color nuevo del autobús.
        :param scale: Escala de la imagen.
        """
        self.img = pygame.image.load(img)  # Load the bus image
        self.x = x
        self.y = y
        self.color = color
        self.img = self.change_color(self.img, self.color)  # Change the image color

        # Scale the image
        original_width, original_height = self.img.get_size()
        self.width = int(original_width * scale)
        self.height = int(original_height * scale)
        self.img = pygame.transform.scale(self.img, (self.width, self.height))

    def update(self):
        """Actualiza la posición del autobús con un movimiento aleatorio."""
        self.x += random.uniform(0.1, 1)

    def draw(self):
        """Dibuja el autobús en la pantalla."""
        SCREEN.blit(self.img, (self.x, self.y))

    def change_color(self, image, new_color):
        """
        Cambia el color de la imagen, reemplazando píxeles que cumplen con un rango específico.
        
        :param image: Superficie de la imagen de entrada.
        :param new_color: Color a aplicar.
        :return: Superficie de imagen con el nuevo color.
        """
        colored_image = image.copy()
        for x in range(colored_image.get_width()):
            for y in range(colored_image.get_height()):
                r, g, b, a = colored_image.get_at((x, y))
                if r > 200 and g < 50 and b < 50:  # Rango para cambiar el color
                    colored_image.set_at((x, y), new_color + (a,))
        return colored_image

    def get_rect(self):
        """Devuelve el rectángulo que encierra al autobús."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Lista de autobuses con diferentes colores y posiciones iniciales
players = [
    Bus(img="bus.png", x=10, y=80, color=(255, 0, 0), scale=0.2),
    Bus(img="bus.png", x=10, y=190, color=(0, 255, 0), scale=0.2),
    Bus(img="bus.png", x=10, y=300, color=(0, 0, 255), scale=0.2),
]

# Bucle principal de la simulación de carrera
running = True
winner_index = []
tmp_time = time.time()
while len(winner_index) < 3 or time.time() - tmp_time < 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(winner_index) < 3:
        tmp_time = time.time()  # Marca el tiempo para verificar la finalización

    finish_line = pygame.Rect(1800, 0, 10, SCREEN_HEIGHT)  # Línea de meta

    # Actualiza la posición de cada autobús y verifica si llega a la línea de meta
    for index, player in enumerate(players):
        player.update()
        if finish_line.colliderect(player.get_rect()) and index not in winner_index:
            winner_index.append(index)  # Registra el índice de los ganadores

    # Dibuja la pantalla de la carrera
    SCREEN.fill((0, 0, 0))
    pygame.draw.rect(SCREEN, (255, 255, 255), finish_line)  # Dibuja la línea de meta
    for player in players:
        player.draw()
    pygame.display.flip()

# Configura la lista de ganadores para la pantalla final
winners = []
for index in winner_index:
    if index == 0:
        color = (255, 0, 0)
    elif index == 1:
        color = (0, 255, 0)
    elif index == 2:
        color = (0, 0, 255)
    winners.append(Bus(img="bus_f.png", color=color, scale=0.5))

# Ajusta la posición de los ganadores en la pantalla final
winners[0].x, winners[0].y = 843.4, 50
winners[1].x, winners[1].y = 543.5, 150
winners[2].x, winners[2].y = 1143.5, 250

# Configuración de fuentes y números para los ganadores
font = pygame.font.Font(None, 100)
text1 = font.render("1", True, (255, 255, 255))
text2 = font.render("2", True, (255, 255, 255))
text3 = font.render("3", True, (255, 255, 255))

# Bucle para mostrar la pantalla final de posiciones
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

    SCREEN.fill((0, 0, 0))
    for winner in winners:
        winner.draw()

    # Muestra los números de posición en la pantalla
    SCREEN.blit(text1, (941, 270))
    SCREEN.blit(text2, (641, 370))
    SCREEN.blit(text3, (1241, 470))
    pygame.display.flip()
