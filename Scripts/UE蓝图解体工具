"""
@PLUGIN_INFO
id: UE_BLUEPRINT_DECOMPOSE_ADVANCED
name: UE蓝图全面解体工具_增强版
description: 全面解体蓝图Actor，提取所有类型的组件（静态网格体、骨骼网格体、灯光、贴花、音频、粒子等），保持材质和属性
category: 蓝图工具
favorite: true
usage: 选择要解体的蓝图Actor，运行脚本即可将蓝图解体为独立的组件Actor，保持所有材质和属性设置
@END_INFO

@PLUGIN_PARAMS
extract_static_mesh|bool|true||提取静态网格体|是否提取静态网格体组件
extract_skeletal_mesh|bool|true||提取骨骼网格体|是否提取骨骼网格体组件
extract_light|bool|true||提取灯光|是否提取各种灯光组件
extract_decal|bool|true||提取贴花|是否提取贴花组件
extract_audio|bool|true||提取音频|是否提取音频组件
extract_particle|bool|true||提取粒子|是否提取粒子系统组件
extract_camera|bool|true||提取摄像机|是否提取摄像机组件
extract_other|bool|true||提取其他组件|是否提取其他类型的组件
preserve_materials|bool|true||保持材质|是否保持原始材质设置
preserve_properties|bool|true||保持属性|是否保持组件属性设置
delete_original|bool|true||删除原始Actor|解体后是否删除原始蓝图Actor
@END_PARAMS
"""

import unreal
import time

def main():
    """主函数"""
    print("=== 🔧 UE蓝图全面解体工具_增强版 ===")
    
    # 获取参数值
    global extract_static_mesh, extract_skeletal_mesh, extract_light, extract_decal
    global extract_audio, extract_particle, extract_camera, extract_other
    global preserve_materials, preserve_properties, delete_original
    
    # 参数初始化
    try:
        extract_static_mesh
    except NameError:
        extract_static_mesh = True
    
    try:
        extract_skeletal_mesh
    except NameError:
        extract_skeletal_mesh = True
    
    try:
        extract_light
    except NameError:
        extract_light = True
    
    try:
        extract_decal
    except NameError:
        extract_decal = True
    
    try:
        extract_audio
    except NameError:
        extract_audio = True
    
    try:
        extract_particle
    except NameError:
        extract_particle = True
    
    try:
        extract_camera
    except NameError:
        extract_camera = True
    
    try:
        extract_other
    except NameError:
        extract_other = True
    
    try:
        preserve_materials
    except NameError:
        preserve_materials = True
    
    try:
        preserve_properties
    except NameError:
        preserve_properties = True
    
    try:
        delete_original
    except NameError:
        delete_original = True
    
    print("📋 脚本参数:")
    print(f"  - 提取静态网格体: {extract_static_mesh}")
    print(f"  - 提取骨骼网格体: {extract_skeletal_mesh}")
    print(f"  - 提取灯光: {extract_light}")
    print(f"  - 提取贴花: {extract_decal}")
    print(f"  - 提取音频: {extract_audio}")
    print(f"  - 提取粒子: {extract_particle}")
    print(f"  - 提取摄像机: {extract_camera}")
    print(f"  - 提取其他组件: {extract_other}")
    print(f"  - 保持材质: {preserve_materials}")
    print(f"  - 保持属性: {preserve_properties}")
    print(f"  - 删除原始Actor: {delete_original}")
    
    # 开始解体操作
    result = decompose_selected_blueprints()
    return result

def decompose_selected_blueprints():
    """解体选中的蓝图Actor"""
    try:
        start_time = time.time()
        
        # 获取选中的Actor
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        selected_actors = editor_actor_subsystem.get_selected_level_actors()
        
        if not selected_actors:
            print("❌ 请先选择要解体的蓝图Actor")
            return False
        
        total_actors = len(selected_actors)
        print(f"🔍 找到 {total_actors} 个选中的Actor...")
        
        processed_actors = 0
        total_components = 0
        
        # 处理每个Actor
        for actor_idx, actor in enumerate(selected_actors):
            if not actor:
                continue
            
            # 显示进度
            if actor_idx % 10 == 0 and actor_idx > 0:
                print(f"  进度: {actor_idx}/{total_actors}")
            
            actor_name = actor.get_name()
            success_count = 0
            
            # 提取各种类型的组件
            if extract_static_mesh:
                success_count += extract_static_mesh_components(actor, preserve_materials, preserve_properties)
            
            if extract_skeletal_mesh:
                success_count += extract_skeletal_mesh_components(actor, preserve_materials, preserve_properties)
            
            if extract_light:
                success_count += extract_light_components(actor, preserve_properties)
            
            if extract_decal:
                success_count += extract_decal_components(actor, preserve_properties)
            
            if extract_audio:
                success_count += extract_audio_components(actor, preserve_properties)
            
            if extract_particle:
                success_count += extract_particle_components(actor, preserve_properties)
            
            if extract_camera:
                success_count += extract_camera_components(actor, preserve_properties)
            
            if extract_other:
                success_count += extract_other_components(actor, preserve_materials, preserve_properties)
            
            # 如果成功提取了组件，删除原始Actor
            if success_count > 0 and delete_original:
                try:
                    editor_actor_subsystem.destroy_actor(actor)
                    processed_actors += 1
                    total_components += success_count
                except Exception as e:
                    print(f"⚠️  删除原始Actor失败: {actor_name} - {str(e)}")
        
        # 显示结果
        elapsed_time = time.time() - start_time
        
        if processed_actors > 0:
            speed = total_components / elapsed_time if elapsed_time > 0 else 0
            print(f"✅ 解体完成：处理了 {processed_actors} 个Actor，提取了 {total_components} 个组件")
            print(f"📊 用时 {elapsed_time:.2f}秒，平均速度 {speed:.1f} 个组件/秒")
            
            # 自动组合提取的组件
            print("🔗 自动组合提取的组件...")
            group_extracted_components()
            
            return True
        else:
            print("❌ 没有找到可解体的组件")
            return False
            
    except Exception as e:
        print(f"❌ 解体过程出错: {str(e)}")
        return False

def extract_static_mesh_components(actor, preserve_materials, preserve_properties):
    """提取静态网格体组件"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.StaticMeshComponent)
        
        for comp_idx, component in enumerate(components):
            if not component or not component.static_mesh:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                mesh_asset = component.static_mesh
                
                # 创建新的静态网格体Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.StaticMeshActor,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor or not new_actor.static_mesh_component:
                    continue
                
                # 设置网格体
                new_actor.static_mesh_component.set_static_mesh(mesh_asset)
                
                # 保持材质
                if preserve_materials:
                    material_count = component.get_num_materials()
                    for i in range(material_count):
                        material = component.get_material(i)
                        if material:
                            new_actor.static_mesh_component.set_material(i, material)
                
                # 保持属性
                if preserve_properties:
                    new_actor.static_mesh_component.set_world_scale3d(world_transform.scale3d)
                    new_actor.static_mesh_component.set_collision_enabled(component.get_collision_enabled())
                    new_actor.static_mesh_component.set_cast_shadow(component.cast_shadow)
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_StaticMesh_{comp_idx}")
                
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取静态网格体组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理静态网格体组件失败: {str(e)}")
    
    return success_count

def extract_skeletal_mesh_components(actor, preserve_materials, preserve_properties):
    """提取骨骼网格体组件"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.SkeletalMeshComponent)
        
        for comp_idx, component in enumerate(components):
            if not component or not component.skeletal_mesh:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                mesh_asset = component.skeletal_mesh
                
                # 创建新的骨骼网格体Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.SkeletalMeshActor,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor or not new_actor.skeletal_mesh_component:
                    continue
                
                # 设置网格体
                new_actor.skeletal_mesh_component.set_skeletal_mesh(mesh_asset)
                
                # 保持材质
                if preserve_materials:
                    material_count = component.get_num_materials()
                    for i in range(material_count):
                        material = component.get_material(i)
                        if material:
                            new_actor.skeletal_mesh_component.set_material(i, material)
                
                # 保持属性
                if preserve_properties:
                    new_actor.skeletal_mesh_component.set_world_scale3d(world_transform.scale3d)
                    new_actor.skeletal_mesh_component.set_collision_enabled(component.get_collision_enabled())
                    new_actor.skeletal_mesh_component.set_cast_shadow(component.cast_shadow)
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_SkeletalMesh_{comp_idx}")
                
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取骨骼网格体组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理骨骼网格体组件失败: {str(e)}")
    
    return success_count

def extract_light_components(actor, preserve_properties):
    """提取灯光组件"""
    success_count = 0
    try:
        # 提取各种类型的灯光
        light_types = [
            (unreal.DirectionalLightComponent, unreal.DirectionalLight),
            (unreal.PointLightComponent, unreal.PointLight),
            (unreal.SpotLightComponent, unreal.SpotLight),
            (unreal.RectLightComponent, unreal.RectLight)
        ]
        
        for light_component_class, light_actor_class in light_types:
            components = actor.get_components_by_class(light_component_class)
            
            for comp_idx, component in enumerate(components):
                if not component:
                    continue
                
                try:
                    # 获取组件信息
                    world_transform = component.get_world_transform()
                    
                    # 创建新的灯光Actor
                    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                    new_actor = editor_actor_subsystem.spawn_actor_from_class(
                        light_actor_class,
                        world_transform.translation,
                        world_transform.rotation.rotator()
                    )
                    
                    if not new_actor:
                        continue
                    
                    # 保持属性
                    if preserve_properties:
                        # 获取灯光组件
                        light_component = new_actor.get_component_by_class(light_component_class)
                        if light_component:
                            # 复制灯光属性
                            if hasattr(component, 'intensity'):
                                light_component.intensity = component.intensity
                            if hasattr(component, 'light_color'):
                                light_component.light_color = component.light_color
                            if hasattr(component, 'attenuation_radius'):
                                light_component.attenuation_radius = component.attenuation_radius
                    
                    # 设置标签
                    light_type_name = light_component_class.__name__.replace('Component', '')
                    new_actor.set_actor_label(f"{actor.get_name()}_{light_type_name}_{comp_idx}")
                    
                    success_count += 1
                    
                except Exception as e:
                    print(f"⚠️  提取灯光组件失败: {str(e)}")
                    continue
    
    except Exception as e:
        print(f"⚠️  处理灯光组件失败: {str(e)}")
    
    return success_count

def extract_decal_components(actor, preserve_properties):
    """提取贴花组件"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.DecalComponent)
        
        for comp_idx, component in enumerate(components):
            if not component:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                
                # 创建新的贴花Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.DecalActor,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor:
                    continue
                
                # 保持属性
                if preserve_properties:
                    decal_component = new_actor.get_component_by_class(unreal.DecalComponent)
                    if decal_component and component.material:
                        decal_component.set_decal_material(component.material)
                        decal_component.set_world_scale3d(world_transform.scale3d)
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_Decal_{comp_idx}")
                
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取贴花组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理贴花组件失败: {str(e)}")
    
    return success_count

def extract_audio_components(actor, preserve_properties):
    """提取音频组件"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.AudioComponent)
        
        for comp_idx, component in enumerate(components):
            if not component:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                
                # 创建新的音频Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.AmbientSound,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor:
                    continue
                
                # 保持属性
                if preserve_properties:
                    audio_component = new_actor.get_component_by_class(unreal.AudioComponent)
                    if audio_component and component.sound:
                        audio_component.set_sound(component.sound)
                        audio_component.set_volume_multiplier(component.volume_multiplier)
                        audio_component.set_pitch_multiplier(component.pitch_multiplier)
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_Audio_{comp_idx}")
                
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取音频组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理音频组件失败: {str(e)}")
    
    return success_count

def extract_particle_components(actor, preserve_properties):
    """提取粒子系统组件"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.ParticleSystemComponent)
        
        for comp_idx, component in enumerate(components):
            if not component:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                
                # 创建新的粒子系统Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.ParticleSystemActor,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor:
                    continue
                
                # 保持属性
                if preserve_properties:
                    particle_component = new_actor.get_component_by_class(unreal.ParticleSystemComponent)
                    if particle_component and component.template:
                        particle_component.set_template(component.template)
                        particle_component.set_world_scale3d(world_transform.scale3d)
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_Particle_{comp_idx}")
                
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取粒子组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理粒子组件失败: {str(e)}")
    
    return success_count

def extract_camera_components(actor, preserve_properties):
    """提取摄像机组件（只提取摄像机本身，不提取其中的模型）"""
    success_count = 0
    try:
        components = actor.get_components_by_class(unreal.CameraComponent)
        
        for comp_idx, component in enumerate(components):
            if not component:
                continue
            
            try:
                # 获取组件信息
                world_transform = component.get_world_transform()
                
                # 创建新的摄像机Actor
                editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                new_actor = editor_actor_subsystem.spawn_actor_from_class(
                    unreal.CameraActor,
                    world_transform.translation,
                    world_transform.rotation.rotator()
                )
                
                if not new_actor:
                    continue
                
                # 保持摄像机属性
                if preserve_properties:
                    camera_component = new_actor.get_component_by_class(unreal.CameraComponent)
                    if camera_component:
                        # 复制摄像机的基本属性
                        camera_component.field_of_view = component.field_of_view
                        camera_component.aspect_ratio = component.aspect_ratio
                        
                        # 复制更多摄像机属性（如果存在）
                        if hasattr(component, 'ortho_width'):
                            camera_component.ortho_width = component.ortho_width
                        if hasattr(component, 'ortho_near_clip_plane'):
                            camera_component.ortho_near_clip_plane = component.ortho_near_clip_plane
                        if hasattr(component, 'ortho_far_clip_plane'):
                            camera_component.ortho_far_clip_plane = component.ortho_far_clip_plane
                        if hasattr(component, 'projection_mode'):
                            camera_component.projection_mode = component.projection_mode
                        if hasattr(component, 'use_field_of_view_for_lod'):
                            camera_component.use_field_of_view_for_lod = component.use_field_of_view_for_lod
                        if hasattr(component, 'lock_to_hmd'):
                            camera_component.lock_to_hmd = component.lock_to_hmd
                        if hasattr(component, 'use_pawn_control_rotation'):
                            camera_component.use_pawn_control_rotation = component.use_pawn_control_rotation
                
                # 设置标签
                new_actor.set_actor_label(f"{actor.get_name()}_Camera_{comp_idx}")
                
                print(f"📷 提取摄像机组件: {actor.get_name()}_Camera_{comp_idx}")
                success_count += 1
                
            except Exception as e:
                print(f"⚠️  提取摄像机组件失败: {str(e)}")
                continue
    
    except Exception as e:
        print(f"⚠️  处理摄像机组件失败: {str(e)}")
    
    return success_count

def extract_other_components(actor, preserve_materials, preserve_properties):
    """提取其他类型的组件"""
    success_count = 0
    try:
        # 提取其他网格体组件
        other_mesh_types = [
            (unreal.InstancedStaticMeshComponent, unreal.InstancedStaticMeshActor),
            (unreal.MeshComponent, unreal.StaticMeshActor)  # 回退到静态网格体
        ]
        
        for mesh_component_class, mesh_actor_class in other_mesh_types:
            components = actor.get_components_by_class(mesh_component_class)
            
            for comp_idx, component in enumerate(components):
                if not component:
                    continue
                
                try:
                    # 获取组件信息
                    world_transform = component.get_world_transform()
                    
                    # 创建新的Actor
                    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
                    new_actor = editor_actor_subsystem.spawn_actor_from_class(
                        mesh_actor_class,
                        world_transform.translation,
                        world_transform.rotation.rotator()
                    )
                    
                    if not new_actor:
                        continue
                    
                    # 设置网格体（如果适用）
                    if hasattr(component, 'static_mesh') and component.static_mesh:
                        mesh_component = new_actor.get_component_by_class(unreal.StaticMeshComponent)
                        if mesh_component:
                            mesh_component.set_static_mesh(component.static_mesh)
                    
                    # 保持材质
                    if preserve_materials:
                        material_count = component.get_num_materials()
                        mesh_component = new_actor.get_component_by_class(unreal.MeshComponent)
                        if mesh_component:
                            for i in range(material_count):
                                material = component.get_material(i)
                                if material:
                                    mesh_component.set_material(i, material)
                    
                    # 保持属性
                    if preserve_properties:
                        mesh_component = new_actor.get_component_by_class(unreal.MeshComponent)
                        if mesh_component:
                            mesh_component.set_world_scale3d(world_transform.scale3d)
                            mesh_component.set_collision_enabled(component.get_collision_enabled())
                            mesh_component.set_cast_shadow(component.cast_shadow)
                    
                    # 设置标签
                    mesh_type_name = mesh_component_class.__name__.replace('Component', '')
                    new_actor.set_actor_label(f"{actor.get_name()}_{mesh_type_name}_{comp_idx}")
                    
                    success_count += 1
                    
                except Exception as e:
                    print(f"⚠️  提取其他组件失败: {str(e)}")
                    continue
    
    except Exception as e:
        print(f"⚠️  处理其他组件失败: {str(e)}")
    
    return success_count

def group_extracted_components():
    """自动组合提取的组件"""
    try:
        # 获取所有选中的Actor
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        selected_actors = editor_actor_subsystem.get_selected_level_actors()
        
        if not selected_actors:
            print("⚠️  没有选中的Actor进行组合")
            return False
        
        # 按原始Actor名称分组
        actor_groups = {}
        for actor in selected_actors:
            if not actor:
                continue
            
            actor_name = actor.get_name()
            # 检查是否是解体后的组件（包含下划线和组件类型）
            if '_StaticMesh_' in actor_name or '_SkeletalMesh_' in actor_name or '_DirectionalLight_' in actor_name or '_PointLight_' in actor_name or '_SpotLight_' in actor_name or '_RectLight_' in actor_name or '_Decal_' in actor_name or '_Audio_' in actor_name or '_Particle_' in actor_name or '_Camera_' in actor_name or '_InstancedStaticMesh_' in actor_name:
                # 提取原始Actor名称
                base_name = actor_name.split('_')[0]
                if base_name not in actor_groups:
                    actor_groups[base_name] = []
                actor_groups[base_name].append(actor)
        
        if not actor_groups:
            print("⚠️  没有找到解体后的组件进行组合")
            return False
        
        # 为每个组创建组合
        grouped_count = 0
        for base_name, actors in actor_groups.items():
            if len(actors) <= 1:
                continue  # 只有一个组件不需要组合
            
            try:
                # 选择该组的所有Actor
                editor_actor_subsystem.set_selected_level_actors(actors)
                
                # 创建组合
                # 注意：UE5.3中可能需要使用不同的API来创建组合
                # 这里使用一个通用的方法
                print(f"🔗 组合 {base_name} 的 {len(actors)} 个组件...")
                
                # 尝试使用UE的编辑器命令来组合
                try:
                    # 使用编辑器子系统来执行组合操作
                    unreal.EditorLevelLibrary.set_selected_level_actors(actors)
                    # 这里可能需要调用UE的编辑器命令，但UE5.3的Python API可能不直接支持
                    # 作为替代方案，我们可以创建一个父Actor来组织这些组件
                    create_parent_actor_for_group(actors, base_name)
                    grouped_count += 1
                except Exception as e:
                    print(f"⚠️  组合 {base_name} 失败: {str(e)}")
                    continue
                
            except Exception as e:
                print(f"⚠️  处理组 {base_name} 失败: {str(e)}")
                continue
        
        if grouped_count > 0:
            print(f"✅ 成功组合了 {grouped_count} 个组件组")
        else:
            print("⚠️  没有成功组合任何组件组")
        
        return grouped_count > 0
        
    except Exception as e:
        print(f"❌ 自动组合失败: {str(e)}")
        return False

def create_parent_actor_for_group(actors, group_name):
    """为组件组创建父Actor"""
    try:
        if not actors:
            return None
        
        # 计算组的位置（使用第一个Actor的位置）
        first_actor = actors[0]
        group_location = first_actor.get_actor_location()
        
        # 创建一个空的Actor作为父级
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        parent_actor = editor_actor_subsystem.spawn_actor_from_class(
            unreal.Actor,
            group_location
        )
        
        if not parent_actor:
            return None
        
        # 设置父Actor的标签
        parent_actor.set_actor_label(f"{group_name}_Group")
        
        # 将子Actor附加到父Actor
        for actor in actors:
            try:
                actor.attach_to_actor(parent_actor, unreal.AttachmentRule.KEEP_WORLD)
            except Exception as e:
                print(f"⚠️  附加Actor失败: {str(e)}")
                continue
        
        print(f"✅ 创建了父Actor {group_name}_Group 并附加了 {len(actors)} 个子组件")
        return parent_actor
        
    except Exception as e:
        print(f"❌ 创建父Actor失败: {str(e)}")
        return None

if __name__ == "__main__":
    main()
