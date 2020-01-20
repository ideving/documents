### 源码安装setuptools
```
python setup.py install
```

### 源码安装pip
```
python setup.py install
```

### 升级setuptools到指定版本 
```
pip install --upgrade setuptools==40.0.0
```

### 升级pip到指定版本
```
python -m pip install --upgrade pip==10.0.0
```

### 使用临时源地址
```
pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com package
```

### 使用默认源地址（pip>=10.0.0) 
```
python -m pip install --upgrade pip
pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
pip config set install.trusted-host mirrors.aliyun.com
pip install some-package
```

### 导出安装包列表到文件
```
pip freeze > requirements.txt
pip freeze --all > requirements.txt
```

### 下载离线包到指定目录
```
pip download xxx  -d /paks
pip download -r requirements.txt  -d /packs
```

### 安装指定的离线包
```
pip install -d /packs -r requirements.txt
pip install --no-index --find-links=/packs xxx
pip install --no-index -f /packs -r requirements.txt
```

### 查看过期的包
```
pip list --outdate
```

### 下载离线包并从局域网安装
```
pip config set download.trusted-host mirrors.aliyun.com
pip download --trusted-host mirrors.aliyun.com -r requirements.txt -d /packs
pip install --no-index -f file://xxx/packs package
```

### 将源码打包（dist 为存放whl文件的位置，src为要打包的文件夹，必须包含setup.py）
```
pip wheel --wheel-dir=/dist /src
```
