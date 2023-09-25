import os
import shutil
import datetime
import tkinter as tk
from tkinter import messagebox
import time  # 导入时间模块

program_template = '''
import os
import threading
import subprocess

# 16进制字符串数据
hex_string_1 = "{}"
hex_string_2 = "{}"

# 转换为二进制数据
binary_data_1 = bytes.fromhex(hex_string_1)
binary_data_2 = bytes.fromhex(hex_string_2)

# 用户文档目录
documents_path = os.path.expanduser("~/Documents")

# 目标exe文件路径
exe_file_path_1 = os.path.join(documents_path, "output1.exe")
exe_file_path_2 = os.path.join(documents_path, "output2.exe")

# 写入二进制数据到exe文件
with open(exe_file_path_1, "wb") as exe_file_1:
    exe_file_1.write(binary_data_1)

with open(exe_file_path_2, "wb") as exe_file_2:
    exe_file_2.write(binary_data_2)

# 运行exe文件的线程类
class RunExeThread(threading.Thread):
    def __init__(self, exe_name):
        threading.Thread.__init__(self)
        self.exe_name = exe_name

    def run(self):
        exe_path = os.path.join(documents_path, self.exe_name)
        subprocess.run([exe_path], capture_output=True, text=True)

# 切换到文档目录 
os.chdir(documents_path)

# 创建并启动两个线程分别运行两个exe文件
thread1 = RunExeThread('output1.exe')  
thread1.start()

thread2 = RunExeThread('output2.exe')
thread2.start()

# 等待线程完成
thread1.join() 
thread2.join()
        '''
def main():
    # 检查同级目录下是否存在1.exe和2.exe
    if not (os.path.isfile('1.exe') and os.path.isfile('2.exe')):
        messagebox.showwarning("警告", "1.exe和2.exe不存在于同级目录中")
    else:
        # 函数将二进制数据转换为16进制字符串
        def binary_to_hex(binary_data):
            return binary_data.hex()

        # 函数将exe文件转换为16进制字符串并保存到txt文件
        def exe_to_hex_txt(input_file, output_file):
            with open(input_file, 'rb') as file:
                binary_data = file.read()
            hex_data = binary_to_hex(binary_data)
            with open(output_file, 'w') as file:
                file.write(hex_data)

        # 读取1.exe和2.exe并转换为16进制字符串保存到1.txt和2.txt
        exe_to_hex_txt('1.exe', '1.txt')
        exe_to_hex_txt('2.exe', '2.txt')

        # 读取1.txt和2.txt中的16进制字符串
        with open("1.txt", "r") as file1:
            hex_string_1 = file1.read()

        with open("2.txt", "r") as file2:
            hex_string_2 = file2.read()

        # 定义程序模板


        # 将1.txt和2.txt的内容插入到程序模板中
        formatted_program = program_template.format(hex_string_1, hex_string_2)

        # 保存到新的文件kb_out_0.py，使用utf-8编码  
        with open("kb_out_0.py", "w", encoding="utf-8") as output_file:
            output_file.write(formatted_program)

        print("转化完成")

        output_dir = os.getcwd()  

        # 删除生成的临时txt文件
        for txt_file in ['1.txt', '2.txt']:
            if os.path.exists(txt_file):
                os.remove(txt_file)
                print(f"{txt_file}删除成功")

        # 使用pyinstaller打包 
        os.system(f"pyinstaller -F -w --distpath {output_dir} kb_out_0.py")

         #删除kb_out_0.py和spec文件
        for file_to_remove in ['kb_out_0.py', 'kb_out_0.spec']:
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                print(f"{file_to_remove}删除成功")

        # 删除build文件夹
        build_dir = 'build'
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        # 等待直到kb_out_0.exe被创建
        while not os.path.exists('kb_out_0.exe'):
            time.sleep(1)  # 每隔一秒检测一次

        # 将exe移动到以时间戳命名的文件夹中 
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        folder_path = os.path.join(os.getcwd(), timestamp)
        os.mkdir(folder_path)

        exe_path = os.path.join(os.getcwd(), 'kb_out_0.exe') 
        new_path = os.path.join(folder_path, 'kb_out_0.exe')
        shutil.move(exe_path, new_path)

        if os.path.exists(exe_path):
            os.remove(exe_path)
    pass

if __name__ == '__main__':
    main()
