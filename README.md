# SM2公钥格式转换

2023/06/19
@author: chenchuan01
@version: 1.0

---

# 程序简介

该程序为命令行程序，可对输入的SM2公钥值进行格式转换  
自动检测输入值的编码类型与公钥格式类型

# 程序原理

先检测输入值的编码类型，为hex或base64。然后统一转换为hex编码，再根据转换后的值，检测其公钥格式为raw或der
最后做统一的输出

# 使用方法

`python main.py`