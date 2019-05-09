import hashlib
import os


def get_str_md5(str):
    md5_obj = hashlib.md5()
    md5_obj.update(str.encode('utf-8'))
    return md5_obj.hexdigest()


def get_file_md5(filepath):
    if os.path.isfile(filepath):
        md5_obj = hashlib.md5()
        f = open(filepath, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            md5_obj.update(b)
        f.close()
        return md5_obj.hexdigest()


if __name__ == '__main__':
    print(strMD5("http://localhost:8000/users/login/"))
    # print(fileMD5('D:\\Download\\Xunlei\\Solo.A.Star.Wars.Story.2018.1080p.BluRay.x264-SPARKS[rarbg]\\solo.a.star.wars.story.2018.1080p.bluray.x264-sparks.mkv'))

