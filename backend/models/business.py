"""业务管理模型（扩展20+菜单模块）"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Date
from datetime import datetime, timezone
from models.base import Base


class EquipmentType(Base):
    """设备类型"""
    __tablename__ = 'equipment_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment='类型名称')
    code = Column(String(50), unique=True, nullable=False, comment='类型编码')
    category = Column(String(50), default='', comment='设备大类')
    description = Column(Text, default='', comment='描述')
    status = Column(Boolean, default=True, comment='状态')
    sort = Column(Integer, default=0, comment='排序')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EquipmentLedger(Base):
    """设备台账"""
    __tablename__ = 'equipment_ledgers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment='设备名称')
    code = Column(String(50), unique=True, nullable=False, comment='设备编号')
    type_id = Column(Integer, default=0, comment='设备类型ID')
    type_name = Column(String(100), default='', comment='设备类型')
    turbine_id = Column(Integer, default=0, comment='关联风机ID')
    turbine_name = Column(String(50), default='', comment='关联风机')
    model = Column(String(100), default='', comment='型号')
    manufacturer = Column(String(100), default='', comment='制造商')
    install_date = Column(String(20), default='', comment='安装日期')
    warranty_expire = Column(String(20), default='', comment='保修到期')
    status = Column(String(20), default='normal', comment='状态: normal/fault/maintenance/scrap')
    description = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class MaintenanceRecord(Base):
    """设备维修记录"""
    __tablename__ = 'maintenance_records'
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, default=0, comment='设备ID')
    equipment_name = Column(String(100), default='', comment='设备名称')
    turbine_id = Column(Integer, default=0, comment='风机ID')
    turbine_name = Column(String(50), default='', comment='风机名称')
    fault_description = Column(Text, default='', comment='故障描述')
    fault_type = Column(String(50), default='', comment='故障类型')
    priority = Column(String(20), default='medium', comment='优先级')
    repair_content = Column(Text, default='', comment='维修内容')
    repair_person = Column(String(50), default='', comment='维修人')
    repair_cost = Column(Float, default=0.0, comment='维修费用')
    start_time = Column(String(20), default='', comment='开始时间')
    end_time = Column(String(20), default='', comment='结束时间')
    status = Column(String(20), default='pending', comment='状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class InspectionPlan(Base):
    """巡检计划"""
    __tablename__ = 'inspection_plans'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment='计划名称')
    turbine_ids = Column(Text, default='', comment='风机ID列表(逗号分隔)')
    turbine_names = Column(Text, default='', comment='风机名称列表')
    cycle = Column(String(20), default='monthly', comment='周期')
    content = Column(Text, default='', comment='巡检内容')
    responsible_person = Column(String(50), default='', comment='负责人')
    start_date = Column(String(20), default='', comment='开始日期')
    end_date = Column(String(20), default='', comment='结束日期')
    status = Column(Boolean, default=True, comment='启用状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class InspectionRecord(Base):
    """巡检记录"""
    __tablename__ = 'inspection_records'
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, default=0, comment='计划ID')
    plan_name = Column(String(100), default='', comment='计划名称')
    turbine_id = Column(Integer, default=0, comment='风机ID')
    turbine_name = Column(String(50), default='', comment='风机名称')
    inspector = Column(String(50), default='', comment='巡检人')
    check_time = Column(String(20), default='', comment='巡检时间')
    items = Column(Text, default='', comment='巡检项目(JSON)')
    result = Column(String(20), default='normal', comment='结果')
    description = Column(Text, default='', comment='说明')
    attachments = Column(Text, default='', comment='附件')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class WorkOrder(Base):
    """工单"""
    __tablename__ = 'work_orders'
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False, comment='工单编号')
    title = Column(String(200), nullable=False, comment='标题')
    type = Column(String(20), default='repair', comment='类型')
    turbine_id = Column(Integer, default=0, comment='风机ID')
    turbine_name = Column(String(50), default='', comment='风机名称')
    priority = Column(String(20), default='medium', comment='优先级')
    description = Column(Text, default='', comment='描述')
    assignee = Column(String(50), default='', comment='指派人')
    deadline = Column(String(20), default='', comment='截止日期')
    progress = Column(Integer, default=0, comment='进度(0-100)')
    status = Column(String(20), default='pending', comment='状态')
    result = Column(Text, default='', comment='处理结果')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SparePart(Base):
    """备件"""
    __tablename__ = 'spare_parts'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment='备件名称')
    code = Column(String(50), unique=True, nullable=False, comment='备件编码')
    model = Column(String(100), default='', comment='型号')
    category = Column(String(50), default='', comment='分类')
    manufacturer = Column(String(100), default='', comment='制造商')
    unit = Column(String(20), default='个', comment='单位')
    price = Column(Float, default=0.0, comment='单价')
    stock = Column(Integer, default=0, comment='库存数量')
    min_stock = Column(Integer, default=0, comment='最低库存')
    max_stock = Column(Integer, default=0, comment='最高库存')
    location = Column(String(100), default='', comment='存放位置')
    status = Column(Boolean, default=True, comment='状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PartTransaction(Base):
    """备件出入库"""
    __tablename__ = 'part_transactions'
    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, nullable=False, comment='备件ID')
    part_name = Column(String(100), default='', comment='备件名称')
    type = Column(String(10), nullable=False, comment='类型: in/out')
    quantity = Column(Integer, default=0, comment='数量')
    before_stock = Column(Integer, default=0, comment='操作前库存')
    after_stock = Column(Integer, default=0, comment='操作后库存')
    operator = Column(String(50), default='', comment='操作人')
    source = Column(String(100), default='', comment='来源/去向')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PowerTarget(Base):
    """发电指标"""
    __tablename__ = 'power_targets'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, comment='年份')
    month = Column(Integer, nullable=False, comment='月份')
    target_kwh = Column(Float, default=0.0, comment='目标电量')
    actual_kwh = Column(Float, default=0.0, comment='实际电量')
    completion_rate = Column(Float, default=0.0, comment='完成率')
    status = Column(String(20), default='pending', comment='状态')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EnergySettlement(Base):
    """电量结算"""
    __tablename__ = 'energy_settlements'
    id = Column(Integer, primary_key=True, index=True)
    settlement_no = Column(String(50), unique=True, nullable=False, comment='结算单号')
    period = Column(String(20), nullable=False, comment='结算周期')
    total_kwh = Column(Float, default=0.0, comment='总电量')
    price_per_kwh = Column(Float, default=0.0, comment='单价')
    total_amount = Column(Float, default=0.0, comment='总金额')
    tax_rate = Column(Float, default=0.0, comment='税率')
    tax_amount = Column(Float, default=0.0, comment='税额')
    final_amount = Column(Float, default=0.0, comment='实付金额')
    customer = Column(String(100), default='', comment='客户')
    status = Column(String(20), default='draft', comment='状态')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CarbonReduction(Base):
    """碳减排管理"""
    __tablename__ = 'carbon_reductions'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, comment='年份')
    month = Column(Integer, nullable=False, comment='月份')
    energy_kwh = Column(Float, default=0.0, comment='发电量')
    reduction_co2 = Column(Float, default=0.0, comment='CO2减排')
    reduction_so2 = Column(Float, default=0.0, comment='SO2减排')
    reduction_nox = Column(Float, default=0.0, comment='NOx减排')
    reduction_dust = Column(Float, default=0.0, comment='粉尘减排')
    standard_coal_saved = Column(Float, default=0.0, comment='节约标准煤')
    trees_equivalent = Column(Float, default=0.0, comment='等效植树')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SafetyInspection(Base):
    """安全巡检"""
    __tablename__ = 'safety_inspections'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment='巡查标题')
    area = Column(String(100), default='', comment='巡查区域')
    inspector = Column(String(50), default='', comment='巡查人')
    check_time = Column(String(20), default='', comment='巡查时间')
    items = Column(Text, default='', comment='巡查项目')
    result = Column(String(20), default='normal', comment='结果')
    description = Column(Text, default='', comment='情况说明')
    rectification = Column(Text, default='', comment='整改措施')
    status = Column(String(20), default='pending', comment='状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SafetyHazard(Base):
    """安全隐患"""
    __tablename__ = 'safety_hazards'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment='隐患标题')
    level = Column(String(20), default='medium', comment='隐患等级')
    area = Column(String(100), default='', comment='所在区域')
    source = Column(String(100), default='', comment='隐患来源')
    description = Column(Text, default='', comment='隐患描述')
    measures = Column(Text, default='', comment='整改措施')
    responsible_person = Column(String(50), default='', comment='责任人')
    deadline = Column(String(20), default='', comment='整改期限')
    status = Column(String(20), default='reported', comment='状态')
    rectification_result = Column(Text, default='', comment='整改结果')
    reviewer = Column(String(50), default='', comment='验收人')
    review_time = Column(String(20), default='', comment='验收时间')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EmergencyPlan(Base):
    """应急预案"""
    __tablename__ = 'emergency_plans'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment='预案名称')
    type = Column(String(50), default='', comment='预案类型')
    level = Column(String(20), default='company', comment='预案级别')
    content = Column(Text, default='', comment='预案内容')
    procedures = Column(Text, default='', comment='处置流程')
    responsible_person = Column(String(50), default='', comment='负责人')
    team_members = Column(Text, default='', comment='应急小组')
    drill_cycle = Column(String(50), default='', comment='演练周期')
    status = Column(Boolean, default=True, comment='启用状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EmergencyDrill(Base):
    """应急演练"""
    __tablename__ = 'emergency_drills'
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, default=0, comment='预案ID')
    plan_name = Column(String(200), default='', comment='预案名称')
    name = Column(String(200), nullable=False, comment='演练名称')
    drill_time = Column(String(20), default='', comment='演练时间')
    location = Column(String(100), default='', comment='演练地点')
    participants = Column(Integer, default=0, comment='参与人数')
    content = Column(Text, default='', comment='演练内容')
    evaluation = Column(Text, default='', comment='评估总结')
    problems = Column(Text, default='', comment='存在问题')
    improvements = Column(Text, default='', comment='改进措施')
    status = Column(String(20), default='planned', comment='状态')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Employee(Base):
    """员工信息"""
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    employee_no = Column(String(50), unique=True, nullable=False, comment='工号')
    name = Column(String(50), nullable=False, comment='姓名')
    gender = Column(String(10), default='', comment='性别')
    phone = Column(String(20), default='', comment='手机')
    email = Column(String(100), default='', comment='邮箱')
    department = Column(String(50), default='', comment='部门')
    position = Column(String(50), default='', comment='岗位')
    entry_date = Column(String(20), default='', comment='入职日期')
    status = Column(String(20), default='active', comment='状态')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ShiftSchedule(Base):
    """排班管理"""
    __tablename__ = 'shift_schedules'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, comment='员工ID')
    employee_name = Column(String(50), default='', comment='员工姓名')
    date = Column(String(20), nullable=False, comment='日期')
    shift_type = Column(String(20), default='day', comment='班次')
    start_time = Column(String(10), default='', comment='开始时间')
    end_time = Column(String(10), default='', comment='结束时间')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AttendanceRecord(Base):
    """考勤记录"""
    __tablename__ = 'attendance_records'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, comment='员工ID')
    employee_name = Column(String(50), default='', comment='员工姓名')
    date = Column(String(20), nullable=False, comment='日期')
    check_in = Column(String(10), default='', comment='签到')
    check_out = Column(String(10), default='', comment='签退')
    status = Column(String(20), default='normal', comment='状态')
    work_hours = Column(Float, default=0.0, comment='工时')
    overtime_hours = Column(Float, default=0.0, comment='加班工时')
    remark = Column(Text, default='', comment='备注')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RevenueItem(Base):
    """收入统计"""
    __tablename__ = 'revenue_items'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, comment='年份')
    month = Column(Integer, nullable=False, comment='月份')
    energy_revenue = Column(Float, default=0.0, comment='电费收入')
    subsidy_revenue = Column(Float, default=0.0, comment='补贴收入')
    carbon_revenue = Column(Float, default=0.0, comment='碳交易收入')
    other_revenue = Column(Float, default=0.0, comment='其他收入')
    total_revenue = Column(Float, default=0.0, comment='总收入')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CostItem(Base):
    """成本分析"""
    __tablename__ = 'cost_items'
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, comment='年份')
    month = Column(Integer, nullable=False, comment='月份')
    category = Column(String(50), nullable=False, comment='成本类别')
    amount = Column(Float, default=0.0, comment='金额')
    description = Column(Text, default='', comment='说明')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
