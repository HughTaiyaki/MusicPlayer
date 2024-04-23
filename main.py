import sys
from Player import Player
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    My_Player = Player()
    # 展示窗口
    My_Player.show()
    # 程序进行循环等待状态
    app.exec()