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
    
    fieldnames = list(rules.keys())
    
    with open(output_path, mode='w', encoding='cp932', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rules)
        
    print(f"\nエクスポート完了: {output_path}")