import pygame
import random
import numpy as np

pygame.init()
pygame.mixer.init()

# --- Configuración ---
ANCHO = 600
ALTO = 700
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Nave vs Invasores Espaciales")

# --- Colores ---
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 150, 255)
AMARILLO = (255, 255, 0)
ROJO_ENEMIGO = (255, 50, 50)
ROSA_CUPULA = (255, 200, 200)
NARANJA = (255, 140, 0)
GRIS = (180,180,180)

# --- Fuentes ---
FUENTE = pygame.font.SysFont("comicsans", 30)
FUENTE_GAMEOVER = pygame.font.SysFont("comicsans", 60)

# --- Generar sonidos ---
def generar_sonido(frecuencia=440, duracion=0.1, volumen=0.5):
    framerate = 44100
    t = np.linspace(0, duracion, int(framerate * duracion), endpoint=False)
    onda = np.sin(2 * np.pi * frecuencia * t) * 32767
    onda = onda.astype(np.int16)
    onda_stereo = np.column_stack([onda, onda])
    sonido = pygame.sndarray.make_sound(onda_stereo)
    sonido.set_volume(volumen)
    return sonido

SONIDO_DISPARO = generar_sonido(880, 0.05)
SONIDO_EXPLOSION = generar_sonido(200, 0.2)

# --- Imágenes con formas ---
# Nave del jugador estilo F-24
NAVE_IMG = pygame.Surface((60, 50), pygame.SRCALPHA)
# Cuerpo alargado
pygame.draw.polygon(NAVE_IMG, AZUL, [
    (30,0),  # punta
    (45,10),
    (50,25),
    (45,40),
    (30,50),
    (15,40),
    (10,25),
    (15,10)
])
# Alas
pygame.draw.polygon(NAVE_IMG, GRIS, [(0,20),(15,25),(0,30)])
pygame.draw.polygon(NAVE_IMG, GRIS, [(60,20),(45,25),(60,30)])
# Cockpit
pygame.draw.circle(NAVE_IMG, BLANCO, (30,20), 4)

# Bala con punta triangular
BALA_IMG = pygame.Surface((5, 15), pygame.SRCALPHA)
pygame.draw.rect(BALA_IMG, AMARILLO, (0, 0, 5, 15))
pygame.draw.polygon(BALA_IMG, (255,200,0), [(0,0),(2.5,-5),(5,0)])

# Corazón de vida
CORAZON_IMG = pygame.Surface((20, 20), pygame.SRCALPHA)
pygame.draw.polygon(CORAZON_IMG, ROJO, [(10,0),(20,7),(16,20),(4,20),(0,7)])

# --- Enemigos futuristas invertidos ---
def crear_enemigo_futurista():
    img = pygame.Surface((50, 40), pygame.SRCALPHA)
    # Cuerpo principal invertido (punta hacia abajo)
    pygame.draw.polygon(img, ROJO_ENEMIGO, [
        (25,40),   # punta inferior
        (35,30),   # ala inferior derecha
        (40,0),    # cola derecha
        (25,10),   # centro trasero
        (10,0),    # cola izquierda
        (15,30)    # ala inferior izquierda
    ])
    # Detalles de luces/cockpit
    pygame.draw.circle(img, ROSA_CUPULA, (25,30), 4)
    pygame.draw.circle(img, NARANJA, (25,25), 2)
    return img

# --- Jugador ---
class Jugador:
    def __init__(self):
        self.x = ANCHO // 2 - 30
        self.y = ALTO - 100
        self.vel = 6
        self.vidas = 5
        self.balas = []

    def mover(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < ANCHO - 60:
            self.x += self.vel

    def disparar(self):
        bala = pygame.Rect(self.x + 27, self.y, 5, 15)
        self.balas.append(bala)
        SONIDO_DISPARO.play()

    def actualizar_balas(self, enemigos):
        puntos = 0
        for bala in self.balas[:]:
            bala.y -= 10
            if bala.y < 0:
                self.balas.remove(bala)
            else:
                for enemigo in enemigos[:]:
                    enemigo_rect = pygame.Rect(enemigo.x, enemigo.y, 50, 40)
                    if bala.colliderect(enemigo_rect):
                        enemigos.remove(enemigo)
                        self.balas.remove(bala)
                        SONIDO_EXPLOSION.play()
                        puntos += 1
                        break
        return puntos

    def dibujar(self, ventana):
        ventana.blit(NAVE_IMG, (self.x, self.y))
        for bala in self.balas:
            ventana.blit(BALA_IMG, (bala.x, bala.y))

# --- Dibujar vidas ---
def dibujar_vidas(ventana, vidas):
    for i in range(vidas):
        ventana.blit(CORAZON_IMG, (10 + i * 25, 10))

# --- Clase enemigo ---
class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 2
        self.img = crear_enemigo_futurista()

    def mover(self):
        self.y += self.vel

    def dibujar(self, ventana):
        ventana.blit(self.img, (self.x, self.y))

# --- Función principal ---
def main():
    reloj = pygame.time.Clock()
    jugador = Jugador()
    enemigos = [Enemigo(random.randint(0, ANCHO-50), random.randint(-150, -40)) for _ in range(5)]
    corriendo = True
    puntos = 0

    while corriendo:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.disparar()

        keys = pygame.key.get_pressed()
        jugador.mover(keys)

        puntos += jugador.actualizar_balas(enemigos)

        # Mover enemigos
        for enemigo in enemigos[:]:
            enemigo.mover()
            if enemigo.y > ALTO:
                enemigos.remove(enemigo)
                jugador.vidas -= 1

        # Generar nuevos enemigos
        if len(enemigos) < 5:
            enemigos.append(Enemigo(random.randint(0, ANCHO-50), random.randint(-150, -40)))

        # Dibujar todo
        VENTANA.fill(NEGRO)
        jugador.dibujar(VENTANA)
        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)
        dibujar_vidas(VENTANA, jugador.vidas)

        texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, BLANCO)
        VENTANA.blit(texto_puntos, (ANCHO - 150, 10))

        pygame.display.flip()

        if jugador.vidas <= 0:
            corriendo = False

    VENTANA.fill(NEGRO)
    texto_gameover = FUENTE_GAMEOVER.render("GAME OVER", True, ROJO)
    VENTANA.blit(texto_gameover, (ANCHO//2 - texto_gameover.get_width()//2, ALTO//2 - texto_gameover.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()

# --- Ejecutar ---
if __name__ == "__main__":
    main()
