import pandas as pd
import requests
import time
import re

from tqdm import trange
from utils_.plot_util_ import plot_

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
    # print(df.shape)
    # print(df.sort_values(by='연번', ascending=False))

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
                x_data = input("input x_data. Choose one.\n[연번, 환자, 확진일, 거주지, 여행력, 접촉력, 퇴원현황]\nWhat would you put in?")
                y_data = input("input y_data. Choose one.\n[연번, 환자, 확진일, 거주지, 여행력, 접촉력, 퇴원현황]\nWhat would you put in?")
                if x_data == y_data:
                    print("The same value was entered.\nTry again.\n\n")
                    continue
                plot = plot_(x_data=df[x_data], y_data=df[y_data])
                num = int(input("Which graph should I draw?\n\n(1 : plot, 2 : histogram, 3 : exit the program)"))
                if num == 1:
                    plot.subplot_(make_plot=1)
                elif num == 2:
                    title = input("Please enter a title : ")
                    x_label = input("Please enter a x_label : ")
                    y_label = input("Please enter a y_label : ")
                    bins = int(input("Please enter a bins : "))
                    plot.histogram_(title=title, x_label=x_label,
                                     y_label=y_label, bins=bins)
                elif num == 3:
                    print("Exit the program.\nGood Bye.")
                    break
                else:
                    print("You entered the wrong number.")
                    continue
                check = int(input("Do you want to try again?(1:Yes)"))
                if check == 1:
                    continue
                else:
                    print("Exit the program.\nGood Bye.")
                    break
        else:
            print("You entered the wrong number.")
            print("Exit the program.\nGood Bye.")
