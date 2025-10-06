# UE-Python-Scripts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-5.3+-blue.svg)](https://www.unrealengine.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)

> 🎮 专为Unreal Engine设计的Python脚本集合，提供强大的编辑器自动化工具和批量处理功能

## 📖 简介

UE-Python-Scripts是一个专门为Unreal Engine开发者设计的Python脚本库，包含了各种实用的编辑器自动化工具。这些脚本可以帮助您：

- 🗂️ **批量管理资产** - 自动整理、重命名、移动项目资产
- 🔧 **蓝图工具** - 解体蓝图、分析组件、优化结构
- 🎨 **材质处理** - 批量替换材质、优化材质设置
- 🏗️ **关卡设计** - 自动化关卡设置、环境工具
- 🎭 **动画工具** - 骨骼网格体处理、动画优化
- ⚡ **性能优化** - 批量操作、数据导出、性能测试

## 🚀 快速开始

### 前置要求

- Unreal Engine 5.3+
- Python 3.7+
- [Python Script Manager Plugin](https://github.com/eish1997/python-script-manager) (推荐)

### 安装方法

1. **克隆仓库**
   ```bash
   git clone https://github.com/eish1997/UE-Python-Scripts.git
   ```

2. **复制脚本到项目**
   ```bash
   # 将脚本复制到您的UE项目的Content/Scripts目录
   cp -r UE-Python-Scripts/scripts/* /path/to/your/project/Content/Scripts/
   ```

3. **在UE编辑器中使用**
   - 打开Python Script Manager插件
   - 选择您需要的脚本
   - 配置参数并运行

## 📁 脚本分类

### 🗂️ 资产管理 (Asset Management)
- **资产整理工具** - 自动分类、重命名、移动项目资产
- **材质工具** - 批量替换场景材质、材质优化
- **批量操作** - 高效的批量处理工具

### 🔧 蓝图工具 (Blueprint Tools)
- **蓝图解体工具** - 将蓝图Actor解体为独立组件
- **蓝图分析工具** - 分析蓝图结构、组件统计
- **组件提取** - 提取特定类型的组件

### 🏗️ 关卡设计 (Level Design)
- **关卡设置工具** - 自动化关卡配置
- **环境工具** - 植被放置、环境优化
- **光照工具** - 批量光照设置

### 🎭 动画工具 (Animation Tools)
- **骨骼网格体工具** - 骨骼重定向、网格体优化
- **动画工具** - 动画压缩、优化
- **蒙皮工具** - 蒙皮权重处理

### ⚡ 实用工具 (Utilities)
- **批量操作** - 通用批量处理工具
- **数据导出** - 项目数据导出和分析
- **性能工具** - 性能监控和优化

### 🧪 测试工具 (Testing)
- **参数测试** - 测试所有参数类型功能
- **压力测试** - 按钮和功能压力测试
- **性能基准** - 性能测试和基准

### 📋 模板 (Templates)
- **基础模板** - 创建新脚本的基础模板
- **工具模板** - 创建工具脚本的模板
- **示例模板** - 各种功能的示例模板

## 🛠️ 脚本编写规范

所有脚本都遵循统一的编写规范：

### 题头格式
```python
"""
@PLUGIN_INFO
id: SCRIPT_UNIQUE_ID
name: 脚本显示名称
description: 脚本功能描述
category: 脚本分类
favorite: true/false
usage: 使用说明
@END_INFO

@PLUGIN_PARAMS
参数定义行...
@END_PARAMS
"""
```

### 支持的参数类型
- `string` - 文本输入
- `int` - 整数输入
- `float` - 浮点数输入
- `bool` - 布尔开关
- `file` - 文件选择 (支持📁📂按钮)
- `folder` - 文件夹选择 (支持📁📂按钮)
- `select` - 下拉选择
- `slider` - 滑块调节
- `button` - 自定义按钮

## 📚 文档

- [快速开始指南](docs/getting-started.md)
- [脚本编写指南](docs/script-writing-guide.md)
- [API参考](docs/api-reference.md)
- [故障排除](docs/troubleshooting.md)

## 🤝 贡献

我们欢迎社区贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解如何参与。

### 贡献方式
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

## 📞 支持

如果您遇到问题或有建议，请：
- 创建 [Issue](https://github.com/eish1997/UE-Python-Scripts/issues)
- 查看 [故障排除指南](docs/troubleshooting.md)
- 参与 [讨论区](https://github.com/eish1997/UE-Python-Scripts/discussions)

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
