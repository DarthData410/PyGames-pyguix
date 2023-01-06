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

# NOTE: Creating a simple Sprite class:
class simplesprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load(os.path.join(os.path.split(os.path.abspath(__file__))[0],"images/TreeSprite.gif")).convert()
        self.rect = self.image.get_rect()

# NOTE: Simple steps for context based PopupMenus:
# ------------------------------------------------
# STEP1: Define the PopupMenuActions inherited class(es). 
# STEP2: Create context/(name).json file
#   a. Make sure that the file is in PopupMenuContext expected format
#   b. Fill in detials related PopupMenu, MenuItems, actions when clicked, what sprite classes popup is valid for
#   c. Save
# STEP3: Initialize *ANY* PopupMenuActions classes, ie: like example below:
# STEP4: Create PopupMenu instance via pygame.BUTTON_RIGHT for MOUSEBUTTONDOWN event.type
# STEP5: If PopupMenu instance active then call PopupMenu.clicked() passing in event_list:
# STEP6: Check if game varaible 'pu' is of type PopupMenu and if so call update()
#          in order to detect user mouse 'hovering' and change PopupMenuItem to hovertext color from theme

# NOTE: STEP1: Define the PopupMenuActions inherited class(es):
class SpriteActions(ui.PopupMenuActions):

    def get_info(self):
        pmi = self.get_active_menuitem()
        s = pmi.contextof
        print(("SpriteActions.get_info(): %s" % s))
    
    def __init__(self,window,rg):
        self.window = window
        self.rg = rg
        super().__init__()

# NOTE: STEP2: Create context/(name).json file: 
# File: simplesprite.json created in pyguix.ui.context

pygame.init()
window = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
all = pygame.sprite.RenderUpdates()
simple_sprite = simplesprite()
run = True
all.add(simple_sprite)

# NOTE: STEP3: Initialize *ANY* PopupMenuActions classes, ie: like example below:
SpriteActions(window,all)

pu = None # NOTE: initialize variable that will be used for all PopupMenus

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
                # NOTE: STEP4: Create PopupMenu instance via pygame.BUTTON_RIGHT for MOUSEBUTTONDOWN event.type
                ui.PopupMenu.clearall(pu)
                # Create new instance of ui.PopupMenu:
                # NOTE: Using theme/default.json for theme color scheme:
                pu = ui.PopupMenu(
                    window=window,
                    target_mouse_pos=pygame.mouse.get_pos(),
                    rg=all
                )
                     
            elif event.button == pygame.BUTTON_LEFT:
                # NOTE: STEP5: If PopupMenu instance active then call 
                # PopupMenu.clicked() passing in event_list:
                if isinstance(pu,ui.PopupMenu):
                    pu.clicked(event_list)

    # NOTE: STEP6: Check if game varaible 'pu' is of type PopupMenu and if so call update()
    # in order to detect user mouse 'hovering' and change PopupMenuItem to hovertext color from theme
    if isinstance(pu,ui.PopupMenu):
        pu.update()
