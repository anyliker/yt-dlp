from math import fabs
import yt_dlp


def get_youtube_download_links(video_url):
    """
    获取 YouTube 视频的下载链接（按格式筛选）
    :param video_url: YouTube 视频链接（如 https://youtu.be/xxxx 或 https://www.youtube.com/watch?v=xxxx）
    :return: 字典，包含不同格式的下载链接和信息
    """
    # yt-dlp 配置：仅提取信息，不下载
    ydl_opts = {
        'quiet': False,          # 静默模式（不输出冗余日志）
        'no_warnings': False,    # 关闭警告
        'format': 'best',       # 默认优先最佳画质
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 提取视频的所有元信息（含下载链接）
            video_info = ydl.extract_info(video_url, download=False)

            # 整理关键信息
            download_links = {
                "title": video_info.get("title"),  # 视频标题
                "duration": video_info.get("duration"),  # 时长（秒）
                "formats": []  # 存储不同格式的下载链接
            }

            # 遍历所有可用格式，筛选常用的（MP4/音频）
            for fmt in video_info.get("formats", []):
                # 跳过无下载链接的格式
                if not fmt.get("url"):
                    continue

                # 提取关键格式信息
                format_info = {
                    "format_id": fmt.get("format_id"),  # 格式ID
                    "ext": fmt.get("ext"),  # 扩展名（mp4/webm/m4a等）
                    "resolution": fmt.get("resolution"),  # 分辨率（如 1080p/720p）
                    "filesize": fmt.get("filesize"),  # 文件大小（字节）
                    "url": fmt.get("url"),  # 核心:下载链接
                    # 是否仅音频
                    "audio_only": fmt.get("acodec") != "none" and fmt.get("vcodec") == "none"
                }
                download_links["formats"].append(format_info)

            return download_links

    except Exception as e:
        print(f"获取链接失败：{str(e)}")
        return None


# ------------------- 测试示例 -------------------
if __name__ == "__main__":
    # 替换为目标 YouTube 视频链接
    yt_url = "https://www.youtube.com/watch?v=odN890XAfek"

    links = get_youtube_download_links(yt_url)
    print('links.....', links)
    if links:
        print(f"视频标题：{links['title']}")
        print("\n可用下载格式及链接：")
        # 筛选 1080p MP4 格式（示例）
        for fmt in links["formats"]:
            if fmt["ext"] == "mp4" and fmt["resolution"] == "1080p":
                print(f"\n【1080p MP4】")
                print(f"文件大小：{fmt['filesize']/1024/1024:.2f} MB")
                print(f"下载链接：{fmt['url']}")
                break
        # 也可打印所有格式
        # for fmt in links["formats"]:
        #     print(f"\n格式：{fmt['ext']} | 分辨率：{fmt['resolution']}")
        #     print(f"链接：{fmt['url']}")
