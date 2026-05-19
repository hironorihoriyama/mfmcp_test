import re

def clean_and_merge_rules(rules):
    """
    1. キーワード重複チェック＆部分一致への統一
    MFCのCSVは「ルール行」とそれに紐づく「仕訳行」の順で並んでいます。
    """
    # 統合対象のチェーン店・共通キーワードリスト
    target_keywords = ["フアミリ-マ-ト", "スターバックス", "カラオケまねきねこ", "スペースマーケット"]
    
    cleaned_rules = []
    is_target_rule = False  # 直前のルール行が統合対象だったかどうかのフラグ
    
    for row in rules:
        if row.get("種類") == "ルール行":
            original_detail = row.get("明細の内容", "")
            
            # キーワードが含まれているかチェック
            matched_keyword = None
            for kw in target_keywords:
                if kw in original_detail:
                    matched_keyword = kw
                    break
            
            if matched_keyword:
                # 汎用的な「部分一致」ルールに書き換える
                row["明細の内容"] = matched_keyword
                row["明細一致条件"] = "部分一致"
                row["優先度"] = "200"  # 汎用ルールの優先度を下げて誤爆を防ぐ
                is_target_rule = True
            else:
                is_target_rule = False
                
        elif row.get("種類") == "仕訳行":
            # 直前のルール行が統合対象（部分一致化）されたものなら、摘要を空にする
            if is_target_rule:
                # 摘要を空欄にすることで、MFC取り込み時に実際の店舗名が適用されます
                row["摘要"] = ""
                
        cleaned_rules.append(row)
        
    return cleaned_rules

def interactive_check_with_claude(rules):
    """
    2. 表記揺れチェック（AI提案 ＋ 人間による目視確認）
    ※まずは対話UIの土台です。後続のステップでここにClaude APIの呼び出しを追加します。
    """
    print("\n--- AIによる表記揺れチェック ---")
    # ここにClaude APIへデータを投げて表記揺れ候補を受け取る処理を実装します
    
    # 疑似的な対話UIのテスト実装
    print("[AI提案] 'Amazon' と 'アマゾン' は同一取引先とみなせます。統合しますか？ (y/n): ", end="")
    ans = input().strip().lower()
    
    if ans == 'y':
        print("  -> 統合を承認しました。（※今回はテストのため実際のデータは変更されません）")
    else:
        print("  -> 統合を見送りました。")
        
    return rules