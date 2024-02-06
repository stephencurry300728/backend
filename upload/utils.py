from datetime import timedelta
import pandas as pd

# 定义解析时间的函数来处理csv中的时间字段以存储到数据库中的DurationField字段
'''
时间持续字段 DurationField 是通过整数来存储时间跨度的，这个整数表示总的微秒数
例如，01:38.5（即1分钟38.5秒）被转换为 timedelta 对象后存储为 98500000 微秒
例如，00:03.4（即3.4秒）被转换为 timedelta 对象后存储为 3400000 微秒
'''
def parse_duration(time_str):
    if pd.isna(time_str) or time_str == '':
        return None  # 处理空值或缺失值
    try:
        parts = time_str.split(':')
        minutes = int(parts[0]) if parts[0] else 0
        seconds = float(parts[1]) if len(parts) > 1 else 0
        return timedelta(minutes=minutes, seconds=seconds)
    except (ValueError, IndexError) as e:
        print(f"解析错误: {e}")  # 打印解析错误
        return None  # 处理无法解析的值