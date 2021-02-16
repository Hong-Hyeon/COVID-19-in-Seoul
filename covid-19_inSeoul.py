import pandas as pd
import requests
import time
import re
import numpy as np
import matplotlib.pyplot as plt

from tqdm import trange

def data_crawl(page_num):
    start_num = (page_num - 1) * 100

    url = 'https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax.php?draw={}'.format(page_num)
    url = "{}&start={}&length=100".format(url, start_num)

    response = requests.get(url)
    data_json = response.json()
    total_page = (data_json['recordsTotal'] // 100) + 1
    return data_json, total_page

def get_page_list(start_page):
    _, total_page = data_crawl(1)
    print(type(total_page))
    page_list = []

    for page_num in trange(start_page,total_page+1):
        one_page,_ = data_crawl(page_num)
        # print(one_page)
        if len(one_page['data']) > 0: # 데이터가 있는 경우에는
            one_page = pd.DataFrame(one_page['data'])
            page_list.append(one_page)
            # 서버에 부담을 줄여주기위해 time.sleep()을 해줌.
            time.sleep(0.5)
        else:
            break

    return page_list

def extract_number(num_str):
    if type(num_str) == str:
        num_str = num_str.replace("corona19","")
        num = re.sub("[^0-9]","",num_str)
        num=int(num)
        return num
    else:
        return num_str

def extract_hangeul(origin_text):
    subtract_text = re.sub("[^가-힣]","",origin_text)
    return subtract_text

def data_prepro(Dataframe):
    Dataframe["연번"] = Dataframe["연번"].map(extract_number)
    Dataframe["퇴원현황"] = Dataframe["퇴원현황"].map(extract_hangeul)
    last_date = Dataframe.iloc[0]["확진일"]
    last_date.replace(".","_")

    return Dataframe

def save_csv(Dataframe):
    filename = './data/covid-19_data.csv'
    Dataframe.to_csv(filename, index=False, encoding='euckr')
    return filename

def load_data(filename):
    df = pd.read_csv(filename, encoding='euckr')
    return df

def data_check(Dataframe):
    print("shape of the Dataframe : {}".format(Dataframe.shape), end='\n\n')
    print("reverse order by number\n")
    print(Dataframe.sort_values(by='연번', ascending=False))
    while True:
        choice_num = int(input("Check data_Enter the number\n(1: head, 2: tail, 3: pass)"))
        if choice_num == 3:
            return True
        elif choice_num == 1:
            print("Data head\n")
            print(Dataframe.head())
        elif choice_num == 2:
            print("Data tail\n")
            print(Dataframe.tail())
        else:
            print("You entered the wrong number.")

if __name__ == '__main__':
    df = pd.concat(get_page_list(start_page=1))
    cols = ['연번','환자','확진일','거주지','여행력','접촉력','퇴원현황']
    df.columns = cols
    
    df = load_data(filename=save_csv(Dataframe=data_prepro(Dataframe=df)))

    if data_check(Dataframe=df) is True:
        plot_check = int(input("Do you want to visualize the data?(1 : Yes, 2: No)"))
        if plot_check == 2:
            print("Exit the program.\nGood Bye.")
        elif plot_check == 1:
            while True:
                check_num = int(input('''check number(1:확진자 수,2:확진자 누적,3:월별확진자 추이) : '''))
                if check_num == 2:
                    df["확진일"] = pd.to_datetime(df["확진일"])
                    fig = plt.figure(figsize=(15,4))
                    plt.plot(df["확진일"].value_counts().sort_index().cumsum())
                    plt.show(block=True)
                elif check_num == 1:
                    df["확진일"] = pd.to_datetime(df["확진일"])
                    fig = plt.figure(figsize=(15, 4))
                    plt.plot(df["확진일"].value_counts().sort_index())
                    plt.axhline(400, color='red', linestyle=':')
                    plt.show(block=True)
                elif check_num ==3:
                    df["확진일"] = pd.to_datetime(df["확진일"])
                    df["월"] = df["확진일"].dt.month
                    month_case = df['월'].value_counts().sort_index()
                    labels = ['1','2','11','12']
                    fig = plt.figure(figsize=(8,8))
                    g = plt.bar(labels,month_case)
                    plt.show(block=True)

        else:
            print("You entered the wrong n  umber.")
            print("Exit the program.\nGood Bye.")
