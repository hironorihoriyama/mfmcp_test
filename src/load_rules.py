import csv
import os

def load_and_reset_ids(file_path):
    """
    MFCの自動仕訳ルールCSVを読み込み、更新用IDを空にしてリストで返す。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"入力ファイルが見つかりません: {file_path}")

    rules = []
    with open(file_path, mode='r', encoding='cp932', newline='') as f:
        reader = csv.DictReader(f)
        
        # システムの記号削除を回避するため、next(iter()) を使用して確実に最初の列名（文字列）を取得します
        first_key = next(iter(reader.fieldnames))
        
        for row in reader:
            # 取得した1列目のキーを指定して値を空欄にします
            row[first_key] = ""
            rules.append(row)
    
    return rules