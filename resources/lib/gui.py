"""
Main GUI for XBMC France 2
"""

import os
import sys
import traceback

import xbmcgui
import xbmc

import france2

import xbmcutils.gui
import xbmcutils.guibuilder

class Logger:
  def write(data):
    xbmc.log(data)
  write = staticmethod(write)
sys.stdout = Logger
sys.stderr = Logger

class France2GUI(xbmcgui.Window):
  """France2 browser GUI."""

  def __init__(self):
    """Setup the default skin"""

    try: 
      self.base_path = os.getcwd().replace(';','')
      if not self.load_skin('default'):
        self.close()

      self.f2 = france2.France2()
      self.player = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)

      main_list = self.get_control('Program List')
      for jt in self.f2.LABELS:
        main_list.addItem(xbmcgui.ListItem(label=jt))
      self.setFocus(main_list)

    except:
      xbmc.log('Exception (init): ' + str(sys.exc_info()[0]))
      traceback.print_exc()
      self.close()

  def load_skin(self, name=None):
    """Loads the GUI skin."""
    if not name:
      name = 'default'
    skin_path = os.path.join(self.base_path, 'skins', name)
    skin = os.path.join(skin_path, 'skin.xml')
    self.img_path = os.path.join(skin_path, 'gfx')
    xbmcutils.guibuilder.GUIBuilder(self, skin, self.img_path,
                                    useDescAsKey=True, fastMethod=True)

    return self.SUCCEEDED

  def show_about(self):
    """Show an 'About' dialog."""
    dlg = xbmcgui.Dialog()
    dlg.ok('A propos', 'Par Erwan Loisant, 2008')

  def get_control(self, desc):
    """Return the control that matches the widget description."""
    return self.controls[desc]['control']

  def play_jt(self, pos):
    """Get the url for the id and start playback."""
    jt = self.f2.get_lastjt(pos)
    self.player.play(jt["url"])

  def refresh_label(self):
    main_list = self.get_control('Program List')
    pos = main_list.getSelectedPosition()
    program = self.f2.PROGRAMS[pos]
    info = self.f2.get_lastjt(pos)
    lbl = self.get_control('edition name')
    lbl.setLabel(program + " : " + info["name"])

  def onAction(self, action):
    """Handle user input events."""
    try:
      self.refresh_label()
      if action == xbmcutils.gui.ACTION_PREVIOUS_MENU:
        self.close()
    except:
      xbmc.log('Exception (onAction): ' + str(sys.exc_info()[0]))
      traceback.print_exc()
      self.close()

  def onControl(self, ctrl):
    """Handle widget events."""
    try: 
      if ctrl is self.get_control('Program List'):
        pos = ctrl.getSelectedPosition()
        program = self.f2.PROGRAMS[pos]
        self.play_jt(pos)
    except:
      xbmc.log('Exception (onControl): ' + str(sys.exc_info()[0]))
      traceback.print_exc()
      self.close()


f2 = France2GUI()
f2.doModal()
del f2

