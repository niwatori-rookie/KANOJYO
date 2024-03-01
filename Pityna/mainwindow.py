import os
import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import qt_pitynaui
import pityna
import sound

#自身で作成したsound.pyをインポート

class MainWindow(QtWidgets.QMainWindow):
    """QtWidgets.QMainWindowを継承したサブクラス
    UI画面の構築を行う
    
    Attributes:
        pityna (obj): Pitynaオブジェクトを保持
        action (bool): ラジオボタンの状態を保持
        ui (obj): Ui_MainWindowオブジェクトを保持      
    """
    def __init__(self):
        """初期化処理

        """
        # スーパークラスの__init__()を実行
        super().__init__()
        # Pitynaオブジェクトを生成
        self.pityna = pityna.Pityna('pityna')
        # ラジオボタンの状態を初期化
        self.action = True
        # Ui_MainWindowオブジェクトを生成
        self.ui = qt_pitynaui.Ui_MainWindow()
        # ログ用のリストを用意
        self.log = []
        # setupUi()で画面を構築、MainWindow自身を引数にすることが必要
        self.ui.setupUi(self)
        
    def putlog(self, str):
        """QListWidgetクラスのaddItem()でログをリストに追加する

        Args:
            str (str): _ユーザーの入力または応答メッセージをログ用に整形した文字列
        """
        self.ui.ListWidgetLog.addItem(str)
        # ユーザーの発言、ピティナの応答それぞれに改行を付けてself.logに追加
        self.log.append(str + '\n')
    
    def prompt(self):
        """ピティナのプロンプトを作る

        Returns:
            str: プロンプトを作る文字列
        """
        # Pitynaクラスのget_name()でオブジェクト名を取得
        p = self.pityna.get_name()
        # 「Responderを表示」がオンならオブジェクト名を付加する
        if self.action == True:
            p += ':' + self.pityna.get_responder_name()
        # プロンプト記号を付けて返す
        return p + '> '

    def change_looks(self):
        """機嫌値によってピティナの表情を切り替えるメソッド
        
        """
        # 応答フレーズを返す直前のピティナの機嫌値を取得
        em = self.pityna.emotion.mood
        # デフォルトの表情
        if -5 <= em <= 5:
            self.ui.LabelShowImg.setPixmap(QtGui.QPixmap(":/re/img//talk.gif"))
        # ちょっと不機嫌な表情
        elif -10 <= em < -5:
            self.ui.LabelShowImg.setPixmap(QtGui.QPixmap(":/re/img/empty.gif"))
        # 怒った表情
        elif -15 <= em < -10:
            self.ui.LabelShowImg.setPixmap(QtGui.QPixmap(":/re/img/angry.gif"))
        # 嬉しさ爆発の表情
        elif 5 < em <= 15:
            self.ui.LabelShowImg.setPixmap(QtGui.QPixmap(":/re/img/happy.gif"))
    
    def writeLog(self):
        """ ログを更新日時と共にログファイルに書き込む
        
        """
        # ログタイトルと更新日時のテキストを作成 
        # 日時は2023-01-01 00:00::00の書式にする
        now = 'Pityna System Dialogue Log: '\
                + datetime.datetime.now().strftime('%Y-%m-%d %H:%m::%S') + '\n'
        # リストlogの先頭要素として更新日時を追加
        self.log.insert(0, now)
        # logのすべての要素をログファイルへに書き込む
        path = os.path.join(os.path.dirname(__file__), 'dics', 'log.txt')
        with open(path, 'a', encoding = 'utf_8') as f:
            f.writelines(self.log)

    def button_talk_slot(self):
        """ [話す]ボタンのイベントハンドラー
        
        ・Pitynaクラスのdialogue()を実行して応答メッセージを取得
        ・入力文字列および応答メッセージをログに出力
        """
        # ラインエディットからユーザーの発言を取得
        value = self.ui.LineEdit.text()
        
        if not value:
            # 未入力の場合は音声を再生して「なに?」と表示
            sound.Music().make_music("なに?")
            sound.Music().play_music()
            self.ui.LabelResponce.setText('なに?')
        else:
            # 発言があれば対話オブジェクトを実行
            # ユーザーの発言を引数にしてdialogue()を実行し、応答メッセージを取得
            response = self.pityna.dialogue(value)
            # ピティナの応答メッセージをラベルに出力
            self.ui.LabelResponce.setText(response)
            # プロンプト記号にユーザーの発言を連結してログ用のリストに出力
            self.putlog('> ' + value)
            # ピティナのプロンプト記号に応答メッセージを連結してログ用のリストに出力
            self.putlog(self.prompt() + response)
            # QLineEditクラスのclear()メソッドでラインエディットのテキストをクリア
            self.ui.LineEdit.clear()

            # 応答メッセージを音声に変換、再生
            sound.Music().make_music(response)
            sound.Music().play_music()
        
        # ピティナのイメージを現在の機嫌値に合わせる
        self.change_looks()
        
    def closeEvent(self, event):
        """ウィジェットを閉じるclose()メソッド実行時にQCloseEventによって呼ばれる
        
        Overrides:
            ・メッセージボックスを表示する。
            ・[Yes]がクリックされたら辞書ファイルとログファイルを更新して画面を閉じる
            ・[No]がクリックされたら辞書ファイルを更新しないで画面を閉じる          

        Args:
            event(QCloseEvent): 閉じるイベント発生時に渡されるQCloseEventオブジェクト
        """
        # Yes|Noボタンを配置したメッセージボックスを表示
        reply = QtWidgets.QMessageBox.question(
                self,
                '質問ですー',
                '辞書を更新してもいい?',
                buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
        
        # [Yes]クリックで辞書ファイルの更新とログファイルへの記録を行う
        if reply == QtWidgets.QMessageBox.Yes:
            self.pityna.save()   # 記憶メソッド実行
            self.writeLog(     ) # 対話の一部始終をログファイルに保存
            event.accept()       # イベントを続行し画面を閉じる
        else:
            # [No]クリックで即座に画面を閉じる
            event.accept()

    def show_responder_name(self):
        """RadioButton_1がオンのときに呼ばれるイベントハンドラー
        
        """
        # ラジオボタンの状態を保持するactionの値をTrueにする
        self.action = True
            
    def hidden_responder_name(self):
        """RadioButton_2がオンのときに呼ばれるイベントハンドラー
        
        """
        # ラジオボタンの状態を保持するactionの値をFalseにする
        self.action = False
