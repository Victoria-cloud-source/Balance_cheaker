import json
import time
from web3 import Web3

# Загрузка конфигурации сетей
with open('networks.json', 'r') as f:
    NETWORKS = json.load(f)

def select_network():
    print("🌐 Выберите сеть для проверки:")
    for idx, (key, net) in enumerate(NETWORKS.items(), start=1):
        print(f"{idx}. {net['name']}")
    
    choice = int(input("Введите номер сети: ")) - 1
    network_keys = list(NETWORKS.keys())
    selected_key = network_keys[choice]
    selected_network = NETWORKS[selected_key]

    return selected_network

def load_wallets(filename="wallets.txt"):
    try:
        with open(filename, 'r') as f:
            addresses = [line.strip() for line in f if line.strip()]
        return addresses
    except FileNotFoundError:
        print("❌ Файл с кошельками не найден.")
        return []

def get_balance(w3, address):
    try:
        checksum_address = w3.toChecksumAddress(address)
        balance_wei = w3.eth.get_balance(checksum_address)
        balance_eth = w3.fromWei(balance_wei, 'ether')
        return float(balance_eth)
    except Exception as e:
        return f"Ошибка: {str(e)}"

def main():
    print("🧾 EVM Баланс чекер v1.0\n")

    network = select_network()
    print(f"\n🔌 Подключение к {network['name']}...\n")

    w3 = Web3(Web3.HTTPProvider(network["rpc_url"]))
    
    if not w3.is_connected():
        print("❌ Не удалось подключиться к узлу. Проверьте RPC URL и интернет соединение.")
        return

    wallets = load_wallets()
    if not wallets:
        print("❌ Нет кошельков для проверки.")
        return

    print(f"🔍 Проверяю балансы на {network['name']} ({len(wallets)} кошельков)\n")

    for i, address in enumerate(wallets, start=1):
        balance = get_balance(w3, address)
        if isinstance(balance, float):
            print(f"[{i}/{len(wallets)}] {address} → {balance:.6f} {w3.chain_id_to_currency_symbol(w3.eth.chain_id)}")
        else:
            print(f"[{i}/{len(wallets)}] {address} → ❌ {balance}")
        time.sleep(0.3)

if __name__ == "__main__":
    main()
