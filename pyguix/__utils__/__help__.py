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


import io
import dataclasses as dc
import enum
import json as js
import pyguix.ui.themes as th
import pyguix.ui.context as cx

# Constants:
MSGBOX_WIDTH=260
MSGBOX_HEIGHT=110
MSGBOX_TXT='OK'
MSGBOX_CANCELED_TXT='CANCELED'
DEFAULT_ENCODING='utf-8' 
MSGBOX_DEFAULT_JSONTHEME='MessageBox_default.json'
MSGBOX_ISSUES_MSG='Issues loading supplied JSON MessageBox theme file. Loading default.'
DC_DIMS_WIDTH="width"
DC_DIMS_HEIGHT="height"
DC_RADIUS="radius"
POPUP_SEPCHAR="[&SEP]"
POPUP_SEPTEXT="-"
POPUP_DEFAULT_JSONCONTEXT='default.json'
POPUP_ISSUES_MSG='Issues loading supplied JSON PopupMenu context file. Loading default.'

# Enums:
PopupMenuItemType = enum.IntEnum('PopupMenuItemType','Action Separator')

# Dataclasses:
# Base dataclasses:
@dc.dataclass
class dimensions:
    width: int
    height: int
    radius: int

    def wh(self) -> tuple:
        """ returns tuple of (width,height) from loaded values """
        return (self.width,self.height)

    def new(v):
        ret = dimensions(
            width=int(v[DC_DIMS_WIDTH]),
            height=int(v[DC_DIMS_HEIGHT]),
            radius=int(v[DC_RADIUS])
        )
        return ret

@dc.dataclass
class color:
    RGB: tuple
    red: int
    green: int
    blue: int

    def new(v):
        r=v["RGB"]
        ret = color(
            RGB=r,
            red=int(r[0]),
            green=int(r[1]),
            blue=int(r[2])
        )
        return ret
    
    def astuple(v):
        nc = color.new(v["color"])
        ret = nc.RGB
        return ret

# MessageBox dataclasses:
@dc.dataclass
class MessageBoxVariables:
    titlemax: float
    messagemax: float
    fontsize: int
    outlinebuffer: int

    def new(v):
        ret = MessageBoxVariables(
            titlemax=float(v["title_max"]),
            messagemax=float(v["message_max"]),
            fontsize=int(v["font_size"]),
            outlinebuffer=int(v["outline_buffer"])
        )
        return ret

@dc.dataclass
class MessageBoxColors:
    default: tuple
    title: tuple
    text: tuple
    button: tuple
    outline: tuple
    titleoutline: tuple
    buttonhover: tuple
    buttonhovertext: tuple

    def new(v):
        ret = MessageBoxColors(
            default=color.astuple(v["default"]),
            title=color.astuple(v["title"]),
            text=color.astuple(v["text"]),
            button=color.astuple(v["button"]),
            outline=color.astuple(v["outline"]),
            titleoutline=color.astuple(v["title_outline"]),
            buttonhover=color.astuple(v["button_hover"]),
            buttonhovertext=color.astuple(v["button_hover_text"])
        )
        return ret

@dc.dataclass
class MessageBoxTitle:
    dimensions: dimensions
    outlinebuffer: int
    fontsize: int
    textupcase: bool

    def new(v):
        ret = MessageBoxTitle(
            dimensions=dimensions.new(v["dimensions"]),
            outlinebuffer=int(v["outline_buffer"]),
            fontsize=int(v["font_size"]),
            textupcase=bool(v["text_upcase"])
        )
        return ret

@dc.dataclass
class MessageBoxCancelButton:
    surfacedimensions: dimensions
    circledimensions: dimensions
    circlebuffer: int
    circletext: str

    def new(v):
        ret = MessageBoxCancelButton(
            surfacedimensions=dimensions.new(v["surface"]["dimensions"]),
            circledimensions=dimensions.new(v["circle"]["dimensions"]),
            circlebuffer=int(v["circle"]["buffer"]),
            circletext=v["circle"]["default_text"]
        )
        return ret

@dc.dataclass
class MessageBoxButtons:
    dimensions: dimensions
    buffer: int
    returnbutton: int
    defaulttext: str

    def new(v):
        ret = MessageBoxButtons(
            dimensions=dimensions.new(v["dimensions"]),
            buffer=int(v["buffer"]),
            returnbutton=int(v["return_button"]),
            defaulttext=v["default_text"]
        )
        return ret

# PopupMenu dataclasses:
@dc.dataclass
class PopupMenuItem:
    text: str
    type: PopupMenuItemType
    identity: str
    action: str 
    clicked: bool = False

    def new(v,id):
        ret = PopupMenuItem(
            text=v["text"],
            type=PopupMenuItemType.Action if int(v["type"]) == 0 else PopupMenuItemType.Separator,
            identity=id,
            action=v["action"]
        )
        return ret

# Classes:
class jsonfile:
    
    def __init__(self,file_path,file):
        self.helper = helper()
        self.__file_path__ = file_path
        self.__file__ = file
        self.filebytes = self.__init__jsontheme_file__()
        self.__encode_type__ = js.detect_encoding(self.filebytes) # Enconding type match
        # TODO: (12/25/22) - Added logic to check against encoding constant and throw error if failed, and use default. 
        self.__jsdict__ = js.loads(self.filebytes) # json file load to dict class

    def __init__jsontheme_file__(self) -> bytes:
        """ internal function that read the path of the themes lib, and loads the passed in JSON theme file. (theme_name) """
        self.__path__ = self.helper.safe_path(self.__file_path__) #th.__path__.__str__())
        self.__file__ = ("%s/%s"  % (self.get_path(),self.__file__))
        # TODO: (12/25/22) - Add logic for checking for targeting {theme}.json file:
        f = io.FileIO(
            file=self.__file__,
            mode='r'
        )
        return f.readall() # read file to bytes object
    
    def __is_valid__(self) -> bool:
        """ internal function that must be implemented at named inherited theme class. base class returns false. """
        return False
    
    def __is_validitem__(self,dict,item) -> bool:
        ret = False
        
        if dict.__contains__(item):
            ret = True
        else:
            print("Missing item: %s" % (item))
        
        return ret
    
    def get_path(self) -> str:
        return self.__path__

    def get_dict(self) -> dict:
        return self.__jsdict__
    
class context(jsonfile):

    def __init__(self,context_name):
        super().__init__(cx.__path__.__str__(),context_name)
        
class theme(jsonfile):

    def __init__(self,theme_name):
        super().__init__(th.__path__.__str__(),theme_name)

class PopupMenuContext(context):

    def __init__(self,context_name=POPUP_DEFAULT_JSONCONTEXT):
        super().__init__(context_name)

        if not self.__is_valid__():
            print(POPUP_ISSUES_MSG)
            super().__init__(POPUP_DEFAULT_JSONCONTEXT)
        
        self.__pmd__ = self.get_dict().get("PopupMenu")
        self.__dets__ = self.__pmd__.get("details")
        self.__act_cls__ = self.__dets__.get("actionclass")
        self.__dims__ = dimensions.new(self.__pmd__.get("dimensions"))
        self.__mis__ = self.__pmd__.get("menuitems")
        self.__mia__ = []
        for m in self.__mis__.items():
            self.__mia__.append(PopupMenuItem.new(m[1].get("popupmenuitem"),m[0]))

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),"PopupMenu")
        ret = ret and self.__is_validitem__(self.get_dict().get("PopupMenu"),"details")
        ret = ret and self.__is_validitem__(self.get_dict().get("PopupMenu"),"dimensions")
        ret = ret and self.__is_validitem__(self.get_dict().get("PopupMenu"),"menuitems") 
        return ret
    
    def get_details(self):
        return self.__dets__
    def get_action_class(self):
        return self.__act_cls__
    def get_dimensions(self) -> dimensions:
        return self.__dims__
    def get_menuitems(self):
        return self.__mia__
    
class MessageBoxTheme(theme):

    # TODO: (12/25/22) - Add logic to check to make sure {theme}.json file is expected format for MessageBox theme file.
    def __init__(self,theme_name=MSGBOX_DEFAULT_JSONTHEME):
        super().__init__(theme_name)

        if not self.__is_valid__():
            print(MSGBOX_ISSUES_MSG)
            super().__init__(MSGBOX_DEFAULT_JSONTHEME)
        
        self.__mbd__ = self.get_dict().get("MessageBox")
        self.__vars__ = MessageBoxVariables.new(self.__mbd__.get("variables"))
        self.__clrs__ = MessageBoxColors.new(self.__mbd__.get("colors"))
        self.__title__ = MessageBoxTitle.new(self.__mbd__.get("title"))
        self.__cnlbtn__ = MessageBoxCancelButton.new(self.__mbd__.get("cancel_button"))
        self.__btns__ = MessageBoxButtons.new(self.__mbd__.get("buttons"))

    def __is_valid__(self) -> bool:
        """ Override version of is_valid for MessageBoxTheme(theme) class. """
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),"MessageBox")
        ret = ret and self.__is_validitem__(self.get_dict().get("MessageBox"),"variables")
        ret = ret and self.__is_validitem__(self.get_dict().get("MessageBox"),"colors")
        ret = ret and self.__is_validitem__(self.get_dict().get("MessageBox"),"title")
        ret = ret and self.__is_validitem__(self.get_dict().get("MessageBox"),"cancel_button")
        ret = ret and self.__is_validitem__(self.get_dict().get("MessageBox"),"buttons")
        return ret

    def get_variables(self) -> MessageBoxVariables:
        return self.__vars__
    def get_colors(self) -> MessageBoxColors:
        return self.__clrs__
    def get_title(self) -> MessageBoxTitle:
        return self.__title__
    def get_cnlbtn(self) -> MessageBoxCancelButton:
        return self.__cnlbtn__
    def get_btns(self) -> MessageBoxButtons:
        return self.__btns__

class helper:

    def get_sepchar2text(self,s) -> str:
        ret = s
        if ret == POPUP_SEPCHAR:
            ret = POPUP_SEPTEXT
        return ret

    def str_rtrim(self,s,i) -> str:
        """ uses passed in string(s=) and trims len of string by provided int(i=) """
        ret = io.StringIO(s)
        ret = ret.read(s.__len__()-i)
        return ret
    
    def safe_path(self,s) -> str:
        """ uses passed in string(s=) and returns a usable path location by .lstrip() & .rstrip() str operations. """
        ret = s.rstrip("']")
        ret = ret.lstrip("['")
        return ret