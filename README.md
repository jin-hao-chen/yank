# yank
Script


# 内部API
+ objects.py文件中以`_`开头的函数为内部API, 不会被封装成对象API暴露给虚拟机
+ list和map容器对象中存储的是Value对象, 不是直接的对象
+ 内部API的obj不是Value对象, 除了list和map中会涉及到Value类型的参数之外, 其他对象均没有
