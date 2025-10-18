# -*- coding: utf-8 -*-
"""
@PLUGIN_INFO
name: 关卡整体变换工具
description: 整体移动，旋转，缩放关卡内的物体。
category: 用户脚本
favorite: false
usage: 关卡整体变换工具
@PLUGIN_PARAMS
@PLUGIN_INFO_END
"""

import math
import unreal

# ============================================
# 参数类
# ============================================

@unreal.uclass()
class LevelTransformParams(unreal.Object):
    execute_mode = unreal.uproperty(int, meta=dict(
        DisplayName="执行模式",
        ToolTip="0=全关卡, 1=仅选中Actor",
        ClampMin=0, ClampMax=1
    ))

    do_translate = unreal.uproperty(bool, meta=dict(DisplayName="启用移动"))
    do_rotate = unreal.uproperty(bool, meta=dict(DisplayName="启用旋转"))
    do_scale = unreal.uproperty(bool, meta=dict(DisplayName="启用缩放"))

    translate = unreal.uproperty(unreal.Vector, meta=dict(DisplayName="移动向量 (X,Y,Z)"))
    rotate = unreal.uproperty(unreal.Rotator, meta=dict(DisplayName="旋转角度 (Pitch,Yaw,Roll)"))
    scale = unreal.uproperty(unreal.Vector, meta=dict(DisplayName="缩放比例 (X,Y,Z)"))

    rotation_pivot = unreal.uproperty(unreal.Vector, meta=dict(
        DisplayName="旋转中心点",
        ToolTip="旋转和缩放的中心点，默认(0,0,0)为世界原点"
    ))

    scale_affects_location = unreal.uproperty(bool, meta=dict(
        DisplayName="缩放影响位置",
        ToolTip="勾选后，物体位置会随缩放比例改变（以旋转中心为基准）"
    ))

    force_apply = unreal.uproperty(bool, meta=dict(
        DisplayName="强制应用操作",
        ToolTip="忽略类型限制，所有Actor都执行勾选的操作"
    ))
    
    verbose_log = unreal.uproperty(bool, meta=dict(
        DisplayName="输出详细日志",
        ToolTip="输出每个Actor执行的操作"
    ))
    
    refresh_viewport = unreal.uproperty(bool, meta=dict(
        DisplayName="执行后刷新视口"
    ))


# ============================================
# 数学工具函数
# ============================================

def rotate_vector_around_pivot(location, pivot, rotation):
    """
    使用UE的Quaternion API实现准确的旋转
    location: unreal.Vector - 要旋转的位置
    pivot: unreal.Vector - 旋转中心点
    rotation: unreal.Rotator - 旋转角度
    返回: unreal.Vector - 旋转后的位置
    """
    # 转换为四元数
    quat = rotation.quaternion()
    
    # 计算相对于pivot的偏移
    offset = location - pivot
    
    # 使用四元数旋转偏移向量
    rotated_offset = quat.rotate_vector(offset)
    
    # 返回旋转后的世界坐标
    return pivot + rotated_offset


def scale_vector_around_pivot(location, pivot, scale):
    """
    以pivot为中心缩放位置
    location: unreal.Vector
    pivot: unreal.Vector
    scale: unreal.Vector
    返回: unreal.Vector
    """
    offset = location - pivot
    scaled_offset = unreal.Vector(
        offset.x * scale.x,
        offset.y * scale.y,
        offset.z * scale.z
    )
    return pivot + scaled_offset


# ============================================
# 类型策略系统
# ============================================

def get_transform_policy(actor):
    """
    返回 (can_move, can_rotate, can_scale, is_directional_light)
    """
    cls_name = actor.get_class().get_name()
    actor_label = actor.get_actor_label()
    
    # 检查是否是蓝图Actor（多种方式判断）
    is_blueprint = (
        "_C" in cls_name or  # 蓝图类通常以 _C 结尾
        "BP_" in actor_label or  # 名称包含 BP_ 前缀
        "Blueprint" in cls_name or
        cls_name.startswith("BP")
    )

    # 方向光特殊处理：不旋转、不移动、不缩放
    if "DirectionalLight" in cls_name:
        return (False, False, False, True)
    
    # 蓝图Actor强制允许完全变换
    if is_blueprint:
        return (True, True, True, False)

    # 完全变换类型（移动+旋转+缩放）
    full_transform_classes = [
        "StaticMeshActor", "SkeletalMeshActor", "InstancedFoliageActor",
        "Landscape", "WaterBody", "WaterBodyOcean", "WaterBodyRiver", "WaterBodyLake"
    ]
    
    # 场景光源（移动+旋转+缩放，但缩放可能只影响某些属性）
    scene_light_classes = [
        "PointLight", "SpotLight", "RectLight"
    ]
    
    # 移动+旋转（不缩放）
    move_rotate_classes = [
        "CameraActor", "CineCameraActor", "VolumetricCloud"
    ]
    
    # 仅移动
    move_only_classes = [
        "ReflectionCapture", "BoxReflectionCapture", "SphereReflectionCapture",
        "PlanarReflection", "PostProcessVolume", "ExponentialHeightFog",
        "PhysicsVolume", "TriggerVolume", "BlockingVolume", "LightmassImportanceVolume"
    ]
    
    # 跳过的类型
    skip_classes = [
        "WorldSettings", "DefaultPhysicsVolume", "SkyAtmosphere"
    ]

    for skip in skip_classes:
        if skip in cls_name:
            return (False, False, False, False)
    
    for t in full_transform_classes:
        if t in cls_name:
            return (True, True, True, False)
    
    for t in scene_light_classes:
        if t in cls_name:
            return (True, True, True, False)  # 场景光源可以缩放（影响范围等）
    
    for t in move_rotate_classes:
        if t in cls_name:
            return (True, True, False, False)
    
    for t in move_only_classes:
        if t in cls_name:
            return (True, False, False, False)

    # 默认策略：可移动 + 可旋转
    return (True, True, False, False)


# ============================================
# 主逻辑
# ============================================

def execute_level_transform(params):
    # 获取Actor列表 - 使用新的API
    if params.execute_mode == 0:
        try:
            # 优先使用新API
            subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
            actors = subsystem.get_all_level_actors()
        except:
            # 降级到旧API
            actors = unreal.EditorLevelLibrary.get_all_level_actors()
    else:
        try:
            subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
            actors = subsystem.get_selected_level_actors()
        except:
            actors = unreal.EditorLevelLibrary.get_selected_level_actors()

    actors = [a for a in actors if a]

    if not actors:
        unreal.log_warning("未找到可操作的Actor。")
        return

    total = len(actors)
    unreal.log(f"[LevelTransform] 找到 {total} 个 Actor，开始变换...")

    # 检查是否有实际的旋转操作
    has_rotation = (params.do_rotate and 
                   (abs(params.rotate.pitch) > 1e-6 or 
                    abs(params.rotate.yaw) > 1e-6 or 
                    abs(params.rotate.roll) > 1e-6))
    
    # 检查是否有实际的缩放操作
    has_scale = (params.do_scale and 
                (abs(params.scale.x - 1.0) > 1e-6 or 
                 abs(params.scale.y - 1.0) > 1e-6 or 
                 abs(params.scale.z - 1.0) > 1e-6))

    pivot = params.rotation_pivot
    
    # 预先收集所有要修改的Actor和它们的原始变换
    transform_list = []
    
    for actor in actors:
        cls_name = actor.get_class().get_name()
        can_move, can_rotate, can_scale, is_directional_light = get_transform_policy(actor)
        
        # 强制应用模式
        if params.force_apply:
            can_move = can_rotate = can_scale = True
        
        # 方向光始终跳过
        if is_directional_light:
            if params.verbose_log:
                unreal.log(f"[Skip] {actor.get_actor_label()} | DirectionalLight (方向光不参与变换)")
            continue
        
        try:
            current_loc = actor.get_actor_location()
            current_rot = actor.get_actor_rotation()
            current_scale = actor.get_actor_scale3d()
            
            transform_list.append({
                'actor': actor,
                'cls_name': cls_name,
                'can_move': can_move,
                'can_rotate': can_rotate,
                'can_scale': can_scale,
                'current_loc': current_loc,
                'current_rot': current_rot,
                'current_scale': current_scale
            })
        except Exception as e:
            unreal.log_warning(f"[Transform] 无法获取属性: {cls_name} -> {e}")
            continue
    
    if not transform_list:
        unreal.log_warning("没有可变换的Actor。")
        return
    
    total = len(transform_list)
    unreal.log(f"[LevelTransform] 将变换 {total} 个 Actor...")
    
    # 使用单个事务包裹所有修改
    with unreal.ScopedEditorTransaction("Level Transform"):
        # 第一步：先标记所有Actor为可修改
        for item in transform_list:
            item['actor'].modify()
        
        # 第二步：执行所有变换
        with unreal.ScopedSlowTask(total, "正在执行整体变换...") as slow_task:
            slow_task.make_dialog(True)

            for i, item in enumerate(transform_list):
                if slow_task.should_cancel():
                    unreal.log("用户取消了操作。")
                    break

                actor = item['actor']
                slow_task.enter_progress_frame(1, f"处理: {actor.get_actor_label()} ({i+1}/{total})")
                
                can_move = item['can_move']
                can_rotate = item['can_rotate']
                can_scale = item['can_scale']
                current_loc = item['current_loc']
                current_rot = item['current_rot']
                current_scale = item['current_scale']
                
                new_loc = current_loc
                new_rot = current_rot
                new_scale = current_scale

                # ===== 1. 缩放 =====
                if has_scale:
                    # 缩放物体自身
                    if can_scale:
                        new_scale = unreal.Vector(
                            current_scale.x * params.scale.x,
                            current_scale.y * params.scale.y,
                            current_scale.z * params.scale.z
                        )
                    
                    # 如果启用"缩放影响位置"，则缩放位置
                    if params.scale_affects_location and can_move:
                        new_loc = scale_vector_around_pivot(current_loc, pivot, params.scale)

                # ===== 2. 旋转 =====
                if has_rotation:
                    # 旋转物体位置（围绕pivot旋转）
                    if can_move:
                        new_loc = rotate_vector_around_pivot(new_loc, pivot, params.rotate)
                    
                    # 旋转物体朝向
                    if can_rotate:
                        # 组合旋转：先应用物体当前旋转，再叠加新旋转
                        combined_quat = params.rotate.quaternion() * current_rot.quaternion()
                        new_rot = combined_quat.rotator()

                # ===== 3. 平移 =====
                if params.do_translate and can_move:
                    new_loc = new_loc + params.translate

                # ===== 应用变换 =====
                try:
                    if can_move:
                        actor.set_actor_location(new_loc, False, True)
                    if can_rotate and has_rotation:
                        actor.set_actor_rotation(new_rot, False)
                    if can_scale and has_scale:
                        # 尝试多种缩放方法以兼容蓝图
                        try:
                            actor.set_actor_scale3d(new_scale)
                        except:
                            # 某些蓝图可能需要通过Root Component设置缩放
                            root_comp = actor.get_editor_property("root_component")
                            if root_comp:
                                root_comp.set_editor_property("relative_scale3d", new_scale)
                except Exception as e:
                    unreal.log_warning(f"[Transform] 应用失败: {actor.get_actor_label()} -> {e}")

                # ===== 详细日志 =====
                if params.verbose_log:
                    ops = []
                    if params.do_translate and can_move: 
                        ops.append("移动")
                    if has_rotation and can_rotate: 
                        ops.append("旋转")
                    if has_scale and can_scale: 
                        ops.append("缩放")
                    if ops:
                        unreal.log(f"[✓] {actor.get_actor_label()} | {cls_name} | {', '.join(ops)}")

    # 刷新视口
    if params.refresh_viewport:
        try:
            unreal.EditorLevelLibrary.editor_set_game_view(False)
            unreal.LevelEditorSubsystem().editor_invalidate_viewports()
        except:
            try:
                unreal.EditorSubsystemLibrary.get_editor_subsystem(
                    unreal.UnrealEditorSubsystem
                ).redraw_all_viewports()
            except Exception as e:
                unreal.log_warning(f"刷新视口失败: {e}")

    unreal.log("[LevelTransform] ✓ 变换完成，可使用 Ctrl+Z 撤销。")


# ============================================
# UI入口
# ============================================

def show_level_transform_dialog():
    params = LevelTransformParams()
    
    # 默认值
    params.execute_mode = 0
    params.do_translate = True
    params.do_rotate = True
    params.do_scale = True
    params.translate = unreal.Vector(0, 0, 0)
    params.rotate = unreal.Rotator(0, 0, 0)
    params.scale = unreal.Vector(1, 1, 1)
    params.rotation_pivot = unreal.Vector(0, 0, 0)
    params.scale_affects_location = True
    params.force_apply = False
    params.verbose_log = False
    params.refresh_viewport = True

    # 显示参数对话框
    options = unreal.EditorDialogLibraryObjectDetailsViewOptions()
    options.show_object_name = False
    options.allow_search = True

    result = unreal.EditorDialog.show_object_details_view(
        "关卡整体变换工具", 
        params, 
        options
    )

    if not result:
        unreal.log("用户取消操作。")
        return

    # 二次确认
    confirm = unreal.EditorDialog.show_message(
        "确认执行",
        f"即将执行整体变换操作：\n"
        f"• 旋转中心: {params.rotation_pivot}\n"
        f"• 移动: {params.translate if params.do_translate else '禁用'}\n"
        f"• 旋转: {params.rotate if params.do_rotate else '禁用'}\n"
        f"• 缩放: {params.scale if params.do_scale else '禁用'}\n\n"
        f"确定要继续吗？",
        unreal.AppMsgType.YES_NO
    )
    
    if confirm != unreal.AppReturnType.YES:
        unreal.log("用户取消执行。")
        return

    execute_level_transform(params)


# ============================================
# 主入口
# ============================================

if __name__ == "__main__":
    show_level_transform_dialog()
