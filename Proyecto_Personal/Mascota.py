import pygame
import win32gui
import win32con
import random

#--- Inicializar pygame.

pygame.init()

#--- Tamaño de la mascota.
width, height = 200, 150

#--- Crear la ventana de la mascota sin bordes.
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.DOUBLEBUF)
pygame.display.set_caption("Mascota")

# Hacer ventana transparente
hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    | win32con.WS_EX_LAYERED
)

win32gui.SetLayeredWindowAttributes(
    hwnd,
    0,
    255,
    win32con.LWA_ALPHA
)

# Color transparente
TRANSPARENT = (255, 0, 255)
screen.fill(TRANSPARENT)
color_key = TRANSPARENT[0] | (TRANSPARENT[1] << 8) | (TRANSPARENT[2] << 16)

win32gui.SetLayeredWindowAttributes(
    hwnd,
    color_key,
    0,
    win32con.LWA_COLORKEY
)

# Cargar imagen (pon aquí tu imagen)
mascota = pygame.image.load("mascota.png").convert_alpha()
mascota = pygame.transform.scale(mascota, (width, height))

# Tamaño pantalla
info = pygame.display.Info()
screen_w = info.current_w
screen_h = info.current_h

# Posición inicial
x = random.randint(0, screen_w - width)
y = random.randint(0, screen_h - height)

# Velocidad
vx = 2
vy = 2

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover ventana
       
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          int(x), int(y), width, height,
                          win32con.SWP_SHOWWINDOW)

    screen.fill(TRANSPARENT)
    screen.blit(mascota, (0, 0))
    pygame.display.update()


    
    # Rebotar en bordes (sin temblar)
    if x <= 0:
        x = 0
        vx *= -1

    elif x >= screen_w - width:
        x = screen_w - width
        vx *= -1


    if y <= 0:
        y = 0
        vy *= -1

    elif y >= screen_h - height:
        y = screen_h - height
        vy *= -1


    # Limpiar
    screen.fill(TRANSPARENT)

    # Dibujar
    screen.blit(mascota, (0, 0))

    # Mover ventana
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        int(x),
        int(y),
        0,
        0,
        win32con.SWP_NOSIZE
    )

    pygame.display.update()

pygame.quit()