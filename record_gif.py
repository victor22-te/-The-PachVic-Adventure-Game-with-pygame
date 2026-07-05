import pygame
import os
import imageio

pygame.init()
pygame.display.set_mode((800, 500)) # hidden or not, just need a surface

directory = os.path.dirname(os.path.realpath(__file__))
bg = pygame.image.load(os.path.join(directory, 'sprites', 'levelBackground.png')).convert_alpha()
player = pygame.image.load(os.path.join(directory, 'sprites', 'Nave2.jpg')).convert_alpha()
meteor1 = pygame.image.load(os.path.join(directory, 'sprites', 'm1.png')).convert_alpha()
meteor2 = pygame.image.load(os.path.join(directory, 'sprites', 'm2.jpg')).convert_alpha()

surf = pygame.Surface((800, 500))

frames = []
bg_y1 = -500
bg_y2 = 0

player_x = 400
meteor_y = -50

for i in range(60): # 60 frames = 3 seconds at 20fps
    # update logic
    bg_y1 += 5
    bg_y2 += 5
    if bg_y1 >= 500: bg_y1 = -500
    if bg_y2 >= 500: bg_y2 = -500
    
    player_x += 2 if i < 30 else -2
    meteor_y += 8
    
    # draw
    surf.blit(bg, (0, bg_y1))
    surf.blit(bg, (0, bg_y2))
    surf.blit(player, (player_x, 400))
    surf.blit(meteor1, (300, meteor_y))
    surf.blit(meteor2, (450, meteor_y - 200))
    
    # capture
    frame = pygame.surfarray.array3d(surf)
    frame = frame.transpose([1, 0, 2])
    frames.append(frame)

if not os.path.exists("media"):
    os.makedirs("media")
imageio.mimsave("media/gameplay.gif", frames, fps=20)
print("GIF saved successfully!")
pygame.quit()
