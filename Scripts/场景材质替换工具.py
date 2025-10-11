"""
@PLUGIN_INFO
id: 9M1pP4sS
name: 场景材质替换工具
description: 批量替换场景内所有可替换材质的物体为指定材质，支持多种材质类型和过滤选项。⚠️ 重要：此操作无法撤回，请确保已保存场景！
category: 材质工具
favorite: true
usage: 选择目标材质，设置替换选项，然后运行脚本即可批量替换场景内所有物体的材质。⚠️ 重要：此操作无法撤回，请确保已保存场景！
@END_INFO

@PLUGIN_PARAMS
target_material|file|/Game/555/Materials/1.1|||选择要替换成的目标材质文件
replace_static_mesh|bool|true||替换静态网格体|是否替换静态网格体组件的材质
replace_skeletal_mesh|bool|true||替换骨骼网格体|是否替换骨骼网格体组件的材质
replace_instanced_static_mesh|bool|true||替换实例化静态网格体|是否替换实例化静态网格体组件的材质
replace_mesh_component|bool|true||替换网格体组件|是否替换其他网格体组件的材质
material_slot_index|int|0|0,10|材质槽索引|指定要替换的材质槽索引，0表示所有槽
use_world_outliner_filter|bool|false||使用世界大纲过滤器|是否只处理世界大纲中选中的Actor
@END_PARAMS
"""

import unreal
import time

def main():
    """主函数"""
    print("=== 🎨 场景材质替换工具 ===")
    
    # 获取参数值
    global target_material, replace_static_mesh, replace_skeletal_mesh
    global replace_instanced_static_mesh, replace_mesh_component, material_slot_index
    global use_world_outliner_filter
    
    # 参数初始化
    try:
        target_material
    except NameError:
        target_material = ""
    
    try:
        replace_static_mesh
    except NameError:
        replace_static_mesh = True
    
    try:
        replace_skeletal_mesh
    except NameError:
        replace_skeletal_mesh = True
    
    try:
        replace_instanced_static_mesh
    except NameError:
        replace_instanced_static_mesh = True
    
    try:
        replace_mesh_component
    except NameError:
        replace_mesh_component = True
    
    try:
        material_slot_index
    except NameError:
        material_slot_index = 0
    
    try:
        use_world_outliner_filter
    except NameError:
        use_world_outliner_filter = False
    
    print("📋 脚本参数:")
    print(f"  - 目标材质: {target_material}")
    print(f"  - 替换静态网格体: {replace_static_mesh}")
    print(f"  - 替换骨骼网格体: {replace_skeletal_mesh}")
    print(f"  - 替换实例化静态网格体: {replace_instanced_static_mesh}")
    print(f"  - 替换网格体组件: {replace_mesh_component}")
    print(f"  - 材质槽索引: {material_slot_index}")
    print(f"  - 使用世界大纲过滤器: {use_world_outliner_filter}")
    
    # 检查目标材质
    if not target_material:
        print("❌ 错误: 未指定目标材质")
        return
    
    # 加载目标材质
    target_material_obj = unreal.EditorAssetLibrary.load_asset(target_material)
    if not target_material_obj:
        print(f"❌ 错误: 无法加载目标材质 {target_material}")
        return
    
    print(f"✅ 目标材质加载成功: {target_material_obj.get_name()}")
    
    # 获取场景中的Actor
    print("🔍 获取场景Actor列表...")
    if use_world_outliner_filter:
        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        print(f"📋 处理世界大纲中选中的 {len(actors)} 个Actor")
    else:
        actors = unreal.EditorLevelLibrary.get_all_level_actors()
        print(f"📋 处理场景中所有 {len(actors)} 个Actor")
    
    if not actors:
        print("❌ 场景中没有找到Actor")
        return
    
    print(f"✅ 找到 {len(actors)} 个Actor")
    
    # 开始批量替换材质
    print("🎨 开始批量替换材质...")
    start_time = time.time()
    processed_components = 0
    
    for i, actor in enumerate(actors):
        try:
            # 处理静态网格体组件
            if replace_static_mesh:
                static_mesh_components = actor.get_components_by_class(unreal.StaticMeshComponent)
                for component in static_mesh_components:
                    if replace_static_mesh_materials(component, target_material_obj, material_slot_index):
                        processed_components += 1
            
            # 处理骨骼网格体组件
            if replace_skeletal_mesh:
                skeletal_mesh_components = actor.get_components_by_class(unreal.SkeletalMeshComponent)
                for component in skeletal_mesh_components:
                    if replace_skeletal_mesh_materials(component, target_material_obj, material_slot_index):
                        processed_components += 1
            
            # 处理实例化静态网格体组件
            if replace_instanced_static_mesh:
                instanced_mesh_components = actor.get_components_by_class(unreal.InstancedStaticMeshComponent)
                for component in instanced_mesh_components:
                    if replace_instanced_static_mesh_materials(component, target_material_obj, material_slot_index):
                        processed_components += 1
            
            # 处理其他网格体组件
            if replace_mesh_component:
                mesh_components = actor.get_components_by_class(unreal.MeshComponent)
                for component in mesh_components:
                    if replace_mesh_component_materials(component, target_material_obj, material_slot_index):
                        processed_components += 1
            
            # 显示进度
            if (i + 1) % 5 == 0 or i == len(actors) - 1:
                print(f"  进度: {i + 1}/{len(actors)} ({processed_components} 个组件已替换)")
                
        except Exception as e:
            print(f"⚠️  处理Actor失败: {actor.get_name()} - {str(e)}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ 材质替换完成：{processed_components} 个组件，用时 {total_time:.2f}秒")
    if total_time > 0:
        print(f"📊 平均速度: {processed_components / total_time:.2f} 个/秒")
    
    # 保存更改
    print("💾 保存更改...")
    try:
        # 使用新的API保存级别
        level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if level_subsystem:
            level_subsystem.save_current_level()
            print("✅ 保存完成")
        else:
            print("⚠️  无法获取LevelEditorSubsystem，跳过保存")
    except Exception as e:
        print(f"⚠️  保存失败: {str(e)}")
    
    print("🎉 === 材质替换完成 ===")

def replace_static_mesh_materials(component, target_material, slot_index):
    """替换静态网格体组件的材质"""
    try:
        material_count = component.get_num_materials()
        print(f"🔍 静态网格体材质数量: {material_count}")
        
        if slot_index == 0:
            # 替换所有材质槽
            if material_count > 0:
                for i in range(material_count):
                    print(f"🎨 替换材质槽 {i}")
                    component.set_material(i, target_material)
                return True
        else:
            # 替换指定材质槽
            if slot_index <= material_count:
                print(f"🎨 替换材质槽 {slot_index}")
                component.set_material(slot_index, target_material)
                return True
            else:
                print(f"⚠️  材质槽 {slot_index} 不存在，组件只有 {material_count} 个材质槽")
                return False
    except Exception as e:
        print("⚠️  替换静态网格体材质失败: " + str(e))
    
    return False

def replace_skeletal_mesh_materials(component, target_material, slot_index):
    """替换骨骼网格体组件的材质"""
    try:
        material_count = component.get_num_materials()
        print(f"🔍 骨骼网格体材质数量: {material_count}")
        
        if slot_index == 0:
            # 替换所有材质槽
            if material_count > 0:
                for i in range(material_count):
                    print(f"🎨 替换材质槽 {i}")
                    component.set_material(i, target_material)
                return True
        else:
            # 替换指定材质槽
            if slot_index <= material_count:
                print(f"🎨 替换材质槽 {slot_index}")
                component.set_material(slot_index, target_material)
                return True
            else:
                print(f"⚠️  材质槽 {slot_index} 不存在，组件只有 {material_count} 个材质槽")
                return False
    except Exception as e:
        print("⚠️  替换骨骼网格体材质失败: " + str(e))
    
    return False

def replace_instanced_static_mesh_materials(component, target_material, slot_index):
    """替换实例化静态网格体组件的材质"""
    try:
        material_count = component.get_num_materials()
        print(f"🔍 实例化静态网格体材质数量: {material_count}")
        
        if slot_index == 0:
            # 替换所有材质槽
            if material_count > 0:
                for i in range(material_count):
                    print(f"🎨 替换材质槽 {i}")
                    component.set_material(i, target_material)
                return True
        else:
            # 替换指定材质槽
            if slot_index <= material_count:
                print(f"🎨 替换材质槽 {slot_index}")
                component.set_material(slot_index, target_material)
                return True
            else:
                print(f"⚠️  材质槽 {slot_index} 不存在，组件只有 {material_count} 个材质槽")
                return False
    except Exception as e:
        print("⚠️  替换实例化静态网格体材质失败: " + str(e))
    
    return False

def replace_mesh_component_materials(component, target_material, slot_index):
    """替换网格体组件的材质"""
    try:
        material_count = component.get_num_materials()
        print(f"🔍 网格体组件材质数量: {material_count}")
        
        if slot_index == 0:
            # 替换所有材质槽
            if material_count > 0:
                for i in range(material_count):
                    print(f"🎨 替换材质槽 {i}")
                    component.set_material(i, target_material)
                return True
        else:
            # 替换指定材质槽
            if slot_index <= material_count:
                print(f"🎨 替换材质槽 {slot_index}")
                component.set_material(slot_index, target_material)
                return True
            else:
                print(f"⚠️  材质槽 {slot_index} 不存在，组件只有 {material_count} 个材质槽")
                return False
    except Exception as e:
        print("⚠️  替换网格体组件材质失败: " + str(e))
    
    return False

if __name__ == "__main__":
    main()
