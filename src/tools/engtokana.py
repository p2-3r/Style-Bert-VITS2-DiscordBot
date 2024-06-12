"""
英語と日本語が混じった文章の英語を、カタカナに変換するプログラム
"""

import re

from alkana.data import data as trans_dict  # type: ignore


# alkana.get_word には型ヒントがないので
def __get_kana_from_dict(word: str) -> str | None:
    try:
        return trans_dict[word.lower()]
    except KeyError:
        return None


def __is_convert_target(word: str) -> bool:
    """
    渡された単語が英語かつ、大文字だけではないなら True を返す。
    """

    if word.isascii():  # 英語かどうか
        if word.isupper():  # 大文字だけかどうか
            return False
        else:
            return True
    else:
        return False


def __split_word(target_word: str) -> list[str]:
    """
    つながった英単語を分割して list[str] にして返す。

    分割の必要がない場合やできなかった場合は入力をそのまま list に入れて返す。

    英語ではない場合も、list に入れてそのまま返す。
    """

    if not __is_convert_target(target_word):  # 英語ではない場合、そのまま返す
        return [target_word]

    target_word_lower = target_word.lower()
    if target_word_lower in trans_dict:
        return [target_word]  # target_word が辞書にある場合そのまま返す

    # target_word の1文字目から、文字数-1文字目, 文字数-2文字目, ... と見ていく
    for i in range(len(target_word_lower), 0, -1):
        target_prefix = target_word_lower[:i]

        # target_word の最初の方が辞書にあったら
        if target_prefix in trans_dict:
            target_suffix = target_word_lower[i:]

            # target_word から見つかった単語を引いて、まだ文字が残っているなら
            if target_suffix != "":
                target_suffix_split = __split_word(target_suffix)  # さらに残りを再帰で分割する
                return [target_word[:i]] + target_suffix_split
            else:
                return [target_word[:i]]

    return [target_word]  # 分割できなかったら入力をそのまま返す


def convert_word_kana(word: str) -> str:
    """
    単語単位で英語をカタカナ読みに変換する。

    変換できないものはそのまま返す。
    """

    if not __is_convert_target(word):
        return word  # 変換したいものでなければそのまま返す

    to_kana_result = __get_kana_from_dict(word)

    # 変換可能だったら変換したもの、できなかったら入力をそのまま返す
    if to_kana_result is not None:
        return to_kana_result
    else:
        return word


def convert_all_text_kana(text: str) -> str:
    """
    入力された文章の英語をすべてカタカナ読みに変換する。

    もし "VeryVeryExcellent" のように英単語がつながっていても、

    単語ごとに分割して、"ベリーベリーエクセレント" のように変換する。
    """

    # 文章をアルファベット続きの部分とそれ以外の部分でリストに分割する
    sep_testlist = re.findall(r'[a-zA-Z]+|[^a-zA-Z]+', text)
    sep_testlist: list[str] = [s.strip() for s in sep_testlist if s.strip() != ""]

    # さらにつながったアルファベットを分割する
    sep_wordlist: list[str] = []
    for i in sep_testlist:
        sep_wordlist += __split_word(i)

    # 内容をそれぞれ変換する
    result_list = [convert_word_kana(i) for i in sep_wordlist]

    # 結果をすべてつなげて返す
    return "".join(result_list)


if __name__ == "__main__":
    # テスト用
    while True:
        input_text = input("変換したい文章を入力: ")
        result = convert_all_text_kana(input_text)
        print(result)
