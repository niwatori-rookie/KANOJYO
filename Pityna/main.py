import sys
from PyQt5 import QtWidgets
import mainwindow

# このモジュールが直接実行された場合に以下の処理を行う
if __name__ == "__main__":
    # QApplicationはウィンドウシステムを初期化し、
    # コマンドライン引数を使用してアプリケーションオブジェクトを構築
    app = QtWidgets.QApplication(sys.argv)
    # 画面を構築するMainWindowクラスのオブジェクトを生成。
    win = mainwindow.MainWindow()
    # メインウィンドウを画面に表示
    win.show()
    # メッセージループを開始、プログラムが終了されるまでメッセージループを維持
    # 終了時に0が返される。
    ret = app.exec()
    # exec_()の戻り値をシステムに返してプログラムを終了
    sys.exit(ret)