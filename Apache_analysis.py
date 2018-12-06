import re
import csv
import glob
import argparse
import datetime
from collections import Counter
import matplotlib.pyplot as plt


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument\
        (
            "file_name",  #分析したいファイルの指定
            help=
            "Please set the file name you want analyze.\
            In the case of needing analysis multiple files, \
            please set common file name and add '*' after it's.",
        )
    parser.add_argument\
        (
            "--s_term",  #期間指定における開始日の指定(任意)
            help="Please set the start year/month/day of the period you want analyze."
        )
    parser.add_argument\
        (
            "--e_term",  #期間指定における終了日の指定(任意)
            help="Please set the end year/month/day of the period you want analyze."
        )
    parser.add_argument\
        (
            "--output_name",  #出力csvファイル名の指定
            help="Please set the csv file name(the part is before '.csv') be outputted as a analysis result"
        )
    return parser.parse_args()


#アクセスログを形式をキーとする辞書へ変換する関数。形式は変更可
def into_dict(line, key=['%h', '%l', '%u', '%t', '%r', '%>s', '%b', '%{Referer}i', '%{User-Agent}i']):
    line = re.split('([]["])', line)  #時間、リクエストの最初の行、サーバが受信したUser-Agentだけ分割
    val, frag = [], True
    for s in line:
        if (s == '[' or s == '"') and frag: frag = False
        elif (s == ']' or s == '"') and not frag: frag = True
        else: val.extend(s.split()) if frag else val.append(s)  #残りの項目も分割しvalに格納
    return dict(zip(key, val)) if len(key) == len(val) else False


#アクセスユーザーを集計している辞書の更新関数
def update_dict(dict1, val, k):
    dict2 = {val: k}
    return Counter(dict1) + Counter(dict2)  #すでに集計されたことのあるユーザーの場合はvalueに加算する


#指定された期間にアクセス時間が含まれているかを判定する関数
def check_in_term(s_term, e_term, t):
    calc_days = lambda x: x[0] * 365 + x[1] * 12 + x[2]  #年/月/日を日変換
    return calc_days(s_term) <= calc_days(t) <= calc_days(e_term)


def main():
    arg = get_args()

    s_term = list(map(lambda x: int(x), re.split('/', arg.s_term))) if arg.s_term else [0, 0, 0]
    e_term = list(map(lambda x: int(x), re.split('/', arg.e_term))) if arg.e_term else [9999, 0, 0]  #期間の設定
    time_checker = lambda x: check_in_term(s_term, e_term, x)

    path = "C:\\var\\log\\httpd\\"
    dct, remote_host_dict, hour = {}, {}, [0] * 24
    mouth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
             'Oct': 10, 'Nov': 11, 'Dec': 12}

    #pathディレクトリ内のfile_nameを含むようなテキストファイルを走査
    for file_dir in glob.glob(path + arg.file_name):
        with open(file_dir) as file:
            for log_line in file:
                dct = into_dict(log_line)  #アクセスログ→辞書
                if not dct:#設定形式とかとなるかを判定
                    print(log_line, '\n上のアクセスログは設定された形式と一致しません')
                    break
                times = re.split('[/:]', dct['%t'])
                t = (int(times[2]), mouth[times[1]], int(times[0]))
                if time_checker(t[:3]):  #指定期間内かの判定
                    hour[int(times[3])] += 1
                    remote_host_dict = update_dict(remote_host_dict, dct['%h'], 1)

    #アクセスユーザーの集計結果をcsvファイルで出力
    result_name = arg.output_name + '.csv' if arg.output_name else "result_{0:%Y%m%d-%H%M%S}.csv".format(datetime.datetime.now())
    header = ['host', 'times']
    with open(result_name, 'w') as file:
        writer = csv.writer(file)  # writerオブジェクトを作成
        writer.writerow(header)  # ヘッダーを書き込む
        writer.writerows(remote_host_dict.most_common())  # 内容を書き込む

    #アクセス時刻の集計結果は棒グラフで出力
    plt.bar(range(0, 24), hour, tick_label=range(0, 24), align="center")
    plt.xlabel("time")
    plt.ylabel("frequency")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()

