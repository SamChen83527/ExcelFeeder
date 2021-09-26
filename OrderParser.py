import pandas as pd


def isValidOrder(df, i):
    if pd.isna(df.at[i, "連絡人姓名"]) and pd.isna(df.at[i, "電話號碼"]):
        return False
    return True


if __name__ == "__main__":
    df = pd.read_excel("./data/阿萬師的床墊89.xlsx", sheet_name='阿萬師')
    # # 轉成 numpy.ndarray 格式
    # nmp=df.values

    length = len(df)
    for i in range(0, length):
        if isValidOrder(df, i):
            print(int(df.at[i, "貨單編號"]), df.at[i, "連絡人姓名"])
