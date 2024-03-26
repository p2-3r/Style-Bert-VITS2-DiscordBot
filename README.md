# アップデート中

現在アップデート中です

(リポジトリの名前を変更したり音声生成をライブラリ版のSBV2に変えたり、インストール方法の変更など)

アップデート完了までお待ちください

# Discord-ReadTextBot-for-Style-Bert-VITS2-API
Style-Bert-VITS2のAPIを使ったDiscordの読み上げボットです

✅ BOTのトークンとStyle-Bert-VITS2のパスをdata.jsonに書き込んで対応したバッチファイルを起動するだけで起動できます

✅ Style-Bert-VITS2の仮想環境を開いてAPIを起動...としなくても、バッチファイルからStyle-Bert-VITS2のAPIを直接起動できます

✅ アップデートもgitを入れているならupdate(need git).batを起動するだけです！

## このBOTの機能

✅ URLやコードブロック、カスタム絵文字は読み上げません

✅ コマンドで使用する声、読み上げ速度を変更できます(ユーザーごとに設定されるのでボイスチャンネルに参加した人たちそれぞれが別の声を使えます！)

✅ 2つ以上のサーバーでそれぞれ同時にボイスチャンネルに参加させても動きます

✅ ;をメッセージの先頭につけると読み上げません

✅ ボイスチャンネルにBOTしかいなくなった時の自動退出

✅ プレフィックスの変更に対応しています 例: s!ping → a?ping

✅ コマンドでボイスチャンネルに誰かが参加したときに自動で入ってくれるように設定できます

✅ スラッシュコマンドに対応しました！

✅ 辞書機能を使えます(大量に設定したい場合はStyle-bertVITS2側のユーザー辞書を変更してください)

## 必要なもの

* Python(作者は3.10.9で動作確認)

* Style-Bert-VITS2

* ffmpeg

* ( Git )

* DiscordのBOTアカウント

## 起動準備

このフォルダ全体をダウンロードしてどこかに置きます。
    
data.jsonの "bot_token" と "style_bertvits2_path" の値をそれぞれトークンとStyle-Bert-VITS2があるパスに書き換えます

例:

```json
{
    "settings": {
        "bot_token": "ThI1sIs2AnE3xAm4PlE5tOkE6n.eXaMpLe.ThI1sIs2AnE3xAm4PlE5tOkE6n",
        "style_bertvits2_path": "C:\\ExampleFolder\\Style-Bert-VITS2",
        "read_limit": 50,
        "url": "127.0.0.1",
        "port": "5000",
        "default_model": "0",
        "prefix": "s!"
    },
    "user_data": {
    },
    "server_data": {
    }
}
```

> [!CAUTION]
>
> ※パスを指定するとき、"\\" ではなく、"/" や "\\\\" を使用するようにしてください
> 
> ❌ C:\\ExampleFolder\\Style-Bert-VITS2
> 
> ⭕ C:/ExampleFolder/Style-Bert-VITS2
>
> ⭕ C:\\\\ExampleFolder\\\\Style-Bert-VITS2

## 起動方法

Botのみを起動したい場合は "run_bot.bat"

Style-Bert-VITS2のAPIのみを起動したい場合は "run_API.bat"

どちらも起動したい場合は "run_botandAPI.bat" を起動します

あとは待機すれば起動します。
    
## BOTの使用方法

プレフィックスを変更している場合はそのプレフィックスを使用してください

* <ins>s!help</ins> ヘルプを表示します

* <ins>s!ping</ins> pong!(BOTの起動確認にどうぞ)

* <ins>s!wav (content)</ins> 指定した内容の音声ファイルを添付して送ってくれます

* <ins>s!join</ins> 使用した人がいるボイスチャンネルに接続します

* <ins>s!change_voice</ins> 使用する声を変更するためのコマンドのヘルプを表示します

* <ins>s!server_settings</ins> 自動参加などサーバーに関する設定を変更するためのコマンドのヘルプを表示します

もしBOTが読み上げてくれなくなったら、BOTのボイスチャンネルへの再接続か、BOT自体の再起動を試してみてください

### <ins>change_voiceコマンドの使用方法</ins>

<ins>s!change_voice models</ins> 使用できるモデル一覧を表示します

<ins>s!change_voice models (number)</ins> 上のコマンドで表示したモデル一覧の番号を選択してそのモデルに変更します 

例: **s!change_voice models 3**

<ins>s!change_voice length</ins> このコマンドの使用方法を表示します

<ins>s!change_voice length (number)</ins> 読み上げ速度を変更します 小さいほど早く、大きいほど遅く読み上げます 

例: **s!change_voice length 1.5**

### <ins>server_settingsコマンドの使用方法</ins>

<ins>s!server_settings status</ins> このサーバーの現在の設定を表示します 

このserver_settingsコマンド以外を使用するにはそのサーバーの管理者である必要があります

<ins>s!server_settings auto_join</ins> そのサーバーのボイスチャンネルに誰かが参加したとき 

"s!join" コマンドを使用しなくても自動で参加してくれるようになります

<ins>s!server_settings auto_ch</ins> そのサーバーの自動参加時に読み上げるチャンネルを、

このコマンドを使用したチャンネルに設定します

## ボットの詳細設定

data.jsonに書かれている内容を変更するとプレフィックス(デフォルトではs!)などを変更することができます
    
* "**read_limit**" BOTが読み上げる上限を設定します。これを超えた文字数は以下略として省略されます

* "**url**" と "**port**" Style-BertVITS2のAPIのURLがこれでない場合、変更して対応してください

* "**default_model**" s!change_voice modelsコマンドを使用したことがない人が使用するデフォルトのモデルを指定できます

* "**prefix**" s!から変更して好きなプレフィックスにすることができます

## update (need git).batについて

起動するとdata.jsonの中身を引き継いで、他ファイルを更新することができます。

~~venvフォルダも削除されるので、次にボットを起動するときは少しお待ちください。~~

"requirements.txt" に変化がない限り、venvフォルダを削除しなくなりました！ 

アップデートしてすぐにBOTを使用できます。

> [!IMPORTANT]
>
> もしエラーでアップデートできなかった場合は、新しくこのフォルダ全体をダウンロードして "data.json" だけ置き換えてください
>
> "data.json" の名前が "data_old.json" になっている場合は "data.json" に名前を変更してから置き換えてください

## 予定(バグ修正とか)

25個以上のモデル、話者に対応させる (できたらやります...)
