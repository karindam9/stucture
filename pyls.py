import json
import sys
import time


def read_json(file_path):
    f = open(file_path)
    data = json.load(f)
    return data


def ls_cmd(data, arg):
    content = data["contents"]
    # print(content)

    if type(arg) == "<class 'str'>":
        func_name = (("test"+arg).replace("-","_")).lower()
    else:
        st = "".join(arg)
        func_name = (replace_all("test"+st)).lower()
        # print(func_name)

    try:
        li = getattr(sys.modules[__name__], func_name)(content)

    except Exception as error:
        li = []
        if "filter" in str(error):
            print('error: It is not a valid filter criteria. Available filters are "dir" and "file"')
        else:
            li = test_path(content, arg[-1])

    if li is not None:

        for i in li:
            print(i)


def test(content):
    for i in content:
        name = i["name"]
        if name.startswith("."):
            pass
        else:
            print(name)


def test_a(content):
    for i in content:
        print(i["name"])


def test_l(content):
    li1 = []
    for i in content:
        if i["name"].startswith("."):
            pass
        else:
            li = time.ctime(i["time_modified"]).split(" ")
            li1.append([i["permissions"], i["size"], li[1], li[2], str(li[3].split(":")[0])+":"+str(li[3].split(":")[1]), i["name"]])

    return li1


def test_h(content):
    li1 = []
    for i in content:
        if i["name"].startswith("."):
            pass
        else:
            li = time.ctime(i["time_modified"]).split(" ")
            st = "k"
            if i["size"] < 1023:
                size = i["size"]
                st = ""
            elif 1023 < i["size"] <= 2048:
                size = round(i["size"]/1024, 1)
                st = "k"
            elif 2048 < i["size"] <= 3072:
                size = round(i["size"]/2048, 1)
                st = "M"

            else:
                size = round(i["size"]/3072, 1)
                st = "G"

            li1.append([i["permissions"], str(size)+st, li[1], li[2], str(li[3].split(":")[0])+":"+str(li[3].split(":")[1]), i["name"]])

    return li1


def test_l_r(content):
    li1 = test_l(content)
    return reversed(li1)


def test_l_r_t(content):
    li1 = test_l_r(content)
    return sorted(li1, reverse=True, key=lambda x: (x[2], x[3], x[4]))


def test_l_r_t_filter_dir(content):
    li1 = test_l_r_t(content)
    li2 = []
    for i in li1:
        # print(i[-1])
        if "." not in i[-1] and i[-1].lower() != "license":
            li2.append(i)

    return li2


def test_l_r_t_filter_file(content):
    li1 = test_l_r_t(content)
    li2 = []
    for i in li1:
        # print(i[-1])
        if "." not in i[-1] and i[-1].lower() != "license":
            pass
        else:
            li2.append(i)

    return li2


def test_path(content, path):
    li1 = []
    for i in content:
        if i["name"] == path:
            if "contents" in i.keys():
                if len(i["contents"]) != 0:
                    for j in i["contents"]:
                        li = time.ctime(j["time_modified"]).split(" ")
                        li1.append([j["permissions"], j["size"], li[1], li[2], str(li[3].split(":")[0])+":"+str(li[3].split(":")[1]), j["name"]])

            else:
                li = time.ctime(i["time_modified"]).split(" ")
                li1.append([i["permissions"], i["size"], li[1], li[2], str(li[3].split(":")[0])+":"+str(li[3].split(":")[1]), i["name"]])
        elif "/" in path:
            path_li = path.split("/")
            if i["name"] == path_li[0]:
                if "contents" in i.keys():
                    if len(i["contents"]) != 0:
                        for j in i["contents"]:
                            if j["name"] == path_li[1]:
                                li = time.ctime(j["time_modified"]).split(" ")
                                li1.append([j["permissions"], j["size"], li[1], li[2], str(li[3].split(":")[0])+":"+str(li[3].split(":")[1]), "./"+i["name"]+"/"+j["name"]])

    # print(path)
    if len(li1) == 0:
        print('error: cannot access "{}": No such file or directory'.format(path))
    return li1


def replace_all(text):
    lis = ["-", "__", "="]
    for i in lis:
        text = text.replace(i, "_")
    return text


if __name__ == "__main__":
    data = read_json("structure.json")
    try:
        if len(sys.argv) == 1:
            ls_cmd(data, "")
        elif len(sys.argv) == 2:
            ls_cmd(data, sys.argv[1])
        else:
            ls_cmd(data, sys.argv[1:len(sys.argv)])

    except Exception as e:
        print(e)
