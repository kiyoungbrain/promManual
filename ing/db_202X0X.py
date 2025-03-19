
import os
import mysql.connector
import pandas as pd
import re
from sqlalchemy import create_engine, MetaData, Table
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# .env 파일에서 202402 수정할것
# .env 파일에서 202402 수정할것
# .env 파일에서 202402 수정할것
# .env 파일에서 202402 수정할것
# .env 파일에서 202402 수정할것
class feeClass:
    def __init__(self, YM, BRAND, use_gcp=False):
        self.YM = YM
        self.BRAND = BRAND

        # GCP 서버
        if use_gcp:
            self.mysql_username = os.getenv('GCP_MYSQL_USERNAME')
            self.mysql_password = os.getenv('GCP_MYSQL_PASSWORD')
            self.mysql_host = os.getenv('GCP_MYSQL_HOST')
            self.mysql_db = os.getenv('GCP_MYSQL_DB')
        else:
            # 내부 서버
            self.mysql_username = os.getenv('MYSQL_USERNAME')
            self.mysql_password = os.getenv('MYSQL_PASSWORD')
            self.mysql_host = os.getenv('MYSQL_HOST')
            self.mysql_db = os.getenv('MYSQL_DB')


    def baemin_almost(self, WHERE):

        #떡참_11월~12월_배민_내역(기획전(통합_5주)).xlsx
        #떡참_12월_배민_내역(FR첫주문할인).xlsx
        #떡참_12월_배민_내역(VIP월간쿠폰북).xlsx
        #떡참_12월_배민_내역(기획전(통합_1주)).xlsx
        #떡참_12월_배민_내역(기획전(통합_3주)).xlsx
        #떡참_12월_배민_내역(브랜드관).xlsx
        #떡참_12월_배민_내역(브랜드찜).xlsx
        #떡참_12월_배민_내역(키워드쿠폰).xlsx
        #떡참_12월_배민_정산_매장별.xlsx

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'baemin_almost' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f'{self.BRAND}_파일없음 패스'
            return

        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if 'summary' not in sheet.lower()]
            return filtered_sheets

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                all_dfs.append(df)



        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_baemin'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'baemin_almost' SUCCESS")

    def baemin_menuHalin(self, WHERE):

        #떡참_11월~12월_배민_내역(메뉴할인).xlsx

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}/메뉴할인'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'baemin_menuHalin' NONE")
            return

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f"{self.BRAND}_파일없음 패스"
            return


        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if 'summary' not in sheet.lower()]
            return filtered_sheets

        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "") for col in df.columns]
            return df

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                df = clean_headers(df)  # Clean headers
                all_dfs.append(df)

        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_baemin_menuhalin'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM
        combined_df['메뉴할인'] = '메뉴할인'

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'baemin_menuHalin' SUCCESS")

    def bamin_etc(self, WHERE):

        #두찜1월배민선물하기 상품권 정산내역.xlsx
        #두찜1월배민쇼핑라이브 상품권 정산내역.xlsx

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}/기타'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'bamin_etc' NONE")
            return

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f"{self.BRAND}_파일없음 패스"
            return

        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if 'summary' not in sheet.lower()]
            return filtered_sheets

        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "") for col in df.columns]
            return df

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                df = clean_headers(df)  # Clean headers
                all_dfs.append(df)

        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_bamin_etc'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM
        combined_df['이벤트구분'] = combined_df['계약채널']

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'bamin_etc' SUCCESS")

    def coupang_main(self, WHERE):

        #떡참_12월_쿠팡이츠_내역_쿠폰3000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰4000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰6000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰11000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰14000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰15000.xlsx
        #떡참_12월_쿠팡이츠_내역_쿠폰888888.xlsx // 취소

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'coupang_main' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f"{self.BRAND}_'coupang_main' NONE"
            return

        # Function to filter sheets that contain '정리' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if '전체' in sheet]
            return filtered_sheets

        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "") for col in df.columns]
            return df

        # Read only sheets with name '정리' from Excel files and append dataframes including header row
        for file in excel_files:
            all_dfs = []
            file_path = os.path.join(directory, file)
            coupon_value = re.search(r'쿠폰(\d+)', file_path).group(1)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                df = clean_headers(df)  # Clean headers
                all_dfs.append(df)


            # Define MySQL connection
            mysql_username = self.mysql_username
            mysql_password = self.mysql_password
            mysql_host = self.mysql_host
            mysql_db = self.mysql_db
            mysql_table = 'prom_coupang'

            # Create SQLAlchemy Engine
            engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

            # Read Excel files and concatenate dataframes (without 'id' column from Excel)
            combined_df = pd.concat(all_dfs, ignore_index=True)
            combined_df['쿠폰'] = coupon_value
            combined_df['YM'] = self.YM
            combined_df['brand'] = self.BRAND
            combined_df['메뉴할인'] = '쿠팡이츠'
            combined_df['사업자등록번호'] = ''

            # Remove commas from all columns
            for column in combined_df.columns:
                combined_df[column] = combined_df[column].replace(',', '', regex=True)

            # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
            combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'coupang_main' SUCCESS")

    def coupang_main_etc(self, WHERE):

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'coupang_main_etc' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f"{self.BRAND}_'coupang_main_etc' NONE"
            return

        # Function to filter sheets that contain '정리' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if '정리' in sheet]
            return filtered_sheets

        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "").replace(" ", "") for col in df.columns]
            return df

        def replace_dash(value):
            if pd.notna(value):
                return str(value).replace('-', '')
            return value

        # Read only sheets with name '정리' from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet, dtype={'사업자등록번호': str})  # Including header row by default
                df = clean_headers(df)  # Clean headers
                # Select only '스토어ID' and '사업자등록번호' columns
                selected_columns = ['스토어ID', '사업자등록번호']
                df = df[selected_columns]
                df['사업자등록번호'] = df['사업자등록번호'].apply(replace_dash)
                # Drop rows where '스토어ID' is NaN
                df = df.dropna(subset=['사업자등록번호'])
                all_dfs.append(df)


        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_coupang_etc'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'coupang_main_etc' SUCCESS")


    @classmethod
    def coupang_join(cls):
        # ✅ 클래스 변수에 접근할 때 cls 사용
        conn = mysql.connector.connect(
            user=cls.mysql_username,
            password=cls.mysql_password,
            host=cls.mysql_host,
            database=cls.mysql_db
        )
        cursor = conn.cursor()

        # Update prom_coupang based on prom_coupang_etc
        update_query = """
        UPDATE prom_coupang
        JOIN prom_coupang_etc ON prom_coupang.storeid = prom_coupang_etc.스토어ID
        SET prom_coupang.사업자등록번호 = prom_coupang_etc.사업자등록번호;
        """
        cursor.execute(update_query)

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print("SQL queries executed successfully.")



    def yogiyo(self, WHERE):

        #202401_INVOICE_379.xlsx
        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'yogiyo' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            print(f'{self.BRAND}_파일없음 패스')
            return

        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if 'raw data' in sheet.lower()]
            return filtered_sheets


        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "").replace(":", "").replace("+", "").replace(" ", "") for col in df.columns]
            return df

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                df = clean_headers(df)  # Clean headers
                all_dfs.append(df)

        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_yogiyo'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'yogiyo' SUCCESS")

    def ttaeng(self, WHERE):

        #202401_INVOICE_379.xlsx
        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'ttaeng' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            print(f'{self.BRAND}_파일없음 패스')
            return

        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if '프로모션' in sheet.lower()]
            return filtered_sheets


        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "").replace(":", "").replace("+", "").replace(" ", "") for col in df.columns]
            return df

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet, header=None)  # Including header row by default

                #사업자번호로 시작하는 헤더의 테이블 들고오기(땡겨요)
                header_row_index = None
                for index, row in df.iterrows():
                    if '사업자번호' in row.values:
                        header_row_index = index
                        break

                # Check if header row index is found
                if header_row_index is not None:
                    # Read the Excel file again with proper header and skip rows up to the header row
                    df = pd.read_excel(file_path, header=header_row_index)

                    # Check if the first column is unnamed
                    if df.columns[0].startswith('Unnamed'):
                        # Drop the first column
                        df.drop(df.columns[0], axis=1, inplace=True)

                df = clean_headers(df)  # Clean headers
                all_dfs.append(df)

        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_ttaeng'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM
        combined_df['거래일시'] = pd.to_datetime(combined_df['거래일시'], format='%Y%m%d %H:%M:%S')

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].astype(str).str.replace(',', '')
            combined_df[column] = combined_df[column].str.replace('(', '').str.replace(')', '')

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'ttaeng' SUCCESS")


    def tkgb(self, WHERE):

        #떡참_11월~12월_배민_내역(기획전(통합_5주)).xlsx
        #떡참_12월_배민_내역(FR첫주문할인).xlsx
        #떡참_12월_배민_내역(VIP월간쿠폰북).xlsx
        #떡참_12월_배민_내역(기획전(통합_1주)).xlsx
        #떡참_12월_배민_내역(기획전(통합_3주)).xlsx
        #떡참_12월_배민_내역(브랜드관).xlsx
        #떡참_12월_배민_내역(브랜드찜).xlsx
        #떡참_12월_배민_내역(키워드쿠폰).xlsx
        #떡참_12월_배민_정산_매장별.xlsx

        # Directory path containing Excel files
        directory = f'./{self.YM}/{self.BRAND}/{WHERE}'

        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'tkgb' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f'{self.BRAND}_파일없음 패스'
            return

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            # 첫 번째 시트만 읽음
            df = pd.read_excel(file_path, sheet_name=0)  # sheet_name=0은 첫 번째 시트를 의미
            all_dfs.append(df)



        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = 'prom_tkgb'

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df['brand'] = self.BRAND
        combined_df['YM'] = self.YM

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].replace(',', '', regex=True)

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"{self.BRAND}_'tkgb' SUCCESS")

    #ect. 과거 취소 내역 계산
    def past_cancel(self, sheetName, tableName):
        # Directory path containing Excel files
        directory = f'./{self.YM}/과거취소/'
        # Get all files in the directory
        try:
            files = os.listdir(directory)
        except:
            print(f"{self.BRAND}_'ttaeng' NONE")

        # Filter only Excel files
        excel_files = [file for file in files if file.endswith('.xlsx')]
        if len(excel_files) == 0:
            f'{self.BRAND}_파일없음 패스'
            return
        # Function to filter sheets that do not contain 'summary' in their names
        def filter_sheets(excel_file):
            file_path = os.path.join(directory, excel_file)
            excel_sheets = pd.ExcelFile(file_path).sheet_names
            filtered_sheets = [sheet for sheet in excel_sheets if sheetName in sheet.lower()]
            return filtered_sheets

        # Function to clean headers (remove parentheses)
        def clean_headers(df):
            df.columns = [col.replace(")", "").replace("(", "").replace(":", "").replace("+", "").replace(" ", "") for col in df.columns]
            return df

        # Read specific sheets from Excel files and append dataframes including header row
        all_dfs = []
        for file in excel_files:
            file_path = os.path.join(directory, file)
            sheets_to_read = filter_sheets(file)
            for sheet in sheets_to_read:
                df = pd.read_excel(file_path, sheet_name=sheet)  # Including header row by default
                all_dfs.append(df)
        df = clean_headers(df)  # Clean headers
        print(all_dfs)

        # Define MySQL connection
        mysql_username = self.mysql_username
        mysql_password = self.mysql_password
        mysql_host = self.mysql_host
        mysql_db = self.mysql_db
        mysql_table = tableName

        # Create SQLAlchemy Engine
        engine = create_engine(f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}/{mysql_db}")

        # Read Excel files and concatenate dataframes (without 'id' column from Excel)
        combined_df = pd.concat(all_dfs, ignore_index=True)

        # Remove commas from all columns
        for column in combined_df.columns:
            combined_df[column] = combined_df[column].astype(str).str.replace(',', '')
            combined_df[column] = combined_df[column].str.replace('(', '').str.replace(')', '')

        # Write DataFrame to MySQL table without replacing it, hence maintaining 'id' column
        combined_df.to_sql(mysql_table, con=engine, if_exists='append', index=False)

        print(f"past_cancel_{tableName} SUCCESS")
##Date
Current_YM = os.getenv('Current_YM')
print(f"{Current_YM}_집계시작")


#main #main #main #main #main #main #main #main #main #main #main #main #main #main #main
#main #main #main #main #main #main #main #main #main #main #main #main #main #main #main
#main #main #main #main #main #main #main #main #main #main #main #main #main #main #main

if __name__ == '__main__':

    # ## 과거취소
    # past_cancel = feeClass(Current_YM, '-')
    # # past_cancel.past_cancel(sheetName='4000300020001200', tableName='past_cancel1')
    # past_cancel.past_cancel(sheetName='기타쿠폰', tableName='past_cancel2')

    #내부서버 : Fasle / GCP서버: True
    use_inner = False

    # ## 두찜
    두찜_Class = feeClass(Current_YM, '두찜', use_inner)
    두찜_Class.baemin_almost('baemin')
    두찜_Class.bamin_etc('baemin')
    두찜_Class.baemin_menuHalin('baemin')
    두찜_Class.coupang_main('coupang')
    두찜_Class.coupang_main_etc('coupang')
    두찜_Class.yogiyo('yogiyo')
    두찜_Class.tkgb('tkgb')

    # # ## 떡참
    떡참_Class = feeClass(Current_YM, '떡참', use_inner)
    떡참_Class.baemin_almost('baemin')
    떡참_Class.bamin_etc('baemin')
    떡참_Class.baemin_menuHalin('baemin')
    떡참_Class.coupang_main('coupang')
    떡참_Class.coupang_main_etc('coupang')
    떡참_Class.yogiyo('yogiyo')
    떡참_Class.tkgb('tkgb')


    # # ## 숯불
    숯불_Class = feeClass(Current_YM, '숯불', use_inner)
    숯불_Class.baemin_almost('baemin')
    숯불_Class.bamin_etc('baemin')
    숯불_Class.baemin_menuHalin('baemin')
    숯불_Class.coupang_main('coupang')
    숯불_Class.coupang_main_etc('coupang')
    숯불_Class.yogiyo('yogiyo')
    숯불_Class.tkgb('tkgb')

    # 두찜_Class.ttaeng('ttaeng')
    # 떡참_Class.ttaeng('ttaeng')
    # 숯불_Class.ttaeng('ttaeng')

    # ## join
    feeClass.coupang_join()