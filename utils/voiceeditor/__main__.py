from janim.gui.application import Application

from main_window import MainWindow


def main():
    app = Application()
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == '__main__':
    main()
