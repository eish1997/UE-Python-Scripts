"""
@PLUGIN_INFO
id: 7K9mN2pQ
name: 参数测试脚本
description: 测试所有类型参数的功能，包括字符串、数字、布尔值、文件、文件夹等
category: 测试工具
favorite: true
@END_INFO

@PLUGIN_PARAMS
test_string|string|预设0||文本输入|这是一个字符串类型的参数，用于测试文本输入功能
test_int|int|123|50,1000|整数输入|这是一个整数类型的参数，用于测试数字输入功能
test_float|float|5.4|0.0,10.0|浮点数输入|这是一个浮点数类型的参数，用于测试小数输入功能
test_bool|bool|false||开关选项|这是一个布尔类型的参数，用于测试开关功能
test_file|file|/Game/Assets/Env/SceneName/网格体/Box_6E785621_01_01_01_01_01_01_01.Box_6E785621_01_01_01_01_01_01_01||文件选择|这是一个文件类型的参数，用于测试📁和📂按钮功能
test_folder|folder|/Game/BP||文件夹选择|这是一个文件夹类型的参数，用于测试📁和📂按钮功能
test_select|select|选项1|选项1,选项2,选项3|下拉选择|这是一个选择类型的参数，用于测试下拉菜单功能
test_slider|slider|0.36|0.0,1.0|滑块调节|这是一个滑块类型的参数，用于测试滑块控件功能
@END_PARAMS
"""


import unreal

def main():
    """主函数：测试所有参数类型"""
    print("=" * 50)
    print("🧪 参数测试脚本开始执行")
    print("=" * 50)
    
    # 获取参数值
    try:
        # 字符串参数
        test_string = globals().get('test_string', '默认字符串')
        print(f"📝 字符串参数: {test_string}")
        print(f"   类型: {type(test_string)}")
        print(f"   长度: {len(test_string)}")
        
        # 整数参数
        test_int = globals().get('test_int', 0)
        print(f"🔢 整数参数: {test_int}")
        print(f"   类型: {type(test_int)}")
        print(f"   是否为偶数: {test_int % 2 == 0}")
        
        # 浮点数参数
        test_float = globals().get('test_float', 0.0)
        print(f"📊 浮点数参数: {test_float}")
        print(f"   类型: {type(test_float)}")
        print(f"   四舍五入: {round(test_float, 2)}")
        
        # 布尔参数
        test_bool = globals().get('test_bool', False)
        print(f"✅ 布尔参数: {test_bool}")
        print(f"   类型: {type(test_bool)}")
        print(f"   取反: {not test_bool}")
        
        # 文件参数
        test_file = globals().get('test_file', '')
        print(f"📄 文件参数: {test_file}")
        print(f"   类型: {type(test_file)}")
        if test_file:
            print(f"   文件路径: {test_file}")
            print(f"   是否为UE路径: {test_file.startswith('/Game/')}")
        
        # 文件夹参数
        test_folder = globals().get('test_folder', '')
        print(f"📁 文件夹参数: {test_folder}")
        print(f"   类型: {type(test_folder)}")
        if test_folder:
            print(f"   文件夹路径: {test_folder}")
            print(f"   是否为UE路径: {test_folder.startswith('/Game/')}")
        
        # 选择参数
        test_select = globals().get('test_select', '')
        print(f"📋 选择参数: {test_select}")
        print(f"   类型: {type(test_select)}")
        print(f"   选择值: {test_select}")
        
        # 滑块参数
        test_slider = globals().get('test_slider', 0)
        print(f"🎚️ 滑块参数: {test_slider}")
        print(f"   类型: {type(test_slider)}")
        print(f"   百分比: {test_slider}%")
        
        print("\n" + "=" * 50)
        print("✅ 所有参数测试完成！")
        print("=" * 50)
        
        # 测试参数组合使用
        print("\n🔧 参数组合测试:")
        if test_bool and test_int > 0:
            print(f"   条件满足: 布尔为True且整数大于0")
            print(f"   计算结果: {test_int * test_float}")
        
        if test_file and test_folder:
            print(f"   文件路径: {test_file}")
            print(f"   文件夹路径: {test_folder}")
            print(f"   路径匹配: {test_file.startswith(test_folder)}")
        
        # 测试UE API调用
        print("\n🎮 UE API测试:")
        try:
            # 测试列出文件夹内容
            if test_folder:
                assets = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(test_folder, recursive=False)
                print(f"   📁 文件夹 '{test_folder}' 包含 {len(assets)} 个资产")
                for i, asset in enumerate(assets[:3]):  # 只显示前3个
                    print(f"      {i+1}. {asset.asset_name}")
                if len(assets) > 3:
                    print(f"      ... 还有 {len(assets) - 3} 个资产")
            
            # 测试文件路径验证
            if test_file:
                print(f"   📄 文件路径: {test_file}")
                if test_file.startswith('/Game/'):
                    print(f"   ✅ 文件路径格式正确")
                else:
                    print(f"   ⚠️ 文件路径不是UE格式")
                    
        except Exception as e:
            print(f"   ❌ UE API调用出错: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 参数测试脚本执行完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 参数测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
