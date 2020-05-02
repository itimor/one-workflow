# django + vue 工作流管理系统
包含 `用户`、`角色`、`菜单`、`权限` 管理， 这是一般后台系统一般都会有的功能， 后续其他功能都可以在这个基础上进行扩展。

- 后端model参考: [loonflow](https://github.com/blackholll/loonflow), 非常不错的一个项目
- 前端设计参考: [花裤衩 vue-element-admin](https://github.com/PanJiaChen/vue-element-admin), 大神作品没得说
## 开发环境
### 后端
安装依赖
```bash
cd backend
pip install -r dev_requirements.txt
```

初始化系统
- 生成管理员账号 `admin 123456`
```bash
python manage.py migrate
python manage.py init_sys
```

生成工作流
- 用户 `ops`,`ops_tl`,`dev`,`dev_tl`,`hr`,`hr_tl`
- 密码 `123456`

```bash
python manage.py init_wf
python manage.py init_ticket
python manage.py init_leave
```

运行
```bash
python manage.py runserver
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 开始使用
使用 `admin` 登录
### 给所有角色分配工作流权限
![role](gifs/role.png)

### 分配菜单 和 数据 权限
![role_edit](gifs/role_edit.png)

### 配置假期工作流
![role](gifs/leave.png)

### 新建工单
![role](gifs/new.png)

### 编辑工单
![role](gifs/edit.png)

### 所有工单
![role](gifs/all.png)