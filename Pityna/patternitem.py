import random
import re

class PatternItem:
    """パターン辞書1行の情報を保持するクラス
    
    Attributes: すべて「パターン辞書1行」のデータ
        modify (int): 機嫌変動値
        pattern (str): 正規表現パターン
        phrases(dictのlist):
            リスト要素の辞書は"応答フレーズ1個"の情報を持つ
            辞書の数は1行の応答フレーズグループの数と同じ
            {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
    """
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """インスタンス変数modify、pattern、phrasesの初期化を実行
        
        Args:
            pattern (str): パターン辞書1行の正規表現パターン(機嫌変動値##パターン)
            phrases (dicのlist）: パターン辞書1行の応答フレーズグループ
        """        
        # インスタンス変数modify、patternの初期化
        self.init_modifypattern(pattern)
        # インスタンス変数phrasesの初期化
        self.init_phrases(phrases)

    def init_modifypattern(self, pattern):
        """インスタンス変数modify(int)、pattern(str)の初期化を行う
        
        パターン辞書の正規表現パターンの部分にSEPARATORをパターンマッチさせる
        マッチ結果のリストから機嫌変動値と正規表現パターンを取り出し、
        インスタンス変数modifyとpatternに代入する
        
        Args:
            pattern(str): パターン辞書1行の正規表現パターン
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(PatternItem.SEPARATOR, pattern)
        # 機嫌変動値を保持するインスタンス変数を0で初期化
        self.modify = 0 
        # マッチ結果の整数の部分が空でなければ機嫌変動値をインスタンス変数modifyに代入
        if m[0][1]:
            self.modify = int(m[0][1])
        # マッチ結果からパターン部分を取り出し、インスタンス変数patternに代入
        self.pattern = m[0][2]
        
    def init_phrases(self, phrases):
        """インスタンス変数phrases(dictのlist)の初期化を行う
        
        パターン辞書の応答フレーズグループにSEPARATORパターンマッチさせる
        マッチ結果のリストから必要機嫌値と応答フレーズを取り出して
        {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}
        の構造をした辞書を作成し、phrases(リスト)に追加

        Args:
            phrases (str): パターン辞書1行の応答フレーズグループ
        """
        # リスト型のインスタンス変数を用意
        self.phrases = []
        # 辞書(dict)オブジェクトを用意
        dic = {}
        # 引数で渡された応答フレーズグループを'|'で分割し、
        # 1個の応答フレーズに対してSEPARATORをパターンマッチさせる
        # {'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}を作成し、
        # インスタンス変数phrases(list)に格納する
        for phrase in phrases.split('|'):
            # 1個の応答フレーズに対してパターンマッチを行う
            m = re.findall(PatternItem.SEPARATOR, phrase)
            # 'need'キーの値を必要機嫌値m[0][1]にする
            # 'phrase'キーの値を応答フレーズm[0][2]にする
            dic['need'] = 0
            if m[0][1]:
                dic['need'] = int(m[0][1])
            dic['phrase'] = m[0][2]
            # 作成した辞書をリストphrasesに追加
            self.phrases.append(dic.copy())

    def match(self, str):
        """ユーザーの発言にパターン辞書1行の正規表現パターンをマッチさせる
        
        Args:
            str(str): ユーザーの発言
            
        Returns:
            Matchオブジェクト: マッチした場合
            None: マッチしない場合
        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        """現在の機嫌値と必要機嫌値を比較し、適切な応答フレーズを抽出する
        
        Args:
            mood(int）: ピティナの現在の機嫌値

        Returns:
            str: 必要機嫌値をクリアした応答フレーズのリストからランダムチョイスした応答
            None: 必要機嫌値をクリアする応答フレーズが存在しない場合
        """
        choices = []
        # インスタンス変数phrasesが保持するすべての辞書(dict)オブジェクトを処理
        for p in self.phrases:
            # 'need'キーの数値とパラメーターmoodをsuitable()に渡し、
            # 必要機嫌値による条件をクリア(戻り値がTrue)していれば、
            # 対になっている応答フレーズをchoicesリストに追加する
            if (self.suitable(p['need'], mood)):
                choices.append(p['phrase'])
        # choicesリストが空であればNoneを返して終了
        if (len(choices) == 0):
            return None
        # choicesリストからランダムに応答フレーズを抽出して返す
        return random.choice(choices)

    def suitable(self, need, mood):
        """現在の機嫌値が必要機嫌値の条件を満たすかを判定
            
        Args:
            need(int): 必要機嫌値
            mood(int): 現在の機嫌値

        Returns:
            bool:必要機嫌値をクリアしていたらTrue、そうでなければFalse
        """
        # 必要機嫌値が0であればTrueを返す
        if (need == 0):
            return True
        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (need > 0):
            return (mood > need)
        # 必要機嫌値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < need)

    def add_phrase(self, phrase):
        """ユーザー発言の形態素が既存のパターン文字列とマッチした場合に、
            Dictionaryのstudy_pattern()メソッドから呼ばれる
        
        パターン辞書1行の応答フレーズグループ末尾に、ユーザー発言を
        新規の応答フレーズとして追加する

        Args:
            phrase(str): ユーザーの発言            
        """
        # 既存の応答フレーズにユーザー発言の形態素が一致するかを順次調べ、
        # 一致するフレーズがあった時点でreturnしてメソッドを終了
        #
        # self.phrases(dicのlist):
        #　　　リスト要素の辞書は"応答フレーズ1個"の情報を持つ
        #     [{'need': 必要機嫌値, 'phrase': '応答フレーズ1個'}, ...]
        # 
        # Block Parameters:
        #     p(dic): 必要機嫌値と応答フレーズ1個の情報を持つ
        for p in self.phrases:
            if p['phrase'] == phrase:
                return
        # リストself.phrasesに、{'need':0, 'phrase':'ユーザーの発言'}を追加
        self.phrases.append({'need': 0, 'phrase': phrase})
        
    def make_line(self):
        """パターン辞書1行データを作る
        
        Returns:
            str: パターン辞書用に成形したデータ
        """
        # '機嫌変動値##パターン文字列'を作る
        pattern = str(self.modify) + '##' + self.pattern
        # 応答フレーズ群のためのリスト
        pr_list = []
        
        # 応答フレーズ群を作成する
        #
        # Block Parameters:
        #    p(dic): 必要機嫌値と応答フレーズ1個の情報を持つ。
        for p in self.phrases:
            # '必要機嫌値##応答フレーズ'を作ってリストに追加する。
            pr_list.append(str(p['need']) + '##' + p['phrase'])
        
        # '機嫌変動値##パターン文字列[TAB]' に|で区切った
        # '必要機嫌値##応答フレーズ' のグループを連結して返す
        return pattern + '\t' + '|'.join(pr_list)

