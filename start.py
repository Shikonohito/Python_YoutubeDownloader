import yt_dlp

def get_url_list(path: str) -> list[str]:
    url_list = list()
    with open(path, 'r') as url_file:
        url_list = [line.rstrip('\n') for line in url_file.readlines()]
    return url_list


def start_download(from_path, to_path, mode='video+audio'):
    yt_url_lst = get_url_list(from_path)

    ydl_opts = {
        'ffmpeg_location': 'E:/Program Files/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe',
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'merge_output_format': 'mp4',
        'outtmpl': f'{to_path}/%(title)s.%(ext)s'
    }

    if mode == 'audio':
        ydl_opts = {
            'ffmpeg_location': 'E:/Program Files/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe',
            'format': 'bestaudio',
            'audio_format': 'mp3',
            'audio_quality': '320K',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': f'{to_path}/%(title)s'
        }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(yt_url_lst)



def main_menu():
    DOWNLOAD_PATH = r"E:\Download\Other"
    URL_PATH = "input_url.txt"
    CHOICE_EXIT = "3"
    while True:
        print("1. Download video from file")
        print("2. Download only audio")
        print(f"{CHOICE_EXIT}. Exit")
        choice = input("Choice: ")

        if choice == "1":
            input(f"Add urls to file {URL_PATH} and press any key to continue...")
            start_download(URL_PATH, DOWNLOAD_PATH)
        elif choice == "2":
            input(f"Add urls to file {URL_PATH} and press any key to continue...")
            start_download(URL_PATH, DOWNLOAD_PATH, 'audio')
        elif choice == CHOICE_EXIT:
            break

        print("=" * 100)


main_menu()