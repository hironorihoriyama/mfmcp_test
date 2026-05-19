import csv
import os

def load_and_reset_ids(file_path):
    """
    MFCの自動仕訳ルールCSVを読み込み、更新用IDを空にしてリストで返す。
    ※ MFCからエクスポートされるCSVはShift-JIS(Windows標準)のため 'cp932' を指定します。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"入力ファイルが見つかりません: {file_path}")

    rules = []
    # cp932はShift-JISの拡張版で、MFCのCSV読み込みに最適です
    with open(file_path, mode='r', encoding='cp932', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 辞書の最初のキー（=更新用IDの列）を取得して値を空にする
            first_key = list(row.keys())
            row[first_key] = ""
            rules.append(row)
    
    return rules