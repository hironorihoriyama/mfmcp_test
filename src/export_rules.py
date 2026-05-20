import csv
import os
import json
import sys
import io

def export_processed_rules(mapping_json_str):
    """
    確定したマッピングに基づき、2種類のCSV（新規用・影響対象用）を出力する [2]。
    """
    try:
        # Claudeから渡されたJSONマッピングをパース
        final_mapping = json.loads(mapping_json_str)
    except Exception as e:
        print(f"JSONのパースに失敗しました: {e}")
        return

    # 最新の入力ファイルを取得
    input_dir = os.path.join("data", "input")
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    if not csv_files:
        print("入力CSVファイルが見つかりません。")
        return
    input_path = os.path.join(input_dir, sorted(csv_files)[-1])

    # 出力パスの定義
    output_new_path = os.path.join("data", "output", "new_journal_rules.csv")
    output_affected_path = os.path.join("data", "output", "affected_original_rules.csv")
    os.makedirs("data/output", exist_ok=True)

    new_rules = []
    affected_rules = []
    
    with open(input_path, mode='r', encoding='cp932', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        first_key = next(iter(fieldnames)) # 更新用IDの列名
        
        is_affected_rule = False # 現在のルール（複数行）が変更対象かどうかのフラグ [2]
        
        for row in reader:
            # ルール行の処理
            if row.get("種類") == "ルール行":
                original_detail = row.get("明細の内容", "").strip()
                
                # マッピングに存在するかチェック
                if original_detail in final_mapping:
                    is_affected_rule = True
                    # 影響を受けた元のデータを保存（ID入り） [2]
                    affected_rules.append(row.copy())
                    
                    # 新規登録用にデータを加工
                    row["明細の内容"] = final_mapping[original_detail]
                    row["明細一致条件"] = "部分一致"
                    row["優先度"] = "200" # 汎用ルールの優先度を下げる
                else:
                    is_affected_rule = False

            # 仕訳行の処理
            elif row.get("種類") == "仕訳行":
                if is_affected_rule:
                    affected_rules.append(row.copy())
                    # 新規登録用は摘要を空にする [2]
                    row["摘要"] = ""

            # 共通処理: 新規登録用CSVのためUpdate IDを空にする [2]
            new_row = row.copy()
            new_row[first_key] = ""
            new_rules.append(new_row)

    # CSVの書き出し
    write_csv(output_new_path, fieldnames, new_rules)
    print(f"-> 【新規登録用】を出力しました: {output_new_path} ({len(new_rules)} 行)")

    write_csv(output_affected_path, fieldnames, affected_rules)
    print(f"-> 【影響対象一覧】を出力しました: {output_affected_path} ({len(affected_rules)} 行)")

def write_csv(path, fieldnames, data):
    with open(path, mode='w', encoding='cp932', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    # Windows環境での標準出力をUTF-8に設定（文字化け対策） [会話履歴]
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("使用法: python src/export_rules.py '<json_mapping>'")
        sys.exit(1)
    
    # 引数全体を結合してJSONとして処理（空白等を含む場合への配慮） [会話履歴]
    mapping_str = " ".join(sys.argv[1:])
    export_processed_rules(mapping_str)