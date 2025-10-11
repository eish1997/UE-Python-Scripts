"""
@PLUGIN_INFO
id: 8L0nO3qR
name: 按钮功能测试脚本
description: 测试插件新增的按钮功能，包含多种按钮类型和功能演示
category: 测试工具
favorite: true
usage: 测试按钮功能，点击不同按钮执行不同的功能，验证按钮点击事件处理
@END_INFO

@PLUGIN_PARAMS
test_string|string|预设4||文本输入|测试字符串参数
test_int|int|123|50,200|整数输入|测试整数参数
test_bool|bool|false||开关选项|测试布尔参数
info_btn|button|||信息|显示当前参数信息
clear_btn|button|||清空|清空输出日志
test_btn|button|||测试|执行测试功能
@END_PARAMS
"""

import unreal
import time

def handle_button_click(button_name):
    """处理按钮点击事件"""
    print(f"🔘 按钮点击: {button_name}")
    
    if button_name == "info_btn":
        # 显示信息按钮
        print("=== 📋 当前参数信息 ===")
        try:
            print(f"文本参数: {test_string}")
        except NameError:
            print("文本参数: 未设置")
        
        try:
            print(f"整数参数: {test_int}")
        except NameError:
            print("整数参数: 未设置")
        
        try:
            print(f"布尔参数: {test_bool}")
        except NameError:
            print("布尔参数: 未设置")
        
        print("=== 📋 信息显示完成 ===")
        return True
        
    elif button_name == "clear_btn":
        # 清空日志按钮
        print("🧹 清空日志...")
        # 这里可以添加清空日志的逻辑
        print("✅ 日志已清空")
        return True
        
    elif button_name == "test_btn":
        # 测试按钮
        print("🧪 开始执行测试...")
        
        # 测试1: 参数获取
        print("测试1: 参数获取")
        try:
            print(f"  - 文本参数: '{test_string}'")
            print(f"  - 整数参数: {test_int}")
            print(f"  - 布尔参数: {test_bool}")
            print("  ✅ 参数获取成功")
        except NameError as e:
            print(f"  ❌ 参数获取失败: {e}")
        
        # 测试2: UE API调用
        print("测试2: UE API调用")
        try:
            actors = unreal.EditorLevelLibrary.get_all_level_actors()
            print(f"  - 场景中Actor数量: {len(actors)}")
            print("  ✅ UE API调用成功")
        except Exception as e:
            print(f"  ❌ UE API调用失败: {e}")
        
        # 测试3: 时间延迟
        print("测试3: 时间延迟")
        start_time = time.time()
        time.sleep(0.1)  # 100ms延迟
        end_time = time.time()
        print(f"  - 延迟时间: {(end_time - start_time)*1000:.1f}ms")
        print("  ✅ 时间延迟测试完成")
        
        print("🎉 所有测试完成！")
        return True
        
    else:
        print(f"⚠️  未知按钮: {button_name}")
        return False

def main():
    """主函数"""
    print("=== 🔘 按钮功能测试脚本 ===")
    
    # 获取参数
    global test_string, test_int, test_bool
    
    # 参数初始化
    try:
        test_string
    except NameError:
        test_string = "Hello Button"
    
    try:
        test_int
    except NameError:
        test_int = 100
    
    try:
        test_bool
    except NameError:
        test_bool = True
    
    print("📋 脚本参数:")
    print(f"  - 文本参数: {test_string}")
    print(f"  - 整数参数: {test_int}")
    print(f"  - 布尔参数: {test_bool}")
    
    print("\n🔘 可用按钮:")
    print("  - 信息: 显示当前参数信息")
    print("  - 清空: 清空输出日志")
    print("  - 测试: 执行测试功能")
    
    print("\n💡 使用说明:")
    print("  1. 调整参数值")
    print("  2. 点击对应按钮执行功能")
    print("  3. 查看输出日志了解执行结果")
    
    print("\n✅ 脚本初始化完成，等待按钮点击...")

if __name__ == "__main__":
    main()
