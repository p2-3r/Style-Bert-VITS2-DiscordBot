from src.json_utils.botdata import BotJson
from src.bots.registers import \
    on_interaction, \
    on_message, \
    on_ready, \
    on_slash, \
    on_voice_state_update
from src.global_data import client, tree


def run() -> None:
    # data.json から設定を取得
    bot_json = BotJson()
    TOKEN = bot_json.data['bot_token']

    # スラッシュコマンドやメッセージ送信時のイベントを登録
    """
    src.bots.registers フォルダに on_message 時などの
    event の時の動作をまとめてあって、.register で登録している
    
    スラッシュコマンド使用時と s!~ のメッセージコマンドの実際の動作は
    src.bots.commands フォルダにまとめてある
    
    ボタンやプルダウンの選択時の動作は
    src.bots.interactions.on_button_click, on_dropdown
    """
    on_interaction.register(client)
    on_message.register(client)
    on_ready.register(client, tree)
    on_voice_state_update.register(client)
    on_slash.register(tree)

    # BOTを起動
    client.run(TOKEN)
