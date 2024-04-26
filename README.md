# 教务管理系统

## 简介

该仓库是教务管理系统的后端部分，使用 Python 的 Flask 框架开发。前端请移步[vue-edu-management-sys](https://github.com/andywang425/vue-edu-management-sys)。

`E-R`文件夹里是数据库关系模式的 E-R 图，应该能帮助理解数据库结构。

## 环境要求

- Python >= v3.11
- SQL Server 2022
- ODBC Driver 18 for SQL Server

## 开始

1. Clone 代码并安装依赖

```sh
git clone https://github.com/andywang425/educational-management-system.git
cd educational-management-system
pip install -r requirements.txt
```

2. 初始化数据库。打开`sql`文件夹，运行`crebas.sql`会生成一个名为`SUEP`的数据库。运行`testdata.sql`可插入一些测试数据。

3. 运行服务器。

```sh
# 开发环境
python app.py
# 生产环境
python run.py
```

4. （可选）通过 submodule 获取前端部分。

```sh
git submodule init
git submodule update
```

前端部分安装依赖、运行的具体方式请移步[vue-edu-management-sys](https://github.com/andywang425/vue-edu-management-sys)。

## 可能出现的问题

### 找不到数据库驱动

```sh
pyodbc.InterfaceError: ('IM002', '[IM002] [Microsoft][ODBC 驱动程序管理器] 未发现数据源名称并且未指定默认驱动程序 (0) (SQLDriverConnect)')
```

解决方法 1：

打开`db`文件夹下的`mssql.py`，尝试把`{{ODBC Driver 18 for SQL Server}}`中的`18`改为`17`。

解决方法 2：

安装驱动，详情见微软官网<https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server>。
