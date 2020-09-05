import pandas as pd
from sqlalchemy import create_engine

def db():
    host     = 'localhost'
    user     = 'system'
    passwd   = 'H5cT7yHB8_'
    port     = 3306
    charset  = 'utf8mb4'
    database = 'data_quality'
    
    engine = create_engine(
        f'mysql+mysqldb://{user}:{passwd}@{host}:{port}/{database}?charset={charset}',
        echo=False,				# 打印sql语句
        max_overflow=0,  		# 超过连接池大小外最多创建的连接
        pool_size=5,  			# 连接池大小
        pool_timeout=30,  		# 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1, 		# 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    return engine


def generateData(startDate=None, endDate=None):
    d = {'date':pd.date_range(start=startDate, end=endDate)}
    data = pd.DataFrame(d)
    data['day_id'] = data['date'].astype(str).str.replace('-', '').astype('int32')
    data['year'] = data['date'].apply(lambda x:x.year).astype('int32')
    data['month'] = data['date'].apply(lambda x:x.month).astype('int32')
    data['day'] = data['date'].apply(lambda x:x.day).astype('int32')
    data['quarter'] = data['date'].apply(lambda x:x.quarter).astype('int32')
    data['day_name'] = data['date'].apply(lambda x:x.day_name())
    data['weekofyear'] = data['date'].apply(lambda x:x.weekofyear)
    data['dayofyear'] = data['date'].apply(lambda x:x.dayofyear).astype('int32')
    data['daysinmonth'] = data['date'].apply(lambda x:x.daysinmonth).astype('int32')
    data['dayofweek'] = data['date'].apply(lambda x:x.dayofweek).astype('int32')
    data['is_leap_year'] = data['date'].apply(lambda x:x.is_leap_year)
    data['is_month_end'] = data['date'].apply(lambda x:x.is_month_end)
    data['is_month_start'] = data['date'].apply(lambda x:x.is_month_start)
    data['is_quarter_end'] = data['date'].apply(lambda x:x.is_quarter_end)
    data['is_quarter_start'] = data['date'].apply(lambda x:x.is_quarter_start)
    data['is_year_end'] = data['date'].apply(lambda x:x.is_year_end)
    data['is_year_start'] = data['date'].apply(lambda x:x.is_year_start)
    return data

data = generateData(startDate='2019-1-01', endDate='2029-12-31')

# data.to_csv('/tmp/dim_date.csv', index = False,index_label = False)

conn = db()
# 插入到mysql中，pandas的bool类型会转换为tinyint(1)类型，0表示False，1表示True
data.to_sql('dim_date', con=conn, if_exists='replace', index=False)