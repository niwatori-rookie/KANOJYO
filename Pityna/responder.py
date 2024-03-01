import random
import re
import analyzer
import itertools

class Responder(object):
    """ 応答クラスのスーパークラス
    """
    def __init__(self, name):
        """ Responderオブジェクトの名前をnameに格納する処理だけを行う
        
        Args:
            name (str)   : 応答クラスの名前
        """
        self.name = name

    def response(self, input, mood, parts):
        """ オーバーライドを前提としたresponse()メソッド
        
        Args:
            input (str): ユーザーの発言
            mood (int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果
        Returns:
            str: 応答メッセージ（ただし空の文字列)
        """
        return ''

class RepeatResponder(Responder):
    """ オウム返しのためのサブクラス
    """
    def __init__(self, name):
        """スーパークラスの__init()__の呼び出しのみを行う

        Args:
            name (str): 応答クラスの名前
        """
        super().__init__(name)
    
    def response(self, input, mood, parts):
        """response()をオーバーライド、オウム返しの返答をする

        Args:
            input (str): ユーザーの発言
            mood (int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果

        Returns:
            str: 応答メッセージ
        """
        # オウム返しの返答をする
        return '{}ってなに？'.format(input)

class RandomResponder(Responder):
    """ ランダムな応答のためのサブクラス
    """
    def __init__(self, name, dic_random):
        """ スーパークラスの__init__()にnameを渡し、
            ランダム応答用のリストをインスタンス変数に格納する。
        
        Args:
            name(str): 応答クラスの名前
            dic_random(list): Dictionaryオブジェクトが保持するランダム応答用のリスト
        """
        super().__init__(name)
        self.random = dic_random

    def response(self, input, mood, parts):
        """ response()をオーバーライド、ランダムな応答を返す

        Args:
            input(str)  : ユーザーの発言
            mood (int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果

        Returns:
            str: リストからランダムに抽出した応答フレーズ
        """
        # リストresponsesからランダムに抽出して戻り値として返す
        return random.choice(self.random)

class PatternResponder(Responder):
    """ パターンに反応するためのサブクラス

    Attributes:
        pattern(objectのlist): リスト要素はPatternItemオブジェクト
        random(strのlist): ランダム辞書の応答フレーズのリスト
    """
    def __init__(self, name, dic_pattern, dic_random):
        """ スーパークラスの__init__()にnameを渡し、
            Dictionaryオブジェクトをインスタンス変数に格納する
        
        Args:
            name(str)   : Responderオブジェクトの名前
            dic_pattern(objectのlist): リスト要素はPatternItemオブジェクト
            dic_random(strのlist): ランダム辞書の応答フレーズのリスト
        """
        super().__init__(name)
        self.pattern = dic_pattern
        self.random = dic_random

    def response(self, input, mood, parts):
        """ パターンにマッチした場合に応答フレーズを抽出して返す

        Args:
            input(str)   : ユーザーの発言
            mood (int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果

        Returns:str:
            パターンにマッチした場合はパターンと対になっている応答フレーズを返す
            パターンマッチしない場合はランダム辞書の応答メッセージを返す
        """
        resp = None
        # patternリストのPatternItemオブジェクトに対して反復処理を行う
        for ptn_item in self.pattern:
            # パターン辞書1行のパターンをユーザーの発言にマッチさせる
            # マッチしたらMatchオブジェクト、そうでなければNoneが返る
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行
            # 現在の機嫌値に見合う応答フレーズを取得する。
            if m:
                resp = ptn_item.choice(mood)
            # choice()の戻り値がNoneでない場合は応答フレーズの
            # %match%をユーザー発言のマッチした文字列に置き換える
            if resp != None:
                return re.sub('%match%', m.group(), resp)
        # パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.random)

class TemplateResponder(Responder):
    """ テンプレートに反応するためのサブクラス
    
    Attributes:
        template (dict): 要素は{ '%noun%の出現回数' : [テンプレートのリスト] } 
        random(list): 要素はランダム辞書の応答フレーズ群
    """
    def __init__(self, name, dic_template, dic_random):
        """ スーパークラスの__init__()にnameを渡し、
            テンプレート辞書とランダム辞書をインスタンス変数に格納する
        
        Args:
            name(str): Responderオブジェクトの名前。            
            dic_template(dic): Dictionaryが保持するテンプレート辞書
            dic_random(list): Dictionaryが保持するランダム辞書
        """
        super().__init__(name)
        self.template = dic_template
        self.random = dic_random
        
    def response(self, input, mood, parts):
        """ テンプレートを使用して応答フレーズを生成する

        Args:
            input(str): ユーザーの発言
            mood(int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果

        Returns:str:
            パターンにマッチした場合はパターンと対になっている応答フレーズを返す
            パターンマッチしない場合はランダム辞書から返す
        """
        # ユーザー発言の名詞の部分のみを保持するリスト
        keywords = []
        # 解析結果partsの「文字列」→word、「品詞情報」→partに順次格納
        #
        # Block Parameters:
        #   word(str): ユーザー発言の形態素
        #   part(str): 形態素の品詞情報
        for word, part in parts:
            # 名詞であれば形態素をkeywordsに追加
            if analyzer.keyword_check(part):
                keywords.append(word)
        # keywordsに格納された名詞の数を取得
        count = len(keywords)
        # keywordsリストに1つ以上の名詞が存在し、
        # 名詞の数に対応する'%noun%'を持つテンプレートが存在すれば
        # テンプレートを利用して応答フレーズを生成する
        if (count > 0) and (str(count) in self.template): # -----⑨
            # テンプレートリストからランダムに1個抽出
            resp = random.choice(
                self.template[str(count)]
                )
            # keywordsから取り出した名詞でテンプレートの%noun%を書き換える
            for word in keywords:
                resp = resp.replace(
                    '%noun%', # 書き換える文字列
                    word,     # 書き換え後の文字列
                    1         # 書き換える回数
                    )
            return resp
        # ユーザー発言に名詞が存在しない、または適切なテンプレートが
        # 存在しない場合はランダム辞書から返す
        return random.choice(self.random)

class MarcovResponder(Responder): # --------------------------------------②
    """ マルコフ連鎖を利用して応答を生成するためのサブクラス
    
    Attributes:
        markovsentence (strのlist): 要素はマルコフ連鎖で作成した応答フレーズ
        random(strのlist): 要素はランダム辞書の応答フレーズ
    """
    def __init__(self, name, dic_marcov, dic_random):
        """ スーパークラスの__init()__にnameを渡し、
            マルコフ辞書とランダム辞書トをインスタンス変数に格納する。
        
        Parameters:
            name(str): Responderオブジェクトの名前。            
            dic_marcov(dic): Dictionaryが保持するマルコフ辞書。
            dic_random(list): Dictionaryが保持するランダム辞書。
        """
        super().__init__(name)
        self.markovsentence = dic_marcov
        self.random = dic_random
        
    def response(self, input, mood, parts): # ----------------------------③
        """ マルコフ辞書を使用して応答フレーズを生成する。

        Args:
            input(str): ユーザーの発言
            mood(int): ピティナの機嫌値
            parts(strのlist): ユーザー発言の解析結果

        Returns:
            str:ユーザーメッセージの形態素がマルコフ連鎖のフレーズに
                [パターンマッチした場合]マッチした中から1個を抽出して返す
                [パターンマッチしない場合]ランダム辞書の応答メッセージを返す            
        """
        # 空のリストを作成
        m = []
        # 解析結果の形態素と品詞に対して反復処理
        for word, part in parts: # ---------------------------------------④
            # インプット文字列に名詞があればそれを含むマルコフ連鎖文を検索
            if analyzer.keyword_check(part): # ---------------------------⑤
                # マルコフ連鎖で生成した文章を1つずつ処理
                for sentence in self.markovsentence:# -------------------⑥
                    # 形態素の文字列がマルコフ連鎖の文章に含まれているか検索する
                    # 最後を'.*?'にすると検索文字列だけにもマッチするので
                    # + '.*'として検索文字列だけにマッチしないようにする
                    find = '.*?' + word + '.*'
                    # マルコフ連鎖文にマッチさせる
                    tmp = re.findall(find, sentence) # -------------------⑦
                    if tmp:
                        # マッチする文章があればリストmに追加
                        m.append(tmp)
        # findall()はリストを返してくるので多重リストをフラットにする
        m = list(itertools.chain.from_iterable(m)) # ---------------------⑧
        # 集合に変換して重複した文章を取り除く
        check = set(m)
        # 再度、リストに戻す
        m = list(check)
        if m:
            # ユーザー発言の名詞にマッチしたマルコフ連鎖文からランダムに選択
            return(random.choice(m)) # -----------------------------------⑨

        # マッチするマルコフ連鎖文がない場合
        return random.choice(self.random) # -------------------⑩