# Nebius Personal AI — ≤3 分钟演示视频脚本

> 目标：Devpost 要求 "a 3-minute or shorter public YouTube video showing your project working."
> 拍摄方式：录屏（OBS / 系统录屏），窗口 = 终端 + 浏览器（访问 demo URL）。
> 关键卖点必须在前 60 秒出现：持久记忆 + 工具调用 + Nemotron via Token Factory。

---

## 镜头 0 — 片头（0:00–0:15）
- 画面：标题卡「Nebius Personal AI · NVIDIA Nemotron on Nebius Token Factory」。
- 旁白：*"This is a private Personal AI. It remembers across sessions, has reusable tools, and runs entirely on NVIDIA Nemotron through Nebius Token Factory."*

## 镜头 1 — 启动 + 记忆写入（0:15–0:50）
- 终端：`python serve.py`（或 `python app.py`）
- 浏览器/ curl 调 `/remember`：
  ```
  curl -X POST localhost:8000/remember -d '{"key":"standup","value":"Team sync Thu 10am"}'
  ```
- 旁白：*"I store a fact locally. Nothing leaves the machine except the chat text to my Nebius endpoint."*

## 镜头 2 — 对话 + 工具调用（0:50–1:40）
- 终端对话：*"What's my standup time?"* → 助手调用 `recall` → 答 "Thu 10am"。
- 旁白：*"The model, Nemotron on Token Factory, decides to call the recall tool and answers from my local memory."*

## 镜头 3 — 持久性证明（1:40–2:20）★ 评委最看重的点
- `Ctrl-C` 关掉服务 → 重新 `python serve.py` 启动。
- curl `/recall?key=standup` → 仍返回 "Thu 10am"。
- 旁白：*"I restarted the server. Memory is file-backed and survived — that's real persistence, not a session cache."*

## 镜头 4 — 提醒工具（2:20–2:45）
- curl `/remind` 设一个 near-future 提醒 → 到点触发。
- 旁白：*"Reusable skills: a remind tool, scheduled locally."*

## 镜头 5 — 结尾（2:45–3:00）
- 画面切回标题卡 + 仓库/Token Factory 水印。
- 旁白：*"Private by design, open by infrastructure. Built on NVIDIA Nemotron + Nebius Token Factory."*

---

## 拍摄清单
- [ ] 录屏软件就绪（OBS / 系统录制）
- [ ] `NEBIUS_API_KEY` 已 `export`（运行 `python app.py` 实测一次对话）
- [ ] `serve.py` 在 localhost:8000 跑通（或已部署 HF Space）
- [ ] 上传 YouTube **Public**（非 Unlisted）
- [ ] 视频链接填进 `DEVPOST_COPY.md` 的占位

> 无 key 时也能拍「工具层」演示：用 `--mock` 走脚本化 Nemotron 响应，先把 UI/流程录出来；正式提交前用真实 key 重录对话段即可。
