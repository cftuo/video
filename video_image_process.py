# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------------------------#
#文件名：video_image_process.py
#主要功能：视频切割，抽帧，图片处理，声音处理，图像文字自动识别
#创建日期：2019-6-20
#创建人： 妥成发
#修改人    修改时间      修改内容
#---------------------------------------------------------------------------------------------------------#
import os
import sys
import time
import requests
import re
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *   #与PyQt4的差别
from PyQt5 import QtCore


    

class MainWindow(QMainWindow):
    '''
    #类名：MainWindow
    #父类：QMainWindow
    #功能：程序界面框架的主窗口
    #参数：无
    '''
    #全局变量定义的地方  
    #设置全显示的字体 
    font = QFont('Times New Roman')  
    #设置正在运行的功能名称，用来创建保存结果及锁定每次只有一个功能在运行，防止相互影响出错
    running_function = None



    def __init__(self, parent = None):
        '''
        #函数名：__init__(self, parent = None)
        #功能：初始化程序界面
        #参数：无
        '''
        super(MainWindow, self).__init__(parent)
        self.resize(1200,800)
        self.setWindowTitle("探索工具")
        self.setWindowIcon(QIcon('image/tool.png'))
        #创建菜单栏 工具栏 状态栏
        self.createActions()  
        self.createMenus()  
        self.createToolBars()
        self.statusBar()
        self.statusBar().showMessage('就绪...')
        
        
        
        
        
        
        
        
    def myInit(self):
        #分割窗 左窗
        self.left_splitter = QSplitter(Qt.Horizontal,self)
        #树形控件
        self.tree_widget = QTreeWidget(self.left_splitter)
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabel("功能导航窗口")
        #右窗
        self.right_splitter = QSplitter(Qt.Vertical,self.left_splitter)
        self.dock = QDockWidget("提示窗口",self.right_splitter)
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        edit = QTextEdit("请浏览左侧选项，选择对应的功能并双击，对应功能窗口将在此处显示。")
        edit.setReadOnly(True)
        font = QFont()
        font.setPointSize(15)
        edit.setFont(font)
        self.dock.setWidget(edit)
        self.left_splitter.setStretchFactor(1,1)
        #设置核心部件
        self.setCentralWidget(self.left_splitter)
        #调用创建窗口的函数
        self.createDockWindows()
        #调用创建树形控件函数
        self.createTreeWidget()
        #创建界面
        self.keyWordsUI()
        

        
        




    def createActions(self):
        '''
        #函数名：createActions(self)
        #功能：创建菜单栏和工具栏对应的槽函数响应关系
        #参数：无
        '''
        self.exitAction = QAction(QIcon("image/exit.png"),"退出",self)  
        self.exitAction.setShortcut("Ctrl+Q")  
        self.exitAction.setStatusTip("退出程序")  
        self.exitAction.triggered.connect(self.close)  
  
        self.aboutAction = QAction("关于",self)  
        self.aboutAction.triggered.connect(self.about)

        self.versionAction = QAction("版本",self)  
        self.versionAction.triggered.connect(self.version)


    def createMenus(self):  
        '''
        #函数名：createMenus(self)
        #功能：添加菜单
        #参数：无
        '''
        fileMenu=self.menuBar().addMenu("文件")
        fileMenu.addAction(self.exitAction)  
  
        aboutMenu=self.menuBar().addMenu("帮助")  
        aboutMenu.addAction(self.aboutAction)
        aboutMenu.addAction(self.versionAction)

  
    def createToolBars(self):  
        '''
        #函数名：createToolBars(self)
        #功能：创建工具栏
        #参数：无
        '''
        fileToolBar=self.addToolBar("File")
        fileToolBar.addAction(self.exitAction)


    def about(self):  
        '''
        #函数名：about(self)
        #功能：关于程序的简要介绍
        #参数：无
        '''
        QMessageBox.about(self,"关于程序",
                "<b>探索工具</b>主要功能是对视频和图片进行处理，解析出其中的有用信息。")


    def version(self):
        '''
        #函数名：version(self)
        #功能：程序版本信息说明
        #参数：无
        '''
        QMessageBox.about(self,"版本",
                "版本：V1.0.1\n作者: 妥成发\n发布日期：2019-6-21")


    #关闭程序时的提示
    def closeEvent(self,event):
        reply = QMessageBox.question(self, "退出提示信息", "确定退出程序吗？", QMessageBox.Yes, QMessageBox.No)
        if QMessageBox.Yes == reply:
            event.accept()
        else:
            event.ignore()









    def saveFilePath(self):
        save_path_name = QFileDialog.getExistingDirectory()
        if 0 == len(save_path_name):
            return
        else:
            self.select_save_path_flag = True
            self.save_path = save_path_name
        
       

    def createDockWindow(self, name = "功能窗口"):
        dock = QDockWidget(name, self.right_splitter)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.hide()
        return dock


    def createDockWindows(self):
        self.dock_1 = self.createDockWindow("下拉词 功能窗口")


    def hideAllWindows(self):
        #隐藏提示窗口
        self.dock.hide()
        #隐藏下拉词窗口
        self.dock_1.hide()


    def createTreeWidget(self):
        font = QFont()
        font.setPointSize(13)
        self.tree_widget.setFont(font)
        #添加根节点
        root = QTreeWidgetItem(self.tree_widget)
        root.setText(0, "All")
        #添加第一个父节点
        father1 = QTreeWidgetItem(root)
        father1.setText(0, "下拉词查询")
        root.addChild(father1)

        #添加最高级节点
        self.tree_widget.addTopLevelItem(root)
        #默认展开节点
        self.tree_widget.expandItem(root)
        #添加Item的响应关系
        self.tree_widget.itemDoubleClicked .connect(self.itemResponse)


    @pyqtSlot()
    def itemResponse(self):
        #树形控件响应规则
        rules = (
            #提示窗规则
            ("All",self.dock.show),
            #下拉词功能窗口
            ("下拉词查询",self.dock_1.show)
            )
        #被双击的item
        item=self.tree_widget.currentItem()
        for item_name,dock_show in rules:
            if item_name ==item.text(0):
                self.hideAllWindows()
                dock_show()



    def keyWordsUI(self):
        #布局的控件
        ui_widget = QWidget()
        ui_layout = QGridLayout()
        ui_layout.setSpacing(20)
        
        #添加种子词
        font = QFont("Time New Roman",16,QFont.Bold)
        font1 = QFont("Time New Roman",16)
        label = QLabel("种子词")
        label.setFont(font)
        ui_layout.addWidget(label,0,0,1,1)   #起始行 起始列 占用行 占用列
        self.dock_1_line_edit_key_words = QLineEdit("")
        self.dock_1_line_edit_key_words.setFont(font1)
        self.dock_1_line_edit_key_words.returnPressed.connect(self.search)  #回车时响应
        ui_layout.addWidget(self.dock_1_line_edit_key_words,0,1,1,7)   #起始行 起始列 占用行 占用列
        search_button = QPushButton("搜索")
        search_button.setFont(font)
        search_button.setToolTip("输入种子词，点击后开始查询对应种子词的下拉词")
        search_button.setAutoDefault(False)
        search_button.clicked.connect(self.search)
        ui_layout.addWidget(search_button,0,8,1,1)   #起始行 起始列 占用行 占用列
        
        #添加清空及采集的按钮
        delete_button = QPushButton("清空")
        delete_button.setFont(font)
        delete_button.setToolTip("点击后清空已经查询到的下拉词")
        delete_button.setAutoDefault(False)
        delete_button.clicked.connect(self.deleteContent)
        ui_layout.addWidget(delete_button,1,3,1,1)   #起始行 起始列 占用行 占用列
        
        collect_button = QPushButton("采集")
        collect_button.setFont(font)
        collect_button.setToolTip("点击后将查询到的下拉词保存到文件中")
        collect_button.setAutoDefault(False)
        collect_button.clicked.connect(self.collectContent)
        ui_layout.addWidget(collect_button,1,5,1,1)   #起始行 起始列 占用行 占用列

        #添加输出内容的编辑控件
        self.dock_1_plain_text_edit_content = QPlainTextEdit()
        self.dock_1_plain_text_edit_content.setReadOnly(True)
        font2 = QFont("Time New Roman",13)
        self.dock_1_plain_text_edit_content.setFont(font2)
        self.dock_1_plain_text_edit_content.setMaximumBlockCount(2000)  #设置最大行数
        ui_layout.addWidget(self.dock_1_plain_text_edit_content,2,0,6,9)   #起始行 起始列 占用行 占用列

        #布局生效
        ui_widget.setLayout(ui_layout)
        self.dock_1.setWidget(ui_widget)



    @pyqtSlot()
    def search(self):
        self.statusBar().showMessage('正在查询')
        #获取种子词
        key_words = self.dock_1_line_edit_key_words.text()
        key_words = key_words.strip()  #去掉两头的空格
        self.dock_1_plain_text_edit_content.appendPlainText("种子词 {} 的下拉词如下：".format(key_words))
        QApplication.processEvents()
        #Drop-down words 查询
        header = {
            'Host': 'www.amazon.com',
            'Referer': 'https://www.amazon.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }
        # 第一步：先把amazon主页拉下来
        #requests.packages.urllib3.disable_warnings()
        try:
            resp = requests.get("https://www.amazon.com/ref=nav_logo", headers=header) # verify=False 不进行SSL验证
        except:
            information_dialog("访问亚马逊主页失败")
            self.statusBar().showMessage('ready')
            return
        resp_text = resp.text
        
        # 第二步：从主页中提取出相关的参数
        ue_id_Re = re.search("ue_id = '(.*?)'", resp_text, re.DOTALL)
        #print(f"ue_id_Re = {ue_id_Re}")
        if ue_id_Re:
            ue_id = ue_id_Re.group(1)
        else:
            ue_id = ""
        ue_sid_Re = re.search("ue_sid = '(.*?)'", resp_text, re.DOTALL)
        #print(f"ue_sid_Re = {ue_sid_Re}")
        if ue_sid_Re:
            ue_sid = ue_sid_Re.group(1)
        else:
            ue_sid = ""
            
        # 第三步：构造请求
        originalKey = key_words         # 原始关键字
        # search_alias = 'mobile'
        # aps                       # All Departments 类别
        search_alias = 'aps'        # 搜索类别，这个是类别下拉框中的。主页源码中也有
        ks = 100                    # 先自己指定，发现并不影响结果
        # https://completion.amazon.com/search/complete?method=completion&mkt=1&r=T9GNBFENMKCSHQ96SN69&s=136-4489048-3064812&c=&p=Gateway&l=en_US&b2b=0&fresh=0&sv=desktop&client=amazon-search-ui&x=String&search-alias=mobile&ks=67&q=c&qs=&cf=1&fb=1&sc=1&
        keywords_url = f"https://completion.amazon.com/search/complete?method=completion&mkt=1&r={ue_id}&s={ue_sid}&c=&p=Gateway&l=en_US&b2b=0&fresh=0&sv=desktop&client=amazon-search-ui&x=String&search-alias={search_alias}&ks={ks}&q={originalKey}&qs=&cf=1&fb=1&sc=1&"
        try:
            second_resp = requests.get(keywords_url, headers=header)
        except:
            information_dialog("查询下拉词失败")
            self.statusBar().showMessage('ready')
            return
        content = second_resp.text
        print(f"secondRespText = {content}")
        if len(content) > 15 :
            result_list = content.split("[")[2].split("]")[0].split(",")
            for i in range(0,len(result_list)):
                self.dock_1_plain_text_edit_content.appendPlainText("{}".format(result_list[i]))
                QApplication.processEvents()
        else:
            information_dialog("查询结果为空")
        resp.close
        self.statusBar().showMessage('ready')
        information_dialog("查询完成")


        
        


    

    @pyqtSlot()
    def deleteContent(self):
        self.dock_1_plain_text_edit_content.clear()



    @pyqtSlot()
    def collectContent(self):
        path = ""
        if True == self.select_save_path_flag:
            path = self.save_path + "/下拉词采集结果"
        else:
            path = "下拉词采集结果"
        createDir(path)
        #获取内容
        content = self.dock_1_plain_text_edit_content.toPlainText ()
        #创建文件对象
        file_time = getTime()
        file_name = path + u"/采集结果_{}.txt".format(file_time)
        file_obj = open(file_name, "w")
        file_obj.write(content)
        file_obj.close()
        information_dialog("采集成功！\n结果保存在 {}".format(file_name))
        
        
        
        
        
        
        
        
        
def information_dialog(info):
    QMessageBox.information(QDialog(),"Information",info)



#创建目录文件夹
def createDir(dir_name):
    is_exists = os.path.exists(dir_name)
    if not is_exists:
        os.makedirs(dir_name)


def getTime():
    time_stamp = time.time()
    time_stamp = time_stamp + 8 * 60 * 60
    year,month,day,hh,mm,ss,wd,y,z = time.gmtime(time_stamp)
    temp = "{0:04d}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}".format(year,month,day,hh,mm,ss)
    return temp


    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
