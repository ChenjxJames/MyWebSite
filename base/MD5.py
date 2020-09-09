import hashlib
import os

SALT = "G0rOgF7z"  # 盐值用于字符串md5加密时插入


def str_add_salt_md5(str):
    """
    :param str:
    :return: md5(str + SALT)
    """
    return str_md5(str + SALT)


def str_md5(str):
    """
    :param str:
    :return: md5(str + SALT)
    """
    md5_obj = hashlib.md5()
    md5_obj.update(str.encode('utf-8'))
    return md5_obj.hexdigest()


def file_md5(filepath):
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
    print(str_add_salt_md5("md5test"))
    # print(fileMD5('D:\\test.txt'))
