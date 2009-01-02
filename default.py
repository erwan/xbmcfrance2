"""
 Copyright (c) 2008 Erwan Loisant <eloisant@gmail.com>

 This file may be used under the terms of the
 GNU General Public License Version 2 (the "GPL"),
 http://www.gnu.org/licenses/gpl.html

 Software distributed under the License is distributed on an "AS IS" basis,
 WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 for the specific language governing rights and limitations under the
 License.
"""

# main import's
import sys
import os

# Script constants
__scriptname__ = "xmbcFrance2"
__author__ = "Erwan Loisant"
__url__ = "http://erwan.jp/xbmcfrance2"
__version__ = "1.0boxee"

# Shared resources
BASE_RESOURCE_PATH = os.path.join(os.getcwd().replace( ";", "" ), "resources")
sys.path.append(os.path.join(BASE_RESOURCE_PATH, "lib"))

# Start the main gui
if __name__ == "__main__":
    import gui
