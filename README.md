# Discord-ReadTextBot-for-Style-Bert-VITS2-API
Style-Bert-VITS2のAPIを使ったDiscordの読み上げボットです

## 必要なもの
Python(作者は3.10.9で動作確認)

## 起動準備
    このフォルダ全体をダウンロードしてどこかに置きます。
    
    data.jsonを開いて、

    "bot_token": "ここにBOTのトークン" と、

    "style_bertvits2_path": "C:/ExampleFolder/Style-Bert-VITS2"の、

    "ここにBOTのトークン"と、"C:/ExampleFolder/Style-Bert-VITS2"を、

    それぞれBOTのトークンとStyle-Bert-VITS2があるパスにします

    ※パスを指定するとき、"\" ではなく、"/" や "\\" を使用するようにしてください

## 使用方法

    Botのみを起動したい場合は "run_bot.bat"

    Style-Bert-VITS2のAPIのみを起動したい場合は "run_API.bat"

    どちらも起動したい場合は "run_botandAPI.bat" を起動します

    あとは待機すれば起動します。
    
## BOTの使用方法

    プレフィックスを変更している場合はそのプレフィックスを使用してください

    s!help ヘルプを表示します

    s!ping pong!

    s!join 使用した人がいるボイスチャンネルに接続します

    s!change_voice 使用する声を変更するためのコマンドのヘルプを表示します

## ボットの詳細設定

data.jsonに書かれている内容を変更するとプレフィックス(デフォルトではs!)などを変更することができます
    
    read_limit BOTが読み上げる上限を設定します。これを超えた文字数は以下略として省略されます

    urlとport Style-BertVITS2のAPIのURLがこれでない場合、変更して対応してください

    default_model s!change_voice modelsコマンドを使用したことがない人が使用するデフォルトのモデルを指定できます

    prefix s!から変更して好きなプレフィックスにすることができます

## 予定(バグ修正とか)

    urlを読み上げない機能がうまく動いていないことの修正

    絵文字を読まないように修正

    ;などを文章の先頭につけると読まないようにする

    やる気があったら辞書機能追加する
