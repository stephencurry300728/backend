from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

# 定义用户信息模型
class NewUser(AbstractUser):

    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]

    roles = models.IntegerField(verbose_name="角色",choices=role_type,default=1)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True,auto_now=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name  
        swappable = 'AUTH_USER_MODEL'

# 定义基础考核信息模型
class Assessment_Base(models.Model):
    file_name = models.CharField(max_length=100, null=True, blank=True)
    record_date = models.DateField(verbose_name="日期", null=True, blank=True)
    crew_group = models.CharField(max_length=50, verbose_name="班组", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="姓名", null=True, blank=True)
    work_certificate_number = models.IntegerField(verbose_name="工作证编号", null=True, blank=True)
    train_model = models.CharField(max_length=20, verbose_name="车型", null=True, blank=True)
    assessment_item = models.CharField(max_length=100, verbose_name="考核项目", null=True, blank=True)
    # 考核结果的选择字段
    EXCELLENT = 3
    QUALIFIED = 2
    NOT_QUALIFIED = 1
    OTHER = 0  # 代表其他所有未知的考核结果
    ASSESSMENT_RESULTS = [
        (EXCELLENT, '优秀'),
        (QUALIFIED, '合格'),
        (NOT_QUALIFIED, '不合格'),
        (OTHER, '其他'),  # 允许有一个“其他”选项
    ]
    # 考核结果现在使用IntegerField来存储
    assessment_result = models.IntegerField(
        choices=ASSESSMENT_RESULTS,
        default=OTHER,  # 默认值设置为0，对应于“其他”
        verbose_name="考核结果"
    )

    class Meta:
        verbose_name = "基础考核信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        # 显示车型信息-文件名-姓名
        return f"{self.file_name} - {self.train_model} - {self.name}"
        
    
class Assessment_09A02(models.Model):
    # 一对一关联基础考核信息, 且有级联删除
    # on_delete=models.CASCADE表示删除基础考核信息时，对应的09A02车型的考核信息也会被删除
    # related_name='assessment_09A02'表示通过基础考核信息可以访问到09A02车型的考核信息
    assessment_base = models.OneToOneField(Assessment_Base, on_delete=models.CASCADE, related_name='assessment_09A02')

    # 耗时字段
    total_duration = models.DurationField(verbose_name="整体耗时",null=True,blank=True) # 整体耗时
    emergency_door_release_duration = models.DurationField(verbose_name="逃生门释放耗时",null=True,blank=True) # 逃生门释放耗时

    # 涉及到操作的字段
    unlock_handle_duration = models.DurationField(verbose_name="解锁逃生门红色手柄耗时",null=True,blank=True) # 解锁逃生门红色手柄耗时
    push_door_duration = models.DurationField(verbose_name="向外推逃生门以完全释放耗时",null=True,blank=True) # 向外推逃生门以完全释放耗时
    release_ramp_duration = models.DurationField(verbose_name="放倒底部踏板耗时",null=True,blank=True) # 放倒底部踏板耗时
    retract_ramp_duration = models.DurationField(verbose_name="复位底部踏板耗时",null=True,blank=True) # 复位底部踏板耗时
    get_butterfly_pin_duration = models.DurationField(verbose_name="拿取蝴蝶销耗时",null=True,blank=True) # 拿取蝴蝶销耗时
    install_butterfly_pin_duration = models.DurationField(verbose_name="正确安装蝴蝶销耗时",null=True,blank=True) # 正确安装蝴蝶销耗时
    get_rod_duration = models.DurationField(verbose_name="拿取扭杆耗时",null=True,blank=True) # 拿取扭杆耗时
    retract_window_duration = models.DurationField(verbose_name="使用扭杆收回逃生门至接近垂直耗时",null=True,blank=True) # 使用扭杆收回逃生门至接近垂直耗时
    reset_rod_duration = models.DurationField(verbose_name="复位扭杆耗时",null=True,blank=True) # 复位扭杆耗时
    excape_second_door_lock_duration = models.DurationField(verbose_name="逃生门二级锁闭耗时",null=True,blank=True) # 逃生门二级锁闭耗时
    excape_first_door_lock_duration = models.DurationField(verbose_name="逃生门一级锁闭耗时",null=True,blank=True) # 逃生门一级锁闭耗时
    remove_butterfly_pin_duration = models.DurationField(verbose_name="取下蝴蝶销耗时",null=True,blank=True) # 取下蝴蝶销耗时
    reset_lock_handle_duration = models.DurationField(verbose_name="复位蝴蝶销耗时",null=True,blank=True) # 复位蝴蝶销耗时
    confirm_left_door_duration = models.DurationField(verbose_name="确认左关门灯耗时",null=True,blank=True) # 确认左关门灯耗时
    confirm_HMI_display_duration = models.DurationField(verbose_name="确认HMI逃生门显示耗时",null=True,blank=True) # 确认HMI逃生门显示耗时

    class Meta:
        verbose_name = "09A02车型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.assessment_base.train_model} - {self.assessment_base.name}"
    
class Assessment_09A0304(models.Model):
    # 一对一关联基础考核信息
    assessment_base = models.OneToOneField(Assessment_Base, on_delete=models.CASCADE, related_name='assessment_09A0304')

    # 耗时字段
    total_duration = models.DurationField(verbose_name="整体耗时", null=True, blank=True)  # 整体耗时
    emergency_door_release_duration = models.DurationField(verbose_name="逃生门释放耗时", null=True, blank=True)  # 逃生门释放耗时

    # 涉及到操作的字段
    remove_red_handle_duration = models.DurationField(verbose_name="取下红色手柄保险销耗时", null=True, blank=True)  # 取下红色手柄保险销耗时
    unlock_red_handle_duration = models.DurationField(verbose_name="解锁红色手柄耗时", null=True, blank=True)  # 解锁红色手柄耗时
    push_door_duration = models.DurationField(verbose_name="向外推出逃生门以完全释放耗时", null=True, blank=True)  # 向外推出逃生门以完全释放耗时
    operate_recovery_rope_duration = models.DurationField(verbose_name="操作回收绳固定手柄耗时", null=True, blank=True)  # 操作回收绳固定手柄耗时
    pull_recovery_rope_duration = models.DurationField(verbose_name="向下拉动回收绳使逃生门上端到位耗时", null=True, blank=True)  # 向下拉动回收绳使逃生门上端到位耗时
    lift_recovery_rope_duration = models.DurationField(verbose_name="向上提起回收绳使逃生门关闭到位耗时", null=True, blank=True)  # 向上提起回收绳使逃生门关闭到位耗时
    reset_red_handle_duration = models.DurationField(verbose_name="复位红色手柄耗时", null=True, blank=True)  # 复位红色手柄耗时
    install_red_handle_duration = models.DurationField(verbose_name="安装红色手柄保险销耗时", null=True, blank=True)  # 安装红色手柄保险销耗时
    reset_recovery_rope_duration = models.DurationField(verbose_name="复位回收绳固定手柄耗时", null=True, blank=True)  # 复位回收绳固定手柄耗时
    confirm_HMI_display_duration = models.DurationField(verbose_name="确认HMI逃生门图标显示耗时", null=True, blank=True)  # 确认HMI逃生门图标显示耗时
    
    class Meta:
        verbose_name = "09A0304车型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.assessment_base.train_model} - {self.assessment_base.name}"

class Assessment_10A01(models.Model):
    # 一对一关联基础考核信息
    assessment_base = models.OneToOneField(Assessment_Base, on_delete=models.CASCADE, related_name='assessment_10A01')

    # 耗时字段
    total_duration = models.DurationField(verbose_name="整体耗时", null=True, blank=True)  # 整体耗时
    emergency_door_release_duration = models.DurationField(verbose_name="逃生门释放耗时", null=True, blank=True)  # 逃生门释放耗时
    
    # 涉及到操作的字段
    unlock_escape_door_box = models.DurationField('解锁逃生门箱体解锁把手', null=True, blank=True)  # 解锁逃生门箱体解锁把手
    remove_escape_door_box_cover = models.DurationField('取下逃生门箱体上盖板', null=True, blank=True)  # 取下逃生门箱体上盖板
    unlock_escape_door_window = models.DurationField('解锁逃生门窗体解锁把手', null=True, blank=True)  # 解锁逃生门窗体解锁把手
    push_escape_door_window = models.DurationField('向外推出逃生门窗体', null=True, blank=True)  # 向外推出逃生门窗体
    release_escape_door_slope = models.DurationField('完全释放逃生门坡道', null=True, blank=True)  # 完全释放逃生门坡道
    retract_escape_door_slope = models.DurationField('完全收回逃生门坡道', null=True, blank=True)  # 完全收回逃生门坡道
    retract_escape_door_window = models.DurationField('收回逃生门窗体', null=True, blank=True)  # 收回逃生门窗体
    reset_escape_door_window_push_rod = models.DurationField('复位逃生门窗体推杆', null=True, blank=True)  # 复位逃生门窗体推杆
    reset_escape_door_window_unlock_handle = models.DurationField('复位逃生门窗体解锁把手', null=True, blank=True)  # 复位逃生门窗体解锁把手
    install_escape_door_box_cover = models.DurationField('安装逃生门箱体上盖板', null=True, blank=True)  # 安装逃生门箱体上盖板
    reset_escape_door_box_unlock_handle = models.DurationField('复位逃生门箱体解锁把手', null=True, blank=True)  # 复位逃生门箱体解锁把手
    close_handle_outer_cover = models.DurationField('关闭把手外盖板', null=True, blank=True)  # 关闭把手外盖板
    confirm_DDU_escape_door_display = models.DurationField('确认DDU逃生门显示', null=True, blank=True)  # 确认DDU逃生门显示
    
    class Meta:
        verbose_name = "10A01车型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.assessment_base.train_model} - {self.assessment_base.name}"
    
class Assessment_10A02(models.Model):
    # 一对一关联基础考核信息
    assessment_base = models.OneToOneField(Assessment_Base, on_delete=models.CASCADE, related_name='assessment_10A02')

    # 耗时字段
    total_duration = models.DurationField(verbose_name="整体耗时", null=True, blank=True)  # 整体耗时
    emergency_door_release_duration = models.DurationField(verbose_name="逃生门释放耗时", null=True, blank=True)  # 逃生门释放耗时

    # 涉及到操作的字段
    operate_escape_door_unlock_handle = models.DurationField('操作逃生门解锁旋钮', null=True, blank=True)  # 操作逃生门解锁旋钮
    release_escape_door_unlock_handle = models.DurationField('释放逃生门解锁把手', null=True, blank=True)  # 释放逃生门解锁把手
    push_escape_door = models.DurationField('向外推出逃生门门板', null=True, blank=True)  # 向外推出逃生门门板
    reduce_escape_door_fall_speed = models.DurationField('逃生门释放过程中借助回收绳减缓门板下落速度', null=True, blank=True)  # 逃生门释放过程中借助回收绳减缓门板下落速度
    lift_escape_door_unlock_handle = models.DurationField('上提卡住逃生门解锁把手', null=True, blank=True)  # 上提卡住逃生门解锁把手
    retract_escape_door = models.DurationField('完全收回逃生门门板', null=True, blank=True)  # 完全收回逃生门门板
    reduce_escape_door_impact_force = models.DurationField('逃生门收回过程最后阶段使用双手支撑逃生门门板减缓关门撞击力度', null=True, blank=True)  # 逃生门收回过程最后阶段使用双手支撑逃生门门板减缓关门撞击力度
    reset_escape_door_lock_handle = models.DurationField('复位解锁手柄锁闭逃生门', null=True, blank=True)  # 复位解锁手柄锁闭逃生门
    reset_escape_door_unlock_handle = models.DurationField('复位逃生门解锁旋钮', null=True, blank=True)  # 复位逃生门解锁旋钮
    reset_escape_door_handle_cover = models.DurationField('复位逃生门把手盖板', null=True, blank=True)  # 复位逃生门把手盖板
    reset_escape_door_unlock_handle_cover = models.DurationField('复位逃生门旋钮盖板', null=True, blank=True)  # 复位逃生门旋钮盖板
    install_escape_door_recovery_rope_cover = models.DurationField('安装逃生门回收绳盖板', null=True, blank=True)  # 安装逃生门回收绳盖板
    confirm_DDU_escape_door_display = models.DurationField('确认DDU逃生门显示', null=True, blank=True)  # 确认DDU逃生门显示

    
    class Meta:
        verbose_name = "10A02车型信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.assessment_base.train_model} - {self.assessment_base.name}"