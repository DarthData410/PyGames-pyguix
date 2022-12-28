# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Copyright 2022 J. Brandon george
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

import random,os 
import pygame
import pyguix.ui.elements as ui 

# NOTE: Game run time helper class, used to contain PopupMenuActions. Optional, but helpful way to manage.
# Showcases interaction with other pyguix.ui.elements (ie: MessageBox)
class PopupMenuActions_x:

    def menuitem_action_one(self,pmi,window,rg):
        mb = ui.MessageBox(
            window=window,
            message_text=pmi.get_text(),
            title=pmi.get_identity(),
            event_list=pygame.event.get(),
            theme="MessageBox_red.json"
        )
    
    def menuitem_action_two(self,pmi,window,rg):
        mb = ui.MessageBox(
            window=window,
            message_text=pmi.get_text(),
            title=pmi.get_identity(),
            event_list=pygame.event.get()
        )
    
    def menuitem_action_three(self,pmi,window,rg):
        t = random.choice(seq=["MessageBox_blue.json","MessageBox_green.json","MessageBox_orange.json"])
        mb = ui.MessageBox(
            window=window,
            message_text=pmi.get_text(),
            title=pmi.get_identity(),
            event_list=pygame.event.get(),
            theme=t 
        )
    
    def sprite_cut(self,pmi,window,rg):
        s = pmi.contextof
        self.copy_sprite = s
        s.remove(rg)
        return self.copy_sprite
    
    def sprite_paste(self,pmi,window,rg):
        t = pmi.mouse_pos
        self.copy_sprite.rect.centerx = t[0]
        self.copy_sprite.rect.centery = t[1]
        ret = self.copy_sprite
        rg.add(ret)
        self.copy_sprite = None
        return ret

    def __init__(self):

        self.dict_exec = dict()
        self.dict_exec["menuitem_action_one"] = self.menuitem_action_one
        self.dict_exec["menuitem_action_two"] = self.menuitem_action_two
        self.dict_exec["menuitem_action_three"] = self.menuitem_action_three
        self.dict_exec["sprite_cut"] = self.sprite_cut
        self.dict_exec["sprite_paste"] = self.sprite_paste

        self.copy_sprite = None
    
    def execute(self,pmi,window,rg):
        
        if self.dict_exec.__contains__(pmi.get_action()):
            ex = self.dict_exec.get(pmi.get_action())
            ex(pmi,window,rg)
        else:
            print("function %s not found!" % pmi.get_action())

# NOTE: PopupMenuAction class created for use in below example. Matches with pyguix.ui.context.sprite.json - context JSON file.
# Will load the context, validate as part of loading the JSON context file, validate match of JSON context file to class instnace
# Validate actions listed for JSON PopupMenu.menuitems.(menu_item).action:"function_name". 
class SpritePopupMenuActions(ui.PopupMenuActions):

    def __init__(self,context,target):

        super().__init__(context,target)
        
    def __check_valid_class__(self) -> bool:
        ret = False
        if self.__class__.__name__ == self.get_context().get_action_class():
            ret = True
        return ret

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__check_valid_class__()
        return ret



class Tree(pygame.sprite.Sprite):

    
    def get_abs_gamepath(self) -> str:
        """ Loads absolute path for current file GoFIshGame.py """
        return os.path.split(os.path.abspath(__file__))[0] # Get Abs path of current file
    
    def get_resdir(self) -> str:
        """ Loads Resource (*\Res) directory """
        
        ret = os.path.join(self.get_abs_gamepath(),"Res")
        return ret

    def loadimage(self,file) -> pygame.Surface:
        """ Load image file based on current files main dir */Res/(image file).* """

        file = os.path.join(self.get_abs_gamepath(),file)
        try:
            surface = pygame.image.load(file).convert()
        except pygame.error:
            raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}')
        return surface.convert() 
    
    def __init__(self):
        
        super().__init__()

        self.image = self.loadimage("TreeSprite.gif")
        self.rect = self.image.get_rect()
        self.popup_context = "sprite.json"



def run():
    pygame.init()
    window = pygame.display.set_mode((600,400))
    clock = pygame.time.Clock()
    run = True

    tr = Tree() # NOTE: Example custom sprite class
    print(tr.__class__.__name__) # returns 'Tree'
    s = pygame.sprite.Sprite()
    print(s.__class__.__name__) # returns 'Sprite'

    all = pygame.sprite.RenderUpdates()
    pu = None  
    all.add(tr)

    # NOTE: For game loop actions:
    pma = PopupMenuActions_x()
    spma = SpritePopupMenuActions("sprite.json",None) #ui.utils.POPUP_DEFAULT_JSONCONTEXT,None)
    print(spma.__class__.__name__) # returns 'SpritePopupMenuActions'

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
                    # NOTE: POPUP TESTING
                    # ***********************
                    # Check to see if the ui.PopupMenu variable 'pu' is currently NOT set to None type.
                    # If this is the case, then call the pu.remove(all) Sprite method, to remove the 
                    # PopupMenu
                    if pu != None:
                        pu.remove(all)
                    pu = ui.PopupMenu(
                        window=window,
                        contextof=pma.copy_sprite,
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
                            # NOTE: Example of PopupMenu & PopupMenuItem class working with 
                            # MessageBox ui.elements class for showing menu item selected.
                            # -------------------------------------------------------------
                            # Below code is example of operating on PopupMenuItem that was 
                            # 'clicked' by user.:
                            show_box=False
                            pma.execute(cpmi,window,all)
                            
                            # NOTE: Tell PopupMenu instance to remove itself from spriteRenderUpdates() group.:
                            pu.remove(all)
                            pu = None
                            msgbox = None

        pygame.display.update()

if __name__ == '__main__':
    run()
    pygame.quit()
    exit()                      
