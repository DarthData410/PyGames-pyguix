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
            theme="MessageBox_red.json"
        )
        
        # NOTE: Added for refresh after pop-up menu is cleared.
        self.window.fill((0,0,0))
        self.rg.draw(self.window)

        ui.MessageBox(
            window = self.window,
            message_text = ("%s (x:%s,y:%s)" % (pmi.contextof,str(pmi.contextof.rect.centerx),str(pmi.contextof.rect.centery))),
            title="Sprite Info",
            width=350,
            event_list=pygame.event.get()
        )

    # NOTE: define bound functions section:
    def sprite_cut(self):
        """ EXAMPLE bound function, target of context supplied PopupMenu instance. 'Cut sprite from location.' """
        pmi = self.get_active_menuitem()
        s = pmi.contextof
        self.copy_sprite = s
        s.remove(self.rg)
        # TODO: keep active for 'cut' operation:
        ui.set_spritecache(s)
    
    def sprite_paste(self):
        """ EXAMPLE bound function, target of context supplied PopupMenu instance. 'Paste sprite to location.' """
        pmi = self.get_active_menuitem()
        t = pmi.mouse_pos
        self.copy_sprite.rect.centerx = t[0]
        self.copy_sprite.rect.centery = t[1]
        ret = self.copy_sprite
        self.rg.add(ret)
        # TODO: remove active target after 'paste' operation
        ui.set_spritecache()
    
    def __init__(self,window,rg):
        # TODO: Finalize best way to pass in active display window and renderupdates group.
        # For now setting as below self.window,self.rg
        self.window = window
        self.rg = rg
        # NOTE: call to super to initialize class
        super().__init__()

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
            event_list=pygame.event.get()
        )


    def __init__(self,window,rg):

        self.window = window
        self.rg = rg
        super().__init__()

# NOTE: Class sprite section
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
            surface = pygame.image.load(file).convert()
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

def run():
    pygame.init()
    window = pygame.display.set_mode((600,400))
    clock = pygame.time.Clock()
    run = True

    tr = Tree() # NOTE: Example custom sprite class
    boat = Boat()
    boat.rect.centerx = 100
    boat.rect.centery = 100

    all = pygame.sprite.RenderUpdates()
    pu = None  
    all.add(tr)
    all.add(boat)

    # NOTE:
    # STEP1: Define the PopupMenuActions inherited class. 
    # STEP2: Create context/(name).json file
    #   a. Make sure that the file is in PopupMenuContext expected format
    #   b. Fill in detials related PopupMenu, MenuItems, actions when clicked, what sprite classes popup is valid for
    #   c. Save
    # STEP3: Initialize *ANY* PopupMenuActions classes, ie: like example below:
    SpriteInfo(window,all)
    BoatSpriteActions(window,all)
    # STEP4: Create PopupMenu instance via pygame.BUTTON_RIGHT for MOUSEBUTTONDOWN event.type
    # STEP5: If BUTTOn_LEFT detected and PopupMenu instance active then check against event list.
    #   a. Once user clicks the PopupMenuActions.(action_name) function will be called passing it 
    #       the clicked PopupMenuItem instance to act upon. 

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
                    if pu != None:
                        pu.remove(all)
                    # Create new instance of ui.PopupMenu:
                    pu = ui.PopupMenu(
                        window=window,
                        target_mouse_pos=pygame.mouse.get_pos(),
                        rg=all
                    )
                     
                elif event.button == pygame.BUTTON_LEFT:
                    if pu != None:
                        cpmi = pu.clicked(event_list)
                        if cpmi != None:
                            
                            # NOTE: Clear the test screen.
                            window.fill((0,0,0))
                            pygame.display.flip()

                            # NOTE: Tell PopupMenu instance to remove itself from spriteRenderUpdates() group.:
                            if pu != None:
                                pu.remove(all)
                                pu = None

        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()                      
