---
title: usefully cmd
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [practise]
---

# Python: pip without sudo

install 

```bash
pip install --user some_pkg
```

export 

note: check the path is exist, if not, check if pyhton3.6 is correct folder name

```bash
export PYTHONPATH=$(python -c "import site, os; print(os.path.join(site.USER_BASE, 'lib', 'python3.6', 'site-packages'))"):$PYTHONPATH
```

run 

```
python ...
```

# Git 

## Git repo contribution 不见了

查看commit log中的邮箱

```bash
git log
git config --global user.email 'email address'
```

## 删除了在恢复

```bash
git reset HEAD file
git checkout -- file
```

删除文件

```bash
git rm --cached file
```

扔掉本地文件，强行同步远程分支

```sql
git reset --hard upstream/master
```

## Git 克隆一个pr

```bash
git fetch origin refs/pull/PR_NUMBER/head:NEW_LOCAL_BRANCH
eg:

git fetch origin pull/611/head:pull_611
git checkout pull_611
```

# Linux cmds

## 查询文件或文件夹大小

```bash
//文件大小
du -sh * | sort -n 
// 文件夹大小
du -lh --max-depth=1
```

## 查询cpu利用

```bash
top -bn 1 -i -c
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head
```







