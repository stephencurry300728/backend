import io
import re
from datetime import datetime

import pandas as pd
from django.db import models, transaction
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Assessment_Base, Assessment_09A02, Assessment_09A0304, Assessment_10A01, Assessment_10A02, NewUser
from .serializers import Assessment09A02Serializer, Assessment09A0304Serializer, Assessment10A01Serializer, Assessment10A02Serializer, AssessmentBaseSerializer
from .utils import get_model_class_for_train_model, parse_duration

# Create your views here.
# 定义分页规则
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

# 驾驶员基本信息筛选排序视图
class AssessmentBaseViewSet(viewsets.ModelViewSet):
    queryset = Assessment_Base.objects.all()
    serializer_class = AssessmentBaseSerializer
    pagination_class = StandardResultsSetPagination
    # 添加OrderingFilter到过滤后端
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    # 允许排序的字段
    ordering_fields = '__all__'  # 允许所有字段可以排序
    ordering = ['record_date']  # 默认按照记录日期升序排列
    
    # 获取所有不重复的 train_model 和 assessment_item 组合，为前端的 科目 提供选项框
    @action(detail=False, methods=['get'], url_path='all-train-and-assessment')
    def all_train_and_assessment_items(self, request, *args, **kwargs):
        # 使用 Django 的 .values() 和 .distinct() 来获取所有不重复的 train_model 和 assessment_item 组合
        queryset = self.get_queryset().values('train_model', 'assessment_item').distinct()

        # 使用 set 来存储唯一的组合
        unique_combinations = set()

        # 遍历查询集，为每个组合创建一个唯一的字符串标识符，然后添加到 set 中
        for item in queryset:
            combination = f"{item['train_model']}-{item['assessment_item']}"
            unique_combinations.add(combination)

        # 将 set 转换回列表形式的数据，分别返回 train_model 和 assessment_item 字段
        result = []
        for combination in unique_combinations:
            train_model, assessment_item = combination.split('-', 1)
            result.append({"train_model": train_model, "assessment_item": assessment_item})

        return Response(result)
    
    # 重写 get_queryset 方法，以便根据日期范围筛选查询集
    def get_queryset(self):
        queryset = super().get_queryset()  # 获取默认查询集
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        train_model = self.request.query_params.get('train_model')
        assessment_item = self.request.query_params.get('assessment_item')

        # 根据日期范围筛选查询集
        if start_date and end_date:
            # 如果有开始日期和结束日期，则筛选在这两个日期范围内的记录
            queryset = queryset.filter(record_date__range=[start_date, end_date])
        elif start_date:
            # 如果只有开始日期，则筛选大于等于开始日期的记录
            queryset = queryset.filter(record_date__gte=start_date)
        elif end_date:
            # 如果只有结束日期，则筛选小于等于结束日期的记录
            queryset = queryset.filter(record_date__lte=end_date)
            
        # 根据 train_model 和 assessment_item 过滤数据
        if train_model:
            queryset = queryset.filter(train_model=train_model)
        if assessment_item:
            queryset = queryset.filter(assessment_item=assessment_item)
            
        return queryset

# 驾驶员详细信息视图
class Assessment09A02ViewSet(viewsets.ModelViewSet):
    queryset = Assessment_09A02.objects.all()
    serializer_class = Assessment09A02Serializer
    pagination_class = StandardResultsSetPagination

class Assessment09A0304ViewSet(viewsets.ModelViewSet):
    queryset = Assessment_09A0304.objects.all()
    serializer_class = Assessment09A0304Serializer
    pagination_class = StandardResultsSetPagination

class Assessment10A01ViewSet(viewsets.ModelViewSet):
    queryset = Assessment_10A01.objects.all()
    serializer_class = Assessment10A01Serializer
    pagination_class = StandardResultsSetPagination

class Assessment10A02ViewSet(viewsets.ModelViewSet):
    queryset = Assessment_10A02.objects.all()
    serializer_class = Assessment10A02Serializer
    pagination_class = StandardResultsSetPagination
    

# 获取当前登录用户信息
class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        # 由于已经登录了，所以request.user肯定是有值的，访问当前登录的用户的id
        user_info = NewUser.objects.filter(id=request.user.id).values().first()

        if user_info:
            role = request.user.roles
            user_info['roles'] = 'admin' if role == 0 else 'user'
            return Response(user_info)
        else:
            return Response({'error': 'User not found.'}, status=404)

# 定义用户登出视图        
class LogoutView(APIView):

    def post(self, request):
        try:
            # 从请求中获取refresh_token
            refresh_token = request.data.get("refresh_token")
            # 如果refresh_token存在，就将其加入黑名单
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # 黑名单化 refresh_token
            # 返回205状态码
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as error:
            # 如果出错，打印错误信息
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 定义文件上传视图
class AssessmentUploadView(APIView):
    '''
    Parses multipart HTML form content, which supports file uploads. 
    request.data and request.FILES will be populated with a QueryDict and MultiValueDict respectively.
    You will typically use both FormParser and MultiPartParser together in order to fully support HTML form data.
    '''
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')

        # 遍历上传的批量文件
        for file_obj in files:
            try:
                # 使用事务处理，以便在处理文件时发生错误时可以回滚
                with transaction.atomic():
                    # 获取单个文件名
                    file_name = file_obj.name
                    # 检查并删除同名文件的旧记录（方便重新上传更新新数据后的新文件）
                    Assessment_Base.objects.filter(file_name=file_name).delete()

                    file_content = file_obj.read()
                    df = None
                    '''
                    'latin1' (或 'iso-8859-1')：西欧语言字符集，是很多西欧语言的标准编码。
                    'ascii'：美国标准信息交换码，只能表示基本的英文字符和一些控制字符。
                    'utf-16'：与UTF-8类似，但使用至少16位（2字节）来编码字符，适用于编码较多的字符集。
                    'utf-32'：使用32位（4字节）来编码字符，与UTF-16类似，但更占用空间，用于需要编码非常多字符的情况。
                    'cp1252'：Windows的西欧字符集，与ISO-8859-1类似，但包含了一些在ISO-8859-1中未定义的打印字符。
                    'gb2312'：简体中文字符集，比GBK和GB18030早，但字符数量较少。
                    'big5'：繁体中文字符集，用于台湾、香港等地区的中文编码。
                    '''
                    for encoding in ['utf-8', 'gbk', 'latin1', 'ascii', 'utf-16', 'utf-32', 'cp1252', 'gb2312', 'big5']:
                        try:
                            # 将文件内容解码为字符串，然后使用pandas读取csv文件
                            io_string = io.StringIO(file_content.decode(encoding))
                            # 剔除第一行关于操作的行
                            df = pd.read_csv(io_string, header=1)
                            break
                        except UnicodeDecodeError:
                            continue

                    if df is None:
                        return Response({'detail': f'文件 {file_name} 无法解码，请检查文件编码格式是否是"UTF-8"或"gbk"!'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    # 删除备注这一列
                    if '备注' in df.columns:
                        df = df.drop('备注', axis=1)

                    '''
                    科目的定义：09A02逃生门释放和收回
                    单科目单人重复填写，只保留最后一次的记录
                    通过按照 姓名、工作证编号、车型 和 考核项目 这几个关键字段排序
                    确保任何具有相同姓名、工作证编号、车型和考核项目的重复记录都会被排列在一起
                    先排序确保重复记录紧密排列，然后只保留最后出现的记录，这样做可以有效地处理数据中的重复项
                    '''   
                    df = df.sort_values(by=['姓名', '工作证编号', '车型','考核项目'])  # 确保DataFrame是按照姓名、工作证编号和考核项目排序的
                    df = df.drop_duplicates(subset=['姓名', '工作证编号','车型', '考核项目'], keep='last') # 如果有重复的考核项目记录，只保留排序后的最后一条记录
                    
                    # 遍历文件中的每一行
                    for index, row in df.iterrows():
                        # 尝试将工作证编号转换为整数，然后转换为字符串
                        try:
                            work_certificate_number = str(int(row.get('工作证编号')))
                        # 如果转换失败，则将工作证编号置为空字符串
                        except (ValueError, TypeError):
                            work_certificate_number = ''
                        
                        # 使用正则表达式判断工作证编号
                        if not re.match(r'^\d{5,}$', work_certificate_number):
                            print(f"跳过文件 {file_name} 中的行 {index}: 工作证编号 '{work_certificate_number}' 不是大于四位数的数字")
                            continue  

                        # 如果乘务班组、姓名、工作证编号都为空，则跳过当前行不录入
                        if pd.isna(row.get('乘务班组')) and pd.isna(row.get('姓名')) and (pd.isna(row.get('工作证编号')) or not re.match(r'^\d{5,}$', work_certificate_number)):
                            print(f"跳过文件 {file_name} 中的行 {index}: 乘务班组、姓名、工作证编号都为空")
                            continue  

                        # 对时间型列 日期、记录日期 进行处理
                        record_date_str = str(row.get('记录日期') or row.get('日期'))
                        # 将数据中的 20231110 转换为 2023-11-10
                        record_date = datetime.strptime(record_date_str, '%Y%m%d').date() if record_date_str else None
                        
                        # 考核结果的映射
                        assessment_result_text = row.get('考核结果')
                        assessment_result_mapping = {
                            '优秀': Assessment_Base.EXCELLENT,
                            '合格': Assessment_Base.QUALIFIED,
                            '不合格': Assessment_Base.NOT_QUALIFIED,
                        }
                        assessment_result = assessment_result_mapping.get(assessment_result_text, Assessment_Base.OTHER)                        

                        # 保存基本信息进数据库
                        assessment_base = Assessment_Base(
                            file_name=file_name,
                            record_date=record_date,
                            crew_group=row.get('乘务班组'),
                            name=row.get('姓名'),
                            work_certificate_number=row.get('工作证编号'),
                            train_model=row.get('车型'),
                            assessment_item=row.get('考核项目'),
                            assessment_result=assessment_result, # 使用转换后的整数值
                        )
                        # 保存基本信息
                        assessment_base.save()

                        # 映射不同车型对应的模型类
                        train_model = row.get('车型')
                        # 不同车型对应了不一样的操作字段
                        model_class = get_model_class_for_train_model(train_model)
                        if model_class:
                            duration_data = {}
                            start_col_index = 7  # 假设从第7列开始是DurationField数据
                            duration_field_names = [field.name for field in model_class._meta.fields if isinstance(field, models.DurationField)]
                            for i, field_name in enumerate(duration_field_names):
                                col_index = start_col_index + i
                                if col_index < len(row):
                                    time_str = row.iloc[col_index]
                                    duration_data[field_name] = parse_duration(time_str) if not pd.isna(time_str) else None
                            # 创建对应的车型实例并保存
                            model_instance = model_class.objects.create(assessment_base=assessment_base, **duration_data)
                            model_instance.save()

            except Exception as e:
                return Response({'detail': f'处理文件 {file_name} 时发生错误: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': '所有文件上传成功。'}, status=status.HTTP_201_CREATED)
