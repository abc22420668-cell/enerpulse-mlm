# EnerPulse (TM) — MLM E-Commerce Platform

## 快速開始

```bash
cp .env.example .env  # 編輯 .env 設定
docker-compose up -d    # 啟動 PostgreSQL + Redis
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 專案 Apps

- `accounts` — 會員認證、個人檔案、二元樹
- `products` — 商品目錄（量子脈衝頻率儀）
- `cart` — 購物車
- `orders` — 訂單 & USDT 付款
- `wallet` — 虛擬錢包（獎金 + 重消）
- `mlm` — 二元樹、獎金計算、推薦連結
- `payment` — USDT 金流整合

## 公司資訊

- **公司名稱**: EnerPulse (TM)
- **主要產品**: 量子脈衝頻率儀
- **獎金制度**: 雙軌制（參考 OlyLife 商業模式）
