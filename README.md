# django-storage-qcloud

Django storage for qcloud's COS

# 介绍

django-storage-qcloud 是一个服务于腾讯云存储的 Django 自定义存储系统。

# 安装

- 使用 pip 安装

```
pip install django-storage-qcloud
```

或者直接从 git 安装

```
pip install git+https://github.com/fordguo/django-storage-qcloud.git
```

- 添加 requirements.txt

```
git+https://github.com/fordguo/django-storage-qcloud.git
```

- 配置 setting.py:
  - 将上传文件存放到云
    `DEFAULT_FILE_STORAGE = 'django_storage_qcloud.storage.QcloudStorage'`
  - 将静态文件存放到云
    `STATICFILES_STORAGE = 'django_storage_qcloud.storage.QcloudStorage'`
  - 替换 SecretId， SecretKey, Region, Bucket 的值
  ```
  QCLOUD_STORAGE_OPTION = {
      'SecretId': 'SecretId 是开发者拥有的项目身份识别 ID，用以身份认证',
      'SecretKey': 'SecretKey 是开发者拥有的项目身份密钥。',
      'Region': '域名中的地域信息',
      'Bucket': '存储桶是 COS 中用于存储数据的容器，每个对象都存储在一个存储桶中',
  }
  ```
  - 其他配置：
    - COS_URL = 'https://www.qixincha.com' # 自定义域名， 不配置将使用 COS 默认域名
    - COS_FAST_CDN = False # 默认加速域名是否开启

* 同步静态文件到云
  `python manage.py collectstatic`

# 要求

1. 支持 Python3.4
