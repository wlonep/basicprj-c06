import os
import sys

from model.user import User
from model.station import Station
from model.train import Train
from core.menu import admin_menu, user_menu
from core.menu import main_menu

if __name__ == '__main__':
    main_menu()