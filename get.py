from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sys

#get list phone number
def getphonenumber():
    url = 'https://anonymsms.com'

        # Gửi yêu cầu HTTP đến URL
    page = requests.get(url)

        # Tạo đối tượng BeautifulSoup với parser 'html.parser'
    soup = BeautifulSoup(page.text, 'html.parser')

        # Bây giờ bạn có thể sử dụng đối tượng soup để phân tích cú pháp HTML


    soup.find('table')

    table=soup.find_all('table')[0]

    world_titles = table.find_all('th')

    world_table_titles = [title.text.strip() for title in world_titles]

    df = pd.DataFrame(columns=world_table_titles)

    column_data = table.find_all('tr')

    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]

        length = len(df)
        df.loc[length] = individual_row_data

    numbers = df["Number"].values

    phone_numbers_list = numbers.tolist()
    phone_numbers_cleaned_list = [number.replace('+', '') for number in phone_numbers_list]

        # Convert the list back to a numpy array
    phone_numbers_cleaned_array = np.array(phone_numbers_cleaned_list, dtype=object)


    return phone_numbers_cleaned_array

def scarp():
    root_url = "https://anonymsms.com/number"

    # Khởi tạo DataFrame rỗng để chứa tất cả dữ liệu
    combined_df = pd.DataFrame()

    # Vòng lặp qua các số điện thoại
    for number in getphonenumber():
        full_url = "{}/{}".format(root_url, number)
        print(full_url)

        # Gửi yêu cầu HTTP GET tới URL
        page = requests.get(full_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Tìm bảng đầu tiên trên trang
        table = soup.find_all('table')[0]

        # Lấy tiêu đề cột từ bảng
        world_titles = table.find_all('th')
        world_table_titles = [title.text.strip() for title in world_titles]

        # Thêm cột 'Phone Number' vào đầu danh sách tiêu đề
        world_table_titles.insert(0, 'cell_number')

        # Tạo DataFrame tạm thời cho bảng hiện tại
        df = pd.DataFrame(columns=world_table_titles)

        # Lấy dữ liệu từ các hàng trong bảng
        column_data = table.find_all('tr')
        for row in column_data[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text.strip() for data in row_data]

            # Thêm số điện thoại vào đầu mỗi hàng dữ liệu
            individual_row_data.insert(0, number)

            # Thêm dữ liệu hàng vào DataFrame tạm thời
            length = len(df)
            df.loc[length] = individual_row_data

        # Đổi tên cột thứ 3 thành 'message'
        df.rename(columns={df.columns[2]: 'message'}, inplace=True)

        # Thêm DataFrame tạm thời vào DataFrame chính
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Lưu DataFrame chính vào file CSV
    combined_df.to_csv('sms_data.csv', index=False)
    print("Dữ liệu đã được lưu vào file combined_data.csv")

#scarp()

def scarp_number(phone_number):
    root_url = "https://anonymsms.com/number"
    # Khởi tạo DataFrame rỗng để chứa tất cả dữ liệu
    combined_df = pd.DataFrame()

    # Định dạng URL đầy đủ với số điện thoại
    full_url = "{}/{}".format(root_url, phone_number)
    print(full_url)

    # Gửi yêu cầu HTTP GET tới URL
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Tìm bảng đầu tiên trên trang
    table = soup.find_all('table')[0]

    # Lấy tiêu đề cột từ bảng
    world_titles = table.find_all('th')
    world_table_titles = [title.text.strip() for title in world_titles]

    # Thêm cột 'Phone Number' vào đầu danh sách tiêu đề
    world_table_titles.insert(0, 'cell_number')

    # Tạo DataFrame tạm thời cho bảng hiện tại
    df = pd.DataFrame(columns=world_table_titles)

    column_data = table.find_all('tr')
    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]

        # Thêm số điện thoại vào đầu mỗi hàng dữ liệu
        individual_row_data.insert(0, phone_number)

        # Thêm dữ liệu hàng vào DataFrame tạm thời
        length = len(df)
        df.loc[length] = individual_row_data

    # Đổi tên cột thứ 3 thành 'message'
    if len(df.columns) > 2:
        df.rename(columns={df.columns[2]: 'message'}, inplace=True)

    # Thêm DataFrame tạm thời vào DataFrame chính
    combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Lưu DataFrame chính vào file CSV
    combined_df.to_csv('sms_data.csv', index=False)
    print("Dữ liệu đã được lưu vào file sms.csv")

phone_number = sys.argv[1]
scarp_number(phone_number)