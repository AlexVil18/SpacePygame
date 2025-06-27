import pygame
import random
import math
import json
import os
from typing import List, Tuple, Optional

# Inicializar PyGame
pygame.init()
pygame.mixer.init()

# Constantes del juego
ANCHO = 800
ALTO = 600
FPS = 60

# Colores con gradientes
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 50)
AZUL = (50, 50, 255)
AMARILLO = (255, 255, 50)
CYAN = (50, 255, 255)
MAGENTA = (255, 50, 255)
GRIS = (128, 128, 128)
NARANJA = (255, 165, 0)
VIOLETA = (138, 43, 226)
VERDE_LIMA = (50, 205, 50)
AZUL_OSCURO = (25, 25, 112)
ROJO_OSCURO = (139, 0, 0)
DORADO = (255, 215, 0)

# Colores para efectos
AZUL_NEON = (0, 191, 255)
ROSA_NEON = (255, 20, 147)
VERDE_NEON = (57, 255, 20)
PURPURA_NEON = (191, 0, 255)

class Estrella:
    """Clase para las estrellas del fondo animado"""
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.velocidad = random.uniform(0.5, 3)
        self.brillo = random.randint(50, 255)
        self.tamaño = random.randint(1, 3)
        self.color = random.choice([BLANCO, CYAN, AMARILLO, AZUL_NEON])

    def actualizar(self):
        self.y += self.velocidad
        if self.y > ALTO:
            self.y = -10
            self.x = random.randint(0, ANCHO)
            self.velocidad = random.uniform(0.5, 3)

    def dibujar(self, pantalla):
        # Efecto de brillo parpadeante
        brillo_actual = int(self.brillo + 30 * math.sin(pygame.time.get_ticks() * 0.01))
        brillo_actual = max(50, min(255, brillo_actual))

        color_con_brillo = tuple(min(255, int(c * brillo_actual / 255)) for c in self.color)
        pygame.draw.circle(pantalla, color_con_brillo, (int(self.x), int(self.y)), self.tamaño)

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 6
        self.ancho = 40
        self.alto = 50
        self.vida = 100
        self.vida_maxima = 100
        self.municion = 50
        self.municion_maxima = 50
        self.puntos = 0
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.escudo = 0
        self.escudo_maximo = 100
        self.tiempo_invulnerable = 0
        self.poder_especial = 0  # 0-100
        self.arma_nivel = 1
        self.velocidad_disparo = 0
        self.efectos_activos = []

    def mover(self, teclas, mouse_pos=None):
        # Movimiento con teclado
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.x > 0:
                self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.x < ANCHO - self.ancho:
                self.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            if self.y > 0:
                self.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            if self.y < ALTO - self.alto:
                self.y += self.velocidad

        # Movimiento con mouse
        if mouse_pos and pygame.mouse.get_pressed()[2]:  # Botón derecho
            mouse_x, mouse_y = mouse_pos
            # Movimiento suave hacia el mouse
            diff_x = mouse_x - (self.x + self.ancho // 2)
            diff_y = mouse_y - (self.y + self.alto // 2)

            if abs(diff_x) > 5:
                self.x += diff_x * 0.1
            if abs(diff_y) > 5:
                self.y += diff_y * 0.1

            # Mantener dentro de los límites
            self.x = max(0, min(ANCHO - self.ancho, self.x))
            self.y = max(0, min(ALTO - self.alto, self.y))

        self.rect.x = self.x
        self.rect.y = self.y

        # Actualizar tiempo de invulnerabilidad
        if self.tiempo_invulnerable > 0:
            self.tiempo_invulnerable -= 1

        # Actualizar velocidad de disparo
        if self.velocidad_disparo > 0:
            self.velocidad_disparo -= 1

    def disparar(self):
        if self.municion > 0 and self.velocidad_disparo <= 0:
            proyectiles = []

            if self.arma_nivel == 1:
                # Disparo simple
                self.municion -= 1
                self.velocidad_disparo = 10
                proyectiles.append(Proyectil(self.x + self.ancho // 2, self.y, -12, CYAN, "laser"))

            elif self.arma_nivel == 2:
                # Disparo doble
                self.municion -= 2
                self.velocidad_disparo = 8
                proyectiles.append(Proyectil(self.x + 10, self.y, -12, CYAN, "laser"))
                proyectiles.append(Proyectil(self.x + self.ancho - 10, self.y, -12, CYAN, "laser"))

            elif self.arma_nivel >= 3:
                # Disparo triple
                self.municion -= 3
                self.velocidad_disparo = 6
                proyectiles.append(Proyectil(self.x + self.ancho // 2, self.y, -12, CYAN, "laser"))
                proyectiles.append(Proyectil(self.x + 10, self.y + 10, -10, AZUL_NEON, "laser"))
                proyectiles.append(Proyectil(self.x + self.ancho - 10, self.y + 10, -10, AZUL_NEON, "laser"))

            return proyectiles
        return []

    def usar_poder_especial(self):
        if self.poder_especial >= 100:
            self.poder_especial = 0
            # Poder especial: Láser devastador
            proyectiles = []
            for i in range(20):
                angle = (i - 10) * 0.2
                vel_x = 15 * math.sin(angle)
                vel_y = -20 * math.cos(angle)
                proyectiles.append(ProyectilEspecial(
                    self.x + self.ancho // 2,
                    self.y,
                    vel_x, vel_y,
                    DORADO,
                    "devastador"
                ))
            return proyectiles
        return []

    def recargar(self):
        self.municion = self.municion_maxima
        self.velocidad_disparo = 30  # Penalización por recargar

    def recibir_danio(self, danio):
        if self.tiempo_invulnerable > 0:
            return

        if self.escudo > 0:
            self.escudo -= danio
            if self.escudo < 0:
                self.vida += self.escudo  # El daño restante va a la vida
                self.escudo = 0
        else:
            self.vida -= danio

        if self.vida < 0:
            self.vida = 0

        self.tiempo_invulnerable = 60  # 1 segundo de invulnerabilidad

    def curar(self, cantidad):
        self.vida += cantidad
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima

    def añadir_escudo(self, cantidad):
        self.escudo += cantidad
        if self.escudo > self.escudo_maximo:
            self.escudo = self.escudo_maximo

    def mejorar_arma(self):
        self.arma_nivel = min(self.arma_nivel + 1, 3)

    def dibujar(self, pantalla):
        # Efecto de parpadeo cuando es invulnerable
        if self.tiempo_invulnerable > 0 and self.tiempo_invulnerable % 10 < 5:
            return

        # Dibujar escudo si está activo
        if self.escudo > 0:
            radio_escudo = 60
            alpha = int((self.escudo / self.escudo_maximo) * 100)
            escudo_surface = pygame.Surface((radio_escudo * 2, radio_escudo * 2), pygame.SRCALPHA)
            pygame.draw.circle(escudo_surface, (*AZUL_NEON, alpha), (radio_escudo, radio_escudo), radio_escudo, 3)
            pantalla.blit(escudo_surface, (self.x - radio_escudo + self.ancho//2, self.y - radio_escudo + self.alto//2))

        # Cuerpo principal de la nave
        # Parte superior (punta)
        pygame.draw.polygon(pantalla, CYAN, [
            (self.x + self.ancho // 2, self.y),
            (self.x + self.ancho // 2 - 5, self.y + 15),
            (self.x + self.ancho // 2 + 5, self.y + 15)
        ])

        # Cuerpo principal
        pygame.draw.polygon(pantalla, AZUL_NEON, [
            (self.x + self.ancho // 2 - 8, self.y + 15),
            (self.x + self.ancho // 2 + 8, self.y + 15),
            (self.x + self.ancho // 2 + 15, self.y + 40),
            (self.x + self.ancho // 2 - 15, self.y + 40)
        ])

        # Alas
        pygame.draw.polygon(pantalla, VERDE_NEON, [
            (self.x, self.y + 30),
            (self.x + 10, self.y + 25),
            (self.x + 15, self.y + 45),
            (self.x + 5, self.y + 50)
        ])

        pygame.draw.polygon(pantalla, VERDE_NEON, [
            (self.x + self.ancho, self.y + 30),
            (self.x + self.ancho - 10, self.y + 25),
            (self.x + self.ancho - 15, self.y + 45),
            (self.x + self.ancho - 5, self.y + 50)
        ])

        # Motores
        pygame.draw.rect(pantalla, ROJO, (self.x + 5, self.y + 45, 8, 5))
        pygame.draw.rect(pantalla, ROJO, (self.x + self.ancho - 13, self.y + 45, 8, 5))

        # Efectos de motor
        for i in range(3):
            flame_y = self.y + 50 + i * 3
            flame_color = random.choice([ROJO, NARANJA, AMARILLO])
            pygame.draw.circle(pantalla, flame_color, (self.x + 9, flame_y), 2)
            pygame.draw.circle(pantalla, flame_color, (self.x + self.ancho - 9, flame_y), 2)

        # Barras de estado mejoradas
        self.dibujar_barras_estado(pantalla)

    def dibujar_barras_estado(self, pantalla):
        barra_ancho = 50
        barra_alto = 8
        barra_x = self.x - 10
        barra_y = self.y - 25

        # Barra de vida
        pygame.draw.rect(pantalla, ROJO_OSCURO, (barra_x, barra_y, barra_ancho, barra_alto))
        vida_ancho = int((self.vida / self.vida_maxima) * barra_ancho)
        pygame.draw.rect(pantalla, VERDE, (barra_x, barra_y, vida_ancho, barra_alto))
        pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 1)

        # Barra de escudo
        if self.escudo > 0:
            barra_y -= 12
            pygame.draw.rect(pantalla, AZUL_OSCURO, (barra_x, barra_y, barra_ancho, barra_alto))
            escudo_ancho = int((self.escudo / self.escudo_maximo) * barra_ancho)
            pygame.draw.rect(pantalla, AZUL_NEON, (barra_x, barra_y, escudo_ancho, barra_alto))
            pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 1)

        # Barra de poder especial
        if self.poder_especial > 0:
            barra_y = self.y - 37 if self.escudo > 0 else self.y - 25
            pygame.draw.rect(pantalla, VIOLETA, (barra_x, barra_y, barra_ancho, barra_alto))
            poder_ancho = int((self.poder_especial / 100) * barra_ancho)
            pygame.draw.rect(pantalla, DORADO, (barra_x, barra_y, poder_ancho, barra_alto))
            pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 1)

class Enemigo:
    def __init__(self, x, y, tipo="basico"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = random.randint(1, 3)
        self.vida = 1
        self.puntos = 10
        self.tiempo_creacion = pygame.time.get_ticks()

        # Configuración por tipo
        if tipo == "tanque":
            self.ancho = 50
            self.alto = 45
            self.vida = 5
            self.velocidad = 1
            self.puntos = 50
            self.color = ROJO
        elif tipo == "rapido":
            self.ancho = 25
            self.alto = 30
            self.vida = 1
            self.velocidad = 5
            self.puntos = 30
            self.color = AMARILLO
        elif tipo == "francotirador":
            self.ancho = 35
            self.alto = 40
            self.vida = 2
            self.velocidad = 1
            self.puntos = 40
            self.color = VIOLETA
        elif tipo == "jefe":
            self.ancho = 80
            self.alto = 60
            self.vida = 15
            self.velocidad = 0.5
            self.puntos = 200
            self.color = ROJO_OSCURO
        else:  # basico
            self.ancho = 30
            self.alto = 35
            self.vida = 2
            self.velocidad = 2
            self.puntos = 20
            self.color = MAGENTA

        self.vida_maxima = self.vida
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.tiempo_disparo = random.randint(60, 180)
        self.contador_disparo = 0
        self.angulo = 0
        self.direccion_x = random.choice([-1, 1])

    def mover(self):
        self.y += self.velocidad
        self.rect.y = self.y

        # Comportamientos específicos por tipo
        if self.tipo == "rapido":
            # Movimiento zigzag
            if random.randint(1, 30) == 1:
                self.direccion_x *= -1
            self.x += self.direccion_x * 2

        elif self.tipo == "francotirador":
            # Movimiento lateral lento
            self.x += math.sin(self.angulo) * 1
            self.angulo += 0.1

        elif self.tipo == "jefe":
            # Movimiento sinusoidal
            self.x += math.sin(pygame.time.get_ticks() * 0.01) * 2

        # Mantener dentro de los límites
        if self.x < 0:
            self.x = 0
            self.direccion_x = 1
        elif self.x > ANCHO - self.ancho:
            self.x = ANCHO - self.ancho
            self.direccion_x = -1

        self.rect.x = self.x

    def disparar(self):
        self.contador_disparo += 1
        proyectiles = []

        if self.contador_disparo >= self.tiempo_disparo:
            self.contador_disparo = 0
            self.tiempo_disparo = random.randint(60, 180)

            if self.tipo == "francotirador":
                # Disparo preciso hacia el jugador
                proyectiles.append(Proyectil(self.x + self.ancho // 2, self.y + self.alto, 6, VIOLETA, "plasma"))

            elif self.tipo == "jefe":
                # Disparo múltiple
                for i in range(5):
                    offset_x = (i - 2) * 15
                    proyectiles.append(Proyectil(self.x + self.ancho // 2 + offset_x, self.y + self.alto, 4, ROJO_OSCURO, "plasma"))

            else:
                # Disparo normal
                proyectiles.append(Proyectil(self.x + self.ancho // 2, self.y + self.alto, 4, self.color, "basic"))

        return proyectiles

    def recibir_danio(self, danio):
        self.vida -= danio
        return self.vida <= 0

    def dibujar(self, pantalla):
        # Efecto de entrada
        tiempo_vida = pygame.time.get_ticks() - self.tiempo_creacion
        if tiempo_vida < 500:  # Primeros 500ms
            alpha = int((tiempo_vida / 500) * 255)
            surface = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            self.dibujar_forma(surface, (0, 0))
            surface.set_alpha(alpha)
            pantalla.blit(surface, (self.x, self.y))
        else:
            self.dibujar_forma(pantalla, (self.x, self.y))

        # Barra de vida para enemigos fuertes
        if self.vida_maxima > 2:
            barra_ancho = self.ancho
            barra_alto = 6
            barra_x = self.x
            barra_y = self.y - 12

            pygame.draw.rect(pantalla, ROJO_OSCURO, (barra_x, barra_y, barra_ancho, barra_alto))
            vida_ancho = int((self.vida / self.vida_maxima) * barra_ancho)
            pygame.draw.rect(pantalla, VERDE, (barra_x, barra_y, vida_ancho, barra_alto))
            pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 1)

    def dibujar_forma(self, superficie, pos):
        x, y = pos

        if self.tipo == "jefe":
            # Forma compleja para el jefe
            pygame.draw.polygon(superficie, self.color, [
                (x + self.ancho // 2, y),
                (x, y + 20),
                (x + 15, y + 30),
                (x, y + self.alto),
                (x + self.ancho, y + self.alto),
                (x + self.ancho - 15, y + 30),
                (x + self.ancho, y + 20)
            ])
            # Detalles del jefe
            pygame.draw.circle(superficie, ROJO, (x + self.ancho // 2, y + 25), 8)
            pygame.draw.rect(superficie, AMARILLO, (x + 10, y + 15, 15, 5))
            pygame.draw.rect(superficie, AMARILLO, (x + self.ancho - 25, y + 15, 15, 5))

        elif self.tipo == "tanque":
            # Forma robusta para el tanque
            pygame.draw.rect(superficie, self.color, (x, y, self.ancho, self.alto))
            pygame.draw.rect(superficie, NARANJA, (x + 5, y + 5, self.ancho - 10, self.alto - 10))
            pygame.draw.rect(superficie, BLANCO, (x, y, self.ancho, self.alto), 3)

        elif self.tipo == "francotirador":
            # Forma triangular alargada
            pygame.draw.polygon(superficie, self.color, [
                (x + self.ancho // 2, y),
                (x, y + self.alto),
                (x + self.ancho, y + self.alto)
            ])
            pygame.draw.circle(superficie, BLANCO, (x + self.ancho // 2, y + 20), 5)

        else:
            # Formas básicas mejoradas
            pygame.draw.polygon(superficie, self.color, [
                (x + self.ancho // 2, y),
                (x, y + self.alto // 2),
                (x + self.ancho // 4, y + self.alto),
                (x + 3 * self.ancho // 4, y + self.alto),
                (x + self.ancho, y + self.alto // 2)
            ])
            pygame.draw.circle(superficie, BLANCO, (x + self.ancho // 2, y + self.alto // 2), 4)

class Proyectil:
    def __init__(self, x, y, velocidad, color, tipo="basic"):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.color = color
        self.tipo = tipo
        self.ancho = 6 if tipo == "basic" else 8
        self.alto = 12 if tipo == "basic" else 16
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.tiempo_creacion = pygame.time.get_ticks()
        self.danio = 1 if tipo == "basic" else 2

    def mover(self):
        self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self, pantalla):
        if self.tipo == "laser":
            # Láser con efecto de energía
            pygame.draw.rect(pantalla, self.color, (self.x - 1, self.y, self.ancho + 2, self.alto))
            pygame.draw.rect(pantalla, BLANCO, (self.x, self.y, self.ancho, self.alto))

        elif self.tipo == "plasma":
            # Plasma con efecto de pulso
            radio = 6 + int(3 * math.sin(pygame.time.get_ticks() * 0.02))
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), radio)
            pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(self.y)), radio // 2)

        else:
            # Proyectil básico
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

class ProyectilEspecial:
    def __init__(self, x, y, vel_x, vel_y, color, tipo):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.tipo = tipo
        self.ancho = 12
        self.alto = 20
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.danio = 5
        self.tiempo_vida = 120  # 2 segundos

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.tiempo_vida -= 1

    def dibujar(self, pantalla):
        # Efecto devastador
        for i in range(3):
            radio = 8 - i * 2
            alpha = 255 - i * 60
            color_con_alpha = (*self.color, alpha)
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), radio)

class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad = 2
        self.ancho = 25
        self.alto = 25
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.angulo = 0
        self.tiempo_creacion = pygame.time.get_ticks()

        # Configuración por tipo
        if tipo == "vida":
            self.color = VERDE
            self.efecto = "Restaura 30 de vida"
        elif tipo == "municion":
            self.color = AZUL
            self.efecto = "Recarga completa"
        elif tipo == "escudo":
            self.color = AZUL_NEON
            self.efecto = "Escudo de energía"
        elif tipo == "arma":
            self.color = DORADO
            self.efecto = "Mejora de arma"
        elif tipo == "poder":
            self.color = VIOLETA
            self.efecto = "Energía especial"
        elif tipo == "velocidad":
            self.color = VERDE_NEON
            self.efecto = "Velocidad aumentada"

    def mover(self):
        self.y += self.velocidad
        self.rect.y = self.y
        self.angulo += 0.1

    def dibujar(self, pantalla):
        # Efecto de rotación y brillo
        centro_x = self.x + self.ancho // 2
        centro_y = self.y + self.alto // 2

        # Aura externa
        radio_aura = 20 + int(5 * math.sin(pygame.time.get_ticks() * 0.01))
        superficie_aura = pygame.Surface((radio_aura * 2, radio_aura * 2), pygame.SRCALPHA)
        pygame.draw.circle(superficie_aura, (*self.color, 50), (radio_aura, radio_aura), radio_aura)
        pantalla.blit(superficie_aura, (centro_x - radio_aura, centro_y - radio_aura))

        # Forma principal rotativa
        puntos = []
        for i in range(6):
            angle = self.angulo + i * math.pi / 3
            px = centro_x + 12 * math.cos(angle)
            py = centro_y + 12 * math.sin(angle)
            puntos.append((px, py))

        pygame.draw.polygon(pantalla, self.color, puntos)
        pygame.draw.polygon(pantalla, BLANCO, puntos, 2)

        # Símbolo central
        if self.tipo == "vida":
            pygame.draw.line(pantalla, BLANCO, (centro_x - 6, centro_y), (centro_x + 6, centro_y), 3)
            pygame.draw.line(pantalla, BLANCO, (centro_x, centro_y - 6), (centro_x, centro_y + 6), 3)
        elif self.tipo == "municion":
            pygame.draw.circle(pantalla, BLANCO, (centro_x, centro_y), 4)
        elif self.tipo == "arma":
            pygame.draw.polygon(pantalla, BLANCO, [
                (centro_x, centro_y - 6),
                (centro_x - 4, centro_y + 6),
                (centro_x + 4, centro_y + 6)
            ])

class Particula:
    def __init__(self, x, y, tipo="explosion"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidad_x = random.uniform(-5, 5)
        self.velocidad_y = random.uniform(-5, 5)
        self.vida = 60
        self.vida_maxima = 60
        self.tamaño = random.randint(2, 6)

        if tipo == "explosion":
            self.color = random.choice([ROJO, NARANJA, AMARILLO, BLANCO])
        elif tipo == "plasma":
            self.color = random.choice([CYAN, AZUL_NEON, BLANCO])
        elif tipo == "energia":
            self.color = random.choice([VIOLETA, MAGENTA, ROSA_NEON])
        else:
            self.color = BLANCO

    def actualizar(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.vida -= 1
        self.velocidad_x *= 0.98  # Fricción
        self.velocidad_y *= 0.98

        if self.tipo == "explosion":
            self.velocidad_y += 0.1  # Gravedad

    def dibujar(self, pantalla):
        if self.vida <= 0:
            return

        alpha = int((self.vida / self.vida_maxima) * 255)
        tamaño_actual = int(self.tamaño * (self.vida / self.vida_maxima))

        if tamaño_actual > 0:
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), tamaño_actual)

class BotonMenu:
    def __init__(self, x, y, ancho, alto, texto, color=GRIS):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = tuple(min(255, c + 50) for c in color)
        self.hover = False
        self.presionado = False

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def click(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos) and mouse_pressed:
            self.presionado = True
            return True
        return False

    def dibujar(self, pantalla, fuente):
        color_actual = self.color_hover if self.hover else self.color
        pygame.draw.rect(pantalla, color_actual, self.rect)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 2)

        texto_surface = fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)

def crear_explosion(x, y, particulas, tipo="explosion", cantidad=15):
    for _ in range(cantidad):
        particulas.append(Particula(x, y, tipo))

def crear_estrellas(num_estrellas):
    return [Estrella() for _ in range(num_estrellas)]

def generar_enemigo(nivel):
    x = random.randint(0, ANCHO - 50)

    # Probabilidades basadas en nivel
    if nivel >= 10 and random.randint(1, 100) <= 5:  # 5% de probabilidad de jefe
        return Enemigo(x, -80, "jefe")
    elif nivel >= 5:
        tipo = random.choices(
            ["basico", "tanque", "rapido", "francotirador"],
            weights=[50, 20, 20, 10]
        )[0]
    else:
        tipo = random.choices(
            ["basico", "tanque", "rapido"],
            weights=[60, 20, 20]
        )[0]

    return Enemigo(x, -50, tipo)

def generar_powerup(x, y):
    tipo = random.choices(
        ["vida", "municion", "escudo", "arma", "poder", "velocidad"],
        weights=[25, 25, 20, 15, 10, 5]
    )[0]
    return PowerUp(x, y, tipo)

def dibujar_hud_mejorado(pantalla, jugador, nivel, fuente):
    # Panel HUD semitransparente
    hud_surface = pygame.Surface((ANCHO, 120), pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, (0, 0, 0, 180), (0, 0, ANCHO, 120))
    pantalla.blit(hud_surface, (0, 0))

    # Información principal
    texto_vida = fuente.render(f"VIDA: {jugador.vida}/{jugador.vida_maxima}", True, VERDE)
    texto_escudo = fuente.render(f"ESCUDO: {jugador.escudo}/{jugador.escudo_maximo}", True, AZUL_NEON)
    texto_municion = fuente.render(f"MUNICIÓN: {jugador.municion}/{jugador.municion_maxima}", True, CYAN)
    texto_puntos = fuente.render(f"PUNTOS: {jugador.puntos:,}", True, DORADO)
    texto_nivel = fuente.render(f"NIVEL: {nivel}", True, BLANCO)
    texto_arma = fuente.render(f"ARMA: Nivel {jugador.arma_nivel}", True, VIOLETA)

    # Posicionar textos
    pantalla.blit(texto_vida, (20, 20))
    pantalla.blit(texto_escudo, (20, 45))
    pantalla.blit(texto_municion, (20, 70))
    pantalla.blit(texto_puntos, (ANCHO - 200, 20))
    pantalla.blit(texto_nivel, (ANCHO - 200, 45))
    pantalla.blit(texto_arma, (ANCHO - 200, 70))

    # Barra de poder especial
    if jugador.poder_especial > 0:
        barra_poder_rect = pygame.Rect(ANCHO // 2 - 100, 20, 200, 20)
        pygame.draw.rect(pantalla, VIOLETA, barra_poder_rect)
        poder_ancho = int((jugador.poder_especial / 100) * 200)
        pygame.draw.rect(pantalla, DORADO, (ANCHO // 2 - 100, 20, poder_ancho, 20))
        pygame.draw.rect(pantalla, BLANCO, barra_poder_rect, 2)

        texto_poder = fuente.render("PODER ESPECIAL", True, BLANCO)
        texto_rect = texto_poder.get_rect(center=(ANCHO // 2, 10))
        pantalla.blit(texto_poder, texto_rect)

    # Controles
    controles = [
        "WASD/Flechas: Mover",
        "ESPACIO: Disparar",
        "Click Izq: Disparar",
        "R: Recargar",
        "Q: Poder Especial",
        "P: Pausa"
    ]

    for i, control in enumerate(controles):
        texto = pygame.font.Font(None, 18).render(control, True, GRIS)
        pantalla.blit(texto, (ANCHO - 180, ALTO - 150 + i * 20))

def mostrar_menu_principal_mejorado(pantalla, fuente_titulo, fuente_menu, estrellas, botones):
    # Actualizar y dibujar estrellas
    for estrella in estrellas:
        estrella.actualizar()
        estrella.dibujar(pantalla)

    # Título con efecto de neón
    titulo = "SPACE DEFENDER"
    for i, char in enumerate(titulo):
        color = [CYAN, AZUL_NEON, VERDE_NEON, VIOLETA][i % 4]
        offset = int(5 * math.sin(pygame.time.get_ticks() * 0.005 + i * 0.5))
        char_surface = fuente_titulo.render(char, True, color)
        pantalla.blit(char_surface, (ANCHO // 2 - len(titulo) * 25 + i * 50, 100 + offset))

    # Subtítulo animado
    subtitulo = "Defiende la Tierra de la invasión alienígena"
    alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.003))
    subtitulo_surface = fuente_menu.render(subtitulo, True, BLANCO)
    subtitulo_surface.set_alpha(alpha)
    subtitulo_rect = subtitulo_surface.get_rect(center=(ANCHO // 2, 200))
    pantalla.blit(subtitulo_surface, subtitulo_rect)

    # Dibujar botones
    for boton in botones:
        boton.dibujar(pantalla, fuente_menu)

    # Efectos de partículas decorativas
    for _ in range(3):
        x = random.randint(0, ANCHO)
        y = random.randint(0, ALTO)
        color = random.choice([CYAN, AZUL_NEON, VERDE_NEON, VIOLETA])
        pygame.draw.circle(pantalla, color, (x, y), 1)

def mostrar_instrucciones_mejoradas(pantalla, fuente_titulo, fuente_texto, estrellas):
    # Fondo de estrellas
    for estrella in estrellas:
        estrella.actualizar()
        estrella.dibujar(pantalla)

    # Panel semitransparente
    panel = pygame.Surface((ANCHO - 100, ALTO - 100), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 200), (0, 0, ANCHO - 100, ALTO - 100))
    pantalla.blit(panel, (50, 50))

    titulo = fuente_titulo.render("INSTRUCCIONES", True, CYAN)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, 100))
    pantalla.blit(titulo, titulo_rect)

    instrucciones = [
        ("CONTROLES:", DORADO),
        ("  WASD / Flechas - Mover nave", BLANCO),
        ("  ESPACIO / Click Izq - Disparar", BLANCO),
        ("  Click Der - Mover con mouse", BLANCO),
        ("  R - Recargar munición", BLANCO),
        ("  Q - Poder especial (cuando esté lleno)", BLANCO),
        ("  P - Pausar juego", BLANCO),
        ("", BLANCO),
        ("ENEMIGOS:", DORADO),
        ("  Púrpura - Enemigo básico (20 pts)", MAGENTA),
        ("  Rojo - Tanque resistente (50 pts)", ROJO),
        ("  Amarillo - Enemigo rápido (30 pts)", AMARILLO),
        ("  Violeta - Francotirador (40 pts)", VIOLETA),
        ("  Rojo Oscuro - JEFE (200 pts)", ROJO_OSCURO),
        ("", BLANCO),
        ("POWER-UPS:", DORADO),
        ("  Verde - Restaura vida (+30)", VERDE),
        ("  Azul - Recarga munición completa", AZUL),
        ("  Azul Neón - Escudo de energía", AZUL_NEON),
        ("  Dorado - Mejora de arma", DORADO),
        ("  Violeta - Energía especial", VIOLETA),
        ("  Verde Neón - Velocidad aumentada", VERDE_NEON),
        ("", BLANCO),
        ("Presiona ESC para volver al menú", GRIS)
    ]

    for i, (linea, color) in enumerate(instrucciones):
        texto = fuente_texto.render(linea, True, color)
        pantalla.blit(texto, (100, 150 + i * 25))

def cargar_puntuaciones():
    try:
        with open("puntuaciones.json", "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_puntuacion(puntos):
    puntuaciones = cargar_puntuaciones()
    puntuaciones.append(puntos)
    puntuaciones.sort(reverse=True)
    puntuaciones = puntuaciones[:10]

    with open("puntuaciones.json", "w") as archivo:
        json.dump(puntuaciones, archivo)

def mostrar_puntuaciones_mejoradas(pantalla, fuente_titulo, fuente_texto, estrellas):
    # Fondo de estrellas
    for estrella in estrellas:
        estrella.actualizar()
        estrella.dibujar(pantalla)

    # Panel de puntuaciones
    panel = pygame.Surface((600, 500), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 220), (0, 0, 600, 500))
    pygame.draw.rect(panel, DORADO, (0, 0, 600, 500), 3)
    pantalla.blit(panel, (ANCHO // 2 - 300, ALTO // 2 - 250))

    titulo = fuente_titulo.render("TOP 10 PUNTUACIONES", True, DORADO)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, 180))
    pantalla.blit(titulo, titulo_rect)

    puntuaciones = cargar_puntuaciones()

    if not puntuaciones:
        texto = fuente_texto.render("No hay puntuaciones registradas", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO // 2, 300))
        pantalla.blit(texto, texto_rect)
    else:
        for i, puntos in enumerate(puntuaciones[:10]):
            # Color diferente para las primeras 3 posiciones
            if i == 0:
                color = DORADO
            elif i == 1:
                color = BLANCO
            elif i == 2:
                color = NARANJA
            else:
                color = GRIS

            texto = fuente_texto.render(f"{i+1:2d}. {puntos:,} puntos", True, color)
            pantalla.blit(texto, (ANCHO // 2 - 100, 230 + i * 35))

    texto_volver = fuente_texto.render("Presiona ESC para volver al menú", True, GRIS)
    texto_rect = texto_volver.get_rect(center=(ANCHO // 2, ALTO - 100))
    pantalla.blit(texto_volver, texto_rect)

def mostrar_game_over_mejorado(pantalla, fuente_titulo, fuente_texto, puntos, estrellas):
    # Fondo de estrellas
    for estrella in estrellas:
        estrella.actualizar()
        estrella.dibujar(pantalla)

    # Efecto de overlay
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (255, 0, 0, 50), (0, 0, ANCHO, ALTO))
    pantalla.blit(overlay, (0, 0))

    # Panel principal
    panel = pygame.Surface((600, 400), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 200), (0, 0, 600, 400))
    pygame.draw.rect(panel, ROJO, (0, 0, 600, 400), 4)
    pantalla.blit(panel, (ANCHO // 2 - 300, ALTO // 2 - 200))

    # Título con efecto de parpadeo
    alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
    titulo = fuente_titulo.render("GAME OVER", True, ROJO)
    titulo.set_alpha(alpha)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 80))
    pantalla.blit(titulo, titulo_rect)

    # Puntuación final
    texto_puntos = fuente_texto.render(f"Puntuación final: {puntos:,}", True, DORADO)
    texto_rect = texto_puntos.get_rect(center=(ANCHO // 2, ALTO // 2 - 20))
    pantalla.blit(texto_puntos, texto_rect)

    # Verificar si es nuevo récord
    puntuaciones = cargar_puntuaciones()
    if not puntuaciones or puntos > puntuaciones[0]:
        texto_record = fuente_texto.render("¡NUEVO RÉCORD!", True, DORADO)
        texto_record_rect = texto_record.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
        pantalla.blit(texto_record, texto_record_rect)

    texto_continuar = fuente_texto.render("Presiona ENTER para continuar", True, GRIS)
    texto_rect = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
    pantalla.blit(texto_continuar, texto_rect)

def mostrar_pausa_mejorada(pantalla, fuente_titulo):
    # Overlay semitransparente
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, ANCHO, ALTO))
    pantalla.blit(overlay, (0, 0))

    # Panel de pausa
    panel = pygame.Surface((400, 200), pygame.SRCALPHA)
    pygame.draw.rect(panel, (0, 0, 0, 200), (0, 0, 400, 200))
    pygame.draw.rect(panel, BLANCO, (0, 0, 400, 200), 3)
    pantalla.blit(panel, (ANCHO // 2 - 200, ALTO // 2 - 100))

    texto = fuente_titulo.render("PAUSA", True, BLANCO)
    texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 30))
    pantalla.blit(texto, texto_rect)

    texto_continuar = fuente_titulo.render("Presiona P para continuar", True, GRIS)
    texto_rect = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 30))
    pantalla.blit(texto_continuar, texto_rect)

def main():
    # Configuración de la pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Defender - Enhanced Edition")
    reloj = pygame.time.Clock()

    # Fuentes mejoradas
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_menu = pygame.font.Font(None, 36)
    fuente_texto = pygame.font.Font(None, 24)
    fuente_hud = pygame.font.Font(None, 20)

    # Crear estrellas de fondo
    estrellas = crear_estrellas(100)

    # Crear botones del menú
    botones_menu = [
        BotonMenu(ANCHO // 2 - 150, 300, 300, 50, "JUGAR", VERDE),
        BotonMenu(ANCHO // 2 - 150, 370, 300, 50, "INSTRUCCIONES", AZUL),
        BotonMenu(ANCHO // 2 - 150, 440, 300, 50, "PUNTUACIONES", VIOLETA),
        BotonMenu(ANCHO // 2 - 150, 510, 300, 50, "SALIR", ROJO)
    ]

    # Estados del juego
    estado = "menu"

    # Variables del juego
    jugador = None
    enemigos = []
    proyectiles_jugador = []
    proyectiles_enemigos = []
    proyectiles_especiales = []
    powerups = []
    particulas = []
    nivel = 1
    enemigos_eliminados = 0
    tiempo_spawn = 0
    pausa = False

    ejecutando = True

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Botón izquierdo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if estado == "menu":
                    if evento.key == pygame.K_1:
                        estado = "jugando"
                        # Inicializar juego
                        jugador = Jugador(ANCHO // 2 - 20, ALTO - 80)
                        enemigos = []
                        proyectiles_jugador = []
                        proyectiles_enemigos = []
                        proyectiles_especiales = []
                        powerups = []
                        particulas = []
                        nivel = 1
                        enemigos_eliminados = 0
                        tiempo_spawn = 0
                        pausa = False
                    elif evento.key == pygame.K_2:
                        estado = "instrucciones"
                    elif evento.key == pygame.K_3:
                        estado = "puntuaciones"
                    elif evento.key == pygame.K_4:
                        ejecutando = False

                elif estado == "instrucciones" or estado == "puntuaciones":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "menu"

                elif estado == "jugando":
                    if evento.key == pygame.K_SPACE:
                        proyectiles = jugador.disparar()
                        proyectiles_jugador.extend(proyectiles)
                    elif evento.key == pygame.K_r:
                        jugador.recargar()
                    elif evento.key == pygame.K_q:
                        proyectiles_esp = jugador.usar_poder_especial()
                        proyectiles_especiales.extend(proyectiles_esp)
                    elif evento.key == pygame.K_p:
                        pausa = not pausa
                    elif evento.key == pygame.K_ESCAPE:
                        estado = "menu"

                elif estado == "game_over":
                    if evento.key == pygame.K_RETURN:
                        estado = "menu"

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado == "menu":
                    for i, boton in enumerate(botones_menu):
                        if boton.click(mouse_pos, True):
                            if i == 0:  # Jugar
                                estado = "jugando"
                                jugador = Jugador(ANCHO // 2 - 20, ALTO - 80)
                                enemigos = []
                                proyectiles_jugador = []
                                proyectiles_enemigos = []
                                proyectiles_especiales = []
                                powerups = []
                                particulas = []
                                nivel = 1
                                enemigos_eliminados = 0
                                tiempo_spawn = 0
                                pausa = False
                            elif i == 1:  # Instrucciones
                                estado = "instrucciones"
                            elif i == 2:  # Puntuaciones
                                estado = "puntuaciones"
                            elif i == 3:  # Salir
                                ejecutando = False

                elif estado == "jugando" and not pausa:
                    if evento.button == 1:  # Botón izquierdo
                        proyectiles = jugador.disparar()
                        proyectiles_jugador.extend(proyectiles)

        # Actualizar botones del menú
        if estado == "menu":
            for boton in botones_menu:
                boton.actualizar(mouse_pos)

        # Lógica del juego
        if estado == "jugando" and not pausa:
            teclas = pygame.key.get_pressed()
            jugador.mover(teclas, mouse_pos)

            # Disparo automático con mouse
            if pygame.mouse.get_pressed()[0]:
                proyectiles = jugador.disparar()
                proyectiles_jugador.extend(proyectiles)

            # Generar enemigos
            tiempo_spawn += 1
            spawn_rate = max(20 - nivel * 2, 8)
            if tiempo_spawn > spawn_rate:
                tiempo_spawn = 0
                enemigos.append(generar_enemigo(nivel))

            # Actualizar enemigos
            for enemigo in enemigos[:]:
                enemigo.mover()

                # Disparos de enemigos
                proyectiles_enemigo = enemigo.disparar()
                proyectiles_enemigos.extend(proyectiles_enemigo)

                # Eliminar enemigos que salen de pantalla
                if enemigo.y > ALTO:
                    enemigos.remove(enemigo)
                    continue

                # Colisión con jugador
                if enemigo.rect.colliderect(jugador.rect):
                    jugador.recibir_danio(30)
                    crear_explosion(enemigo.x, enemigo.y, particulas, "explosion", 20)
                    enemigos.remove(enemigo)

            # Actualizar proyectiles del jugador
            for proyectil in proyectiles_jugador[:]:
                proyectil.mover()

                if proyectil.y < -20:
                    proyectiles_jugador.remove(proyectil)
                    continue

                # Colisiones con enemigos
                for enemigo in enemigos[:]:
                    if proyectil.rect.colliderect(enemigo.rect):
                        if enemigo.recibir_danio(proyectil.danio):
                            jugador.puntos += enemigo.puntos
                            jugador.poder_especial += 5
                            if jugador.poder_especial > 100:
                                jugador.poder_especial = 100

                            enemigos_eliminados += 1
                            crear_explosion(enemigo.x, enemigo.y, particulas, "explosion", 25)

                            # Generar power-up
                            if random.randint(1, 4) == 1:
                                powerups.append(generar_powerup(enemigo.x, enemigo.y))

                            enemigos.remove(enemigo)
                        else:
                            crear_explosion(proyectil.x, proyectil.y, particulas, "plasma", 5)

                        proyectiles_jugador.remove(proyectil)
                        break

            # Actualizar proyectiles especiales
            for proyectil in proyectiles_especiales[:]:
                proyectil.mover()

                if (proyectil.x < -50 or proyectil.x > ANCHO + 50 or
                    proyectil.y < -50 or proyectil.y > ALTO + 50 or
                    proyectil.tiempo_vida <= 0):
                    proyectiles_especiales.remove(proyectil)
                    continue

                # Colisiones con enemigos
                for enemigo in enemigos[:]:
                    if proyectil.rect.colliderect(enemigo.rect):
                        if enemigo.recibir_danio(proyectil.danio):
                            jugador.puntos += enemigo.puntos
                            enemigos_eliminados += 1
                            crear_explosion(enemigo.x, enemigo.y, particulas, "energia", 30)
                            enemigos.remove(enemigo)
                        break

            # Actualizar proyectiles de enemigos
            for proyectil in proyectiles_enemigos[:]:
                proyectil.mover()

                if proyectil.y > ALTO + 20:
                    proyectiles_enemigos.remove(proyectil)
                    continue

                # Colisión con jugador
                if proyectil.rect.colliderect(jugador.rect):
                    jugador.recibir_danio(15)
                    crear_explosion(proyectil.x, proyectil.y, particulas, "plasma", 8)
                    proyectiles_enemigos.remove(proyectil)

            # Actualizar power-ups
            for powerup in powerups[:]:
                powerup.mover()

                if powerup.y > ALTO:
                    powerups.remove(powerup)
                    continue

                # Colisión con jugador
                if powerup.rect.colliderect(jugador.rect):
                    if powerup.tipo == "vida":
                        jugador.curar(30)
                    elif powerup.tipo == "municion":
                        jugador.recargar()
                    elif powerup.tipo == "escudo":
                        jugador.añadir_escudo(50)
                    elif powerup.tipo == "arma":
                        jugador.mejorar_arma()
                    elif powerup.tipo == "poder":
                        jugador.poder_especial += 25
                        if jugador.poder_especial > 100:
                            jugador.poder_especial = 100
                    elif powerup.tipo == "velocidad":
                        jugador.velocidad += 1

                    crear_explosion(powerup.x, powerup.y, particulas, "energia", 10)
                    powerups.remove(powerup)

            # Actualizar partículas
            for particula in particulas[:]:
                particula.actualizar()
                if particula.vida <= 0:
                    particulas.remove(particula)

            # Subir de nivel
            if enemigos_eliminados >= nivel * 8:
                nivel += 1
                enemigos_eliminados = 0
                jugador.poder_especial += 20  # Bonus por subir de nivel
                if jugador.poder_especial > 100:
                    jugador.poder_especial = 100

            # Verificar game over
            if jugador.vida <= 0:
                guardar_puntuacion(jugador.puntos)
                estado = "game_over"

        # Renderizado
        pantalla.fill(NEGRO)

        if estado == "menu":
            mostrar_menu_principal_mejorado(pantalla, fuente_titulo, fuente_menu, estrellas, botones_menu)

        elif estado == "instrucciones":
            mostrar_instrucciones_mejoradas(pantalla, fuente_titulo, fuente_texto, estrellas)

        elif estado == "puntuaciones":
            mostrar_puntuaciones_mejoradas(pantalla, fuente_titulo, fuente_texto, estrellas)

        elif estado == "jugando":
            # Dibujar estrellas de fondo
            for estrella in estrellas:
                estrella.actualizar()
                estrella.dibujar(pantalla)

            # Dibujar elementos del juego
            jugador.dibujar(pantalla)

            for enemigo in enemigos:
                enemigo.dibujar(pantalla)

            for proyectil in proyectiles_jugador:
                proyectil.dibujar(pantalla)

            for proyectil in proyectiles_enemigos:
                proyectil.dibujar(pantalla)

            for proyectil in proyectiles_especiales:
                proyectil.dibujar(pantalla)

            for powerup in powerups:
                powerup.dibujar(pantalla)

            for particula in particulas:
                particula.dibujar(pantalla)

            # Dibujar HUD
            dibujar_hud_mejorado(pantalla, jugador, nivel, fuente_hud)

            # Mostrar pausa si está activa
            if pausa:
                mostrar_pausa_mejorada(pantalla, fuente_titulo)

        elif estado == "game_over":
            mostrar_game_over_mejorado(pantalla, fuente_titulo, fuente_texto, jugador.puntos, estrellas)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()