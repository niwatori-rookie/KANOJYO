# kanojyo_talk（戦場ヶ原ひたぎVer.）

![empty](https://github.com/niwatori-rookie/kanojyo_talk/assets/138978518/37f341b3-b913-406a-9a64-c52ce05e070d)

・コードスペース（容量大きいファイルを除く）：https://shiny-xylophone-7v9vpq9xr9q6cpvvw.github.dev/

・プログラムの環境

＃＃＃（フロントエンド）＃＃＃

・pyqt5

・Qt designer

＃＃＃（バックエンド）＃＃＃

・python


#環境構築（準備中）

1:Cmake、visualstudioのC++ツール（VScodeとの連携も必要だかすでにしてある。）

2pyopenjtalkのライブラリのインストール（むず過ぎ）

3cythonのライブラリのインストール


#プログラムの詳細

・VALL-E-Xを使用そして新たにsound.pyを実装し、mainwiodows.pyにimportをした。

・VALL-E-Xの音声処理があまりにも重たかったので、並列処理（threading）を実装した。

※参考サイト：https://zenn.dev/nekoallergy/articles/py-advance-threading-01

#その他

3階マルコフ連鎖、形態素解析を採用。
Web Speech APIとの連携（既に実行済み）。


#動画等



![image](https://github.com/niwatori-rookie/kanojyo_talk-Ver.-/assets/138978518/d36fd2dc-37d2-4a2e-a309-bc0d159690be)






