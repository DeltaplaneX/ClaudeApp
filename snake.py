#!/usr/bin/env python3
"""
Juego de Snake en Python usando pygame
Controles:
- Flechas para mover la serpiente
- ESC para salir
- ESPACIO para reiniciar después de Game Over
"""

import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TAMANO_CELDA = 20
FPS = 15

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 200, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Direcciones
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)


class Snake:
    """Clase que representa la serpiente"""

    def __init__(self):
        """Inicializa la serpiente en el centro de la pantalla"""
        self.reset()

    def reset(self):
        """Reinicia la serpiente a su estado inicial"""
        centro_x = ANCHO_VENTANA // (2 * TAMANO_CELDA)
        centro_y = ALTO_VENTANA // (2 * TAMANO_CELDA)
        self.cuerpo = [
            (centro_x, centro_y),
            (centro_x - 1, centro_y),
            (centro_x - 2, centro_y)
        ]
        self.direccion = DERECHA
        self.nueva_direccion = DERECHA
        self.creciendo = False

    def mover(self):
        """Mueve la serpiente en la dirección actual"""
        self.direccion = self.nueva_direccion
        cabeza_x, cabeza_y = self.cuerpo[0]
        dir_x, dir_y = self.direccion
        nueva_cabeza = (cabeza_x + dir_x, cabeza_y + dir_y)

        self.cuerpo.insert(0, nueva_cabeza)

        if not self.creciendo:
            self.cuerpo.pop()
        else:
            self.creciendo = False

    def cambiar_direccion(self, nueva_direccion):
        """Cambia la dirección de la serpiente (no permite giro de 180 grados)"""
        dir_x, dir_y = self.direccion
        nueva_x, nueva_y = nueva_direccion

        # Prevenir giro de 180 grados
        if (dir_x, dir_y) != (-nueva_x, -nueva_y):
            self.nueva_direccion = nueva_direccion

    def crecer(self):
        """Marca que la serpiente debe crecer en el siguiente movimiento"""
        self.creciendo = True

    def colisiona_consigo_misma(self):
        """Verifica si la cabeza colisiona con el cuerpo"""
        return self.cuerpo[0] in self.cuerpo[1:]

    def colisiona_con_paredes(self):
        """Verifica si la serpiente colisiona con las paredes"""
        x, y = self.cuerpo[0]
        return (x < 0 or x >= ANCHO_VENTANA // TAMANO_CELDA or
                y < 0 or y >= ALTO_VENTANA // TAMANO_CELDA)

    def dibujar(self, superficie):
        """Dibuja la serpiente en la superficie"""
        for i, (x, y) in enumerate(self.cuerpo):
            rect = pygame.Rect(
                x * TAMANO_CELDA,
                y * TAMANO_CELDA,
                TAMANO_CELDA,
                TAMANO_CELDA
            )
            # Cabeza más oscura
            color = VERDE_OSCURO if i == 0 else VERDE
            pygame.draw.rect(superficie, color, rect)
            pygame.draw.rect(superficie, NEGRO, rect, 1)  # Borde


class Comida:
    """Clase que representa la comida"""

    def __init__(self):
        """Inicializa la comida en una posición aleatoria"""
        self.posicion = self.generar_posicion()

    def generar_posicion(self):
        """Genera una posición aleatoria para la comida"""
        x = random.randint(0, ANCHO_VENTANA // TAMANO_CELDA - 1)
        y = random.randint(0, ALTO_VENTANA // TAMANO_CELDA - 1)
        return (x, y)

    def reposicionar(self, serpiente):
        """Reposiciona la comida evitando el cuerpo de la serpiente"""
        while True:
            self.posicion = self.generar_posicion()
            if self.posicion not in serpiente.cuerpo:
                break

    def dibujar(self, superficie):
        """Dibuja la comida en la superficie"""
        x, y = self.posicion
        rect = pygame.Rect(
            x * TAMANO_CELDA,
            y * TAMANO_CELDA,
            TAMANO_CELDA,
            TAMANO_CELDA
        )
        pygame.draw.rect(superficie, ROJO, rect)
        pygame.draw.rect(superficie, NEGRO, rect, 1)  # Borde


class Juego:
    """Clase principal del juego"""

    def __init__(self):
        """Inicializa el juego"""
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption('Snake - Python')
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        self.reset()

    def reset(self):
        """Reinicia el juego"""
        self.serpiente = Snake()
        self.comida = Comida()
        self.puntuacion = 0
        self.game_over = False

    def manejar_eventos(self):
        """Maneja los eventos del teclado"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False

                if self.game_over:
                    if evento.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if evento.key == pygame.K_UP:
                        self.serpiente.cambiar_direccion(ARRIBA)
                    elif evento.key == pygame.K_DOWN:
                        self.serpiente.cambiar_direccion(ABAJO)
                    elif evento.key == pygame.K_LEFT:
                        self.serpiente.cambiar_direccion(IZQUIERDA)
                    elif evento.key == pygame.K_RIGHT:
                        self.serpiente.cambiar_direccion(DERECHA)

        return True

    def actualizar(self):
        """Actualiza el estado del juego"""
        if not self.game_over:
            self.serpiente.mover()

            # Verificar colisión con la comida
            if self.serpiente.cuerpo[0] == self.comida.posicion:
                self.serpiente.crecer()
                self.comida.reposicionar(self.serpiente)
                self.puntuacion += 10

            # Verificar colisiones
            if (self.serpiente.colisiona_consigo_misma() or
                self.serpiente.colisiona_con_paredes()):
                self.game_over = True

    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        self.ventana.fill(NEGRO)

        # Dibujar la cuadrícula (opcional)
        for x in range(0, ANCHO_VENTANA, TAMANO_CELDA):
            pygame.draw.line(self.ventana, (40, 40, 40), (x, 0), (x, ALTO_VENTANA))
        for y in range(0, ALTO_VENTANA, TAMANO_CELDA):
            pygame.draw.line(self.ventana, (40, 40, 40), (0, y), (ANCHO_VENTANA, y))

        # Dibujar serpiente y comida
        self.serpiente.dibujar(self.ventana)
        self.comida.dibujar(self.ventana)

        # Dibujar puntuación
        texto_puntuacion = self.fuente_pequena.render(
            f'Puntuación: {self.puntuacion}',
            True,
            BLANCO
        )
        self.ventana.blit(texto_puntuacion, (10, 10))

        # Dibujar mensaje de game over
        if self.game_over:
            texto_game_over = self.fuente.render('GAME OVER', True, ROJO)
            texto_reiniciar = self.fuente_pequena.render(
                'Presiona ESPACIO para reiniciar',
                True,
                BLANCO
            )

            rect_game_over = texto_game_over.get_rect(
                center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 20)
            )
            rect_reiniciar = texto_reiniciar.get_rect(
                center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 20)
            )

            self.ventana.blit(texto_game_over, rect_game_over)
            self.ventana.blit(texto_reiniciar, rect_reiniciar)

        pygame.display.flip()

    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True

        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    juego = Juego()
    juego.ejecutar()


if __name__ == '__main__':
    main()
