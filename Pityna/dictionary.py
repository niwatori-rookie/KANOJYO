import os
import re
import analyzer
from patternitem import PatternItem
from markov import Markov

class Dictionary(object):
    """ランダム辞書とパターン辞書のデータをインスタンス変数に格納する

    Attributes:
        random(strのlist):
        ランダム辞書のすべての応答メッセージを要素として格納
        [メッセージ1, メッセージ2, メッセージ3, ...]

        pattern(PatternItemのlist):
            [PatternItem1, PatternItem2, PatternItem3, ...]
        
        template (dict):
            テンプレート辞書の情報を保持する
            {'空欄の数': [テンプレート1, テンプレート2, ...], ...}
        
        markovsentence(strのlist):
            マルコフ連鎖で生成した応答フレーズを保持する
    """
    def __init__(self):
        """インスタンス変数random,pattern,randomd_path,dir_patternの初期化

        """        
        # ランダム辞書のメッセージのリストを作成
        self.random =  self.make_random_list()
        # パターン辞書1行データを格納したPatternItemオブジェクトのリストを作成
        self.pattern = self.make_pattern_dictionary()
        # テンプレート辞書を作成
        self.template = self.make_template_dictionary()
        # マルコフ辞書を作成
        self.markovsentence = self.make_markov_dictionary()

    def make_random_list(self):
        """ランダム辞書ファイルのデータを読み込んでリストrandomに格納する。
        
            Returns:
                list: ランダム辞書の応答メッセージを格納したリスト
        """
        # random.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'random.txt')
        # ランダム辞書ファイルオープン
        rfile = open(path, 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        r_lines = rfile.readlines()
        # ファイルオブジェクトをクローズ
        rfile.close()
        # 末尾の改行と空白文字を取り除いてリストrandom_listに格納
        random_list = []
        for line in r_lines:
            str = line.rstrip('\n')
            if (str!=''):
                random_list.append(str)

        return random_list

    def make_pattern_dictionary(self):
        """パターン辞書ファイルのデータを読み込んでリストpatternitem_listに格納

        Returns:
            PatternItemのlist: PatternItemはパターン辞書1行のデータを持つ
        """
        # pattern.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'pattern.txt')
        # パターン辞書オープン
        pfile = open(path, 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        # ファイルオブジェクトをクローズ
        pfile.close()
        # 末尾の改行と空白文字を取り除いてリストpattern_listに格納
        pattern_list = []
        for line in p_lines:
            str = line.rstrip('\n')
            if (str!=''):
                pattern_list.append(str)

        # パターン辞書の各行をタブで切り分けて以下の変数に格納
        #
        # ptn パターン辞書1行の正規表現パターン
        # prs パターン辞書1行の応答フレーズグループ
        #
        # ptn、prsを引数にしてPatternItemオブジェクトを1個生成し、patternitem_listに追加
        # パターン辞書の行の数だけ繰り返す
        patternitem_list = []
        for line in pattern_list:
            ptn, prs = line.split('\t')
            patternitem_list.append(PatternItem(ptn, prs))
        return patternitem_list

    def make_template_dictionary(self):
        """テンプレート辞書ファイルから辞書オブジェクトのリストを作る
        
        Returns:(dict):
            {'空欄の数': [テンプレート1, テンプレート2, ...], ...}
        """
        # template.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'template.txt')
        # テンプレート辞書ファイルオープン
        tfile = open(path, 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        t_lines = tfile.readlines()
        tfile.close()

        # 末尾の改行と空白文字を取り除いてリストに格納
        new_t_lines = []
        for line in t_lines:
            str = line.rstrip('\n')
            if (str!=''):
                new_t_lines.append(str)

        # テンプレート辞書の各行をタブで切り分けて、
        # '%noun%'の出現回数をキー、テンプレート文字列のリストを値にした辞書を作る
        # 
        # new_t_lines: テンプレート辞書の1行データのリスト
        # Block parameter:
        #   line(str): テンプレート辞書の1行データ
        template_dictionary = {}
        for line in new_t_lines:
            # 1行データをタブで切り分けて、以下の変数に格納
            # 
            # count: %noun%の出現回数
            # tempstr: テンプレート文字列
            count, tempstr = line.split('\t')
            # template_dictionaryのキーにcount('%noun%'の出現回数)が存在しなければ
            # countをキー、空のリストをその値として辞書template_dictionaryに追加
            if not count in template_dictionary:
                template_dictionary[count] = []
            # countキーのリストにテンプレート文字列を追加
            template_dictionary[count].append(tempstr)
            
        return template_dictionary

    def make_markov_dictionary(self):
        """ マルコフ辞書を作成
        
        """
        # ログからマルコフ連鎖で生成した文章を保持するリスト
        sentences = []
        # Markovオブジェクトを生成
        markov = Markov()
        # マルコフ連鎖で生成された文章群を取得
        text = markov.make()
        # 各文章の末尾の改行で分割してリストに格納
        sentences = text.split('\n')
        # リストから空の要素を取り除く
        if '' in sentences:
            sentences.remove('')
        
        return sentences

    def study(self, input, parts):
        """ ユーザーの発言を学習する

        Args:
            input(str): ユーザーの発言
            parts(strの多重list):
                ユーザー発言の形態素解析結果
                例:[['わたし', '名詞,代名詞,一般,*'],
                    ['は', '助詞,係助詞,*,*'], ... ]
        """
        # 入力された文字列末尾の改行を取り除く
        input = input.rstrip('\n')
        # ユーザー発言を引数にして、ランダム辞書に登録するメソッドを呼ぶ
        self.study_random(input)
        # ユーザー発言と解析結果を引数にして、パターン辞書の登録メソッドを呼ぶ
        self.study_pattern(input, parts)
        # 解析結果を引数にして、テンプレート辞書に登録するメソッドを呼ぶ。
        self.study_template(parts)

    def study_random(self, input):
        """ ユーザーの発言をランダム辞書に書き込む

        Args:
            input(str): ユーザーの発言            
        """
        # ユーザーの発言がランダム辞書に存在しなければself.randomの末尾に追加
        if not input in self.random:
            self.random.append(input)

    def study_pattern(self, input, parts):
        """ ユーザーの発言を学習し、パターン辞書への書き込みを行う

        Args:
            input(str): ユーザーの発言
            parts（strの多重list): 形態素解析結果の多重リスト    
        """
        # ユーザー発言の形態素の品詞情報がkeyword_check()で指定した
        # 品詞と一致するか、繰り返しパターンマッチを試みる
        #
        # Block Parameters:
        #     word(str): ユーザー発言の形態素
        #     part(str): ユーザー発言の形態素の品詞情報
        for word, part in parts:
            # 形態素の品詞情報が指定の品詞にマッチしたときの処理
            if analyzer.keyword_check(part):
                # PatternItemオブジェクトを保持するローカル変数
                depend = None
                # マッチングしたユーザー発言の形態素が、パターン辞書の
                # パターン部分に一致するか、繰り返しパターンマッチを試みる
                #
                # Block Parameters:
                #   ptn_item(str): パターン辞書1行のデータ(obj:PatternItem）。
                for ptn_item in self.pattern:
                    # パターン辞書のパターン部分とマッチしたら形態素とメッセージを
                    # 新規のパターン/応答フレーズとして登録する処理に進む
                    if re.search(
                            ptn_item.pattern, # パターン辞書のパターン部分。
                            word              # ユーザーメッセージの形態素
                            ):
                        # パターン辞書1行データのオブジェクトを変数dependに格納
                        depend = ptn_item
                        # マッチしたらこれ以上のパターンマッチは行わない
                        break
                    
                # ユーザー発言の形態素がパターン辞書のパターン部分とマッチしていたら、
                # 対応する応答フレーズグループの最後にユーザー発言を丸ごと追加する。
                if depend:
                    depend.add_phrase(input) # 引数はユーザー発言
                else:
                    # パターン辞書に存在しない形態素であれば、
                    # 新規のPatternItemオブジェクトを生成してpatternリストに追加する
                    self.pattern.append(
                        PatternItem(word, input)
                        )

    def study_template(self, parts):
        """ユーザーの発言を学習し、テンプレート辞書オブジェクトに登録する

        Args:
            parts（strのlistを格納したlist): ユーザーメッセージの解析結果
        """
        tempstr = ''
        count = 0
        
        # ユーザーメッセージの形態素が名詞であれば形態素を'%noun%'に書き換え、
        # そうでなければ元の形態素のままにして、「やっぱり%noun%だよね」のような
        # パターン文字列を作る。
        #
        # Block Parameters:
        #     word(str): ユーザー発言の形態素
        #     part(str): ユーザー発言の形態素の品詞情報
        for word, part in parts:
            # 形態素が名詞であればwordに'%noun%'を代入してカウンターに1加算する
            if (analyzer.keyword_check(part)):
                word = '%noun%'
                count += 1
            # 形態素または'%noun%'を追加する
            tempstr += word

        # '%noun%'が存在する場合のみ、self.templateに追加する処理に進む
        if count > 0:
            # countの数値を文字列に変換
            count = str(count)
            #　テンプレート文字列の'%noun%'の出現回数countが
            #　self.templateのキーとして存在しなければ
            # countの値をキー、空のリストをその値としてself.templateに追加
            if not count in self.template:
                self.template[count] = []

            # 処理中のテンプレート文字列tempstrが、self.templateのcountを
            #　キーとするリスト内に存在しなければ、リストにtempstrを追加する
            if not tempstr in self.template[count]:
                self.template[count].append(tempstr)

    def save(self):
        """ self.random、self.pattern、self.Templateの内容をファイルに書き込む
        
        """
        # ---ランダム辞書への書き込み--- #
        # 各フレーズの末尾に改行を追加する
        for index, element in enumerate(self.random):
            self.random[index] = element +'\n'
        # random.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'random.txt')
        # ランダム辞書ファイルを更新
        with open(path, 'w', encoding = 'utf_8') as f:
            f.writelines(self.random)
        
        # ---パターン辞書への書き込み--- #
        # パターン辞書ファイルに書き込むデータを保持するリスト
        pattern = []
        # パターン辞書のすべてのPatternItemオブジェクトから
        # 辞書ファイル1行のフォーマットを繰り返し作成する。
        for ptn_item in self.pattern:
            # make_line()で作成したフォーマットの末尾に改行を追加
            pattern.append(ptn_item.make_line() + '\n')
        
        # pattern.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'pattern.txt')
        # パターン辞書ファイルに書き込む
        with open(path, 'w', encoding = 'utf_8') as f:
            f.writelines(pattern)
        
        # ---テンプレート辞書への書き込み--- #
        # テンプレート辞書ファイルに書き込むデータを保持するリスト
        templist = []
        # ''%noun%'の出現回数[TAB]テンプレート\n'の1行を作り、
        # '%noun%'の出現回数ごとにリストにまとめる
        #
        # Block Parameters:
        #     key(str): テンプレートのキー('%noun%'の出現回数)
        #     val(str): テンプレートのリスト
        for key, val in self.template.items():
            # 同一のkeyの値で、'%noun%'の出現回数[TAB」テンプレート\n'の1行を作る
            #
            # Block Parameter:
            #     v(str): テンプレート1個
            for v in val:
                templist.append(key + '\t' + v + '\n')
        # リスト内のテンプレートをソート
        templist.sort()
        # template.txtのフルパスを取得
        path = os.path.join(os.path.dirname(__file__), 'dics', 'template.txt')
        # テンプレート辞書に書き込む
        with open(path, 'w', encoding = 'utf_8') as f:
            f.writelines(templist)