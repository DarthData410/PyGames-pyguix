
import pygame
import random
import pyguix.ui.elements as ui

# STEP1:
# NOTE: Example SnapHUD Part Information class. Mapped functions deliver information|persist for HUD parts.
class SnapHUDPartInfoExample(ui.SnapHUDPartInfo):

    # NOTE: Example bound function called by reflection OR by in game logic to update 'listening' SnapHUDPart:
    # This example simply allows for setting of value or getting current value when calling .part_one()
    # You can easily add other logic in part_one() that then updates the value when called. 
    # Yet still important is to return the part value.
    def part_one(self,v=None):
        return self.partinfo("part_one",v)
    
    def part_two(self,v=None):
        return self.partinfo("part_two",v)
    
    def part_three(self,v=None):
        return ("P3: %s" % self.part_two())
    
    def part_four(self,v=None):
        return self.partinfo("part_four",v)

    def __init__(self) -> None:
        super().__init__()

# NOTE: pygame init() and game loop variables:
pygame.init()
window = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
all = pygame.sprite.RenderUpdates()
run = True

# NOTE: uncomment following line to set a global theme:
#ui.globaltheme("ex_orange.json")

# STEP2: Create a SnapHUD context file. Can easily copy/paste and modify the context/SnapHUD_default.json file
# The marriage between STEP1 with the rest of the pyguix.ui.elements.SnapHUD* classes and interactions take place
# based on what is in the provided context JSON file. Also default settings file is: pyguix/ui/settings/SanpHUD.json

# STEP3:
# NOTE: Important that the SnapHUDPartInfo class instance for game loop is created before the 
# SnapHUD instance.
shinfo = SnapHUDPartInfoExample()

# STEP4:
# NOTE: SnapHUD instance created AFTER the Info class instance.  
shud = ui.SnapHUD(window=window,rg=all)

# NOTE: Main example game loop:
while run:
    pygame.display.update()
    clock.tick(40)
    event_list = pygame.event.get()
        
    window.fill((125,125,125)) # clear test window
    all.draw(window)

    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            
            # NOTE: When 'u' key is pressed update of snaphud info .part_two() is called.
            # Passing in a random number then as a string value of '<randomint> Points!'
            if event.key == pygame.K_u:
                
                # NOTE: Do something with part_two() HUD display function:
                i = random.randint(1,100)
                ss = ("%s Points!" % i)
                shinfo.part_two(ss)
                
                # NOTE: Do something with part_four() HUD display function:
                if shinfo.part_four() == "what?":
                    shinfo.part_four("then...")
                elif shinfo.part_four() == "then...":
                    shinfo.part_four("what?")
                else:
                    shinfo.part_four("what?")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                
                # STEP5: 
                if shud.clicked(): # NOTE: Check if SnapHUD was clicked()
                    
                    # NOTE: Example for performing some logic and calling to update 
                    # SnapHUDPartInfoExample.part_one() & *.part_two():
                    i = random.randint(1,100)
                    if i < 50:
                        pts = "Less than 50"
                    else:
                        pts = "Greater than 50"
                    shinfo.part_one(("Part One #: %s" % str(i)))
                    shinfo.part_two(pts)
    
    # STEP 6:
    shud.update() # NOTE: update() called to check for 'hover'

