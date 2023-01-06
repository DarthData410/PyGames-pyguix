# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Copyright 2022 J. Brandon George
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import pygame
import pyguix.ui.elements as ui 

# NOTE: ui.PopupMenuActions classes section:
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
        self.window.fill((0,0,0))
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
        self.window.fill((0,0,0))
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
    
# NOTE: A ui.PopupMenuActions instance that has a single function/action mapping for Boat sprite to show info.
class BoatSpriteActions(ui.PopupMenuActions):

    def info(self):
        pmi = self.get_active_menuitem()

        self.window.fill((0,0,0))
        self.rg.draw(self.window)

        ui.MessageBox(
            window = self.window,
            message_text = ("%s (x:%s,y:%s)" % (pmi.contextof,str(pmi.contextof.rect.centerx),str(pmi.contextof.rect.centery))),
            title="Sprite Info",
            width=350,
            event_list=pygame.event.get(),
            theme=self.theme
        )


    def __init__(self,window,rg,theme="default.json"):

        self.window = window
        self.rg = rg
        self.theme = theme
        super().__init__()

# NOTE: A ui.PopupMenuActions instance that has a single function/action mapping for River sprite to change its image.
class RiverSpriteActions(ui.PopupMenuActions):

    def change_image(self):
        pmi = self.get_active_menuitem()
        s = pmi.contextof
        if s.direction=="up":
            s.image = s.images[0]
            s.direction = "down"

        else:
            s.image = s.images[1]
            s.direction = "up"
        #print(("%s sprite image changed." % str(s)))
           
    def __init__(self,window,rg):
        self.window = window
        self.rg = rg
        super().__init__()

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

class Tree(BaseSprite):

    
    def __init__(self):
        
        super().__init__()

        self.image = self.loadimage("TreeSprite.gif")
        self.rect = self.image.get_rect()

class Boat(BaseSprite):

    def __init__(self):

        super().__init__()

        self.image = self.loadimage("BoatSprite.gif")
        self.rect = self.image.get_rect()        

class River(BaseSprite):

    def __init__(self):

        super().__init__()

        self.images = [
            self.loadimage("LandRiverSprite.gif"),
            self.loadimage("LandRiverSprite_UP.gif")
        ]
        
        self.direction = "down"
        self.image = self.images[0]
        self.rect = self.image.get_rect()
# END SPRITE Define Section.

def run():
    pygame.init()
    window = pygame.display.set_mode((600,400))
    pygame.display.set_caption("Right click on any Sprite|Image")
    clock = pygame.time.Clock()
    run = True

    # NOTE: 
    # Add sprites to game, and set starting x,y pos.
    tr = Tree()
    boat = Boat()
    boat.rect.centerx = 100
    boat.rect.centery = 100
    ri = River()
    ri.rect.centerx = 200
    ri.rect.centery = 200
    
    # NOTE:
    # Create a RenderUpdates() group used for game, add sprites.
    all = pygame.sprite.RenderUpdates()
    all.add(tr)
    all.add(boat)
    all.add(ri)

    # NOTE: Set globaltheme to be used across all elements. When supplied, overrides instance specific theme supplied:
    ui.globaltheme("ex_red.json")
    
    # NOTE: Initialize *ANY* PopupMenuActions classes, ie: like example below:
    # NOTE: Comment out an example PopupMenuActions derived class below. You will notice that the mapped context
    # will not take place, and therefore no detection of a PopupMenu to render. This is why initialization of
    # specific game instance PopupMenuActions ONCE creates the needed pyguix.ui.elements.globalcontext() values
    SpriteInfo(window,all)
    BoatSpriteActions(window,all)
    RiverSpriteActions(window,all)

    # NOTE: Finally create game wide variable used for PopupMenu instance(s):
    pu = None  

    # NOTE: Main game loop:
    while run:
        pygame.display.update()
        clock.tick(40)
        event_list = pygame.event.get()
        
        window.fill((0,0,0)) # clear test window
        all.draw(window)
        
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
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

        # NOTE: Check to make sure pu variable is of type ui.PopupMenu, if so then
        # call .update() for updating when user mouse is 'hovering' over PopupMenu.PopupMenuItem
        if isinstance(pu,ui.PopupMenu):
            pu.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()                      
