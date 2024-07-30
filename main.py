from PyQt6 import QtWidgets
from keyboard import Ui_Form
import pygame
import threading, time
from Keys import *

class Main(Ui_Form,QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)

        self.key_map = key_map
        self.setupUi(self)
        self.initialize_sounds()
        self.init_connection()
        self.init_button_map()
        self.current_sound_thread = None
        self.sound_thread_lock = threading.Lock()
        self.last_key_press_time = {}
        self.debounce_interval = 0.1

    def init_connection(self):
        notes = ['C2', 'C2H', 'D2', 'D2H', 'E2', 'F2', 'F2H', 'G2', 'G2H',
                 'A2', 'A2H', 'B2', 'C3', 'C3H', 'D3', 'D3H', 'E3', 'F3',
                 'F3H', 'G3', 'G3H', 'A3', 'A3H', 'B3']
        for note in notes:
            button = getattr(self, note)
            button.clicked.connect(lambda checked, note=note: self.play_sound(note))

    def initialize_sounds(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # Adjust as needed
        pygame.mixer.init()
        self.sounds = {}
        for note in ['C2','C2H','D2','D2H','E2','F2','F2H','G2','G2H','A2','A2H','B2','C3','C3H','D3','D3H',
                'E3','F3','F3H','G3','G3H','A3','A3H','B3']:
            # Replace 'path/to/note.wav' with the actual file path for the note
            self.sounds[note] = pygame.mixer.Sound(f'Notes/{note}.mp3')

    def play_sound(self, note):
        self.sounds[note].play()

    def keyPressEvent(self, event):
        current_time = time.time()
        if event.key() in self.key_map:
            last_time = self.last_key_press_time.get(event.key(), 0)
            if current_time - last_time > self.debounce_interval:
                self.play_sound(key_map[event.key()])
                self.last_key_press_time[event.key()] = current_time
                if event.key() in self.button_map:
                    self.button_map[event.key()].setStyleSheet("background-color: yellow")
                elif event.key() in self.button_map_H:
                    self.button_map_H[event.key()].setStyleSheet("background-color: yellow")

    def keyReleaseEvent(self, event):
        if event.key() in self.button_map:
            self.button_map[event.key()].setStyleSheet("")
        elif event.key() in self.button_map_H:
            self.button_map_H[event.key()].setStyleSheet("background-color: black")

    def init_button_map(self):
        self.button_map = {
            QtCore.Qt.Key.Key_A: self.C2,
            QtCore.Qt.Key.Key_S: self.D2,
            QtCore.Qt.Key.Key_D: self.E2,
            QtCore.Qt.Key.Key_F: self.F2,
            QtCore.Qt.Key.Key_G: self.G2,
            QtCore.Qt.Key.Key_H: self.A2,
            QtCore.Qt.Key.Key_J: self.B2,
            QtCore.Qt.Key.Key_K: self.C3,
            QtCore.Qt.Key.Key_Z: self.C3,
            QtCore.Qt.Key.Key_X: self.D3,
            QtCore.Qt.Key.Key_C: self.E3,
            QtCore.Qt.Key.Key_V: self.F3,
            QtCore.Qt.Key.Key_B: self.G3,
            QtCore.Qt.Key.Key_N: self.A3,
            QtCore.Qt.Key.Key_M: self.B3,
        }
        self.button_map_H = {
            QtCore.Qt.Key.Key_W: self.C2H,
            QtCore.Qt.Key.Key_E: self.D2H,
            QtCore.Qt.Key.Key_T: self.F2H,
            QtCore.Qt.Key.Key_Y: self.G2H,
            QtCore.Qt.Key.Key_U: self.A2H,
            QtCore.Qt.Key.Key_3: self.C3H,
            QtCore.Qt.Key.Key_4: self.D3H,
            QtCore.Qt.Key.Key_6: self.F3H,
            QtCore.Qt.Key.Key_7: self.G3H,
            QtCore.Qt.Key.Key_8: self.A3H
        }


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())