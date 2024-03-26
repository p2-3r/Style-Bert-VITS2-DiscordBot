# アップデート中

現在アップデート中です

(リポジトリの名前を変更したり音声生成をライブラリ版のSBV2に変えたり、インストール方法の変更など)

アップデート完了までお待ちください

# アップデート: ライブラリ版のSBV2に対応しました。

v2.0以前を使用している方はすみませんが、インストールしなおしてください。

# Style-Bert-VITS2-DiscordBot

Style-Bert-VITS2のライブラリを使ったDiscordの読み上げボットです

## 機能

・ joinコマンドを使用したチャンネルの読み上げ

・ モデル、話者、スタイルの切り替え

・ サーバー辞書、自動参加の設定

・ BOTしかいなくなった場合の自動退出

・ ユーザーごとに別の声を使用できます

・ プレフィックスの変更

## 必要なもの

・ Discordのボットアカウントとそのトークン

(BOTはインテンツの設定がONになっている必要があります。)

#### (手動でインストールする場合)

・ Python (3.10.11で動作確認)

・ Git

・ ffmpeg

## インストール

[ここ](https://github.com/p2-3r/Style-Bert-VITS2-DiscordBot/releases/download/v2.0/SBV2_DiscordBot_Install.bat) から "SBV2_DiscordBot_Install.bat" のバッチファイルを

ダウンロードしてインストールしたい場所で起動します。

必要なもののダウンロードが完了して、"完了しました。" と表示されたら、

"Style-Bert-VITS2-DiscordBot" フォルダ内の "bot_start.bat"を起動します。

#### 手動インストール

Python、git、ffmpegがすでにある人は追加でpythonなどをダウンロードせずに

手動でインストールすることもできます。

```
git clone https://github.com/p2-3r/Style-Bert-VITS2-DiscordBot.git
```

"bot_start.bat"を起動、または自分で仮想環境を作成して起動します。

```
python -m venv venv

"venv/Scripts/activate"

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r requirements.txt

python main.py
```

一度インストールすると、次からは "bot_start.bat" で起動できます。

## 起動準備

"model_assets" フォルダ内に使用したいモデルを入れます。

botを起動するとトークンが設定されていない場合は聞いてくるので入力します。

※モデルが一つも入っていない場合起動できません。

## BOTの使用方法

スラッシュコマンド、またはprefix + コマンド名で使用できます。 

(/ping または s!pingなど)

```
s!ping pong!

s!wav (content) 現在のモデルで(content)の内容の音声が送信されます。

s!join 使用した人がいるボイスチャンネルに参加

s!leave ボイスチャンネルから退席

s!model, s!speaker, s!style それぞれモデル、話者、スタイルの変更メニューを表示

s!dic サーバー辞書のメニューを表示 (デフォルトでは管理者のみ変更可能)

s!server 自動参加などのサーバー設定を表示 (管理者のみ変更可能)
```

## 詳細設定

"data.json" ファイルを開いて設定を変更できます。

```
bot_token: 使用したいボットのトークンを設定。

read_limit: 何文字目まで読むかの設定 これを超えた文字数は以下略されます。

default_model: モデルを変更していないユーザーに使用されるモデルの設定 (model_assetsフォルダの中のフォルダ名で指定)。

prefix: BOTのプレフィックス (デフォルトではs!) の設定。

models_upperlimit: モデルをたくさん読みこみすぎてメモリを消費しすぎないようにデフォルトでは3つに制限しています。
                    複数のモデルが読み込まれるのを許容する場合は数値を上げてください。

device: 音声合成に使用するデバイス。 "cpu" や "cuda" などで指定してください。

user_data: ユーザーごとにどのモデルや話者を使用しているかの情報などが保存されています。

server_data: サーバーごとの自動参加などの設定が保存されています。
```

## アップデート

update.batの起動、または git pull などで更新できます。

## 予定など

特になし？

## 追記

pythonなどがなくても実行できるようにと考えましたが、

ちゃんと動作するか不安なのでもし動かなければ教えてください...
