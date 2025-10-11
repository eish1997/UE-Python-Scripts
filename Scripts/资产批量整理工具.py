"""
@PLUGIN_INFO
id: 0N2qQ5tT
name: 资产批量整理工具
description: 高效的批量资产整理工具，支持自动分类、批量移动和重命名处理，集成内容浏览器路径选择功能，支持多种参数类型和交互方式
category: 资产管理
favorite: true
usage: 使用📁按钮从内容浏览器选择路径，📂按钮手动输入路径，设置批处理数量和重命名选项，然后运行脚本即可自动整理资产
@END_INFO

@PLUGIN_PARAMS
target_base_path|folder|/Game/555||目标路径|使用📁按钮从内容浏览器选择目标文件夹，或使用📂按钮手动输入路径
batch_size|int|100|50,500|批处理数量|控制每次处理的资产数量，范围50-500
enable_rename|bool|true||自动重命名|当发现同名资产时是否自动重命名
scan_path|folder|/Game||扫描路径|使用📁按钮选择要扫描的文件夹，或使用📂按钮手动输入路径
use_batch_operations|bool|true||批量操作|是否使用批量操作API提高处理效率
@END_PARAMS
"""

import unreal
import time

def main():
    # 获取参数值
    global target_base_path, batch_size, enable_rename, scan_path, use_batch_operations
    
    # 参数初始化
    try:
        target_base_path
    except NameError:
        target_base_path = "/Game/Assets/Env/SceneName"
    
    try:
        batch_size
    except NameError:
        batch_size = 100
    
    try:
        enable_rename
    except NameError:
        enable_rename = True
    
    try:
        scan_path
    except NameError:
        scan_path = "/Game"
    
    try:
        use_batch_operations
    except NameError:
        use_batch_operations = True
    
    # @PROGRESS: 开始批量操作模式...
    print("=== 🚀 批量操作资产整理工具启动 ===")
    print("目标路径: " + target_base_path)
    print("扫描路径: " + scan_path)
    print("批量操作: " + ("开启" if use_batch_operations else "关闭"))
    
    # 禁用自动保存和实时更新
    print("\n⚡ 正在禁用实时保存和更新...")
    disable_realtime_operations()
    
    try:
        start_time = time.time()
        
        # 快速扫描
        # @PROGRESS: 快速扫描资产中...
        print("🔍 扫描资产...")
        scan_start = time.time()
        categorized_assets = scan_assets_fast(scan_path)
        scan_time = time.time() - scan_start
        
        total_to_process = sum(len(assets) for assets in categorized_assets.values())
        
        if total_to_process == 0:
            print("没有需要整理的资产")
            return
        
        print("✅ 扫描完成：" + str(total_to_process) + " 个资产，用时 " + str(scan_time) + "秒")
        for category, assets in categorized_assets.items():
            if assets:
                print("  " + category + ": " + str(len(assets)) + " 个")
        
        # 使用批量移动API
        # @PROGRESS: 开始批量移动操作...
        print("\n🚀 开始批量移动 " + str(total_to_process) + " 个资产...")
        move_start = time.time()
        
        if use_batch_operations:
            processed_count = batch_move_all_assets(categorized_assets)
        else:
            processed_count = move_assets_individually(categorized_assets)
        
        move_time = time.time() - move_start
        print("✅ 移动完成：" + str(processed_count) + " 个资产，用时 " + str(move_time) + "秒")
        print("📊 移动速度: " + str(processed_count / move_time) + " 个/秒")
        
        # 批量保存
        # @PROGRESS: 保存更改中...
        print("\n💾 保存更改...")
        save_start = time.time()
        batch_save_all()
        save_time = time.time() - save_start
        print("✅ 保存完成，用时 " + str(save_time) + "秒")
        
        # 清理重定向器
        # @PROGRESS: 清理重定向器中...
        print("\n🧹 清理重定向器...")
        cleanup_start = time.time()
        redirector_count = cleanup_redirectors()
        cleanup_time = time.time() - cleanup_start
        
        total_time = time.time() - start_time
        
        print("\n🎉 === 批量整理完成 ===")
        print("✅ 处理资产: " + str(processed_count) + " 个")
        print("🧹 清理重定向: " + str(redirector_count) + " 个")
        print("⚡ 总用时: " + str(total_time) + " 秒")
        print("📊 平均速度: " + str(processed_count / total_time) + " 个/秒")
        
        print("\n📈 详细分析:")
        print("  扫描: " + str(scan_time) + "秒 (" + str(scan_time/total_time*100) + "%)")
        print("  移动: " + str(move_time) + "秒 (" + str(move_time/total_time*100) + "%)")
        print("  保存: " + str(save_time) + "秒 (" + str(save_time/total_time*100) + "%)")
        print("  清理: " + str(cleanup_time) + "秒 (" + str(cleanup_time/total_time*100) + "%)")
        
    except Exception as e:
        print("❌ 处理过程中出错: " + str(e))
    finally:
        # 恢复设置
        print("\n🔄 恢复实时操作设置...")
        restore_realtime_operations()

def disable_realtime_operations():
    """禁用实时操作以提高性能"""
    console_commands = [
        "Editor.MainFrame.SetTitleBarText",
        "Editor.LevelEditor.SetShowFPS false",
        "Editor.LevelEditor.SetShowStats false",
        "Editor.LevelEditor.SetShowViewportInfo false",
        "Editor.LevelEditor.SetShowViewportInfo false",
        "Editor.LevelEditor.SetShowViewportInfo false"
    ]
    
    try:
        success_count = 0
        for cmd in console_commands:
            try:
                unreal.EditorCommandLibrary.execute_command(cmd)
                success_count += 1
            except:
                pass
        
        print("✅ 禁用实时操作：" + str(success_count) + "/" + str(len(console_commands)) + " 个命令成功")
        
    except Exception as e:
        print("⚠️  禁用实时操作失败: " + str(e))

def scan_assets_fast(scan_path):
    """快速扫描资产并按类型分类"""
    categorized_assets = {
        "Meshes": [],
        "Materials": [],
        "Textures": [],
        "Blueprints": [],
        "Animations": [],
        "Audio": [],
        "Other": []
    }
    
    # 获取所有资产
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    all_assets = asset_registry.get_assets_by_path(scan_path, recursive=True)
    
    for asset in all_assets:
        # 获取资产路径
        if hasattr(asset, 'get_full_name'):
            asset_path = asset.get_full_name().split(' ')[1]
        else:
            asset_path = str(asset.package_name + '.' + asset.asset_name)
            
        if not asset_path.startswith('/Game/'):
            continue
            
        asset_class = str(asset.asset_class_path.asset_name)
        
        # 分类资产
        if asset_class == "StaticMesh":
            categorized_assets["Meshes"].append(asset_path)
        elif asset_class in ["Material", "MaterialInstanceConstant"]:
            categorized_assets["Materials"].append(asset_path)
        elif asset_class in ["Texture2D", "TextureCube"]:
            categorized_assets["Textures"].append(asset_path)
        elif asset_class == "Blueprint":
            categorized_assets["Blueprints"].append(asset_path)
        elif asset_class in ["AnimSequence", "AnimBlueprint"]:
            categorized_assets["Animations"].append(asset_path)
        elif asset_class in ["SoundWave", "SoundCue"]:
            categorized_assets["Audio"].append(asset_path)
        else:
            categorized_assets["Other"].append(asset_path)
    
    return categorized_assets

def batch_move_all_assets(categorized_assets):
    """批量移动所有资产"""
    all_move_operations = []
    
    for category, assets in categorized_assets.items():
        if not assets:
            continue
            
        folder_path = target_base_path + "/" + category
        print("📂 准备移动 " + category + ": " + str(len(assets)) + " 个资产")
        target_folder = target_base_path + "/" + category
        
        # 确保目标文件夹存在
        unreal.EditorAssetLibrary.make_directory(target_folder)
        
        for asset_path in assets:
            # 从路径中提取资产名称
            asset_name = asset_path.split('/')[-1]
            target_path = target_folder + "/" + asset_name
            
            # 检查目标路径是否已存在
            if unreal.EditorAssetLibrary.does_asset_exist(target_path):
                if enable_rename:
                    counter = 1
                    while unreal.EditorAssetLibrary.does_asset_exist(target_path):
                        new_path = target_folder + "/" + asset_name + "_" + str(counter).zfill(2)
                        target_path = new_path
                        counter += 1
                else:
                    continue
            
            all_move_operations.append((asset_path, target_path))
    
    print("📋 准备执行 " + str(len(all_move_operations)) + " 个移动操作")
    
    try:
        # 使用批量移动API
        processed_count = batch_move_assets(all_move_operations)
        return processed_count
    except Exception as e:
        print("⚠️  批量API失败，使用备用方法: " + str(e))
        return move_assets_individually(categorized_assets)

def batch_move_assets(move_operations):
    """批量移动资产"""
    processed_count = 0
    
    # 分批处理
    for i in range(0, len(move_operations), batch_size):
        current_batch = move_operations[i:i + batch_size]
        print("🔄 执行批次 " + str(i//batch_size + 1) + "/" + str((len(move_operations)-1)//batch_size + 1) + ": " + str(len(current_batch)) + " 个操作")
        
        # 批量重命名
        try:
            batch_rename_assets(current_batch)
        except Exception as e:
            print("⚠️  批量重命名失败: " + str(e))
        
        # 逐个移动
        success_count = 0
        for j, (source_path, target_path) in enumerate(current_batch):
            try:
                if unreal.EditorAssetLibrary.does_asset_exist(source_path):
                    unreal.EditorAssetLibrary.rename_asset(source_path, target_path)
                    success_count += 1
                    processed_count += 1
                
                if j % 10 == 0:  # 每10个显示一次进度
                    print("  进度: " + str(i + j + 1) + "/" + str(len(move_operations)) + " (" + str(success_count) + " 成功)")
            except Exception as e:
                print("移动失败: " + source_path + " -> " + target_path + " 错误: " + str(e))
    
    return processed_count

def batch_rename_assets(move_operations):
    """批量重命名资产"""
    # 这里可以添加批量重命名逻辑
    pass

def move_assets_individually(categorized_assets):
    """逐个移动资产（备用方法）"""
    processed_count = 0
    
    for category, assets in categorized_assets.items():
        if not assets:
            continue
            
        target_folder = target_base_path + "/" + category
        unreal.EditorAssetLibrary.make_directory(target_folder)
        
        for asset_path in assets:
            try:
                # 从路径中提取资产名称
                asset_name = asset_path.split('/')[-1]
                target_path = target_folder + "/" + asset_name
                
                if not unreal.EditorAssetLibrary.does_asset_exist(target_path):
                    unreal.EditorAssetLibrary.rename_asset(asset_path, target_path)
                    processed_count += 1
            except Exception as e:
                print("移动失败: " + asset_path + " 错误: " + str(e))
    
    return processed_count

def batch_save_all():
    """批量保存所有更改"""
    try:
        # 保存所有资产
        unreal.EditorAssetLibrary.save_loaded_assets()
        # 保存地图
        unreal.EditorLevelLibrary.save_current_level()
    except Exception as e:
        print("⚠️  批量保存失败，尝试备用方法: " + str(e))
        try:
            # 备用保存方法
            unreal.EditorAssetLibrary.save_directory("/Game")
        except Exception as e2:
            print("⚠️  备用保存也失败: " + str(e2))

def cleanup_redirectors():
    """清理重定向器"""
    redirector_count = 0
    
    try:
        # 获取所有重定向器
        redirector_paths = []
        all_assets = unreal.EditorAssetLibrary.list_assets("/Game", recursive=True)
        
        for asset_path in all_assets:
            if asset_path.endswith("_Redirector"):
                redirector_paths.append(asset_path)
        
        if redirector_paths:
            print("🗑️  批量删除 " + str(len(redirector_paths)) + " 个重定向器")
            
            # 批量删除重定向器
            for redirector_path in redirector_paths:
                try:
                    unreal.EditorAssetLibrary.delete_asset(redirector_path)
                    redirector_count += 1
                except Exception as e:
                    print("删除重定向器失败: " + redirector_path + " 错误: " + str(e))
        
    except Exception as e:
        print("⚠️  清理重定向失败: " + str(e))
    
    return redirector_count

def restore_realtime_operations():
    """恢复实时操作设置"""
    try:
        # 恢复设置
        console_commands = [
            "Editor.LevelEditor.SetShowFPS true",
            "Editor.LevelEditor.SetShowStats true",
            "Editor.LevelEditor.SetShowViewportInfo true"
        ]
        
        for cmd in console_commands:
            try:
                unreal.EditorCommandLibrary.execute_command(cmd)
            except:
                continue
        
        print("✅ 已恢复实时操作设置")
        
    except Exception as e:
        print("⚠️  恢复设置失败: " + str(e))

if __name__ == "__main__":
    main()