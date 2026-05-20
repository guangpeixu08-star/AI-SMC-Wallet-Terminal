import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - TokenCoreBridge: %(message)s")


class TokenCoreBridge:
    """
    [黑客松 Demo 版本]
    模拟 TokenCore (Rust) 的底层通信桥接器。
    用于在 Windows 环境下快速跑通前端 UI 和业务流，接口完全兼容真实的 tcx-cli。
    """

    def __init__(self, cli_executable: str = "tcx-cli"):
        self.cli_path = cli_executable
        logging.info("初始化 TokenCoreBridge (安全模拟模式已开启)")

    def generate_account(self, chain: str = "ETH") -> dict:
        """模拟：调用底层算力派生新账户"""
        logging.info(f"请求底层引擎生成 {chain} 链账户...")
        time.sleep(1.2)  # 假装底层在进行复杂的密码学计算

        # 针对不同链生成逼真的模拟地址
        # 利用时间戳生成不同的尾号，确保每次点击生成的地址看起来不一样
        tail = str(int(time.time() * 1000))[-4:]

        if chain in ["ETH", "BNB", "BASE"]:
            mock_address = f"0x71C95911E9a5D330f4D0c410b27b9{tail}"
        elif chain == "SOL":
            mock_address = f"HN7cABqLq46ZwZJ9EEA8vVv{tail}R5z39"
        elif chain == "TRON":
            mock_address = f"T9yD14Nj9j7xAB4dbGeiX9h8cq{tail}"
        else:
            mock_address = f"0x_Unknown_{tail}"

        mock_data = {
            "address": mock_address,
            "private_key": f"0x_mock_private_key_{chain}_do_not_use_in_production"
        }
        return {"status": "success", "data": mock_data}

    def sign_transaction(self, private_key: str, tx_payload: dict) -> dict:
        """模拟：执行离线安全签名"""
        logging.info("请求底层执行离线冷签名...")
        time.sleep(1)  # 假装在签名

        mock_data = {
            "raw_tx": f"0x02f8720183038d7ea8485...mock_signed_hash...{str(int(time.time()))[-4:]}8a9c",
            "tx_hash": f"0x123abc456def7890abcdef1234567890abcdef{str(int(time.time()))[-4:]}"
        }
        return {"status": "success", "data": mock_data}