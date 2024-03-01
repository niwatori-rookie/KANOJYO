import responder
import random
import dictionary
import analyzer

class Pityna(object):
    """ ピティナの本体クラス
    
    Attributes:
        name (str): Pitynaオブジェクトの名前を保持
        dictionary (obj:Dictionary): Dictionaryオブジェクトを保持
        res_repeat (obj:RepeatResponder): RepeatResponderオブジェクトを保持
        res_random (obj:RandomResponder): RandomResponderオブジェクトを保持
        res_pattern (obj:PatternResponder): PatternResponderオブジェクトを保持
        res_template (obj:TemplateResponder): TemplateResponderオブジェクトを保持
        res_markov (obj:MarcovResponder): MarcovResponderオブジェクトを保持
    """
    def __init__(self, name):
        """ Pitynaオブジェクトの名前をnameに格納
            Responderオブジェクトを生成してresponderに格納
            
        Args:
            name(str)   : Pitynaオブジェクトの名前
        """
        # Pitynaオブジェクトの名前をインスタンス変数に代入
        self.name = name
        # Dictionaryを生成
        self.dictionary = dictionary.Dictionary()
        # Emotionを生成
        self.emotion = Emotion(self.dictionary.pattern)
        # RepeatResponderを生成
        self.res_repeat = responder.RepeatResponder('Repeat?')
        # RandomResponderを生成
        self.res_random = responder.RandomResponder(
                'Random', self.dictionary.random)
        # PatternResponderを生成
        self.res_pattern = responder.PatternResponder(
            'Pattern',
            self.dictionary.pattern,  # パターン辞書
            self.dictionary.random    # ランダム辞書
            )
        # TemplateResponderを生成
        self.res_template = responder.TemplateResponder(
            'Template',
            self.dictionary.template, # テンプレート辞書
            self.dictionary.random    # ランダム辞書
            )
        # MarkovResponderを生成
        self.res_markov = responder.MarcovResponder(
            'Markov',
            self.dictionary.markovsentence, # マルコフ辞書
            self.dictionary.random          # ランダム辞書
            )
    
    def dialogue(self, input):
        """ 応答オブジェクトのresponse()を呼び出して応答文字列を取得する

        Args:
            input(str): ユーザーの発言        
            Returns:
                str: 応答フレーズ
        """
        # ピティナの機嫌値を更新する
        self.emotion.update(input)
        # ユーザーの発言を解析
        parts = analyzer.analyze(input)
        # 1～100の数値をランダムに生成
        x = random.randint(1, 100)
        # 30以下ならPatternResponderオブジェクトにする
        if x <= 30:
            self.responder = self.res_pattern
        # 31～50以下ならTemplateResponderオブジェクトにする
        elif 31 <= x <= 50:
            self.responder = self.res_template
        # 51～70以下ならRandomResponderオブジェクトにする
        elif 51 <= x <= 68:
            self.responder = self.res_random
        # 71～90以下ならMarkovResponderにする
        elif 69 <= x <= 90:
            self.responder = self.res_markov
        # それ以外はRepeatResponderオブジェクトにする
        else:
            self.responder = self.res_repeat

        # 応答フレーズを生成
        resp = self.responder.response(
            input,             # ユーザーの発言
            self.emotion.mood, # ピティナの機嫌値
            parts              # ユーザー発言の解析結果
            ) # ------------------------------------------------④
        # 学習メソッドを呼ぶ
        self.dictionary.study(input, parts)
        # 応答フレーズを返す
        return resp

    def save(self):
        """ Dictionaryのsave()を呼ぶ中継メソッド
        
        """
        self.dictionary.save()
    
    def get_responder_name(self):
        """ 応答に使用されたオブジェクト名を返す
        
        Returns:
            str: responderに格納されている応答オブジェクト名
        """
        return self.responder.name

    def get_name(self):
        """ Pitynaオブジェクトの名前を返す

        Returns:
            str: Pitynaクラスの名前
        """
        return self.name

class Emotion:
    """ ピティナの感情モデル
    
    Attributes:
        pattern (PatternItemのlist): [PatternItem1, PatternItem2, PatternItem3, ...]
        mood (int): ピティナの機嫌値を保持
    """
    # 機嫌値の上限／下限と回復値をクラス変数として定義
    MOOD_MIN = -15 
    MOOD_MAX = 15
    MOOD_RECOVERY = 0.5

    def __init__(self, pattern):
        """インスタンス変数patternとmoodを初期化する

        Args:
            pattern(dict): Dictionaryのpattern(中身はPatternItemのリスト)
        """
        # Dictionaryオブジェクトのpatternをインスタンス変数dictionaryに格納
        self.pattern = pattern
        # 機嫌値moodを0で初期化
        self.mood = 0

    def update(self, input):
        """ 機嫌値を変動させるメソッド
            
        ・機嫌値をプラス/マイナス側にMOOD_RECOVERYの値だけ戻す
        ・ユーザーの発言をパターン辞書にマッチさせ、機嫌値を変動させる

        Args:
            input(str) : ユーザーの発言
        """
        # 機嫌値を徐々に戻す処理
        if self.mood < 0:
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MOOD_RECOVERY
        
        # パターン辞書の各行の正規表現をユーザーの発言に繰り返しパターンマッチさせる
        # マッチした場合はadjust_mood()で機嫌値を変動させる
        for ptn_item in self.pattern:
            if ptn_item.match(input):
                self.adjust_mood(ptn_item.modify)
                break

    def adjust_mood(self, val):
        """ 機嫌値を増減させるメソッド

        Args:
            val(int) : 機嫌変動値
        """
        # 機嫌値moodの値を機嫌変動値によって増減する
        self.mood += int(val)
        # MOOD_MAXとMOOD_MINと比較して、機嫌値が取り得る範囲に収める
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN
