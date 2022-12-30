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

import pygame 
import pyguix.__utils__.__help__ as utils

uth = utils.helper()
# NOTE: When an action class is created, the base scope class adds its targetclasses as keys
# to the following dict(), with a value of the action class instance to use
# TODO: Need to finlize elements.init and what is actually done. 
reg_json2pmas = uth.init_reg_json2pmas()
reg_pmas = uth.init_reg_pmas()
reg_tc2pma = dict()

spritecache = dict()
def set_spritecache(v=None):
    """ When v=Sprite, then passed in Sprite is acted upon for executing PopupMenuActions class. \n call set_spritecache() to clear cache. """
    spritecache[utils.POPUP_ACT]=v
set_spritecache()

# ******************************************************************************************

# Classes:
class MessageBox(pygame.sprite.Sprite):
    """ pyguix.ui.elements.MessageBox ui class """

    def __init__(
            self,
            window,
            message_text=utils.MSGBOX_TXT,
            title=utils.MSGBOX_TXT,
            buttons=(utils.MSGBOX_TXT,),
            width=utils.MSGBOX_WIDTH,
            height=utils.MSGBOX_HEIGHT,
            event_list=None,
            theme=utils.MSGBOX_DEFAULT_JSONTHEME,
            rg=None
        ):
        
        super().__init__()

        # Init MessageBox JSON theme file:
        self.theme = self.__init_messagebox_theme__(theme)

        # Init MessageBox dimensions and variables:
        self.__init_messagebox_dimesions__(window,width,height,buttons,message_text,title,event_list)
        
        # MessageBox outline surface:
        self.box_outline_surf = self.__get_box_outline_surf__()
        
        # MessageBox (inner) surface:
        self.box_surf = self.__get_box_surf__()
        
        # Init title details:
        self.__init_title_details__()

        # Init button details. (includes cancel button.):
        self.__init_button_details__()

        # Blit message text surface:
        self.msgtext_surf = self.__get_message_text__()
        self.__blit_msgtext_surf__()
        
        # Blit title outline surface:
        self.__blit_title_outline_surf__()

        # Add MessageBox to sprite.RenderUpdates() group.:
        self.image = self.box_outline_surf
        self.rect = pygame.Rect((self.box_outline_pos+(self.box_outline_width,self.box_outline_height)))
        
        if type(rg) == type(pygame.sprite.RenderUpdates()):
            self.rg = rg
        else:
            self.rg = pygame.sprite.RenderUpdates()

        self.rg.add(self)

        # Check if event_list is sent in, if so 'self-contained' MessageBox mode executing.:
        if self.event_list != None:
            while self.wait(self.event_list):
                self.event_list = pygame.event.get()

    def __init_messagebox_theme__(self,theme) -> utils.MessageBoxTheme:
        """ internal function that loads passed in (or default) MessageBox JSON theme. """
        return utils.MessageBoxTheme(theme)

    def __init_messagebox_dimesions__(self,window,width,height,buttons,message_text,title,event_list):
        """ internal function that initializes the MessageBox dimensions, and passed in variables. """
        self.__wait__ = True
        self.__canceled__ = False
        self.window = window
        self.box_width = width 
        self.box_outline_width = self.box_width+self.theme.get_variables().outlinebuffer
        self.box_height= height
        self.box_outline_height = self.box_height+self.theme.get_variables().outlinebuffer
        self.buttons = buttons
        self.message_text = self.__message_text_max__(message_text)
        self.title = self.__title_text_max__(title)
        self.w_width,self.w_height = window.get_size()
        self.event_list = event_list
    
    def __init_title_details__(self):
        """ internal function that initializes the title, title surface and title outline surface details. """
        self.title_width = self.box_width
        self.title_outline_width = self.title_width
        self.title_height = self.theme.get_title().dimensions.height
        self.title_outline_height = self.title_height + self.theme.get_title().outlinebuffer
        self.title_outline_surf = pygame.Surface((self.title_outline_width,self.title_outline_height))
        self.title_outline_surf.fill(self.theme.get_colors().titleoutline)
        self.title_surf = pygame.Surface((self.title_width,self.title_height))
        self.title_surf.fill(self.theme.get_colors().title)
        # TODO: (12/26/22) Finaize custom font
        title_font = pygame.font.Font(None,self.theme.get_title().fontsize)
        title_font.set_bold(True)
        # TODO: (12/26/22) Finalize custom font
        self.title_text_surf = title_font.render(self.title, True, self.theme.get_colors().text)
        self.title_surf.blit(self.title_text_surf, self.title_text_surf.get_rect(
            center=(
                    (
                        (self.title_width // 2),
                        (self.title_height // 2)
                    ) 
                )
            )
        )
    
    def __init_button_details__(self):
        """ internal function that initializes the button details based on passed in button string names. Includes cancel button. """
        # Cancel button (X):
        self.cancel_button_surf = self.__get_cancel_button__()
        self.__blit_cancel_button__()
        self.__clicked__= utils.MSGBOX_CANCELED_TXT

        # Button dimensions:
        self.btn_dims = self.theme.get_btns().dimensions.wh() 
        self.btn_buffer = self.theme.get_btns().buffer 

        # Build buttons:
        self.btn_array = []
        btn_order = 0
        for b in self.buttons:
            self.btn_array.append(
                (
                    b,
                    self.__get_button__(b,btn_order)
                )
            )
            btn_order += 1
        
        # Blit buttons:
        self.__blit_buttons__()

    def __get_box_outline_surf__(self) -> pygame.Surface:
        """ internal function that returns MessageBox outline surface for element creation. """
        self.box_outline_pos = (
            ((self.w_width // 2)-(self.box_outline_width // 2)),
            ((self.w_height // 2)-(self.box_outline_height // 2))
        )
        ret = pygame.Surface((self.box_outline_width,self.box_outline_height))
        ret.fill(self.theme.get_colors().outline)
        return ret
    
    def __get_box_surf__(self) -> pygame.Surface:
        """ internal function that returns MessageBox surface for element creation. """
        self.box_pos = (
            ((self.box_outline_width // 2)-(self.box_width // 2)),
            ((self.box_outline_height // 2)-(self.box_height // 2))
        )
        ret = pygame.Surface((self.box_width,self.box_height))
        ret.fill(self.theme.get_colors().default)
        return ret
    
    def __blit_box_outline__(self):
        """ internal function that will blit changes made, so they appear on MessageBox. """
        self.box_outline_surf.blit(
            self.box_surf, 
            self.box_surf.get_rect(
                center=(
                    (self.box_outline_width//2),
                    (self.box_outline_height//2)
                )
            )
        )
    
    def __blit_title_outline_surf__(self):
        """ internal function that will blit changes made to title, so they appear on MessageBox. """
        self.title_outline_surf.blit(
            self.title_surf, 
            self.title_surf.get_rect()
        )
        self.box_surf.blit(self.title_outline_surf, self.title_outline_surf.get_rect())
        self.__blit_box_outline__()
    
    def __blit_msgtext_surf__(self):
        """ internal function that will blit MessageBox text to box_surf """
        self.box_surf.blit(
            self.msgtext_surf, 
            self.msgtext_surf.get_rect(
                center=(
                    self.box_width // 2,
                    (self.box_height // 2)-4
                )
            )
        )
    
    def __blit_cancel_button__(self):
        """ internal function that will blit the cancel button to the current title surface. """
        but_center = (
            self.title_width-self.theme.get_cnlbtn().circlebuffer, 
            self.title_height-self.theme.get_cnlbtn().circlebuffer 
        )
        self.title_surf.blit(self.cancel_button_surf,self.cancel_button_surf.get_rect(center=but_center))
    
    def __blit_buttons__(self):
        """ internal function that will blit buttons based on buttons sent as part of instance init() """
        for btn in self.btn_array:
            btup = btn[1] # btup tuple (ie: (surface,(center dimensions)))
            bt_surf = btup[0] # button_surface (bt_surf.get_rect(center=bt_center))
            bt_center = btup[1] # button_center 
            self.box_surf.blit(bt_surf, bt_surf.get_rect(center=bt_center))
    
    def __get_cancel_button_pos__(self) -> tuple:
        """ returns cancel button (X) (x,y) cords for usage of collidepoint() dectection with mouse. """
        ret = ( 
                # X= related to position of MessageBox and width(s):
                self.box_outline_pos[0]+self.box_pos[0]+(
                        self.title_width-self.theme.get_cnlbtn().circlebuffer 
                    )+(
                        self.theme.get_cnlbtn().surfacedimensions.width-( 
                                self.theme.get_cnlbtn().circledimensions.width 
                            )
                        )-(
                            self.theme.get_cnlbtn().circledimensions.radius // 2 
                ),
                # Y= related to position of MessagBox and height(s): 
                self.box_outline_pos[1]+self.box_pos[1]+(
                    self.title_height-self.theme.get_cnlbtn().circlebuffer 
                    )+(
                         self.theme.get_cnlbtn().surfacedimensions.height -( 
                                self.theme.get_cnlbtn().circledimensions.height 
                            )
                        )-(
                            self.theme.get_cnlbtn().circledimensions.radius // 2 
                ) 
            )
        return ret

    def __get_cancel_button__(self,hover=False) -> pygame.Surface:
        """ returns MessageBox cancel button. When hover will highlight in UI. """
        # TODO: (12/26/22) Finalize custom font.
        font = pygame.font.Font(None,self.theme.get_variables().fontsize) 
        butsurf_dims = self.theme.get_cnlbtn().surfacedimensions.wh() 
        button_surf = pygame.Surface(butsurf_dims)
        button_surf.fill(self.theme.get_colors().title)
        
        button_clr = self.theme.get_colors().default
        text_clr = self.theme.get_colors().text
        if hover:
            # DRAW Circle Hover color:
            button_clr = self.theme.get_colors().button
            text_clr = self.theme.get_colors().buttonhovertext

        butcircle_dims = self.theme.get_cnlbtn().circledimensions.wh() 
        text_surface = font.render(self.theme.get_cnlbtn().circletext, True, text_clr)
        # DRAW Circle:
        cbr = self.theme.get_cnlbtn().circledimensions.radius
        pygame.draw.circle(button_surf,button_clr,butcircle_dims,cbr,cbr) 
        # BLIT to button_surface that will be returned:
        button_surf.blit(text_surface, text_surface.get_rect(center = butcircle_dims))
        return button_surf        
    
    def __get_button__(self,b,border=0,hover=False) -> tuple:
        """ returns a new messagebox button for use with messagebox. """
        # TODO: (12/26/22) Finalize custom font
        font = pygame.font.Font(None, self.theme.get_variables().fontsize)
        dims_center = ((self.btn_dims[0] // 2)+1,(self.btn_dims[1] // 2)+1) 
        button_surf = pygame.Surface(self.btn_dims)
        
        # Hover Outline setup:
        bod = self.btn_dims[0]+2,self.btn_dims[1]+2
        button_outline = pygame.Surface(bod)
        
        button_outline_clr = self.theme.get_colors().titleoutline 
        button_text_clr = self.theme.get_colors().text 

        if hover:
            button_outline_clr = self.theme.get_colors().buttonhover 
            button_text_clr = self.theme.get_colors().buttonhovertext 

        button_outline.fill(button_outline_clr)
        # TODO: (12/26/22) Finalize custom font
        text_surface = font.render(b, True, button_text_clr) 

        button_surf.fill(self.theme.get_colors().button)
        button_surf.blit(text_surface, text_surface.get_rect(center = (dims_center[0],(dims_center[1]))))
        button_outline.blit(button_surf, button_surf.get_rect(center = (dims_center[0],dims_center[1])))

        tar_width = (self.box_width // self.buttons.__len__())
        tar_width = (tar_width // 2) + (tar_width * border)
        
        button_center = (
            (tar_width), 
            ((self.box_height-self.btn_dims[1])+self.btn_buffer)
        )

        ret = (button_outline,button_center)
        return ret
    
    def __get_button_pos__(self,bc) -> tuple:
        """ internal function that will use the passed in bc (button cetner) current value and calculate (x,y) cords/POSition for given button. """
        return (
            self.box_outline_pos[0]+self.box_pos[0]+bc[0],
            self.box_outline_pos[1]+self.box_pos[1]+bc[1]
        )
    
    def __get_message_text__(self) -> pygame.Surface:
        """ returns a surface that is ready for blit() call upon message box surface to display messagebox message. """
        # TODO: (12/26/22) Finalize custom font.
        font = pygame.font.Font(None, self.theme.get_variables().fontsize)
        text_surface = font.render(self.message_text, True, self.theme.get_colors().text)
        return text_surface    
    
    def __message_text_max__(self,msg) -> str:
        """ returns safe text for message, based on max constant percentage of message box width. """
        return self.__base_text_max__(msg, self.theme.get_variables().messagemax)

    def __title_text_max__(self,msg) -> str:
        """ returns safe text for title, based on max constant percentage of message box width. """
        return self.__base_text_max__(msg,self.theme.get_variables().titlemax,self.theme.get_title().textupcase)

    def __base_text_max__(self,s,max,up=False) -> str:
        """ base internal function called for safe title and message text. """
        if s.__len__() > (self.box_width * max):
            m = int(self.box_width*max)
            r = (s.__len__()-m)+3
            s = uth.str_rtrim(s,r)
            s = ("%s..." % s)
        if up:    
            s = s.upper()    
        return s

    def __event_list_check_keys__(self,event_list):
        """ internal function that will process passed in event_list for key pressed while MessageBox is active and take directed action. """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__wait__ = False
                    self.__clicked__ = utils.MSGBOX_CANCELED_TXT
                    self.__canceled__ = True
                elif event.key == pygame.K_RETURN:
                    self.__wait__ = False
                    self.__clicked__ = self.buttons[self.theme.get_btns().returnbutton] 

    def __event_list_check_button__(self,event_list,b=utils.MSGBOX_CANCELED_TXT):
        """ internal function that will process passed in event_list and update MessageBox properties. """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.__wait__ = False # set wait() to False
                    if b != utils.MSGBOX_CANCELED_TXT:
                        self.__clicked__ = b # set clicked() to selected button text.
                    else:
                        self.__clicked__ = utils.MSGBOX_CANCELED_TXT # set clicked() to CANCELED_TXT
                        self.__canceled__ = True
  
    def __update_cancel_button__(self,event_list):
        """ internal function that uses passed in event_list and operates off of it to track user intreaction with MessageBox cancel button. """
        # CANCEL BUTTON (X):
        cancelbtn_pos = self.__get_cancel_button_pos__()
            
        # NOTE: (12/24/22) Check for mouse collide with rect of cancel button.
        # if so mark as hover and change UI to show hover button.:
        cbhover = self.cancel_button_surf.get_rect(center=cancelbtn_pos).collidepoint(pygame.mouse.get_pos())
        if cbhover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.cancel_button_surf = self.__get_cancel_button__(True)
            self.__event_list_check_button__(event_list)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.cancel_button_surf = self.__get_cancel_button__()
        self.__blit_cancel_button__()
        # NOTE: Blit title outline surface so changes to cancel button appear.:
        self.__blit_title_outline_surf__()
    
    def __update_buttons__(self,event_list):
        """ internal function that uses passed in event_list and operates off of it to track user interaction with MessageBox buttons for selection choice / .clicked() value. """
        count=0
        for btn in self.btn_array:
            bt = btn[0] # bt string (ie: 'Yes','No')
            btup = btn[1] # btup tuple (ie: (surface,(center dimensions)))
            bt_surf = btup[0] # button_surface (bt_surf.get_rect(center=bt_center))
            bt_center = btup[1] # button_center 
            
            # NOTE: (12/23/22) Check for mouse collide with rect of button from array.
            # if so mark as hover and change UI to show hover of button vs. not.
            btn_pos = self.__get_button_pos__(bt_center)
            hover = bt_surf.get_rect(center=btn_pos).collidepoint(pygame.mouse.get_pos())
            self.btn_array.pop(count) # Remove button from array
            if hover:
                nb = self.__get_button__(bt,count,True) # Get hover button
                self.__event_list_check_button__(event_list,bt)
            else:
                nb = self.__get_button__(bt,count) # Get standard button

            nb_surf = nb[0]
            nb_center = nb[1]
            self.box_surf.blit(nb_surf, nb_surf.get_rect(center=nb_center))
            self.__blit_box_outline__()
            self.btn_array.insert(count,(bt,nb))
            count += 1
    
    def update(self, event_list):
        """ called from the wait() method to process the buttons and to check collide against each MessageBox button. """
        # Cancel Button:
        self.__update_cancel_button__(event_list)

        # Selection Buttons:
        self.__update_buttons__(event_list)

        # Check for keys pressed by user (ie: return or esacpe keys):
        self.__event_list_check_keys__(event_list)

        # DRAW MessageBox and update display:
        self.rg.draw(self.window)
        pygame.display.flip()

    def wait(self,event_list) -> bool:
        """ returns True if waiting for user input, False if user has made a choice. """
        self.update(event_list)
        if not self.__wait__:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        return self.__wait__
    
    def clicked(self) -> str:
        """ returns the string value of the button text pressed. """
        return self.__clicked__
    
    def canceled(self) -> bool:
        """ returns True if MessageBox instance was canceled, False otherwise. """
        return self.__canceled__

# NOTE: PopupMenu Section:
class PopupMenuActions(object):
    """ pyguix.ui.elements.PopupMenuActions class. Meant to be subed and paired with context (*.json) file for menu item actions. """

    def __init__(self):
        
        # TODO: Finalize a 'safe' method for checking full type as str vs. loaded json2pmans mapping dict().
        self.__context_name__ = reg_json2pmas[str("%s" % type(self))] #context

        self.__context__ = self.__init_context__()
        self.__target__ = ""
        self.__target_classes__ = self.__init_target_classes__()
        self.__funcmap__ = self.__init_funcmap__()

        if not self.__is_valid__():
            errmsg = ("Invalid JSON context (%s) supplied mapping with PopupMenuActions (%s) class. [pyguix]" % (self.get_context_name(),self.get_context().get_action_class()))
            raise LookupError(errmsg)    
     
        # TODO: Need to finalize context and contextof vars and how these are used through instance.
        if reg_pmas[self.get_context().get_action_class()] == None:
            reg_pmas[self.get_context().get_action_class()] = self
            for t in self.get_target_classes():
                if not reg_tc2pma.__contains__(t):
                    reg_tc2pma[t] = self.get_context().get_action_class()
                else:
                    raise LookupError(("Targetclass (%s) listed multiple times. Look at JSON Context files. Current file %s [pyguix]" % (t,self.get_context_name())))

        self.__act_pmi__ = None

    def __is_valid__(self) -> bool:
        """ base is_valid checks """
        ret = self.__check_valid_class__()
        ret = ret and self.__check_valid_functions__()
        return ret
    
    def __init_context__(self) -> utils.PopupMenuContext:
        return utils.PopupMenuContext(self.get_context_name())
    
    def __init_target_classes__(self) -> tuple:
        return self.get_context().get_target_classes()
    
    def __init_funcmap__(self) -> dict:
        ret = dict()
        for mi in self.get_context().get_menuitems():
            if mi.type == utils.PopupMenuItemType.Action:
                ret[mi.identity] = mi.action
        return ret

    def __add_function__(self,k,v):
        self.__functions__[k] = v

    def __check_valid_functions__(self) -> bool:
        ret = True
        for mi in self.get_funcmap():
            func = self.get_funcmap().get(mi)
            found = False
            for s in self.__dir__():
                if func == s:
                    found = True
            ret = ret and found
            if not found:
                raise LookupError(
                    ("Bad match between JSON context file (%s) mapping and action class (%s) [pyguix] \n Issue with function (%s) missing from action class. [pyguix]" % (
                        self.get_context_name(),
                        self.get_context().get_action_class(),
                        func)
                )
            )
        return ret
    
    def __check_valid_class__(self) -> bool:
        ret = False
        if ("%s" % type(self)) == self.get_context().get_action_class():
        #if self.__class__.__name__ == self.get_context().get_action_class():
            ret = True
        if not ret:
            raise LookupError("JSON context file (%s) with name %s & %s class don't match. Check the JSON file. [pyguix]" % (self.get_context_name(),self.get_context().get_action_class(),self.__class__.__name__))
        return ret

    def get_isvalid(self) -> bool:
        return self.__isvalid__
    
    def get_context_name(self) -> str:
        return self.__context_name__
    
    def get_context(self) -> utils.PopupMenuContext:
        return self.__context__

    def set_target(self,target):
        self.__target__ = target
    
    def get_target(self):
        return self.__target__
    
    def get_target_classes(self):
        return self.__target_classes__
    
    def get_funcmap(self):
        return self.__funcmap__
    
    def get_active_menuitem(self):
        return self.__act_pmi__

    def execute(self): # TODO: Need to finalize
        ex = self.get_funcmap().get(self.__act_pmi__.get_identity())
        eval(("self.%s()" % (ex)))

class PopupMenuItem(pygame.Surface):
    """ pyguix.ui.elements.PopupMenuItem ui class """

    def __init__(self,window,dataclass,pos=(0,0),dims=(0,0)):

        super().__init__(size=dims)

        self.__dataclass__ = dataclass
        self.__init_dimensions(window,pos,dims)
        self.image = self.__init_item__()
        self.rect = pygame.Rect((pos,dims))
        self.mouse_pos = (0,0)
        self.contextof = None
        
    def __init_dimensions(self,window,pos,dims):
        self.window = window
        self.width = dims[0]
        self.height = dims[1]
        self.w_width,self.w_height = window.get_size()
        if self.__get_pmi__().type == utils.PopupMenuItemType.Separator:
            i=0
            ntext = uth.get_sepchar2text(self.__get_pmi__().text)
            while i < self.width:
                i+=1
                ntext = ntext + uth.get_sepchar2text(self.__get_pmi__().text)
            self.__get_pmi__().text = ntext

        self.pos = pos
        self.dims = dims
    
    def __get_pmi__(self) -> utils.PopupMenuItem:
        return self.__dataclass__

    def __init_item__(self) -> pygame.Surface:
        f = pygame.font.Font(None,18) # TODO: Finalize font from theme JSON
        text_surface = f.render(self.get_text(), True, (230,220,210)) # TODO: Finalize text color from theme JSON
        return text_surface
    
    def get_text(self) -> str:
        return self.__get_pmi__().text
    def get_type(self) -> utils.PopupMenuItemType:
        return self.__get_pmi__().type
    def get_identity(self) -> str:
        return self.__get_pmi__().identity
    def get_action(self) -> str:
        return self.__get_pmi__().action
    def get_clicked(self) -> bool:
        return self.__get_pmi__().clicked

class PopupMenu(pygame.sprite.Sprite):
    """ pyguix.ui.elements.PopupMenu ui class """

    def __init__(self,window,context=utils.POPUP_DEFAULT_JSONCONTEXT,contextof=None,rg=None,target_mouse_pos=(0,0)):

        super().__init__()

        self.tpma = None

        if type(rg) == type(pygame.sprite.RenderUpdates()):
            self.rg = rg
        else:
            self.rg = pygame.sprite.RenderUpdates()

        # determine if ANY object class was clicked on.:
        # NOTE: Get class for popup mouse pos collide context of:
        if spritecache[utils.POPUP_ACT] != None:
            self.__contextof__ = spritecache[utils.POPUP_ACT]  
        else:
            self.__contextof__ = self.__get_contextof__()
        
        self.__contextof_pum__ = self.__init_context_of__(self.__contextof__)

        # Init PopupMenu context JSON file:
        self.__context__ = self.__init_popup_context__(self.__contextof_pum__) #context)
        if self.__context__.get_action_class() == "" or self.__context__.get_action_class() == None:
            # DO NOT RENDER POPUP
            return

        # Init MessageBox dimensions and variables:
        self.__init_dimensions__(window)
        
        self.rg.add(self)
        self.update()
        self.target_mouse_pos=target_mouse_pos
    
    def __init_popup_context__(self,context) -> utils.PopupMenuContext:
        return utils.PopupMenuContext(context)

    def __init_context_of__(self,cat):
        tos = ("%s" % type(cat))
        ret = None

        if cat != None:
            # NOTE: Following tos must be a perfect match <class '(module).(class)'> 
            # (ie: <class '__main__.SomeSpriteClass'>)
            if reg_tc2pma.__contains__(tos): 
                    tos_pma = reg_pmas[reg_tc2pma[tos]] 
                    self.tpma = tos_pma
                    ret = tos_pma.get_context_name()
                    #break

        if ret == None:
            ret = utils.POPUP_DEFAULT_JSONCONTEXT
        
        return ret
    
    def __get_contextof__(self): 
        # NOTE: Based on passed in RenderUpdates group, grab Sprite (if any) that collide with pygame.mouse.get_pos()
        ret = None
        for s in self.rg:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                ret = s
        return ret

    def __init_dimensions__(self,window):
        self.window = window
        self.dims = self.__get_context__().get_dimensions() # NOTE: Now part of PopupMenu_*.json context file. 
        self.width = self.dims.width
        self.box_outline_width = self.width + 4 # TODO: Remove hardcoded buffer
        self.height = self.dims.height
        self.box_outline_height = self.height + 4 # TODO: Remove hardcoded buffer
        self.w_width,self.w_height = window.get_size()
        self.pmis=[]
        self.__clicked__ = None
    
    def __get_box_outline_surf__(self,pos=(0,0)) -> pygame.Surface:
        """ internal function that returns MessageBox outline surface for element creation. """
        if pos == (0,0):
            pos = ((self.w_width // 2),(self.w_height // 2))

        self.box_outline_pos = (
            (pos[0]+4), 
            (pos[1]+4) 
        )

        # Check to make sure that pos will not allow popup to draw beyond window bounds:
        bop = self.box_outline_pos
        wd = (self.w_width,self.w_height)
        bod = (self.box_outline_width,self.box_outline_height)
        # TODO: (12/26/22) - Need to revisit this when target is passed in vs. just cords. 
        # mostly works except for bottom right hand corner of screen. 
        if bop[0]+bod[0] > wd[0]:
            bop = (
                bop[0]-(
                    (bop[0]+bod[0])-wd[0]
                ),
                bop[1]
            )
        
        if bop[1]+bod[1] > wd[1]:
            bop = (
                bop[0],
                bop[1] - (
                    (bop[1]+bod[1])-wd[1]
                )
            )
        
        self.box_outline_pos = bop
        # NOTE: End check for screen/display placemenet of popup
        ret = pygame.Surface((self.box_outline_width,self.box_outline_height))
        ret.fill((100,100,100))  #self.theme.get_colors().outline)
        return ret

    def __get_button__(self,pos,dc) -> PopupMenuItem:

        pmi = PopupMenuItem(
            window=self.window,
            dataclass=dc,
            pos=pos,
            dims=(self.dims.width,15) # TODO: Need to finalize dimensions of menu items vs. hardcoded height value
        )
        return pmi
    
    def __get_context__(self) -> utils.PopupMenuContext:
        return self.__context__

    def update(self):

        # MessageBox outline surface:
        pos = pygame.mouse.get_pos()
        self.box_outline_surf = self.__get_box_outline_surf__(pos=pos)
        
        # TODO: Move the following section for an __init__* to build out menu items, seprators, etc.
        miorder=0
        for mi in self.__get_context__().get_menuitems():
            pos2=(
                self.box_outline_pos[0],(self.box_outline_pos[1]+((15+5)*miorder)) #<-NOTE: [A] MUST MATCH [B] + BUFFER *************
            )
            p2 = self.__get_button__(pos2,mi)
            pis2 = pygame.Surface(size=(self.dims.width,15)) # TODO: Need to finalize dimensions of menu items.
            pis2.fill((100,100,100)) # TODO: Finalize color theme apply.
            pis2.blit(p2.image,p2.image.get_rect())
            self.box_outline_surf.blit(pis2,pis2.get_rect(topleft=(
                        pis2.get_rect().x,(pis2.get_rect().y+((15+5)*miorder)) #<-NOTE: [B] HERE IS B! + BUFFER ******************
                    )
                )
            )
            self.pmis.append(p2)
            miorder+=1


        # Add popup to sprite.RenderUpdates() group.:
        self.image = self.box_outline_surf
        self.rect = pygame.Rect((self.box_outline_pos+(self.box_outline_width,self.box_outline_height)))

        self.rg.draw(self.window)
        pygame.display.flip()

    def clicked(self,event_list=None) -> PopupMenuItem:

        ret = self.__clicked__
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for p in self.pmis:
                        if p.get_type() == utils.PopupMenuItemType.Action:
                            if p.rect.collidepoint(pygame.mouse.get_pos()):
                                p.mouse_pos = self.target_mouse_pos
                                p.contextof = self.__contextof__
                                self.__clicked__ = p
                                ret = p
                                
                                # NOTE: Must remove self from passed in render group.
                                self.remove(self.rg)
                                # NOTE: This will use the target PopupMenuAction instance and call to 
                                # execute() the active PopupMenuItem related action:
                                if self.tpma != None:
                                    self.tpma.__act_pmi__ = p
                                    self.tpma.execute()
                                    

        return ret
# NOTE: End PopupMenu Section

                            