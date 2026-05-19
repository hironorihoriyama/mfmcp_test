import csv
import os

def export_rules_to_csv(rules, output_path):
    """
    最適化されたルールのリストを、MFCインポート用のCSVとして保存する。
    """
    if not rules:
        print("出力するデータがありません。")
        return
    
    # 出力先ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 【修正箇所】リストの最初の1行（辞書）を安全に取り出し、そのキーをヘッダー列名として取得します
    first_row = next(iter(rules))
    fieldnames = list(first_row.keys())
    
    with open(output_path, mode='w', encoding='cp932', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rules)
        
    print(f"\nエクスポート完了: {output_path}")