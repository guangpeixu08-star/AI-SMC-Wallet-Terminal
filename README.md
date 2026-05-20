# 📊 AI-SMC 智能资产管理终端 (AI-SMC Wallet Terminal)

> 🏆 **imToken 10th Anniversary Hackathon - AI 共创极客作品**
> 
> 本项目贯彻 **“Vibe Coding”** 理念，致力于用最低的交互门槛，构建具备华尔街级别的 Smart Money (SMC) 自动化追踪与资产隔离管理终端。

## 💡 项目简介 (Project Overview)

在 Web3 交易中，普通用户难以实时追踪巨鲸（Whales）动向，且现有的 AI 钱包极易将私钥暴露在前端或脚本内存中，存在极大的安全隐患。

本终端旨在打造一个 **“能听懂人话的智能加密资产管家”**。用户只需输入自然语言指令（如：“帮我用主账户跟单波段巨鲸01”），系统的大语言模型语义层即可自动解析意图、分配路由，并**安全隔离**地调用底层密码学内核完成跨链操作。

## 🛡️ 核心架构与安全声明 (Security & Architecture)

本项目采用了 **“Python 胶水层前端 + TokenCore Rust 物理隔离底层”** 的极客架构设计：

- **前端交互 (Streamlit)**：提供极致流畅的数据大屏、SMC 胜率计算与策略路由分配。
- **意图解析 (AI NLP)**：将用户的大白话实时转换为结构化的 JSON 交易体 (Transaction Payload)。
- **隔离签名引擎 (TokenCore Bridge)**：**【核心安全亮点】** 所有的私钥派生、加密和离线交易签名，**100% 拒绝在 Python 内存中计算**。系统通过 `subprocess` 后台静默唤醒官方提供的 `tcx-cli` (Rust 编译的二进制执行文件) 进行物理级算力隔离。
  
*(注：为方便评审验证交互流，当前 Demo 仓库桥接层采用 Mock 数据演示。进入主网部署时，仅需将同目录下的 `tcx-cli` 替换为官方原生二进制文件，业务代码 0 修改即可无缝衔接。)*

## ✨ 核心功能点 (Key Features)

1. **跨链巨鲸狙击雷达**：支持自定义注入 ETH、SOL、BSC、BASE 等多链的 SMC 目标，一键开启自动化跟单路由。
2. **多态资产驾驶舱**：告别简陋的插件 UI，实时汇聚本地多钱包资产总值与动态余额。
3. **极简 AI 交互舱**：将复杂的 Gas 计算、跨链桥接、ABI 授权，全部转化为自然语言对话输入。
4. **强风控 Policy 拦截**：在交由 TokenCore 签名前，本地策略库（如：单笔最大限制 1.0 ETH）会进行交易前的刚性熔断自察。

## 🛠️ 技术栈 (Tech Stack)

- **UI & 业务流**: Python 3.9+, Streamlit, Pandas (数据结构化)
- **底层签名内核**: imToken TokenCore (`tcx-cli` 原生集成)
- **集成模式**: Facade Pattern (外观模式) + 进程级通信隔离

## 🚀 快速启动 (Quick Start)

```bash
# 1. 克隆本仓库
git clone [https://github.com/你的用户名/AI-SMC-钱包终端.git](https://github.com/你的用户名/AI-SMC-钱包终端.git)

# 2. 安装 Python 依赖
pip install streamlit pandas numpy

# 3. 启动交互式终端大屏
streamlit run app.py
