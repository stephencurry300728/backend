import os
import sys
import threading
import time
import socket
import webbrowser
from django.core.management import execute_from_command_line, call_command
from django.db.utils import OperationalError
import django


def find_available_port(host, start_port):
    """从给定的起始端口开始，找到一个可用的端口"""
    for port in range(start_port, start_port + 50):  # 检查从start_port开始的50个端口
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) != 0:
                return port
    raise IOError("找不到可用的端口")


def open_browser(port):
    """在服务器启动后自动打开浏览器，确保服务器已经开始监听端口"""
    print("正在检查服务器是否启动...")
    while not is_port_open("127.0.0.1", port):
        print("等待服务器启动...")
        time.sleep(1)
    print("服务器已启动，正在打开浏览器...")
    webbrowser.open(f'http://127.0.0.1:{port}/')


def is_port_open(host, port):
    """检查指定的端口是否开放（即服务器是否就绪）"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # 设置超时时间
        result = sock.connect_ex((host, port))
        return result == 0


# def check_migrations_and_apply():
#     """检查并应用数据库迁移"""
#     db_path = 'db.sqlite3'
#     if not os.path.exists(db_path):
#         print("数据库不存在，将执行迁移。")
#         call_command('migrate', interactive=False)
#     else:
#         try:
#             from upload.models import NewUser, Assessment_Base, Assessment_Classification
#             NewUser.objects.exists()
#             Assessment_Base.objects.exists()
#             Assessment_Classification.objects.exists()
#         except OperationalError as e:
#             if 'no such table' in str(e):
#                 call_command('migrate', interactive=False)
#                 print("数据库迁移已执行。")
#             else:
#                 raise


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()
    # check_migrations_and_apply()

    if len(sys.argv) == 1:
        port = find_available_port('127.0.0.1', 8000)  # 从8000端口开始寻找可用端口
        sys.argv.extend(["runserver", f"{port}", "--noreload"])
        threading.Thread(target=open_browser, args=(port,)).start()

    execute_from_command_line(sys.argv)
