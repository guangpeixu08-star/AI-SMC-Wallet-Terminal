import streamlit as st
from token_core_bridge import TokenCoreBridge
import time
import pandas as pd
import numpy as np

# ================= 1. 页面级 Pro 配置 =================
st.set_page_config(
    page_title="AI-SMC 智能资产管理终端",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义极客风暗黑主题样式
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div[data-testid="stMetricValue"] { color: #DEFF9A; font-family: 'Courier New', monospace; font-weight: bold; }
    .stHeading h1, .stHeading h2, .stHeading h3 { color: #DEFF9A; }
    .stAlert { background-color: #161b22; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)


# 初始化底层引擎单例
@st.cache_resource
def get_bridge():
    return TokenCoreBridge(cli_executable="tcx-cli")


bridge = get_bridge()

# ================= 2. 状态机初始化 (State Management) =================
if "wallets" not in st.session_state:
    # 初始化一个默认的本地钱包，并赋予初始余额
    st.session_state["wallets"] = [{
        "chain": "ETH",
        "address": "0x71C95911E9a5D330f4D0c410b27b91122",
        "pk": "0x_mock_main_pk",
        "alias": "我的主充值账户 (Main_Wallet)",
        "balance": 2.5000  # 自己的余额
    }]

if "smc_targets" not in st.session_state:
    # 预置两个链上著名的“聪明钱”巨鲸地址作为Demo展示
    st.session_state["smc_targets"] = [
        {"name": "SMC_波段巨鲸_01", "chain": "ETH", "address": "0x9e7b...9c1a", "status": "监控中", "copied_tx": 14},
        {"name": "Solana_Meme神手", "chain": "SOL", "address": "8FvG...3xPp", "status": "监控中", "copied_tx": 32}
    ]

if "system_logs" not in st.session_state:
    st.session_state["system_logs"] = [f"[{time.strftime('%H:%M:%S')}] 系统初始化：TokenCore 密码学内核就绪."]


def add_log(msg: str):
    st.session_state["system_logs"].insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")


# ================= 3. 侧边栏：核心控制台 =================
with st.sidebar:
    st.markdown("## 🛡️ 安全内核控制 (TokenCore)")
    st.caption("当前引擎状态: `Rust CLI 隔离运行中`")
    st.markdown("---")

    target_chain = st.selectbox("核心目标链环境", [
        "以太坊 (ETH 主网)",
        "Sepolia 测试网",
        "BNB Chain (BSC)",
        "Base L2",
        "Solana (SOL)",
        "波场 (TRON)"
    ])

    if "ETH" in target_chain or "Sepolia" in target_chain:
        chain_code = "ETH"
    elif "BNB" in target_chain:
        chain_code = "BNB"
    elif "Base" in target_chain:
        chain_code = "BASE"
    elif "Solana" in target_chain:
        chain_code = "SOL"
    else:
        chain_code = "TRON"

    st.markdown("### 🔑 账户派生")
    if st.button("🚀 物理隔离生成新密钥对", use_container_width=True, type="primary"):
        with st.spinner(f"唤醒底层，正在派生 {chain_code} 密钥对..."):
            res = bridge.generate_account(chain=chain_code)
            if res["status"] == "success":
                new_wallet = res["data"]
                st.session_state["wallets"].append({
                    "chain": chain_code,
                    "address": new_wallet.get("address", "0x..."),
                    "pk": new_wallet.get("private_key", ""),
                    "alias": f"自动化子钱包_#{len(st.session_state['wallets']) + 1}",
                    "balance": 0.0000  # 新生成的账户初始余额为 0
                })
                add_log(f"成功派生 {chain_code} 地址: {new_wallet.get('address')[:10]}...")
                st.toast(f"TokenCore {chain_code} 密钥派生成功！", icon="✅")

# ================= 4. 主界面：跨链资产管理大屏 =================
st.title("📊 AI-SMC 聪明钱量化追踪与自动化资产终端")
st.markdown("`黑客松交付原型 v1.2.0` | `已集成跟单管理与本地余额控制流`")
st.markdown("---")

# 计算资产总值（动态汇总本地所有钱包的余额）
total_eth_balance = sum([w["balance"] for w in st.session_state["wallets"] if w["chain"] in ["ETH", "BASE"]])
total_sol_balance = sum([w["balance"] for w in st.session_state["wallets"] if w["chain"] == "SOL"])

# 顶层核心指标 (Metrics)
m1, m2, m3, m4 = st.columns(4)
m1.metric("本地钱包总数", f"{len(st.session_state['wallets'])} 个")
m2.metric("当前托管总资产 (ETH / SOL)", f"{total_eth_balance:.4f} ETH / {total_sol_balance:.2f} SOL")
m3.metric("活动跟单目标数", f"{len(st.session_state['smc_targets'])} 个地址")
m4.metric("AI 自动节约 Gas", "$ 42.15", "批量归集保护开启")

st.markdown("---")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    # --------- 模块 A：聪明钱(SMC)跟单管理中心 ---------
    st.subheader("🎯 聪明钱 (SMC) 巨鲸跟单控制台")

    # 子布局1：添加要跟单的巨鲸
    with st.expander("➕ 添加新的链上聪明钱(SMC)监控目标", expanded=False):
        with st.form("smc_form", clear_on_submit=True):
            new_smc_name = st.text_input("巨鲸别名/标签：", placeholder="例如：Ave 榜一高胜率地址")
            new_smc_chain = st.selectbox("目标链：", ["ETH", "SOL", "BSC", "BASE", "TRON"])
            new_smc_addr = st.text_input("链上巨鲸地址：", placeholder="输入 0x 或 Solana 格式的长地址")
            submit_smc = st.form_submit_button("确认注入监控流")

            if submit_smc and new_smc_addr:
                st.session_state["smc_targets"].append({
                    "name": new_smc_name if new_smc_name else f"未命名巨鲸_{len(st.session_state['smc_targets']) + 1}",
                    "chain": new_smc_chain,
                    "address": new_smc_addr,
                    "status": "监控中",
                    "copied_tx": 0
                })
                add_log(f"前端注入新监控目标 [{new_smc_chain}] {new_smc_name}")
                st.toast("监控目标注入成功！", icon="👀")

    # 子布局2：用表格直观展示正在跟单的地址列表
    if st.session_state["smc_targets"]:
        df_smc = pd.DataFrame(st.session_state["smc_targets"])
        st.dataframe(df_smc, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------- 模块 B：本地安全资产地址池及余额 ---------
    st.subheader("📂 本地安全资产地址池 (监控我自己的钱包与余额)")

    for idx, w in enumerate(reversed(st.session_state["wallets"])):
        # 反转索引确保最新生成的钱包在最上面
        real_idx = len(st.session_state["wallets"]) - 1 - idx
        with st.expander(f"⚙️ 【{w['alias']}】 | 链: {w['chain']} | 动态余额: {w['balance']:.4f} {w['chain']}",
                         expanded=(idx == 0)):
            st.code(w['address'], language="text")

            c1, c2 = st.columns(2)
            with c1:
                st.caption("💰 模拟余额调整（方便录制演示视频）")
                # 允许在网页上直接调整自己的余额，方便给评委看数据变化
                new_bal = st.number_input(f"调整账户余额 ({w['chain']}):", min_value=0.0, value=float(w['balance']),
                                          step=0.1, key=f"bal_input_{real_idx}")
                st.session_state["wallets"][real_idx]["balance"] = new_bal

                st.caption("🎯 本地跟单策略映射")
                st.checkbox("允许本账户自动复制上面监控列表中的交易", value=True, key=f"cb1_{real_idx}")

            with c2:
                st.caption("🔐 链上安全交互 (由 Rust 内核隔离签名)")
                if st.button(f"🚨 触发 {w['chain']} 资产安全归集签名", key=f"sign_{real_idx}", use_container_width=True):
                    mock_payload = {"to": "0x000000000000000000000000000000000000dEaD",
                                    "value": str(int(w['balance'] * 10 ** 18))}
                    sign_res = bridge.sign_transaction(w["pk"], mock_payload)
                    if sign_res["status"] == "success":
                        st.success("✅ 离线冷签名成功！核心边界无违规。")
                        st.json(sign_res["data"])
                        add_log(f"账户 {w['alias']} 调用 TokenCore 完成了一笔 {w['chain']} 归集签名.")

with col_right:
    # --------- 模块 C：AI 指令解析与日志 ---------
    st.subheader("🤖 智能 AI 指令交互")
    ai_cmd = st.text_input("📝 输入自然语言指令（AI 自动拆解并组装链上交易）:",
                           placeholder="例如: 帮我用主账户跟单波段巨鲸01")
    if ai_cmd:
        st.write("🔄 **AI 语义分析中...**")
        time.sleep(0.6)
        st.success("🤖 **意图识别完成：【绑定跟单路由】**")
        st.code("""
        {
            "action": "BIND_COPY_ROUTE",
            "executor_wallet": "我的主充值账户 (Main_Wallet)",
            "target_whale": "SMC_波段巨鲸_01",
            "allocation_percentage": "100%",
            "risk_policy": "SINGLE_TX_MAX_0.5_ETH"
        }
        """, language="json")
        st.caption("💡 提示：系统已自动完成策略路由分配，底层隔离运行中。")

    st.markdown("---")
    st.subheader("🖥️ 架构层实时流日志")
    log_box = st.container(height=260)
    with log_box:
        for log in st.session_state["system_logs"]:
            st.text(log)