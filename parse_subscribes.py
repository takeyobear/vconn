import requests
from bs4 import BeautifulSoup
import re
import re
from datetime import datetime

# 获取当前年份和月份
current_year = datetime.now().strftime("%Y")
current_month = datetime.now().strftime("%m")
current_day = datetime.now().strftime("%d")
date_variable = f"{current_year}{current_month}{current_day}"

url = f"https://www.cfmem.com/{current_year}/{current_month}/{date_variable}-32-v2rayclashsingbox-vpn.html"
print(url)

# 发送请求获取页面内容
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(html_content, 'html.parser')

# 提取页面中的文字内容
text = soup.get_text()

# 输出结果

yaml_links = re.findall(r'clash\s*->\s*(https://fs\.v2rayse\.com/share/\d{8}/[a-zA-Z0-9_-]+\.yaml)', text)
# 假设获取到第一个链接
if yaml_links:
    yaml_link = yaml_links[0]

    # 发送请求获取 YAML 文件内容
    response_yaml = requests.get(yaml_link)
    yaml_content = response_yaml.text

    # 将 YAML 内容按行分割，并过滤掉以 '#' 开头的注释行
    yaml_lines = yaml_content.splitlines()
    filtered_lines = [line for line in yaml_lines if not line.strip().startswith('#')]

    # 重新组合过滤后的内容
    yaml_content_modified = '\n'.join(filtered_lines)
    
    # 在头部添加 LastUpdate 字段
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yaml_content_modified = f"# 节点类型：vmess, vless, trojan\n# LastUpdate: {current_time}\n\n{yaml_content_modified}"


    # 将修改后的 YAML 文件保存到本地路径
    save_path = "subscribe/clash_providers01.yaml"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(yaml_content_modified)

    print(f"成功保存 YAML 文件到 {save_path}")
else:
    print("未找到符合条件的 YAML 链接")