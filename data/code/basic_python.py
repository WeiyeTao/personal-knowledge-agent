# basic_demo.py
"""
A simple Python demo file showing basic syntax.
"""

# 1. 变量与基本数据类型
name = "Weiye"
age = 25
height = 1.75
is_student = True

print(f"👋 Hello, my name is {name}, I'm {age} years old.")

# 2. 条件语句
if age < 18:
    print("You are a minor.")
elif age < 60:
    print("You are an adult.")
else:
    print("You are a senior.")

# 3. 列表与循环
fruits = ["apple", "banana", "cherry"]
print("\n🍎 My fruits list:")
for fruit in fruits:
    print("-", fruit)

# 4. 字典与键值访问
person = {"name": name, "age": age, "city": "Singapore"}
print(f"\n📍 {person['name']} lives in {person['city']}.")

# 5. 函数定义与调用
def greet(user_name):
    """Return a greeting message."""
    return f"Hello, {user_name}! Welcome to Python."

print("\n🧠 Function demo:")
print(greet("Barry"))

# 6. 类与对象
class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def introduce(self):
        return f"My name is {self.name}, and I study {self.major}."

s1 = Student("Weiye Tao", "Machine Learning in Robotics")
print("\n🎓 Class demo:")
print(s1.introduce())

# 7. 用户输入（可选）
# comment out to avoid blocking
# user_input = input("\nType your favorite fruit: ")
# print(f"Nice! You like {user_input}.")

# 8. 循环与条件结合
print("\n🔢 Counting even numbers under 10:")
for i in range(10):
    if i % 2 == 0:
        print(i, "is even")

print("\n✅ Demo finished.")
