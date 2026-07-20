import pygame
import pymunk

SCREEN_DIMENSIONS = (300, 600)

def flipy(y):
    return -y + SCREEN_DIMENSIONS[1]

pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
running = True

space = pymunk.Space()
space.gravity = 0.0, -900.0
BALL_TYPE = 0
TERRAIN_TYPE = 1
SPIKE_TYPE = 2

ball_body = pymunk.Body(mass = 10, moment = 1, body_type=pymunk.Body.DYNAMIC)
ball_body.position = (150, 600)
ball_shape = pymunk.Circle(ball_body, 10)
ball_shape.collision_type = BALL_TYPE
space.add(ball_body, ball_shape)

platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_body.position = (150, 300)
platform_body.angle = 0.5
platform_shape = pymunk.Poly.create_box(platform_body, (120, 10))
platform_shape.collision_type = TERRAIN_TYPE
space.add(platform_body, platform_shape)

def end_sim(arbiter, space, data):
    running = False

can_jump = False
def flip_jump_state(arbiter, space, data):
    global can_jump
    can_jump = not can_jump
space.on_collision(BALL_TYPE, TERRAIN_TYPE, begin=flip_jump_state, separate=flip_jump_state)
space.on_collision(BALL_TYPE, SPIKE_TYPE, begin=end_sim)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif can_jump and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball_body.velocity = (ball_body.velocity.x, 350)
    
    #print(can_jump)
    screen.fill('white')

    # render
    pygame.draw.circle(screen, pygame.Color('black'), 
                       (int(ball_shape.body.position.x), 
                       int(flipy(ball_shape.body.position.y))), 
                       int(ball_shape.radius), 2)
    
    pygame.draw.polygon(screen, pygame.Color('black'), [(v.x, flipy(v.y)) for v in [platform_body.local_to_world(v) for v in platform_shape.get_vertices()]])

    dt = 1.0 / 60.0
    for x in range(1):
        space.step(dt)
    
    if ball_body.position[1] < -50:
        ball_body.position = (150, 600)
        ball_body.velocity = (0, 0)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()