# group5
通过Django+Mysql/Sqlite+Vue2构建前端，基于Keras神经网络库，使用了nltk自然语言处理包。系统功能：用户登录注册、模型训练、模型预测
**中文**   
## 开发环境  
python 3.9.1  
下载地址：https://www.python.org/downloads/release/python-391/  
python安装完成后，配置仓库镜像地址
pip config set global.index-url  https://pypi.tuna.tsinghua.edu.cn/simple（如果出现问题，可能是网速问题切换热点尝试一下）    
nodejs 16.13.1（官网下载或者直接在工具包解压）  
node安装完，配置npm仓库的镜像地址  
npm config set registry https://registry.npmmirror.com/  
## 项目运行
### 后台
1、在项目根目录backend下cmd打开控制台  
2、创建虚拟环境 python -m venv venv（可以在python中创建，并且我已创建环境直接激活即可）  
3、激活虚拟环境 call venv\scripts\activate.bat  
4、安装项目所需依赖pip install -r requirements.txt  
如果重新创建了虚拟环境需要完成下面一步：  
5、将“工具包”目录下的nltk_data压缩包解压到backend/venv目录下  
6、启动项目python manage.py runserver 0.0.0.0:9008
### 前端  
1、项目根目录web下执行 npm i  
2、运行项目 npm run dev
## 账号密码  
superadmin   
admin123456  
## 使用说明
1、数据集目录下有两个文件，其中【test.csv】，是测试上传识别的  
2、【train.csv】 这个是训练时候用到的数据集  
3、spam_classifier.h5 是经过30轮次训练后的模型，其参数指标为：  
正确率: 0.9083  
精度: 0.91141  
召回率: 0.9083  
F1得分: 0.90974  









