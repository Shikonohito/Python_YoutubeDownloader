from pytube import StreamQuery
from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip
from pathlib import Path
from re import sub
from ytexceptions import ItagError


def clear_title(title: str):
    return sub(r'[\\/:*?"<>|]', '', title)


def get_itag_audio(yt_stream: StreamQuery, abr: str):
    for stream in yt_stream:
        print(stream)
        if stream.abr == abr:
            return stream.itag
    raise ItagError


def download_audio(yt_obj: YouTube, path: str, abr: str):
    ys = yt_obj.streams.filter(mime_type="audio/mp4")
    try:
        selected_itag = get_itag_audio(ys, abr)
        print("Audio download started...")
        yt_obj.streams.get_by_itag(selected_itag).download(output_path=path)
        print("Audio downloaded.")
    except ItagError as exc:
        print("Download interrupted")
        print(exc.message)
        raise exc


def get_itag_video(yt_stream: StreamQuery, res: str):
    for stream in yt_stream:
        print(stream)
        if stream.resolution == res:
            return stream.itag
    raise ItagError


def download_video(yt_obj: YouTube, path: str, res: str):
    ys = yt_obj.streams.filter(mime_type="video/mp4", res=res)
    try:
        selected_itag = get_itag_video(ys, res)
        print("Video download started...")
        yt_obj.streams.get_by_itag(selected_itag).download(output_path=path)
        print("Video downloaded.")
    except ItagError as exc:
        print("Download interrupted")
        print(exc.message)
        raise exc


def merge_video_audio(video_path, audio_path, save_path):
    if not Path(save_path).exists():
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        video.audio = audio
        video.write_videofile(save_path, threads=8)
        # TODO:
        #  write_videofile как-будто не закрывает поток. Исправить.

# TODO:
#  Вытащить из download_youtube_video всё то, что не относится к скачиванию, в отдельные функции

def download_youtube_video(url: str, path: str):
    yt = YouTube(url, use_po_token=True, token_file="token_file.json")
    title = clear_title(yt.title)
    print(title)

    path_video = path + f"\\{title}.mp4"
    path_audio = path + f"\\{title}.m4a"
    merged_video_path = path + f"\\{title}_edited.mp4"

    is_audio_downloaded = Path(path_audio).exists()
    is_video_downloaded = Path(path_video).exists()

    if not is_audio_downloaded:
        download_audio(yt, path, "128kbps")

    if not is_video_downloaded:
        download_video(yt, path, "720p")

    merge_video_audio(path_video, path_audio, merged_video_path)

    # TODO:
    #  Анлинки иногда не срабатывают. Исправить.
    Path(path_video).unlink()
    print(f"{path_video} removed")
    Path(path_audio).unlink()
    print(f"{path_audio} removed")
    Path(merged_video_path).rename(path_video)



def download_rollback(url, path):
    yt = YouTube(url, use_po_token=True, token_file="token_file.json")
    title = yt.title

    path_video = path + f"\\{title}.mp4"
    path_audio = path + f"\\{title}.m4a"

    if Path(path_audio).exists():
        Path(path_audio).unlink()

    if Path(path_video).exists():
        Path(path_video).unlink()

# TODO:
#  Создать функцию-менеджер, которая вызывает друг за другом функции

def get_url_list(path: str) -> list[str]:
    url_list = list()
    with open(path, 'r') as url_file:
        url_list = [line.rstrip('\n') for line in url_file.readlines()]
    return url_list


URL_PATH = "input_url.txt"
DOWNLOAD_PATH = r"E:\Download\Other"

yt_url_lst = get_url_list(URL_PATH)
download_result = []


for url in yt_url_lst:
    try:
        download_youtube_video(url, DOWNLOAD_PATH)
        download_result.append((url, "Success"))
    except (IOError, ItagError) as exc:
        download_result.append((url, "Failed"))
        print(exc)
        download_rollback(url, DOWNLOAD_PATH)

for result in download_result:
    print(result)

