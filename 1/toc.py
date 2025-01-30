import json
import re


def update_headings_in_ipynb(ipynb_file):
    """ 指定された .ipynb ファイル内の見出しに対して、正しい番号付けを行います。 """
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    heading_counts = [0, 0, 0, 0, 0, 0]  # 見出しレベルごとのカウンター（# ～ ######）

    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            new_source = []
            for line in cell['source']:
                # 見出しの検出（既存の番号も考慮）
                match = re.match(r'^(#{1,6})\s+((\d+(\.\d+)*)\s+)?(.+)', line)
                
                if match:
                    level = len(match.group(1))  # 見出しのレベル
                    existing_number = match.group(3)  # 既存の番号（例: 1.2.3）
                    title = match.group(5).strip()  # 見出しのタイトル

                    # 正しい番号を決定
                    heading_counts[level:] = [0] * (6 - level)  # 下位レベルをリセット
                    heading_counts[level - 1] += 1
                    correct_number = '.'.join(map(str, heading_counts[:level]))
                    
                    # 既存の番号がある場合、正しいか確認
                    if existing_number:
                        if existing_number != correct_number:
                            # 間違った番号を上書き
                            correct_heading = f"{match.group(1)} {correct_number} {title}"
                        else:
                            # 正しい場合はそのまま
                            correct_heading = line
                    else:
                        # 新しい番号を振る場合
                        correct_heading = f"{match.group(1)} {correct_number} {title}"
                    
                    new_source.append(correct_heading)
                else:
                    new_source.append(line)
            cell['source'] = new_source

    # ファイルに書き戻す
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 実行例
update_headings_in_ipynb('1/DeepLearningFromScratch1.ipynb')
