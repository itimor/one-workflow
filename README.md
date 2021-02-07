# django + vue 工作流管理系统
包含 `用户`、`角色`、`菜单`、`权限` 管理， 这是基础的工作流系统，初始化会生成请假工作流， 也可以自行配置其他工作流比如，发布工单等。

[comment]: <> (- 后端model参考: [loonflow]&#40;https://github.com/blackholll/loonflow&#41;, 非常不错的一个项目)
[comment]: <> (- 前端设计参考: [花裤衩 vue-element-admin]&#40;https://github.com/PanJiaChen/vue-element-admin&#41;, 大神作品没得说)
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
![role](https://github.com/itimor/one-workflow/raw/master/gifs/role.png)

### 分配菜单 和 数据 权限
![role_edit](https://github.com/itimor/one-workflow/raw/master/gifs/role_edit.png)

### 配置假期工作流
![role](https://github.com/itimor/one-workflow/raw/master/gifs/leave.png)

### 新建工单
![role](https://github.com/itimor/one-workflow/raw/master/gifs/new.png)

### 编辑工单
![role](https://github.com/itimor/one-workflow/raw/master/gifs/edit.png)

### 所有工单
![role](https://github.com/itimor/one-workflow/raw/master/gifs/all.png)