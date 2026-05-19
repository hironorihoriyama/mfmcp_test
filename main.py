import os
from src.load_rules import load_and_reset_ids
from src.clean_rules import clean_and_merge_rules, interactive_check_with_claude
from src.export_rules import export_rules_to_csv

def main():
    # 入力ファイルと出力ファイルのパスを定義
    input_file = os.path.join("data", "input", "office_journal_rules_20260519_095938.csv")
    output_file = os.path.join("data", "output", "new_journal_rules.csv")
    
    print("==================================================")
    print("  MF自動仕訳ルール リファクタリングツールを起動")
    print("==================================================")
    
    # 1. データの読み込みと初期化
    print(f"\n[STEP 1] ファイルを読み込んでいます...\n  対象: {input_file}")
    try:
        rules = load_and_reset_ids(input_file)
        print(f"  -> 読み込み成功: {len(rules)} 行のデータを取得しました。")
    except Exception as e:
        print(f"  -> [エラー] {e}")
        return

    # 2. 定型キーワードの重複チェックと統合
    print("\n[STEP 2] キーワード統合処理を実行しています...")
    cleaned_rules = clean_and_merge_rules(rules)
    print("  -> 完了しました。")
    
    # 3. AIと連携した表記揺れチェック（インタラクティブ）
    print("\n[STEP 3] 表記揺れチェックを開始します...")
    final_rules = interactive_check_with_claude(cleaned_rules)
    
    # 4. 洗い替え用CSVの出力
    print("\n[STEP 4] 新しいCSVファイルを生成しています...")
    export_rules_to_csv(final_rules, output_file)
    
    print("\n==================================================")
    print("  すべての処理が完了しました！")
    print("  [次のアクション]")
    print("  1. MFクラウドの画面で既存のルールを「全選択 → 一括削除」してください。")
    print("  2. 生成された 'data/output/new_journal_rules.csv' をインポートしてください。")
    print("==================================================")

if __name__ == "__main__":
    main()