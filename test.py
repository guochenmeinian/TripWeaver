#!/usr/bin/env python3
"""
测试：到底是FunctionTool还是docstring让agent能读取描述？
"""

from google.adk.tools import FunctionTool

print("🧪 测试：描述来源分析")
print("="*60)

# ===== 测试1: 有docstring的函数 =====
def function_with_docstring():
    """This is a SECRET_MESSAGE_ABC from docstring"""
    return "result from docstring function"

# ===== 测试2: 没有docstring的函数 =====
def function_without_docstring():
    return "result from no-docstring function"

# ===== 测试3: 空docstring的函数 =====
def function_empty_docstring():
    """"""
    return "result from empty-docstring function"

# ===== 测试4: 复杂docstring的函数 =====
def function_complex_docstring():
    """
    Complex function with detailed docstring.
    
    This function has multiple lines and contains SPECIAL_CODE_XYZ.
    
    Args:
        None
        
    Returns:
        str: A simple result
        
    Note:
        The magic number is 42.
    """
    return "result from complex-docstring function"

print("🔍 创建FunctionTool前 - 检查原始函数的docstring:")
print("-"*50)
print(f"function_with_docstring.__doc__: {function_with_docstring.__doc__}")
print(f"function_without_docstring.__doc__: {function_without_docstring.__doc__}")
print(f"function_empty_docstring.__doc__: {function_empty_docstring.__doc__}")
print(f"function_complex_docstring.__doc__: {function_complex_docstring.__doc__}")

print("\n🔧 创建FunctionTool实例:")
print("-"*50)

# 创建FunctionTool实例
tool1 = FunctionTool(function_with_docstring)
tool2 = FunctionTool(function_without_docstring)
tool3 = FunctionTool(function_empty_docstring)
tool4 = FunctionTool(function_complex_docstring)

print(f"Tool1 (有docstring):")
print(f"  名称: {tool1.name}")
print(f"  描述: {tool1.description}")
print(f"  描述长度: {len(tool1.description) if tool1.description else 0}")

print(f"\nTool2 (无docstring):")
print(f"  名称: {tool2.name}")
print(f"  描述: {tool2.description}")
print(f"  描述长度: {len(tool2.description) if tool2.description else 0}")

print(f"\nTool3 (空docstring):")
print(f"  名称: {tool3.name}")
print(f"  描述: {tool3.description}")
print(f"  描述长度: {len(tool3.description) if tool3.description else 0}")

print(f"\nTool4 (复杂docstring):")
print(f"  名称: {tool4.name}")
print(f"  描述: {tool4.description}")
print(f"  描述长度: {len(tool4.description) if tool4.description else 0}")

print("\n🔍 测试：能否手动修改FunctionTool的描述？")
print("-"*50)

# 尝试修改描述
try:
    original_desc = tool1.description
    tool1.description = "MANUALLY_CHANGED_DESCRIPTION_999"
    print(f"✅ 成功修改Tool1描述:")
    print(f"  原始: {original_desc}")
    print(f"  修改后: {tool1.description}")
except Exception as e:
    print(f"❌ 无法修改描述: {e}")

print("\n📊 结论分析:")
print("-"*50)
print("1. FunctionTool是否自动读取函数的docstring？")
print("2. 没有docstring的函数会得到什么描述？")
print("3. 能否手动覆盖FunctionTool的描述？")

print("\n🎯 这回答了你的问题:")
print("- 是FunctionTool自动读取docstring，还是ADK本身就能读函数描述？")
print("- docstring vs FunctionTool，哪个是关键因素？")