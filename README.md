# kanojyo_talk（戦場ヶ原ひたぎVer.）

![empty](https://github.com/niwatori-rookie/kanojyo_talk/assets/138978518/37f341b3-b913-406a-9a64-c52ce05e070d)

・コードスペース（容量大きいファイルを除く）：https://shiny-xylophone-7v9vpq9xr9q6cpvvw.github.dev/

・プログラムの環境

＃＃＃（フロントエンド）＃＃＃

・pyqt5

・Qt designer

＃＃＃（バックエンド）＃＃＃

・python


### 環境構築（準備中）

---------------------------------------------------------------------------

1:Cmake、visualstudioのC++ツール（VScodeとの連携も必要だかすでにしてある。）

2pyopenjtalkのライブラリのインストール(難しい)　　　

Some basic python commands are:
```
pip install pyopenjtalk --no-build-isolation
```

3cythonのライブラリのインストール


※※2の参照先（pyopenjtalkのgithubのReadmeから）※※

ビルド要件
Python パッケージは、open_jtalk および hts_engine_API の Python バインディングを作成するために cython に依存しています。 pyopenjtalk をビルドしてインストールするには、次のツールが必要です。

・C/C++ コンパイラ (C/C++ 拡張機能を構築するため)

・cmake

・cython

---------------------------------------------------------------------------



### プログラムの詳細

---------------------------------------------------------------------------

・VALL-E-Xを使用そして新たにsound.pyを実装し、mainwiodows.pyにimportをした。

・VALL-E-Xの音声処理があまりにも重たかったので、並列処理（threading）を実装した。

※参考サイト：https://zenn.dev/nekoallergy/articles/py-advance-threading-01

・3階マルコフ連鎖、形態素解析を採用。

・Web Speech APIとの連携（既に実行済み）。｛tryとexceptによる例外処理｝

※参考サイト：https://enjoy-life-fullest.com/2024/01/06/%E5%88%9D%E5%BF%83%E8%80%85%E5%90%91%E3%81%91-python%E3%81%A7%E8%AD%B0%E4%BA%8B%E9%8C%B2%E4%BD%9C%E6%88%90%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%AA%E3%82%A2%E3%83%AB%E3%82%BF%E3%82%A4%E3%83%A0/


### UI画面

---------------------------------------------------------------------------

![image](https://github.com/niwatori-rookie/kanojyo_talk-Ver.-/assets/138978518/d36fd2dc-37d2-4a2e-a309-bc0d159690be)


### 動画によるシュミレーション

---------------------------------------------------------------------------




### 今後の予定

---------------------------------------------------------------------------

・APIなどを導入することで、話しているうちに認知症の度合いを判断してくれるような機能を搭載する。





