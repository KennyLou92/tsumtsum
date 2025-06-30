import re
import json

# 讀入 tsum.js
with open('tsum.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 擷取 const tsumData = [ ... ];
match = re.search(r'const tsumData\s*=\s*(\[[\s\S]*?\]);', content)
if not match:
    raise ValueError("❌ 找不到 tsumData 陣列")

tsum_array_str = match.group(1)

# 將 JS key 加上雙引號 + 移除 ,] 結尾
def fix_js_to_json(js_text):
    js_text = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1 "\2":', js_text)
    js_text = re.sub(r',\s*\]', ']', js_text)
    return js_text

tsum_array_json_str = fix_js_to_json(tsum_array_str)
tsum_data = json.loads(tsum_array_json_str)

# 加入 skill_label，從 image 的第一張圖抓出 tsum 名
for tsum in tsum_data:
    image = tsum.get("image", "")
    
    # 若為 list，取第一個
    if isinstance(image, list):
        image = image[0] if image else ""

    # 解析 block_<tsum名>_l.png
    if isinstance(image, str):
        match_img = re.match(r'block_([a-zA-Z0-9_]+)_l\.png', image)
        if match_img:
            tsum_name = match_img.group(1).lower()
            tsum["skill_label"] = f"win_tsumskill_{tsum_name}.png"

# 輸出為 JS 格式
new_json = json.dumps(tsum_data, ensure_ascii=False, indent=2)
new_js = f"const tsumData = {new_json};\n"

with open('tsum.js', 'w', encoding='utf-8') as f:
    f.write(new_js)

print("✅ skill_label 已根據 image（第一張圖）加入成功！")
