import pygame

class Timer:
    def __init__(self, duration, end_func = None):
        self.duration = duration
        self.end_func = end_func
        self.start_time = 0
        self.active = False

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def stop(self):
        self.active = False
        if self.end_func:
            self.end_func()

    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.duration:
                self.stop()