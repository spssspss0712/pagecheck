# Notes

记录每个决定的「为什么」，以及当下还说不清的东西。

## 待搞清楚

- [ ] uvicorn 和 FastAPI 为什么是两个分开的包？
- [ ] 返回一个 dict，为什么客户端收到的是 JSON？
- [ ] TestClient 没起服务器，怎么发的请求？
- [ ] --host 0.0.0.0 和 127.0.0.1 的区别？
- [ ] 为什么端口要用 $PORT 环境变量？
- [ ] pip freeze 出来的传递依赖要不要全留着？



1. installed the macOS command line developer tools, python3 version 3.9.6, do I need upgrade python, what is the upgrade command, tried python3 --upgrade, incorrect
2. source .venv/bin/activate, why we need this
3. why we need to install uvicorn and httpx, I know fastapi is for api, pytest is for unit test
4. WARNING: You are using pip version 21.2.4; however, version 26.0.1 is available.

5. from fastapi import FastAPI 是从fastapi这个模块或者这个包，调用FASTAPI 这个方法, 不过这个方法怎么用，有哪些参数字段，在什么地方可以快速查询或学习呢，还是说些后端程序，这些常用的基本会记住，大部分的调用方式都很固定，很规则
6. uvicorn main:app -reload 详细解释, http://127.0.0.1:8000/ 显示json {"detail":"Not Found"},
```
INFO:     Will watch for changes in these directories: ['/Users/jie/Documents/Job/Project/pagecheck']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [23835] using WatchFiles
INFO:     Started server process [23837]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:55326 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55326 - "GET /favicon.ico HTTP/1.1" 404 Not Found
```
7. why not from pytest import TestClient, but from fastapi.testclient
8. how assert works in test
9. how pytest works, pytest -v what does v means
10. for .gitignore I can see .pytest_cache and .venv right now, how about __pycache__/,*.pyc and .DS_Store
11. what is .yml
12 
```
git init
git add .
git commit -m "Add health endpoint, test and CI"
git branch -M main
```

## 已确认的