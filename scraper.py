import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
from datetime import datetime, timedelta

# LeetCode站点配置
LEETCODE_SITES = {
    "us": {
        "base_url": "https://leetcode.com",
        "name": "LeetCode US"
    },
    "cn": {
        "base_url": "https://leetcode.cn",
        "name": "LeetCode China"
    }
}

# 定义要监控的LeetCode题目（使用题目slug）
PROBLEMS = [
    {
        "name": "Two Sum",
        "slug": "two-sum"
    },
    {
        "name": "Add Two Numbers",
        "slug": "add-two-numbers"
    },
    {
        "name": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters"
    },
    {
        "name": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays"
    },
    {
        "name": "Longest Palindromic Substring",
        "slug": "longest-palindromic-substring"
    }
]

# 数据存储文件
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "online_users.json")

# 确保数据目录存在
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 构建题目URL
def build_problem_url(site, slug):
    return f"{LEETCODE_SITES[site]['base_url']}/problems/{slug}/"

# 从LeetCode页面抓取在线人数
def scrape_online_users(problem_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(problem_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        # 查找在线人数元素
        # 注意：LeetCode页面结构可能会变化，需要根据实际情况调整选择器
        online_users_element = soup.find("div", class_=lambda x: x and "online" in x.lower())
        if online_users_element:
            text = online_users_element.get_text(strip=True)
            # 提取数字
            match = re.search(r"(\d+,?\d*)\s+users", text)
            if match:
                return int(match.group(1).replace(",", ""))
        
        return 0
    except Exception as e:
        print(f"Error scraping {problem_url}: {e}")
        return 0

# 保存数据到JSON文件
def save_data(data):
    try:
        # 读取现有数据
        existing_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        
        # 添加新数据
        existing_data.append(data)
        
        # 只保留最近30天的数据
        thirty_days_ago = datetime.now() - timedelta(days=30)
        filtered_data = [item for item in existing_data if datetime.fromisoformat(item["timestamp"]) >= thirty_days_ago]
        
        # 保存过滤后的数据
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        print("Data saved successfully")
    except Exception as e:
        print(f"Error saving data: {e}")

# 主函数
def main(site="us"):
    print(f"Starting to scrape LeetCode online users from {LEETCODE_SITES[site]['name']}...")
    
    timestamp = datetime.now().isoformat()
    results = []
    
    # 遍历所有题目并抓取在线人数
    for problem in PROBLEMS:
        problem_url = build_problem_url(site, problem["slug"])
        online_users = scrape_online_users(problem_url)
        results.append({
            "name": problem["name"],
            "online_users": online_users
        })
        print(f"{problem['name']}: {online_users} online users")
        
        # 避免请求过于频繁
        time.sleep(1)
    
    # 构建数据对象
    data = {
        "timestamp": timestamp,
        "site": site,
        "problems": results
    }
    
    # 保存数据
    save_data(data)
    
    print("Scraping completed")

if __name__ == "__main__":
    import sys
    
    # 默认爬取美国站，可以通过参数指定站点
    site = sys.argv[1] if len(sys.argv) > 1 else "us"
    
    # 验证站点参数
    if site not in LEETCODE_SITES:
        print(f"Error: Invalid site '{site}'. Available sites: {list(LEETCODE_SITES.keys())}")
        sys.exit(1)
    
    main(site)