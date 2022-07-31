# coding=utf-8

# version2.0
# ROW_NUM = (11329, 11332) #行号范围(文件夹号)
# COL_NUM = (52200, 52207) #列号范围(文件名号)
# 每个文件夹为一行


import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from ctypes import windll

global PARA

# 和ctypes解决字体模糊问题
windll.shcore.SetProcessDpiAwareness(1)
# 调用Tk()创建主窗口
root_window =tk.Tk()
# 设置窗口title
root_window.title("tile merge tool v2.0")
# 设置窗口大小
root_window.geometry('600x300')

# 设置文字标签
tk.Label(root_window,text="文件目录：").grid(row=0)
tk.Label(root_window,text="行号范围：").grid(row=1)
tk.Label(root_window,text="列号范围：").grid(row=2)
tk.Label(root_window,text="瓦片宽度：").grid(row=3)
tk.Label(root_window,text="瓦片高度：").grid(row=3)
tk.Label(root_window,text="文件格式：").grid(row=4)

# 选择目录
tile_path = tk.Entry(root_window)
def pik_path():
  path = filedialog.askdirectory()
  print(path)
  tile_path.insert(0,path+"/")
  return
tile_path_pik = tk.Button(root_window,text="选择",command=pik_path).grid(row=0,column=2)

# 创建输入框控件
# 行列号
ent_row_min = tk.Entry(root_window)
ent_row_max = tk.Entry(root_window)
ent_col_min = tk.Entry(root_window)
ent_col_max = tk.Entry(root_window)
# 瓦片尺寸
ent_tile_width = tk.Entry(root_window)
ent_tile_height = tk.Entry(root_window)
# 文件目录
ent_tile_ext = tk.Entry(root_window)
# 设置控件布局
tile_path.grid(row=0, column=1, padx=10, pady=5)
ent_row_min.grid(row=1, column=1, padx=10, pady=5)
ent_row_max.grid(row=1, column=2, padx=10, pady=5)
ent_col_min.grid(row=2, column=1, padx=10, pady=5)
ent_col_max.grid(row=2, column=2, padx=10, pady=5)
ent_tile_width.grid(row=3, column=1, padx=10, pady=5)
ent_tile_height.grid(row=3, column=2, padx=10, pady=5)
ent_tile_ext.grid(row=4, column=1, padx=10, pady=5)

# 设置参数
def set_para():
  global PARA
  PARA = {
    "tile_path":tile_path.get(),
    "row_num":(int(ent_row_min.get()),int(ent_row_max.get())),
    "col_num":(int(ent_col_min.get()),int(ent_col_max.get())),
    "tile_size":(int(ent_tile_width.get()),int(ent_tile_height.get())),
    "tile_ext":ent_tile_ext.get()
  }
  return

# 默认参数
def set_default():
  ent_row_min.insert(0, "11329")
  ent_row_max.insert(0, "11332")
  ent_col_min.insert(0, "52200")
  ent_col_max.insert(0, "52207")
  ent_tile_width.insert(0, "256")
  ent_tile_height.insert(0, "256")
  ent_tile_ext.insert(0, "jpg")
  tile_path.insert(0,"./tiles/")
  return

# 创建按钮
tk.Button(root_window, text="测试数据", command=set_default).grid(row=5,column=0)
tk.Button(root_window, text="确认参数", command=set_para).grid(row=5,column=1)
tk.Button(root_window, text="开始拼接", command=root_window.quit).grid(row=5,column=2)

tk.Label(root_window,text="create by wang",font=('Microsoft yahei',8, 'italic'),bg="#fcf").grid(row=6,column=0,padx=10,pady=10)

#开启主循环，显示主窗口
root_window.mainloop()



# ROW_NUM = (11329, 11332) #行号范围(文件夹号)
# COL_NUM = (52200, 52207) #列号范围(文件名号)
ROW_NUM = PARA["row_num"] #行号范围(文件夹号)
COL_NUM = PARA["col_num"] #列号范围(文件名号)
TILE_EXT = PARA["tile_ext"] #瓦片格式
#TILE_PATH = "./tiles/" #瓦片文件夹
TILE_PATH = PARA["tile_path"] #瓦片文件夹
WIDTH = PARA["tile_size"][0] #瓦片宽度
LENGTH = PARA["tile_size"][1] #瓦片高度

def creat_step_list(min,max,i=1):
  # 创建等差数列
  list = []
  while (min <= max):
    list.append(min)
    min = min + i
  return list

folders = creat_step_list(ROW_NUM[0],ROW_NUM[1],1)
files = creat_step_list(COL_NUM[0],COL_NUM[1],1)

# 创建底图,尺寸为文件夹个数x高度,文件个数x宽度
IMG_OUT = Image.new("RGB", (len(files)*WIDTH,len(folders)*LENGTH))
# 默认黑色瓦片
IMG_blk = Image.new("RGB", (WIDTH,LENGTH))
# 获取瓦片体积
tile_size = os.path.getsize(TILE_PATH + str(ROW_NUM[0]) +"/"+ os.listdir(TILE_PATH+str(ROW_NUM[0])+"/")[0])
# 估算输出图片大小
out_size =(ROW_NUM[1]-ROW_NUM[0]+1) * (COL_NUM[1]-COL_NUM[0]) * tile_size /1024/1024 #单位是MB
#print("output file size is %f GB. " % round(out_size,3))


info = tk.messagebox.askokcancel(title = "文件大小提示",message="预计文件大小："+ str(round(out_size,3))+ "MB")
if (info == False):
  os._exit(0)

# 开始拼接,南北为y,东西为x
for y in range(len(folders)):
 for x in range(len(files)):
   img_path = TILE_PATH+str(folders[y])+"/"+str(files[x])+"."+TILE_EXT
   try:
     img = Image.open(img_path)
   except IOError:
     IMG_OUT.paste(IMG_blk, (WIDTH*x,WIDTH*y)) #未找到图片时，粘贴默认图片
   else:
     IMG_OUT.paste(img, (WIDTH*x,WIDTH*y))
   x = x+1
 y = y+1

IMG_OUT.show()





