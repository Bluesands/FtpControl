## 该项目的使用目标是工程项目文件夹很多,需要频繁更新,不适合团队使用.
### 使用说明:
+ ```git clone https://github.com/Bluesands/FtpControl.git && cd FtpControl```
+ ```cp conf/configtemplete.ini conf/your_project_name.ini```
+ ```vim your_project_name.ini```进行配置你的项目
+ 如果你的项目以上传目标主机,更新文件只需在终端执行```python run.py your_project_name```
+ 如果你想使用本项目首次上传你的project,则只需在终端执行```python run.py your_project_name init```

注意:本项目只适合linux/Mac环境,适合多个项目,只需为每个项目制定配置文件即可.
