import csv
import os
import json
import sys
import io

# 出力のエンコーディングをUTF-8に固定（Windows対策）
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
def get_structured_merchant_data(file_path):
    """
    CSVを読み込み、2行1セットの構造を維持しながら、
    「明細の内容」をキーとしたIDとデータのマッピングを作成する。
    """
    if not os.path.exists(file_path):
        return {"error": f"入力ファイルが見つかりません: {file_path}"}

    merchant_map = {}
    
    try:
        with open(file_path, mode='r', encoding='cp932', newline='') as f:
            reader = csv.DictReader(f)
            # CSVの1列目（更新用IDのヘッダー）を確実に取得
            first_key = next(iter(reader.fieldnames))
            
            current_rule_id = None
            current_merchant = None
            
            for row in reader:
                # 「ルール行」の場合：IDと明細の内容（キーワード）を記憶
                if row.get("種類") == "ルール行":
                    current_rule_id = row.get(first_key, "")
                    current_merchant = row.get("明細の内容", "").strip()
                    
                    if not current_merchant:
                        continue
                        
                    if current_merchant not in merchant_map:
                        merchant_map[current_merchant] = {
                            "ids": [],
                            "rule_count": 0,
                            "original_data_samples": []
                        }
                    
                    # IDの追跡リストに追加
                    if current_rule_id:
                        merchant_map[current_merchant]["ids"].append(current_rule_id)
                    
                    merchant_map[current_merchant]["rule_count"] += 1
                    
                    # Claudeが判断しやすいようにサンプル情報を追加（例：金融機関など）
                    sample = f"[{row.get('金融機関', '共通')}] {row.get('口座', '')}"
                    if sample not in merchant_map[current_merchant]["original_data_samples"]:
                        merchant_map[current_merchant]["original_data_samples"].append(sample)
                
                # 「仕訳行」は直前のルール行に紐付くが、ここではID追跡が主目的のためカウントは不要
                # 必要に応じて仕訳行の勘定科目などもマッピングに含めることが可能
                
        return merchant_map

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Windows環境での標準出力をUTF-8に設定
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    # data/input フォルダ内の最新CSVを取得
    input_dir = os.path.join("data", "input")
    if not os.path.exists(input_dir):
        print(json.dumps({"error": "data/input ディレクトリが存在しません。"}, ensure_ascii=False))
        sys.exit(1)
        
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(json.dumps({"error": "CSVファイルが見つかりません。"}, ensure_ascii=False))
        sys.exit(1)

    target_csv = os.path.join(input_dir, sorted(csv_files)[-1])
    
    # 構造化されたデータをJSONで出力
    result = get_structured_merchant_data(target_csv)
    print(json.dumps(result, ensure_ascii=False, indent=2))