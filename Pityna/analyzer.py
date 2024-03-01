import re
# janome.tokenizerからTokenizerをインポート
from janome.tokenizer import Tokenizer

def analyze(text):
    """ 形態素解析を行う

    Args:
        text(str): 解析対象の文章
            
        Returns:
            strのlistを格納したlist:
                形態素と品詞のリストを格納した2次元のリスト
    """
    t = Tokenizer()           # Tokenizerオブジェクトを生成
    tokens = t.tokenize(text) # 形態素解析を実行
    result = []               # 解析結果の形態素と品詞を格納するリスト
    
    # リストからTokenオブジェクトを1つずつ取り出す
    for token in tokens:
        # 形態素と品詞情報ををリスト形式で取得してresultの要素として追加
        result.append(
            [token.surface, token.part_of_speech])

    return(result)

def keyword_check(part):
    """ 品詞が名詞であるか調べる

    Args:
        part(str): 形態素解析結果から抽出したの品詞の部分 
            
        Returns:
            Matcオブジェクト: 品詞が名詞にマッチした場合
            None: 名詞にマッチしない場合
            
    """
    return re.match(
        '名詞,(一般|固有名詞|サ変接続|形容動詞語幹)',
        part
        )

def parse(text):
    """ 形態素解析によって形態素を取り出す

    Args:
        text(str): マルコフ辞書のもとになるテキスト
        
    Returns(list):
        形態素のリスト
    """
    # Tokenizerオブジェクトを生成
    t = Tokenizer()
    # 形態素解析を実行
    tokens = t.tokenize(text)
    # 形態素を格納するリスト
    result = []
    # 形態素(見出し)の部分を抽出してリストに追加
    for token in tokens:
        result.append(token.surface)

    return(result)
