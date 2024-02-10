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

    どちらも起動したい場合は "run_botandAPI.bat" を起動します。

    あとは待機すれば起動します。
    
## BOTの使用方法

    プレフィックスを変更している場合はそのプレフィックスを使用してください

    s!help ヘルプを表示します

    s!ping pong!

    s!join 使用した人がいるボイスチャンネルに接続します

    s!change_voice 使用する声を変更するためのコマンドのヘルプを表示します
