
import pygame
import random,os
import pyguix.ui.elements as ui

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

# NOTE: An example PopupMenuActions class, with three function. Mapped to context of sprite_info.json.
class SpriteInfo(ui.PopupMenuActions):
    # NOTE: Simple function, prints PopupMenuItem details, as well as uses ui.MessageBox to show pmi/target sprite info:
    def sprite_info(self):
        # NOTE: self.get_active_menuitem() returns base class 'clicked' menu item, with included contextof. (ie: Sprite class target)
        pmi = self.get_active_menuitem()
        
        print(pmi)
        print(pmi.contextof)
        print(pmi.mouse_pos)
        print(pmi.get_text())
        print(pmi.get_identity())
        print(pmi.get_action())
        
        # NOTE: Added for refresh after pop-up menu is cleared.
        self.window.fill((125,125,125))
        self.rg.draw(self.window)

        # NOTE: Generate ui.MessageBox instance to display passed in expected sprite variable
        ui.MessageBox(
            window=self.window,
            message_text=("Menu Item id: %s, action: %s" % (pmi.get_identity(),pmi.get_action())),
            title=("%s clicked" % pmi.get_text()),
            width=370,
            event_list=pygame.event.get(),
            theme=self.theme
        )
        
        # NOTE: Added for refresh after pop-up menu is cleared.
        self.window.fill((125,125,125))
        self.rg.draw(self.window)

        ui.MessageBox(
            window = self.window,
            message_text = ("%s (x:%s,y:%s)" % (pmi.contextof,str(pmi.contextof.rect.centerx),str(pmi.contextof.rect.centery))),
            title="Sprite Info",
            width=350,
            event_list=pygame.event.get(),
            theme=self.theme
        )

    # NOTE: define bound functions section:
    def sprite_cut(self):
        #EXAMPLE bound function, target of context supplied PopupMenu instance. 'Cut sprite from location.' 
        # *********************************************************************************************
        # NOTE: 'Cut a Sprite' Steps for using globals, (ie: ui.spritecache()) as well as set_enabled()
        # *********************************************************************************************
        # STEP1: Get active menu item, via base class bound function
        pmi = self.get_active_menuitem()
        # STEP2: Create a local variable from the active menu item, 'context of'
        s = pmi.contextof
        # STEP3: Remove the 'context of' Sprite from the targeted RenderUpdates Sprite group.
        s.remove(self.rg)
        # STEP4: Set the ui.spritecache() global variable
        ui.spritecache(s)
        # STEP5: Update what actions are enabled vs. not via base class bound function, set_enabled()
        self.set_enabled('sprite_info',False)
        self.set_enabled('sprite_cut',False)
        self.set_enabled('sprite_paste')
        # *********************************************************************************************
    
    def sprite_paste(self):
        # EXAMPLE bound function, target of context supplied PopupMenu instance. 'Paste sprite to location.' 
        # *********************************************************************************************
        # NOTE: 'Paste a Sprite' Steps (ie: ui.spritecache()) as well as set_enabled()
        # *********************************************************************************************
        # STEP1: Get active menu item, via base class bound function
        pmi = self.get_active_menuitem()
        # STEP2: Get target mouse position, where pointer will 'Paste' sprite.
        t = pmi.mouse_pos
        # STEP3: Call ui.spritecache() to get the current active target (cat)
        s = ui.spritecache()
        # STEP4: Set the rect.center(x,y) to mouse_pos(x,y)
        s.rect.center = t
        # STEP5: Add sprite to target RenderUpdates group 
        self.rg.add(s)
        # STEP6: Call to clear the global spritecache()
        ui.clear_spritecache()
        # STEP7: Update what actions are enabled vs. one's that are not. (Reverse order from sprite_cut)
        self.set_enabled('sprite_paste',False)
        self.set_enabled('sprite_cut')
        self.set_enabled('sprite_info')
        # *********************************************************************************************

    def __init__(self,window,rg,theme="default.json"):
        # TODO: Finalize best way to pass in active display window and renderupdates group.
        # For now setting as below self.window,self.rg
        self.window = window
        self.rg = rg
        self.theme = theme
        # NOTE: call to super to initialize class
        super().__init__()


# NOTE: pygame init() and game loop variables:
pygame.init()
window = pygame.display.set_mode((600,400))
pygame.display.set_caption("all ui.elements demo")
clock = pygame.time.Clock()
all = pygame.sprite.RenderUpdates()
run = True

# NOTE: uncomment following line to set a global theme:
ui.globaltheme("default.json")

# NOTE: Important that the SnapHUDPartInfo class instance for game loop is created before the 
# SnapHUD instance.
shinfo = SnapHUDPartInfoExample()

# NOTE: SnapHUD instance created AFTER the Info class instance.  
shud = ui.SnapHUD(window=window,rg=all)

# NOTE: Class sprite section
# BaseSprite in which all custom Sprite classes are derived from in this example.:
class BaseSprite(pygame.sprite.Sprite):

    def get_abs_gamepath(self) -> str:
        """ Loads absolute path for current file.py """
        return os.path.split(os.path.abspath(__file__))[0] # Get Abs path of current file
    
    def get_resdir(self) -> str:
        """ Loads Resource (*\images) directory """
        
        ret = os.path.join(self.get_abs_gamepath(),"images")
        return ret

    def loadimage(self,file) -> pygame.Surface:
        """ Load image file based on current files main dir */images/(image file).* """

        file = os.path.join(self.get_resdir(),file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}')
        return surface.convert() 

    def __init__(self):

        super().__init__()
# NOTE: Example sprite class:
class Tree(BaseSprite):

    
    def __init__(self):
        
        super().__init__()

        self.image = self.loadimage("TreeSprite.gif")
        self.rect = self.image.get_rect()

tr = Tree()
all.add(tr)

# NOTE: Initialize *ANY* PopupMenuActions classes, ie: like example below:
SpriteInfo(window,all)

# NOTE: Finally create game wide variable used for PopupMenu instance(s):
pu = None

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
            if event.button == pygame.BUTTON_RIGHT:
                ##################################### 
                # NOTE: PopupMenu Example
                # ***********************
                # Check to see if the ui.PopupMenu variable 'pu' is currently NOT set to None type.
                ui.PopupMenu.clearall(pu)
                # Create new instance of ui.PopupMenu:
                pu = ui.PopupMenu(
                    window=window,
                    target_mouse_pos=pygame.mouse.get_pos(),
                    rg=all,
                    theme="ex_blue.json" # NOTE: When globaltheme() set, the THIS VALUE IS OVERRIDE by global.
                )
            
            elif event.button == pygame.BUTTON_LEFT:
                
                # NOTE: If PopupMenu instance active then call PopupMenu.clicked() passing in event_list:
                if isinstance(pu,ui.PopupMenu):
                    pu.clicked(event_list)

                # NOTE: Check if SnapHUD was clicked()
                if shud.clicked(): 
                    
                    # NOTE: Example for performing some logic and calling to update 
                    # SnapHUDPartInfoExample.part_one() & *.part_two():
                    i = random.randint(1,100)
                    if i < 50:
                        pts = "Less than 50"
                    else:
                        pts = "Greater than 50"
                    shinfo.part_one(("Part One #: %s" % str(i)))
                    shinfo.part_two(pts)
    
    shud.update() # NOTE: update() called to check for 'hover'
    
    # NOTE: Check to make sure pu variable is of type ui.PopupMenu, if so then
    # call .update() for updating when user mouse is 'hovering' over PopupMenu.PopupMenuItem
    if isinstance(pu,ui.PopupMenu):
        pu.update()

