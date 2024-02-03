from datetime import timedelta
import pandas as pd
from .models import Assessment_09A02, Assessment_09A0304, Assessment_10A01, Assessment_10A02

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

# 反向操作，将数据库中的DurationField字段的值转换为字符串转递给前端 
'''
# 这里假设 duration 是数据库中的一个DurationField字段所存储的值
duration = timedelta(microseconds=98500000)
formatted_str = format_duration(duration)
print(formatted_str)  # 输出: 1:38.5
'''
def format_duration(duration):
    if duration is None:
        return None

    # 将总微秒数转换为秒数
    total_seconds = duration.total_seconds()
    # 计算分钟和秒
    minutes, seconds = divmod(total_seconds, 60)
    # 格式化输出
    return f"{int(minutes)}:{seconds:04.1f}"

# 从列中获取对应的值
def get_model_class_for_train_model(train_model):
    """
    根据车型字符串返回相应的Django模型类。
    """
    model_mapping = {
        '09A02': Assessment_09A02,
        '09A03': Assessment_09A0304,
        '09A04': Assessment_09A0304,
        '10A01': Assessment_10A01,
        '10A02': Assessment_10A02,
    }
    return model_mapping.get(train_model, None)
