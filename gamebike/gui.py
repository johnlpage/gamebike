import os
import pygame
import time
import random

class GameGUI :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print(f"I'm running under X display = {disp_no}")
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        drivers = ['svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print(f"Driver: {driver} failed.")
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print (f"Framebuffer size: {size[0]} x {size[1]}")
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((50, 0, 0))        
        # Initialise font support
        pygame.font.init()
        pygame.mouse.set_visible(False)
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def showdata(self):
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        # apply it to text on a label
        label = myfont.render("Python and Pygame are Fun!", 1, (255,255,255))
        # put the label object on the screen at point x=100, y=100
        self.screen.blit(label, (100, 100))
        # Update the display    
        pygame.display.update()


if __name__ == "__main__":
    # Create an instance of the PyScope class
    scope = GameGUI()
    scope.showdata()
    
    time.sleep(10)
