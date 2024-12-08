import requests
import json

# GitHub API URL for the main directory
GITHUB_API_URL = "https://api.github.com/repos/blackmatrix7/ios_rule_script/contents/rule/QuantumultX"

# 输出文件路径
OUTPUT_FILE = "quantumultx_list_links.txt"

# 创建空的输出文件
open(OUTPUT_FILE, "w").close()

# 函数：获取文件和文件夹，处理分页
def fetch_files(url):
    download_links = []
    while True:
        # 请求当前 URL 并获取分页数据
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})

        # 检查返回的状态码
        if response.status_code != 200:
            print(f"Error: Received HTTP {response.status_code} from GitHub API")
            break

        response_body = response.json()

        # 输出调试信息，检查 API 返回内容
        print(f"API Response Body: {json.dumps(response_body, indent=2)}")  # 打印响应内容

        # 提取 .list 文件的下载链接
        for item in response_body:
            print(f"Processing item: {json.dumps(item, indent=2)}")  # 打印每个文件或文件夹的详细信息
            if item["type"] == "file" and item["name"].endswith(".list"):
                download_links.append(item["download_url"])
                print(f"Found .list file: {item['download_url']}")

        # 检查是否有分页（next page）
        if "Link" in response.headers and 'rel="next"' in response.headers["Link"]:
            # 获取下一页的 URL
            next_page_url = response.headers["Link"].split(',')[1].split(';')[0].strip("<>").strip()
            print(f"Fetching next page: {next_page_url}")
            url = next_page_url
        else:
            break

    return download_links

# 主函数
def main():
    # 获取所有 .list 文件的下载链接
    download_links = fetch_files(GITHUB_API_URL)

    # 如果找到下载链接，保存到文件中
    if download_links:
        with open(OUTPUT_FILE, "w") as f:
            for link in download_links:
                f.write(link + "\n")
        print(f"Extracted download links have been saved to {OUTPUT_FILE}")
    else:
        print(f"No .list file links found.")

    # 输出所有下载链接
    print("Extracted download links:")
    for link in download_links:
        print(link)

if __name__ == "__main__":
    main()
