# -*- coding: utf-8 -*-
"""
UE5.3 随机工具集成版 - 带UI参数设置
包含：随机选择、随机旋转、随机缩放

使用方法：
1. 在场景中选择要处理的Actor
2. 在UE5 Python控制台执行此脚本
3. 在弹出的UI中设置参数
4. 点击OK执行，Ctrl+Z可撤销

作者：Claude
版本：1.0
"""

import unreal
import random


# ============================================
# 参数类定义 - 自动生成UI
# ============================================

@unreal.uclass()
class RandomToolParameters(unreal.Object):
    """随机工具参数类"""
    
    # ===== 功能开关 =====
    enable_selection = unreal.uproperty(bool, meta=dict(
        Category="功能开关",
        DisplayName="启用随机选择",
        ToolTip="从选中的Actor中随机选择一部分"
    ))
    
    enable_rotation = unreal.uproperty(bool, meta=dict(
        Category="功能开关",
        DisplayName="启用随机旋转",
        ToolTip="随机旋转选中的Actor"
    ))
    
    enable_scale = unreal.uproperty(bool, meta=dict(
        Category="功能开关",
        DisplayName="启用随机缩放",
        ToolTip="随机缩放选中的Actor"
    ))
    
    # ===== 随机选择参数 =====
    selection_mode = unreal.uproperty(int, meta=dict(
        Category="随机选择",
        DisplayName="选择模式",
        ToolTip="1=选择N个 | 2=选择百分比 | 3=取消选择保留N个",
        ClampMin=1, ClampMax=3, UIMin=1, UIMax=3
    ))
    
    select_count = unreal.uproperty(int, meta=dict(
        Category="随机选择",
        DisplayName="选择数量",
        ToolTip="模式1：要选择的数量 | 模式3：要保留的数量",
        ClampMin=1, ClampMax=1000, UIMin=1, UIMax=100
    ))
    
    select_percentage = unreal.uproperty(float, meta=dict(
        Category="随机选择",
        DisplayName="选择百分比",
        ToolTip="模式2：选择百分比（0.5 = 50%）",
        ClampMin=0.01, ClampMax=1.0, UIMin=0.01, UIMax=1.0
    ))
    
    # ===== 随机旋转参数 =====
    rotation_mode = unreal.uproperty(int, meta=dict(
        Category="随机旋转",
        DisplayName="旋转模式",
        ToolTip="1=完全随机(0-360度) | 2=范围随机(当前±N度)",
        ClampMin=1, ClampMax=2, UIMin=1, UIMax=2
    ))
    
    rotate_x = unreal.uproperty(bool, meta=dict(
        Category="随机旋转",
        DisplayName="旋转X轴 (Roll)",
        ToolTip="是否随机旋转X轴（滚动/翻滚）"
    ))
    
    rotate_y = unreal.uproperty(bool, meta=dict(
        Category="随机旋转",
        DisplayName="旋转Y轴 (Pitch)",
        ToolTip="是否随机旋转Y轴（俯仰）"
    ))
    
    rotate_z = unreal.uproperty(bool, meta=dict(
        Category="随机旋转",
        DisplayName="旋转Z轴 (Yaw)",
        ToolTip="是否随机旋转Z轴（偏航/左右旋转）- UE中Z轴朝上"
    ))
    
    rotation_range_x = unreal.uproperty(float, meta=dict(
        Category="随机旋转",
        DisplayName="X轴旋转范围",
        ToolTip="模式2：旋转范围±N度",
        ClampMin=0.0, ClampMax=180.0, UIMin=0.0, UIMax=180.0
    ))
    
    rotation_range_y = unreal.uproperty(float, meta=dict(
        Category="随机旋转",
        DisplayName="Y轴旋转范围",
        ToolTip="模式2：旋转范围±N度",
        ClampMin=0.0, ClampMax=180.0, UIMin=0.0, UIMax=180.0
    ))
    
    rotation_range_z = unreal.uproperty(float, meta=dict(
        Category="随机旋转",
        DisplayName="Z轴旋转范围",
        ToolTip="模式2：旋转范围±N度",
        ClampMin=0.0, ClampMax=180.0, UIMin=0.0, UIMax=180.0
    ))
    
    # ===== 随机缩放参数 =====
    scale_mode = unreal.uproperty(int, meta=dict(
        Category="随机缩放",
        DisplayName="缩放模式",
        ToolTip="1=统一缩放(等比例) | 2=独立缩放(各轴独立)",
        ClampMin=1, ClampMax=2, UIMin=1, UIMax=2
    ))
    
    scale_range_mode = unreal.uproperty(int, meta=dict(
        Category="随机缩放",
        DisplayName="范围模式",
        ToolTip="1=绝对范围(0.5-2.0倍) | 2=相对范围(当前±30%)",
        ClampMin=1, ClampMax=2, UIMin=1, UIMax=2
    ))
    
    scale_x = unreal.uproperty(bool, meta=dict(
        Category="随机缩放",
        DisplayName="缩放X轴",
        ToolTip="独立缩放模式：是否缩放X轴"
    ))
    
    scale_y = unreal.uproperty(bool, meta=dict(
        Category="随机缩放",
        DisplayName="缩放Y轴",
        ToolTip="独立缩放模式：是否缩放Y轴"
    ))
    
    scale_z = unreal.uproperty(bool, meta=dict(
        Category="随机缩放",
        DisplayName="缩放Z轴",
        ToolTip="独立缩放模式：是否缩放Z轴"
    ))
    
    # 统一缩放-绝对范围
    scale_min_uniform = unreal.uproperty(float, meta=dict(
        Category="随机缩放",
        DisplayName="统一最小缩放",
        ToolTip="统一缩放+绝对范围：最小缩放倍数",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_max_uniform = unreal.uproperty(float, meta=dict(
        Category="随机缩放",
        DisplayName="统一最大缩放",
        ToolTip="统一缩放+绝对范围：最大缩放倍数",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    # 统一缩放-相对范围
    scale_variance_uniform = unreal.uproperty(float, meta=dict(
        Category="随机缩放",
        DisplayName="统一缩放变化",
        ToolTip="统一缩放+相对范围：变化百分比(0.3=±30%)",
        ClampMin=0.0, ClampMax=1.0, UIMin=0.0, UIMax=1.0
    ))
    
    # 独立缩放-绝对范围
    scale_min_x = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="X轴最小缩放",
        ToolTip="独立缩放+绝对范围：X轴最小值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_max_x = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="X轴最大缩放",
        ToolTip="独立缩放+绝对范围：X轴最大值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_min_y = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Y轴最小缩放",
        ToolTip="独立缩放+绝对范围：Y轴最小值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_max_y = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Y轴最大缩放",
        ToolTip="独立缩放+绝对范围：Y轴最大值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_min_z = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Z轴最小缩放",
        ToolTip="独立缩放+绝对范围：Z轴最小值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    scale_max_z = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Z轴最大缩放",
        ToolTip="独立缩放+绝对范围：Z轴最大值",
        ClampMin=0.01, ClampMax=10.0, UIMin=0.1, UIMax=5.0
    ))
    
    # 独立缩放-相对范围
    scale_variance_x = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="X轴变化范围",
        ToolTip="独立缩放+相对范围：X轴变化(0.2=±20%)",
        ClampMin=0.0, ClampMax=1.0, UIMin=0.0, UIMax=1.0
    ))
    
    scale_variance_y = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Y轴变化范围",
        ToolTip="独立缩放+相对范围：Y轴变化(0.2=±20%)",
        ClampMin=0.0, ClampMax=1.0, UIMin=0.0, UIMax=1.0
    ))
    
    scale_variance_z = unreal.uproperty(float, meta=dict(
        Category="随机缩放|独立缩放",
        DisplayName="Z轴变化范围",
        ToolTip="独立缩放+相对范围：Z轴变化(0.2=±20%)",
        ClampMin=0.0, ClampMax=1.0, UIMin=0.0, UIMax=1.0
    ))
    
    # ===== 通用参数 =====
    random_seed = unreal.uproperty(int, meta=dict(
        Category="通用设置",
        DisplayName="随机种子",
        ToolTip="固定种子可重复结果（0=随机）",
        ClampMin=0, ClampMax=99999, UIMin=0, UIMax=10000
    ))
    
    print_details = unreal.uproperty(bool, meta=dict(
        Category="通用设置",
        DisplayName="打印详细信息",
        ToolTip="在Output Log中显示详细执行信息"
    ))


# ============================================
# 核心功能实现
# ============================================

class RandomToolExecutor:
    """随机工具执行器"""
    
    def __init__(self, params):
        self.params = params
        self.min_scale_limit = 0.01
        
        # 设置随机种子
        if params.random_seed > 0:
            random.seed(params.random_seed)
    
    def get_selected_actors(self):
        """获取选中的Actor"""
        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        return list(actors)
    
    # ===== 随机选择功能 =====
    
    def execute_random_selection(self, actors):
        """执行随机选择"""
        if not self.params.enable_selection:
            return actors
        
        unreal.log("=" * 60)
        unreal.log("执行随机选择...")
        
        total = len(actors)
        selected = []
        
        if self.params.selection_mode == 1:
            # 模式1：选择N个
            count = min(self.params.select_count, total)
            selected = random.sample(actors, count)
            unreal.log(f"从 {total} 个Actor中随机选择了 {count} 个")
            
        elif self.params.selection_mode == 2:
            # 模式2：选择百分比
            count = max(1, int(total * self.params.select_percentage))
            selected = random.sample(actors, count)
            unreal.log(f"从 {total} 个Actor中随机选择了 {self.params.select_percentage*100}% ({count} 个)")
            
        elif self.params.selection_mode == 3:
            # 模式3：取消选择，保留N个
            keep_count = min(self.params.select_count, total)
            selected = random.sample(actors, keep_count)
            unreal.log(f"从 {total} 个Actor中随机保留了 {keep_count} 个")
        
        # 更新选择
        unreal.EditorLevelLibrary.set_selected_level_actors(selected)
        
        if self.params.print_details:
            unreal.log("选中的Actor:")
            for actor in selected:
                unreal.log(f"  - {actor.get_name()}")
        
        return selected
    
    # ===== 随机旋转功能 =====
    
    def execute_random_rotation(self, actors):
        """执行随机旋转"""
        if not self.params.enable_rotation:
            return
        
        # 检查是否至少选择了一个轴
        if not (self.params.rotate_x or self.params.rotate_y or self.params.rotate_z):
            unreal.log_warning("随机旋转：请至少启用一个旋转轴")
            return
        
        unreal.log("=" * 60)
        unreal.log("执行随机旋转...")
        
        axes = []
        if self.params.rotate_x:
            axes.append("X(Roll)")
        if self.params.rotate_y:
            axes.append("Y(Pitch)")
        if self.params.rotate_z:
            axes.append("Z(Yaw)")
        unreal.log(f"旋转轴: {', '.join(axes)}")
        
        if self.params.rotation_mode == 1:
            unreal.log("模式：完全随机旋转 (0-360度)")
            for actor in actors:
                actor.modify()
                old_rot = actor.get_actor_rotation()
                
                # UE坐标系：X=Roll, Y=Pitch, Z=Yaw（Z轴朝上）
                new_rot = unreal.Rotator(
                    roll=random.uniform(0, 360) if self.params.rotate_x else old_rot.roll,
                    pitch=random.uniform(0, 360) if self.params.rotate_y else old_rot.pitch,
                    yaw=random.uniform(0, 360) if self.params.rotate_z else old_rot.yaw
                )
                
                actor.set_actor_rotation(new_rot, False)
                
                if self.params.print_details:
                    unreal.log(f"{actor.get_name()}: Roll={new_rot.roll:.1f}° Pitch={new_rot.pitch:.1f}° Yaw={new_rot.yaw:.1f}°")
        
        elif self.params.rotation_mode == 2:
            ranges = []
            if self.params.rotate_x:
                ranges.append(f"X(Roll):±{self.params.rotation_range_x}°")
            if self.params.rotate_y:
                ranges.append(f"Y(Pitch):±{self.params.rotation_range_y}°")
            if self.params.rotate_z:
                ranges.append(f"Z(Yaw):±{self.params.rotation_range_z}°")
            unreal.log(f"模式：范围随机旋转 ({', '.join(ranges)})")
            
            for actor in actors:
                actor.modify()
                old_rot = actor.get_actor_rotation()
                
                # UE坐标系：X=Roll, Y=Pitch, Z=Yaw（Z轴朝上）
                new_rot = unreal.Rotator(
                    roll=old_rot.roll + random.uniform(-self.params.rotation_range_x, self.params.rotation_range_x) if self.params.rotate_x else old_rot.roll,
                    pitch=old_rot.pitch + random.uniform(-self.params.rotation_range_y, self.params.rotation_range_y) if self.params.rotate_y else old_rot.pitch,
                    yaw=old_rot.yaw + random.uniform(-self.params.rotation_range_z, self.params.rotation_range_z) if self.params.rotate_z else old_rot.yaw
                )
                
                actor.set_actor_rotation(new_rot, False)
                
                if self.params.print_details:
                    unreal.log(f"{actor.get_name()}: Roll={new_rot.roll:.1f}° Pitch={new_rot.pitch:.1f}° Yaw={new_rot.yaw:.1f}°")
    
    # ===== 随机缩放功能 =====
    
    def clamp_scale(self, value):
        """确保缩放值在有效范围内"""
        return max(value, self.min_scale_limit)
    
    def execute_random_scale(self, actors):
        """执行随机缩放"""
        if not self.params.enable_scale:
            return
        
        unreal.log("=" * 60)
        unreal.log("执行随机缩放...")
        
        if self.params.scale_mode == 1:
            # 统一缩放
            unreal.log("缩放模式：统一缩放（等比例）")
            
            if self.params.scale_range_mode == 1:
                # 绝对范围
                unreal.log(f"范围：{self.params.scale_min_uniform} 到 {self.params.scale_max_uniform} 倍")
                
                for actor in actors:
                    actor.modify()
                    scale_factor = random.uniform(self.params.scale_min_uniform, self.params.scale_max_uniform)
                    scale_factor = self.clamp_scale(scale_factor)
                    
                    new_scale = unreal.Vector(scale_factor, scale_factor, scale_factor)
                    actor.set_actor_scale3d(new_scale)
                    
                    if self.params.print_details:
                        unreal.log(f"{actor.get_name()}: 缩放 = {scale_factor:.3f}")
            
            else:
                # 相对范围
                unreal.log(f"范围：当前大小 ±{self.params.scale_variance_uniform*100}%")
                
                for actor in actors:
                    actor.modify()
                    current_scale = actor.get_actor_scale3d()
                    current_avg = (current_scale.x + current_scale.y + current_scale.z) / 3.0
                    
                    scale_factor = current_avg * random.uniform(
                        1.0 - self.params.scale_variance_uniform,
                        1.0 + self.params.scale_variance_uniform
                    )
                    scale_factor = self.clamp_scale(scale_factor)
                    
                    new_scale = unreal.Vector(scale_factor, scale_factor, scale_factor)
                    actor.set_actor_scale3d(new_scale)
                    
                    if self.params.print_details:
                        unreal.log(f"{actor.get_name()}: 缩放 = {scale_factor:.3f}")
        
        elif self.params.scale_mode == 2:
            # 独立缩放
            if not (self.params.scale_x or self.params.scale_y or self.params.scale_z):
                unreal.log_warning("独立缩放：请至少启用一个缩放轴")
                return
            
            axes = []
            if self.params.scale_x:
                axes.append("X")
            if self.params.scale_y:
                axes.append("Y")
            if self.params.scale_z:
                axes.append("Z")
            unreal.log(f"缩放模式：独立缩放（轴：{', '.join(axes)}）")
            
            if self.params.scale_range_mode == 1:
                # 绝对范围
                ranges = []
                if self.params.scale_x:
                    ranges.append(f"X:{self.params.scale_min_x}-{self.params.scale_max_x}")
                if self.params.scale_y:
                    ranges.append(f"Y:{self.params.scale_min_y}-{self.params.scale_max_y}")
                if self.params.scale_z:
                    ranges.append(f"Z:{self.params.scale_min_z}-{self.params.scale_max_z}")
                unreal.log(f"范围：{', '.join(ranges)}")
                
                for actor in actors:
                    actor.modify()
                    current_scale = actor.get_actor_scale3d()
                    
                    new_x = random.uniform(self.params.scale_min_x, self.params.scale_max_x) if self.params.scale_x else current_scale.x
                    new_y = random.uniform(self.params.scale_min_y, self.params.scale_max_y) if self.params.scale_y else current_scale.y
                    new_z = random.uniform(self.params.scale_min_z, self.params.scale_max_z) if self.params.scale_z else current_scale.z
                    
                    new_x = self.clamp_scale(new_x)
                    new_y = self.clamp_scale(new_y)
                    new_z = self.clamp_scale(new_z)
                    
                    new_scale = unreal.Vector(new_x, new_y, new_z)
                    actor.set_actor_scale3d(new_scale)
                    
                    if self.params.print_details:
                        unreal.log(f"{actor.get_name()}: X={new_x:.3f}, Y={new_y:.3f}, Z={new_z:.3f}")
            
            else:
                # 相对范围
                ranges = []
                if self.params.scale_x:
                    ranges.append(f"X:±{self.params.scale_variance_x*100}%")
                if self.params.scale_y:
                    ranges.append(f"Y:±{self.params.scale_variance_y*100}%")
                if self.params.scale_z:
                    ranges.append(f"Z:±{self.params.scale_variance_z*100}%")
                unreal.log(f"范围：{', '.join(ranges)}")
                
                for actor in actors:
                    actor.modify()
                    current_scale = actor.get_actor_scale3d()
                    
                    new_x = current_scale.x * random.uniform(1.0 - self.params.scale_variance_x, 1.0 + self.params.scale_variance_x) if self.params.scale_x else current_scale.x
                    new_y = current_scale.y * random.uniform(1.0 - self.params.scale_variance_y, 1.0 + self.params.scale_variance_y) if self.params.scale_y else current_scale.y
                    new_z = current_scale.z * random.uniform(1.0 - self.params.scale_variance_z, 1.0 + self.params.scale_variance_z) if self.params.scale_z else current_scale.z
                    
                    new_x = self.clamp_scale(new_x)
                    new_y = self.clamp_scale(new_y)
                    new_z = self.clamp_scale(new_z)
                    
                    new_scale = unreal.Vector(new_x, new_y, new_z)
                    actor.set_actor_scale3d(new_scale)
                    
                    if self.params.print_details:
                        unreal.log(f"{actor.get_name()}: X={new_x:.3f}, Y={new_y:.3f}, Z={new_z:.3f}")
    
    # ===== 主执行函数 =====
    
    def execute(self):
        """执行所有启用的功能"""
        # 获取选中的Actor
        actors = self.get_selected_actors()
        
        if not actors:
            unreal.log_error("❌ 没有选中任何Actor！请先在场景中选择要处理的Actor。")
            return False
        
        # 检查是否至少启用了一个功能
        if not (self.params.enable_selection or self.params.enable_rotation or self.params.enable_scale):
            unreal.log_warning("⚠️ 请至少启用一个功能！")
            return False
        
        unreal.log("\n" + "=" * 60)
        unreal.log("🎲 UE随机工具集 - 开始执行")
        unreal.log("=" * 60)
        unreal.log(f"📋 初始选中: {len(actors)} 个Actor")
        
        enabled_features = []
        if self.params.enable_selection:
            enabled_features.append("随机选择")
        if self.params.enable_rotation:
            enabled_features.append("随机旋转")
        if self.params.enable_scale:
            enabled_features.append("随机缩放")
        
        unreal.log(f"✅ 启用功能: {', '.join(enabled_features)}")
        
        if self.params.random_seed > 0:
            unreal.log(f"🎯 随机种子: {self.params.random_seed}")
        
        # 使用事务系统支持撤销
        with unreal.ScopedEditorTransaction("Random Tool Execute") as trans:
            # 1. 随机选择（可能会改变actors列表）
            if self.params.enable_selection:
                actors = self.execute_random_selection(actors)
            
            # 2. 随机旋转
            if self.params.enable_rotation:
                self.execute_random_rotation(actors)
            
            # 3. 随机缩放
            if self.params.enable_scale:
                self.execute_random_scale(actors)
        
        unreal.log("=" * 60)
        unreal.log("✅ 执行完成！")
        unreal.log("=" * 60 + "\n")
        
        return True


# ============================================
# UI对话框和主入口
# ============================================

def show_random_tool_ui():
    """显示随机工具UI对话框"""
    
    # 检查是否选中了Actor
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    
    if not selected_actors or len(selected_actors) == 0:
        unreal.log_error("❌ 没有选中任何Actor！请先在场景中选择要处理的Actor。")
        return
    
    # 创建参数对象
    params = RandomToolParameters()
    
    # 设置默认值
    # 功能开关
    params.enable_selection = False
    params.enable_rotation = False
    params.enable_scale = True
    
    # 随机选择默认值
    params.selection_mode = 1
    params.select_count = 3
    params.select_percentage = 0.5
    
    # 随机旋转默认值
    params.rotation_mode = 1
    params.rotate_x = False
    params.rotate_y = False
    params.rotate_z = True
    params.rotation_range_x = 30.0
    params.rotation_range_y = 45.0
    params.rotation_range_z = 60.0
    
    # 随机缩放默认值
    params.scale_mode = 1
    params.scale_range_mode = 1
    params.scale_x = True
    params.scale_y = True
    params.scale_z = True
    params.scale_min_uniform = 0.5
    params.scale_max_uniform = 2.0
    params.scale_variance_uniform = 0.3
    params.scale_min_x = 0.8
    params.scale_max_x = 1.5
    params.scale_min_y = 0.8
    params.scale_max_y = 1.5
    params.scale_min_z = 0.5
    params.scale_max_z = 2.0
    params.scale_variance_x = 0.2
    params.scale_variance_y = 0.2
    params.scale_variance_z = 0.3
    
    # 通用设置默认值
    params.random_seed = 0
    params.print_details = True
    
    # 创建对话框选项
    options = unreal.EditorDialogLibraryObjectDetailsViewOptions()
    options.show_object_name = False
    options.allow_search = True
    
    # 显示对话框
    result = unreal.EditorDialog.show_object_details_view(
        "🎲 随机工具集 - 参数设置",
        params,
        options
    )
    
    if result:
        # 用户点击OK，执行工具
        executor = RandomToolExecutor(params)
        executor.execute()
    else:
        unreal.log("❌ 用户取消了操作")


def show_complete_workflow():
    """完整工作流程（已废弃，使用show_random_tool_ui代替）"""
    show_random_tool_ui()


# ============================================
# 快速预设功能
# ============================================

def quick_random_scale():
    """快速预设：随机缩放（0.7-1.3倍）"""
    params = RandomToolParameters()
    params.enable_selection = False
    params.enable_rotation = False
    params.enable_scale = True
    params.scale_mode = 1
    params.scale_range_mode = 1
    params.scale_min_uniform = 0.7
    params.scale_max_uniform = 1.3
    params.random_seed = 0
    params.print_details = False
    
    executor = RandomToolExecutor(params)
    executor.execute()


def quick_random_rotation_z():
    """快速预设：随机旋转Z轴（完全随机）"""
    params = RandomToolParameters()
    params.enable_selection = False
    params.enable_rotation = True
    params.enable_scale = False
    params.rotation_mode = 1
    params.rotate_x = False
    params.rotate_y = False
    params.rotate_z = True
    params.random_seed = 0
    params.print_details = False
    
    executor = RandomToolExecutor(params)
    executor.execute()


def quick_select_half():
    """快速预设：随机选择50%"""
    params = RandomToolParameters()
    params.enable_selection = True
    params.enable_rotation = False
    params.enable_scale = False
    params.selection_mode = 2
    params.select_percentage = 0.5
    params.random_seed = 0
    params.print_details = False
    
    executor = RandomToolExecutor(params)
    executor.execute()


# ============================================
# 主入口
# ============================================

if __name__ == "__main__":
    # 直接显示参数UI（推荐）
    show_random_tool_ui()
    
    # 或者使用快速预设
    # quick_random_scale()
    # quick_random_rotation_z()
    # quick_select_half()


# ============================================
# 使用说明
# ============================================
"""
🎯 使用方法：

1. 基本使用：
   - 在场景中选择要处理的Actor（Outliner中多选）
   - 在UE5 Python控制台执行此脚本
   - 在弹出的UI中勾选要使用的功能并设置参数
   - 点击OK执行
   - 按Ctrl+Z可以撤销（不会有提示）

2. UI参数说明：

   【功能开关】
   - 启用随机选择：从选中Actor中随机选择
   - 启用随机旋转：随机旋转Actor
   - 启用随机缩放：随机缩放Actor
   
   【随机选择】
   - 模式1：选择固定数量
   - 模式2：选择百分比
   - 模式3：取消选择，保留指定数量
   
   【随机旋转】（已修正UE坐标系）
   - X轴 = Roll（滚动）
   - Y轴 = Pitch（俯仰）
   - Z轴 = Yaw（偏航，左右旋转）⭐ Z轴朝上
   - 模式1：完全随机(0-360度)
   - 模式2：范围随机(当前±N度)
   
   【随机缩放】
   - 缩放模式：统一缩放 vs 独立缩放
   - 范围模式：绝对范围 vs 相对范围
   - 独立缩放可选择要缩放的轴

3. 实用场景：

   场景A - 随机分布石头：
   ✓ 启用随机旋转（Z轴完全随机）
   ✓ 启用随机缩放（0.7-1.3倍）
   
   场景B - 稀疏植被：
   ✓ 启用随机选择（保留30%）
   
   场景C - 自然树木：
   ✓ 启用随机旋转（Z轴完全随机）
   ✓ 启用随机缩放（相对±20%）
   
   场景D - 随机装饰物：
   ✓ 启用随机选择（选择50%）
   ✓ 启用随机旋转（XYZ完全随机）
   ✓ 启用随机缩放（0.5-2.0倍）

4. 快速预设：

   如果不想每次都设置参数，可以使用快速预设：
   
   quick_random_scale()      # 快速随机缩放
   quick_random_rotation_z() # 快速随机旋转Z轴
   quick_select_half()       # 快速选择50%
   
   在脚本末尾取消注释相应函数即可

5. 随机种子：

   - 设为0：每次随机结果不同
   - 设为固定数字（如42）：可重复相同的随机结果
   - 用于测试或需要一致性的场景

6. 撤销支持：

   - 所有操作都支持Ctrl+Z撤销
   - 在Undo History中显示为"Random Tool Execute"
   - 可以完整恢复到执行前的状态

7. 组合使用：

   可以同时启用多个功能，执行顺序为：
   1. 随机选择（会改变处理的Actor数量）
   2. 随机旋转（对选中的Actor旋转）
   3. 随机缩放（对选中的Actor缩放）

8. 注意事项：

   - 至少要启用一个功能
   - 旋转功能至少要选择一个轴
   - 独立缩放至少要选择一个轴
   - 建议先在小范围测试，满意后再大批量使用

9. 常见问题：

   Q: 为什么撤销不起作用？
   A: 确保在执行后立即按Ctrl+Z，不要进行其他操作
   
   Q: 如何保存常用的参数设置？
   A: 可以修改脚本中的默认值，或使用快速预设功能
   
   Q: 可以只对某些类型的Actor操作吗？
   A: 先在Outliner中选择特定类型的Actor，再运行脚本

10. 进阶技巧：

    - 配合UE的Selection Sets保存选择
    - 使用随机种子记录满意的随机结果
    - 多次运行不同参数组合叠加效果
    - 结合Blueprint进一步自动化

作者：Claude
版本：1.0
更新：2024
"""