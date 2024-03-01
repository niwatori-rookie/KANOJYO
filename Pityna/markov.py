import os
import re
import random
import analyzer

class Markov:
    """ Markovクラス

    """
    def make(self):
        """ Pitynaオブジェクト生成時に呼ばれるメソッド
            ログファイルからマルコフ連鎖で文章群を生成する
            
            Returns:
                str: マルコフ辞書から生成した応答フレーズ
        """
        # log.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'log.txt')
        # ログファイルを読み取りモードでオープン。
        with open(path, "r", encoding = 'utf_8') as f:
            text = f.read()
        # プロンプトの文字を取り除く。
        text = re.sub('> ','', text)
        # ピティナの応答オブジェクトの文字列を取り除く
        text = re.sub(
            'pityna:Repeat?|pityna:Random|pityna:Pattern|'\
            'pityna:Template|pityna:Markov|pityna',
            '',
            text)
        # ログのタイトルとタイムスタンプを行ごと取り除く。
        text = re.sub(
            'Pityna System Dialogue Log:.*\n',
            '',
            text)
        # 空白行が含まれていると\n\nが続くので\n1つに置き換えて、空白行をなくす。
        text = re.sub('\n\n','\n', text)
        # ログファイルの会話文を形態素に分解してリストにする。
        wordlist = analyzer.parse(text)

        return self.make_markovdictionary(wordlist)

    def make_markovdictionary(self, wordlist):
        """ make()から呼ばれる
            実際にマルコフ連鎖で文章群を生成する
            
            Args:
                wordlist(strのリスト): ログの会話文を形態素に分解したリスト  
            Returns:
                str: マルコフ連鎖で生成した応答フレーズ
        """
        # マルコフ辞書用のdictオブジェクトを作成
        markov = {}
        # 辞書のキー(タプル)に設定する変数
        p1 = ''
        p2 = ''
        p3 = ''
        #  ログの会話文のすべての形態素からマルコフ辞書を作成する
        for word in wordlist:
            if p1 and p2 and p3:
                # p1、p2、p3のすべてに値が格納されていればサフィックスを追加
                if (p1, p2, p3) not in markov:
                    # markovに(p1, p2, p3)キーが存在しなければ
                    # 新しい要素として、{(p1, p2, p3)： [空のリスト]} を追加
                    markov[(p1, p2, p3)] = []
                # (p1, p2, p3)キーの値のリストにwordを追加
                # 既存の(p1, p2, p3)キーがあればリスト要素末尾にwordが追加される
                markov[(p1, p2, p3)].append(word)
            # p1をp2、p2をp3、p3をwordの値に置き換える
            # forループでwordの形態素がp3→p2→p1の順で埋められていく
            p1, p2, p3 = p2, p3, word

        # マルコフ辞書から文章を作り出す
        count = 0
        sentence = ''
        # markovのキーをランダムに抽出し、プレフィックス1～3に代入
        p1, p2, p3  = random.choice(list(markov.keys()))
        while count < len(wordlist):
            # キーが存在するかチェック
            if ((p1, p2, p3) in markov) == True:
                # 文章にする単語を取得
                tmp = random.choice(markov[(p1, p2, p3)])
                # 取得した単語をsentenceに追加
                sentence += tmp
            # 3つのプレフィックスの値を置き換える
            p1, p2, p3 = p2, p3, tmp
            count += 1

        # 閉じ括弧を削除
        sentence = re.sub('」', '', sentence)
        #開き括弧を削除
        sentence = re.sub('「', '', sentence)

        # 生成した文章を戻り値として返す
        return sentence
