#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Tkinter as tk
import tkFileDialog as td
import os
import io
import json
import subprocess as shell

window = tk.Tk()

with open(r'../hexo-tool/config.json') as load_f:
        global config_json
        config_json = json.load(load_f, encoding='utf-8')

current_image_dir = ''      
        
post_dir = config_json.get('post_dir').encode('utf-8')

def main():
    window.title(config_json.get('title'))
    window.geometry('800x400')
    init_menus()
    init_frame()
    window.resizable(width=False, height=False)
    window.mainloop()

def parse_folder(dir_path):
    if dir_path == '':
        return dir_path
    else:
        dps = dir_path.split('/')
        return dps[len(dps) - 1]
    
var_image_path = tk.StringVar(None, '当前图片目录：' + parse_folder(post_dir), None)  #文字变量存储器
var_image_num = tk.StringVar(None, '请选择...', None)  #当前目录图片数量

def shell_command(cmd):
    shell_console.insert('insert', '\n' + cmd) 
    output = shell.Popen(cmd, stdout=shell.PIPE, shell=True)
    for line in output.stdout:
        shell_console.insert('insert', '\n' + line.rstrip())
    #output.stdout.close()
    output.communicate()

def folder_file_num(dir_path):
    count = 0
    for root,dirs,files in os.walk(dir_path):    #遍历统计
        for each in files:
                count += 1   #统计文件夹下文件个数
    return count
    

def image_folder():  #选择图片目录
    global current_image_dir
    ip = td.askdirectory(title='选择图片文件夹', initialdir=post_dir)
    if ip == '':
        ip = post_dir
    current_image_dir = ip
    var_image_path.set('当前图片目录：' + parse_folder(ip))
    var_image_num.set('目录内图片数：' + str(folder_file_num(current_image_dir)))

def new_post():
    inputt = input_text.get()
    if inputt == '':
        shell_console.insert('insert', '\n请在最底下输入框输入要创建的文件名（不要后缀.md)')
        return
    np = 'cd ' + config_json.get('blog_dir') + ' && hexo new ' + inputt
    shell_command(np)
def new_drafts():
    inputt = input_text.get()
    if inputt == '':
        shell_console.insert('insert', '\n请在最底下输入框输入要创建的文件名（不要后缀.md)')
        return
    nd = 'cd ' + config_json.get('blog_dir') + ' && hexo new draft ' + inputt
    shell_command(nd)

def local_publish():
    lp = 'cd ' + config_json.get('blog_dir') + ' && hexo server'
    shell_command(lp)

def drafts_to_post():
    inputt = input_text.get()
    if inputt == '':
        shell_console.insert('insert', '\n请在最底下输入框输入草稿文件名（不要后缀.md)')
        return
    dtp = 'cd ' + config_json.get('blog_dir') + ' && hexo publish ' + inputt
    shell_command(dtp)

def post_to_drafts():
    inputt = input_text.get()
    if inputt == '':
        shell_console.insert('insert', '\n请在最底下输入框输入文件名（不要后缀.md)')
        return
    cp = 'mv -f ' + config_json.get('post_dir') + '/' + inputt + ' ' + config_json.get('drafts_dir') + '/' + inputt
    cpmd = 'mv ' + config_json.get('post_dir') + '/' + inputt + '.md ' + config_json.get('drafts_dir') + '/' + inputt + '.md'
    shell_command(cp)
    shell_command(cpmd)

def delete_drafts():
    inputt = input_text.get()
    if inputt == '':
        shell_console.insert('insert', '\n请在最底下输入框输入草稿文件名（不要后缀.md)')
        return
    rm = 'rm -rf ' + config_json.get('drafts_dir') + '/' + inputt
    rmmd = 'rm ' + config_json.get('drafts_dir') + '/' + inputt + '.md'
    shell_command(rm)
    shell_command(rmmd)

def local_stop():
    print('stop server')

def cut_image():
    shell_console.insert('insert', '\nctrl + shift + A')

def upload_image():
    if current_image_dir == '':
        shell_console.insert('insert', '\n请选择需要编辑的文章图片目录')
        return
    img_file = td.askopenfilename(title='选择图片', initialdir=config_json.get('default_image_path'))
    s_png = ".png"
    s_jpg = ".jpg"
    s_jpeg = ".jpeg"
    s_gif = ".gif"
    if img_file.endswith(s_png) or img_file.endswith(s_jpg) or img_file.endswith(s_jpeg) or img_file.endswith(s_gif):
        if img_file.endswith(s_png) or img_file.endswith(s_jpg) or img_file.endswith(s_jpeg):
            cs = 'convert -resize "' + str(config_json.get('img_max_width')) + ' >" ' + img_file + ' ' + img_file
            shell_command(cs)

        if img_file.endswith(s_jpg) or img_file.endswith(s_jpeg):
            qs = 'convert -quality ' +  config_json.get('img_jpg_qulity') + ' ' + img_file + ' ' + img_file
            shell_command(qs)

        ss = 'cp ' + img_file + ' ' + current_image_dir + '/image' + str(folder_file_num(current_image_dir) + 1) + os.path.splitext(img_file)[1]
        shell_command(ss)
        var_image_num.set('目录内图片数：' + str(folder_file_num(current_image_dir)))

    else:
        shell_console.insert('insert', '\n请选择图片文件(jpg、jpeg、gif、png)')

def publishing():
    #备份文件
    copy = 'rm -rf ' + config_json.get('copy_repository') + ' && cp -af ' + config_json.get('blog_dir') + ' ' + config_json.get('copy_repository')
    shell_command(copy)
    #替换图片图床
    qshell_init = 'cd ' + config_json.get('qshell_path') + ' && qshell account ' + config_json.get('qiniu_ak') + ' ' + config_json.get('qiniu_sk')
    shell_command(qshell_init)
    qshell_upload = 'cd ' + config_json.get('qshell_path') + ' && qshell qupload 20 qshell-config'
    shell_command(qshell_upload)
    #替换字符串
    sed_r = 'sed -i "s#img\ src=\\\"#&http://qiniucdn.dp2px.com/#g" `grep img\ src=\\\" -rl ' + config_json.get('copy_repository') + '/source/_posts`'
    shell_command(sed_r) 
    #压缩资源
    press_res = 'cd ' + config_json.get('copy_repository') + ' && hexo g && gulp'
    shell_command(press_res)
    #git提交
    git_push = 'cd ' + config_json.get('copy_repository') + ' && git add . && git commit -m \"submit\" && git push'
    #shell_console.insert('insert', '\n' + git_push) 
    #shell_command(git_push)

def init_menus():  #初始化菜单
    menubar = tk.Menu(window)

    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=filemenu)
    filemenu.add_command(label='新建文章', command=new_post)
    filemenu.add_command(label='新建草稿', command=new_drafts)
    filemenu.add_command(label='草稿转文章', command=drafts_to_post)
    filemenu.add_command(label='文章转草稿', command=post_to_drafts)
    filemenu.add_separator()
    filemenu.add_command(label='删除草稿', command=delete_drafts)

    editmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='编辑', menu=editmenu)
    editmenu.add_command(label='截图', command=cut_image)
    editmenu.add_command(label='图片目录', command=image_folder)
    editmenu.add_command(label='压缩上传图片', command=upload_image)

    publishmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='发布', menu=publishmenu)
    publishmenu.add_command(label='启动本地服务', command=local_publish)
    publishmenu.add_command(label='停止本地服务', command=local_stop)
    publishmenu.add_command(label='备份并发布', command=publishing)

    window.config(menu=menubar)

def init_frame(): #初始化页面布局
    frame_head = tk.Frame(bd=12, bg='#F25652')
    frame_head.pack(side=tk.TOP, fill=tk.X, expand=False)

    image_folder_label = tk.Label(frame_head, textvariable=var_image_path, bg='#F25652', foreground='#F1F0E2', font=('Arial', 12), width=30, height=2)
    image_folder_label.pack(side=tk.LEFT)

    image_number = tk.Label(frame_head, textvariable=var_image_num, bg='#F25652', foreground='#F1F0E2', font=('Arial', 12), width=20, height=2)
    image_number.pack(side=tk.RIGHT)

    global frame_footer
    frame_footer = tk.Frame(height=60, bg='#252526')
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    input_label = tk.Label(frame_footer, text='请输入文章名称：', bg='#252526', foreground='#F1F0E2')
    input_label.pack(side=tk.LEFT)

    global input_text
    input_text = tk.Entry(frame_footer)
    input_text.pack(fill=tk.X)

    frame_content = tk.Frame()
    frame_content.pack(side=tk.TOP, fill=tk.BOTH,  expand=False)
    global shell_console
    shell_scroll = tk.Scrollbar(frame_content)
    shell_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    shell_console = tk.Text(frame_content, bg='#3E4E59', foreground='#F1F0E2', height=20)
    shell_console.pack(fill=tk.BOTH)
    shell_scroll.config(command=shell_console.yview)
    shell_console.config(yscrollcommand=shell_scroll.set)

main()
