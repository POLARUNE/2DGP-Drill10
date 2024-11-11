from random import randint

from pico2d import get_time, load_image
from state_machine import *
import game_world
import game_framework

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH =  40.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14



class Run:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.action = 2
            bird.face_dir = 1
            bird.dir = 1
        bird.frame = 0
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if bird.action == 2 and int(bird.frame) == 4:
            bird.action = 1
            bird.frame = 0
        if bird.action == 1 and int(bird.frame) == 4:
            bird.action = 0
            bird.frame = 0
        if bird.action == 0 and int(bird.frame) == 3:
            bird.action = 2
            bird.frame = 0
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x <= 0:
            bird.dir, bird.face_dir = 1, 1
        if bird.x >= 1600:
            bird.dir, bird.face_dir = -1, -1

    @staticmethod
    def draw(bird):
        if bird.face_dir == 1:
            bird.image.clip_draw(int(bird.frame) * int(918/5), bird.action * int(506/3), int(918/5), int(506/3), bird.x, bird.y, 80, 80)
        else:
            bird.image.clip_composite_draw(int(bird.frame) * int(918/5), bird.action * int(506/3), int(918/5), int(506/3), 0, 'h', bird.x, bird.y, 80, 80)


class Bird:
    def __init__(self):
        self.x, self.y = randint(0,1600), 500
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()