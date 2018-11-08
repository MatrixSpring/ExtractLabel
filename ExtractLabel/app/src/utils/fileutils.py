'''
普通文件持久化或者缓存持久化
'''
import os


def save(data):
    with open('NormalFilePersistence.txt', 'w') as open_file:
        open_file.write(data)


def loadLine(path):
    with open(path, 'r', encoding='utf-8') as open_file:
        return open_file.readlines()


def loadFile(path):
    with open(path, 'r', encoding='utf-8') as open_file:
        return open_file.read()


def parse(response):
    print(response.body.decode('unicode_escape'))


def load_file(path):
    file = open(path, 'r', encoding='utf-8')
    lines = file.readlines()  # 读取全部内容 ，并以列表方式返回
    return ''.join(lines)


def save_class_notes(category_path, content_list, class_save_path):
    if not os.path.isdir(category_path):
        print("【{0}】不是目录".format(category_path))
        exit(-1)

    # 先将某一类的内容添加到列表
    files_path = []
    for filename in os.listdir(category_path):
        files_path.append(class_save_path + filename)

    print('files_path', len(files_path), ", ".join(files_path))

    for content_item in content_list:
        position = content_item['position']
        print('content_item', files_path[position[0]], content_item['remarks'], position[0])
        fp = open(files_path[position[0]], "a", encoding='utf-8', errors='ignore')
        fp.write(content_item['remarks'] + '\n')
        fp.close()


def get_file_child_name(category_path):
    if not os.path.isdir(category_path):
        print("【{0}】不是目录".format(category_path))
        exit(-1)

        # 先将某一类的内容添加到列表
    files_name = []
    for filename in os.listdir(category_path):
        files_name.append(filename)
    return files_name