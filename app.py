import streamlit as st
import pandas as pd
import numpy as np

# set to wide mode
st.set_page_config(layout="wide")

st.title('Analisis Input dan Output')


# make sidebar
st.sidebar.title('Masukkan data')
# input data1 using file_uploader
transaksi_sektor = st.sidebar.file_uploader(
    'Upload data transaksi antar sektor', type='xlsx')
# input data2 using file_uploader
input_sektor = st.sidebar.file_uploader(
    'Upload data input total sektor', type='xlsx')
# input data3 using file_uploader
jumlah_tenaga_kerja = st.sidebar.file_uploader(
    'Upload data jumlah tenaga kerja', type='xlsx')

# make 3 tabs, preview data, sektor unggulan, angka penggandaan
tabs1, tabs2, tabs3 = st.tabs(
    ['Preview Data', 'Sektor Unggulan', 'Angka Penggandaan'])
with tabs1:
    st.write('Data Transaksi Antar Sektor')
    if transaksi_sektor is not None:
        df1 = pd.read_excel(transaksi_sektor, index_col=0)
        st.write(df1)
    st.write('Data Input Total Sektor')
    if input_sektor is not None:
        df2 = pd.read_excel(input_sektor)
        st.write(df2)
    st.write('Data Jumlah Tenaga Kerja')
    if jumlah_tenaga_kerja is not None:
        df3 = pd.read_excel(jumlah_tenaga_kerja)
        st.write(df3)

with tabs2:
    st.write("Matriks koefisien input")
    if transaksi_sektor is not None and input_sektor is not None:
        df_A = df1.copy()
        df_A = df_A.div(df2.iloc[0], axis=1)
        df_A
    st.write("Matriks Kebalikan Leontief")
    if transaksi_sektor is not None and input_sektor is not None:
        # create identity matrix
        I = np.identity(len(df_A))
        I = pd.DataFrame(I, df_A.index, df_A.columns)
        # substract df_A with identity matrix
        df_B = I.sub(df_A)
        # create inverse matrix of df_B
        df_B_matrix = df_B.values
        df_B_inverse = pd.DataFrame(np.linalg.inv(
            df_B_matrix), df_B.index, df_B.columns)
        df_B_inverse
    st.write("Total Backward Linkage")
    if transaksi_sektor is not None and input_sektor is not None:
        tbl = df_B_inverse.sum(axis=0)
        # set column name to 'Total Backward Linkage'
        tbl.name = 'Total Backward Linkage'
        tbl = tbl.T
        tbl = tbl.to_frame()
        # get the index rank
        tbl['Rank'] = tbl['Total Backward Linkage'].rank(ascending=False)
        tbl
    st.write("Total Forward Linkage")
    if transaksi_sektor is not None and input_sektor is not None:
        tfl = df_B_inverse.sum(axis=1)
        # set column name to 'Total Forward Linkage'
        tfl.name = 'Total Forward Linkage'
        tfl = tfl.T
        tfl = tfl.to_frame()
        # get the index rank
        tfl['Rank'] = tfl['Total Forward Linkage'].rank(ascending=False)
        tfl
    st.write("Index daya penyebaran")
    if transaksi_sektor is not None and input_sektor is not None:
        # tbl divide by mean of tbl
        tbl = tbl.div(tbl.mean())
        tbl['Rank'] = tbl['Total Backward Linkage'].rank(ascending=False)
        tbl
    st.write("Index derajat kepekaan")
    if transaksi_sektor is not None and input_sektor is not None:
        tfl = tfl.div(tfl.mean())
        tfl['Rank'] = tfl['Total Forward Linkage'].rank(ascending=False)
        tfl
    st.write("Sektor Unggulan")

with tabs3:
    st.write("angka penggandaan output")
    if transaksi_sektor is not None and input_sektor is not None and jumlah_tenaga_kerja is not None:
        # sum of df_B_inverse
        sum_B = df_B_inverse.sum()
        sum_B.name = 'Angka Penggandaan Output'
        sum_B = sum_B.T
        sum_B = sum_B.to_frame()
        sum_B['Rank'] = sum_B['Angka Penggandaan Output'].rank(ascending=False)
        sum_B
    st.write("Angka Pengganda Kesempatan Kerja")
    # df3 divide by sum of df2
    if transaksi_sektor is not None and input_sektor is not None and jumlah_tenaga_kerja is not None:
        df3 = df3.div(df2.sum())
        matriks_tk = df3.values
        dot_tk = np.dot(matriks_tk, df_B_inverse)
        # set column name to columns of df3
        dot_tk = pd.DataFrame(dot_tk, df3.index, df3.columns)
        dot_tk = dot_tk.T
        # set column name to "Angla Penggandaan Kesempatan Kerja"
        dot_tk.columns = ['Angka Penggandaan Kesempatan Kerja']
        dot_tk['Rank'] = dot_tk['Angka Penggandaan Kesempatan Kerja'].rank(
            ascending=False)
        dot_tk['100 kali'] = dot_tk['Angka Penggandaan Kesempatan Kerja']*100
        dot_tk['1000 kali'] = dot_tk['Angka Penggandaan Kesempatan Kerja']*1000
        dot_tk
