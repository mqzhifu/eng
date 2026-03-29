import pymysql
import cloudscraper
from bs4 import BeautifulSoup
import time
import random
import sys
import re
from datetime import datetime

# ========================
# 【全局通用配置变量】
# ========================
CONFIG = {
    "REQUEST_TIMEOUT": 10,
    "SLEEP_SHORT_MIN": 0.8,
    "SLEEP_SHORT_MAX": 1.2,
    "SLEEP_LONG_MIN": 4,
    "SLEEP_LONG_MAX": 6,
    "BATCH_REQUEST_MIN": 7,
    "BATCH_REQUEST_MAX": 9,
    "FAIL_LIMIT": 3,
    "AFTER_FAIL_SLEEP": 10
}

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "mqzhifu123",
    "database": "test",
    "charset": "utf8mb4"
}

# ========================
# 日期解析
# ========================
def parse_born_date(born_str):
    if not born_str:
        return None

    try:
        s = str(born_str).strip()
        s = re.sub(r'([a-z])(\d)', r'\1 \2', s, flags=re.I)
        s = re.sub(r'([A-Za-z])(\d{4})', r'\1 \2', s)
        s = re.sub(r'\d+([stndrh]{2})', lambda m: m.group().strip("stndrh"), s, flags=re.I)
        s = s.replace("of", "").replace("  ", " ").strip()

        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

        parts = s.split()
        day = parts[1]
        month_str = parts[2]
        year = parts[3]
        month = month_map[month_str]
        dt = datetime(int(year), int(month), int(day))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def parse_html_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = {
        'name': None,
        'also_known_as': None,
        'Age': None,
        'Height': None,
        'born_date': None,
        'Born': None,
        'Birthplace': None
    }

    h1 = soup.find('h1')
    if h1:
        result['name'] = h1.get_text(strip=True)

    aka_h2 = soup.find('h2', id='aka')
    if aka_h2:
        txt = aka_h2.get_text(strip=True)
        if 'Also known as:' in txt:
            ali = txt.replace('Also known as:', '').strip()
            result['also_known_as'] = [a.strip() for a in ali.split('-') if a.strip()]

    labels = soup.find_all('span', class_='label')
    for label in labels:
        key = label.get_text(strip=True).rstrip(':')
        val = label.find_next_sibling('span', class_='value')
        if not val:
            continue
        v = val.get_text(strip=True)

        if key == 'Age':
            v = re.sub(r'\s*years old\s*', '', v, flags=re.I).strip()
            result['Age'] = v

        elif key == 'Height':
            m = re.search(r'(\d+)\s*cm', v)
            result['Height'] = f"{m.group(1)}cm" if m else ""

        elif key == 'Born':
            result['Born'] = v
            result['born_date'] = parse_born_date(v)

        elif key == 'Birthplace':
            result['Birthplace'] = v

    return result

def is_name_exists(conn, name):
    print(f"📊 执行SQL: SELECT id FROM babepedia_info WHERE name = %s 参数: ({name})")
    cur = conn.cursor()
    cur.execute("SELECT id FROM babepedia_info WHERE name = %s", (name,))
    exist = cur.fetchone() is not None
    cur.close()
    return exist

# ========================
# 入库SQL
# ========================
def save_to_db(conn, data):
    name = data.get('name')
    if not name:
        print("❌ 无姓名，跳过")
        return

    ak = ', '.join(data['also_known_as']) if data['also_known_as'] else None
    age = data.get("Age")
    height = data.get("Height")
    born_date = data.get("born_date")
    born = data.get("Born")
    bp = data.get("Birthplace")

    ts = int(time.time())
    ig = 0
    cur = conn.cursor()

    if is_name_exists(conn, name):
        sql = """UPDATE babepedia_info
                 SET also_known_as=%s, Age=%s, Height=%s, born_date=%s, Born=%s, Birthplace=%s, up_time=%s, is_ignore=%s
                 WHERE name=%s"""
        cur.execute(sql, (ak, age, height, born_date, born, bp, ts, ig, name))
        print(f"✅ 更新 → {name}")
    else:
        sql = """INSERT INTO babepedia_info
                 (name, also_known_as, Age, Height, born_date, Born, Birthplace, add_time, up_time, is_ignore)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(sql, (name, ak, age, height, born_date, born, bp, ts, ts, ig))
        print(f"✅ 新增 → {name}")

    conn.commit()
    cur.close()

def create_scraper():
    return cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows'})

# ========================
# 主程序：已放开全部数据，无100条限制
# ========================
def main():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        print(f"📊 执行SQL: SELECT name FROM new_girl_2 WHERE name != '' ORDER BY name ASC")
        cur.execute("SELECT name FROM new_girl_2 WHERE name != '' ORDER BY name ASC")
        name_list = [r[0].strip() for r in cur.fetchall() if r[0].strip()]

        # ✅ 已放开限制，抓取全部
        total = len(name_list)
        print(f"📋 本次处理：{total} 条（全部数据）")
        cur.close()
    except Exception as e:
        print("数据库错误：", e)
        return

    scraper = create_scraper()
    requested = []
    success = fail = skip = exist = total_fail = 0

    for i, name in enumerate(name_list, 1):
        print(f"\n===== {i}/{total} | {name} =====")
        if is_name_exists(conn, name):
            print("ℹ️ 已存在，跳过")
            exist += 1
            continue

        url = f"https://www.babepedia.com/babe/{name.replace(' ', '_')}"
        print(f"🌍 请求: {url}")
        requested.append(name)

        try:
            resp = scraper.get(url, timeout=CONFIG["REQUEST_TIMEOUT"])
            if resp.status_code != 200:
                print(f"❌ 请求失败")
                fail += 1
                total_fail += 1
                if total_fail >= CONFIG["FAIL_LIMIT"]:
                    print(f"⏸ 累计失败，休眠10秒")
                    time.sleep(10)
                    total_fail = 0
                time.sleep(random.uniform(0.8,1.2))
                continue

            if "no exact match" in resp.text.lower():
                print("❌ 页面不存在")
                skip += 1
                time.sleep(random.uniform(0.8,1.2))
                continue

            data = parse_html_content(resp.text)
            print(f"🧹 解析完成: {data}")
            save_to_db(conn, data)
            success += 1
            time.sleep(random.uniform(0.8,1.2))

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            fail += 1
            total_fail += 1
            if total_fail >= 3:
                time.sleep(10)
                total_fail = 0
            continue

    conn.close()
    print("\n=== 全部处理完成 ===")
    print(f"✅ 请求过的名称列表：{requested}")
    print(f"✅ 成功入库：{success}")
    print(f"❌ 请求失败：{fail}")
    print(f"ℹ️ 已存在跳过：{exist}")
    print(f"🚫 页面不存在：{skip}")

if __name__ == "__main__":
    main()

