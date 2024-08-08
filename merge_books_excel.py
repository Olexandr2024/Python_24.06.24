import pandas as pd

# Функция для очистки текста от точек, дефисов и пробелов
def clean_text(text):
    return str(text).replace('.', '').replace('-', '').replace(' ', '').lower()

# Загрузка данных из Листа1 и Листа2
file_path = 'D:\Учеба ИТ\Python_24.06.24\path_to_your_excel_file.xlsx'  # Укажите путь к вашему файлу Excel
sheet1 = 'Лист1'
sheet2 = 'Лист2'

df1 = pd.read_excel(file_path, sheet_name=sheet1)
df2 = pd.read_excel(file_path, sheet_name=sheet2)

# Проверка названий столбцов
print("Названия столбцов в Лист1:", df1.columns)
print("Названия столбцов в Лист2:", df2.columns)

# Используем названия столбцов "A" и "B"
column_name = 'A'

# Очистка названий книг
df1['cleaned_title'] = df1[column_name].apply(clean_text)
df2['cleaned_title'] = df2[column_name].apply(clean_text)

# Объединение данных на основе очищенных названий
merged_df = pd.merge(df1, df2[['cleaned_title', 'B']], on='cleaned_title', how='left')

# Переименование столбца B в B_y, чтобы избежать конфликта имен
merged_df.rename(columns={'B': 'B_y'}, inplace=True)

# Запись результата обратно в Лист1
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    merged_df[[column_name, 'B_y']].to_excel(writer, sheet_name=sheet1, index=False, header=False, startcol=0, startrow=0)

# Переименование столбца B_y обратно в B для сохранения результата в новом файле
merged_df.rename(columns={'B_y': 'B'}, inplace=True)

# Запись результата в новый файл
merged_df.to_excel('result.xlsx', index=False, columns=[column_name, 'B'])
