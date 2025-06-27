# Space Defender 🚀✨

Un emocionante juego de naves espaciales desarrollado en Python usando la librería PyGame. Defiende la Tierra de la invasión alienígena en este arcade clásico con mecánicas modernas, efectos visuales espectaculares y controles intuitivos.

## 📋 Descripción del Proyecto

Space Defender es un juego de shoot 'em up donde controlas una nave espacial para defender la Tierra de oleadas de enemigos alienígenas. El juego incluye múltiples tipos de enemigos, power-ups avanzados, sistema de puntuación, efectos visuales con partículas, controles con mouse y una progresión de dificultad por niveles con jefes épicos.

## 🎮 Características Principales

### ✨ Funcionalidades
- **Resolución HD**: 800x600 píxeles para una experiencia visual superior
- **Controles híbridos**: Compatibilidad total con teclado y mouse
- **Interfaz interactiva**: Menús completamente navegables con mouse
- **Efectos visuales avanzados**: Partículas diferenciadas, animaciones fluidas y colores neón
- **Sistema de escudo**: Protección adicional con barra de estado independiente
- **Poderes especiales**: Láser devastador con sistema de carga por combate

### 🎯 Sistema de Combate Avanzado
- **Múltiples niveles de arma**: 3 niveles de mejora (simple, doble, triple)
- **Disparo automático**: Click y mantén presionado para disparo continuo
- **Proyectiles especiales**: Láser devastador con efectos de área
- **Munición estratégica**: Sistema de recarga con penalización temporal
- **Poder especial**: Se carga eliminando enemigos y se activa con 'Q'

### 👾 Enemigos Diversificados
- **Enemigo básico (púrpura)**: Movimiento estándar con disparo básico (20 pts)
- **Tanque (rojo)**: Resistente con 5 puntos de vida y blindaje (50 pts)
- **Enemigo rápido (amarillo)**: Movimiento zigzag impredecible (30 pts)
- **Francotirador (violeta)**: Disparo preciso con movimiento lateral (40 pts)
- **JEFE (rojo oscuro)**: Enemigo épico con múltiples disparos y 15 HP (200 pts)

### 🎁 Power-ups
- **Vida (verde)**: Restaura 30 puntos de vida
- **Munición (azul)**: Recarga completa instantánea
- **Escudo (azul neón)**: Escudo de energía que absorbe 50 puntos de daño
- **Mejora de arma (dorado)**: Aumenta el nivel del armamento
- **Energía especial (violeta)**: Carga 25% del poder especial
- **Velocidad (verde neón)**: Incrementa permanentemente la velocidad de movimiento

### 🎨 Efectos Visuales Espectaculares
- **Fondo estrellado dinámico**: 100 estrellas animadas con brillo parpadeante
- **Sistema de partículas avanzado**: 
  - Explosiones con físicas realistas
  - Efectos de plasma para impactos
  - Partículas de energía para poderes especiales
- **Animaciones de entrada**: Enemigos aparecen con efecto de materialización
- **Efectos de motor**: Llamas animadas en la nave del jugador
- **Barras de estado con transparencia**: HUD moderno y elegante

## 🎯 Controles

### ⌨️ Controles de Teclado
| Tecla | Acción |
|-------|--------|
| WASD / ← → ↑ ↓ | Mover nave |
| ESPACIO | Disparar |
| R | Recargar munición |
| Q | Poder especial (cuando esté cargado) |
| P | Pausar/Reanudar |
| ESC | Volver al menú |

### 🖱️ Controles de Mouse
| Acción | Control |
|--------|---------|
| Click Izquierdo | Disparo automático |
| Click Derecho | Mover nave hacia el cursor |
| Hover | Resaltar botones del menú |
| Click en botones | Navegación completa del menú |

### 🎮 Navegación de Menús
- **Menú principal**: Totalmente interactivo con mouse
- **Botones con efectos hover**: Cambio de color al pasar el cursor
- **Teclas de acceso rápido**: Compatibilidad con teclado (1-4)

## 🏗️ Estructura del Código

### 🔧 Clases Principales

#### `Jugador`
- **Nuevos atributos**: escudo, poder_especial, arma_nivel, tiempo_invulnerable
- **Métodos ampliados**: `usar_poder_especial()`, `añadir_escudo()`, `mejorar_arma()`
- **Movimiento híbrido**: Soporte para teclado y mouse simultáneo
- **Sistema de invulnerabilidad**: Frames de invencibilidad tras recibir daño

#### `Enemigo`
- **Nuevos tipos**: "francotirador" y "jefe" con comportamientos únicos
- **IA mejorada**: Patrones de movimiento específicos por tipo
- **Efectos visuales**: Animación de entrada y barras de vida para enemigos fuertes
- **Disparos diferenciados**: Cada tipo tiene patrones de disparo únicos

#### `Proyectil`
- **Tipos diferenciados**: "basic", "laser", "plasma" con efectos visuales únicos
- **Daño variable**: Diferentes tipos causan distinto daño
- **Efectos visuales**: Animaciones específicas por tipo de proyectil

#### `ProyectilEspecial`
- **Físicas avanzadas**: Movimiento con velocidad en X e Y
- **Efectos devastadores**: Múltiples capas de efectos visuales
- **Tiempo de vida limitado**: Auto-destrucción temporal
- **Alto daño**: 5 puntos de daño por impacto

#### `PowerUp`
- **6 tipos diferentes**: Ampliado de 3 a 6 tipos de mejoras
- **Efectos rotativos**: Animación de rotación constante
- **Aura luminosa**: Efecto de brillo pulsante
- **Símbolos distintivos**: Iconografía única para cada tipo

#### `Particula`
- **Tipos diferenciados**: "explosion", "plasma", "energia"
- **Físicas realistas**: Gravedad y fricción
- **Colores temáticos**: Paleta de colores según el tipo
- **Transparencia progresiva**: Efecto de desvanecimiento

#### `Estrella`
- **Fondo dinámico**: Estrellas en movimiento constante
- **Efectos de brillo**: Parpadeado realista
- **Colores variados**: Múltiples tonalidades
- **Velocidades diferentes**: Efecto de profundidad

#### `BotonMenu`
- **Interactividad completa**: Detección de hover y click
- **Efectos visuales**: Cambio de color en hover
- **Renderizado personalizado**: Estilo consistente con el juego

### 🎨 Funciones de Renderizado

#### Funciones de Menú Actualizadas
- `mostrar_menu_principal_mejorado()`: Título animado con efectos neón
- `mostrar_instrucciones_mejoradas()`: Panel semitransparente con información completa
- `mostrar_puntuaciones_mejoradas()`: Ranking con colores oro, plata y bronce
- `mostrar_game_over_mejorado()`: Detección de récords y efectos visuales
- `mostrar_pausa_mejorada()`: Overlay elegante con panel central

#### Funciones de Juego
- `dibujar_hud_mejorado()`: HUD semitransparente con múltiples barras de estado
- `crear_explosion()`: Soporte para múltiples tipos de partículas
- `crear_estrellas()`: Generación del fondo estrellado dinámico
- `generar_enemigo()`: Sistema basado en nivel con probabilidades de jefe

## 🛠️ Requisitos Técnicos

### Dependencias
```bash
pip install pygame
```