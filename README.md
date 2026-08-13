# 📚 KitobJavon — Book-Crossing & Book Marketplace (O'zbekiston)

Telegram bot + Mini App orqali kitob sotish, ijaraga berish va almashtirish platformasi.

## ✅ Bot tokeni allaqachon ulangan
`backend/.env` va `bot/.env` fayllarida bot tokeningiz turibdi (git'ga tushmaydi —
`.gitignore`da). Boshqa hech narsa qo'lda kiritmasdan pastdagi buyruqlarni bajarsangiz
bo'ldi. Faqat `WEBAPP_URL` (bot/.env) — frontendni deploy qilgach to'ldiriladi.

## Tuzilma
```
book-marketplace/
├── bot/          → aiogram bot (/start → WebApp tugmasi)   [Python]
├── backend/      → Django + Django REST Framework API      [Python]
└── frontend/     → Telegram Mini App (Vue 3 + Vite)         [Vue.js]
```

## 1. Backend'ni ishga tushirish (Django)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
`BOT_TOKEN`, `SECRET_KEY` va h.k. `backend/.env`dan avtomatik o'qiladi
(`python-dotenv` orqali) — qo'lda `export` qilish shart emas.

API `http://localhost:8000/api/health` orqali tekshiriladi.

Admin panel kerak bo'lsa: `python manage.py createsuperuser` va `http://localhost:8000/admin/`.

### API endpointlari
- `GET  /api/health`
- `GET  /api/cities`
- `POST /api/auth/register` — `{phone, password, full_name?}` → `{token, user}`
- `POST /api/auth/login` — `{phone, password}` → `{token, user}`
- `GET  /api/books` — `?city=&status=&search=` filtrlari bilan
- `POST /api/books` — autentifikatsiya + telefon talab qiladi
- `GET  /api/books/mine/list` — autentifikatsiya talab qiladi
- `GET  /api/books/<id>`
- `DELETE /api/books/<id>` — faqat egasi
- `POST /api/upload` — autentifikatsiya talab qiladi, rasm yuklash
- `GET  /api/profile/me` — joriy foydalanuvchi profili
- `PATCH /api/profile/me` — profilni to'ldirish/yangilash (`full_name`, `phone`, `city`)

Autentifikatsiya ikki xil:
1. **Telefon + parol** — `/api/auth/register` yoki `/api/auth/login` orqali `token` oling,
   keyin himoyalangan so'rovlarda `Authorization: Bearer <token>` yuboring.
2. **Telegram Mini App** — `X-Telegram-Init-Data` headeri (avvalgidek).

Kitob qo'shishdan oldin telefon raqam kerak.

## 2. Botni ishga tushirish

```bash
cd bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python bot.py
```
`BOT_TOKEN` `bot/.env`dan avtomatik o'qiladi. `WEBAPP_URL`ni frontendni deploy
qilgach shu faylda yangilang (Telegram Mini App faqat **HTTPS** manzilda ochiladi).

## 3. Frontend'ni ishga tushirish (Vue 3 + Vite)

```bash
cd frontend
npm install
cp .env.example .env    # VITE_API_BASE ni backend manzilingizga moslang
npm run dev              # lokal: http://localhost:5500
```

Productionga tayyorlash:
```bash
npm run build             # natija: frontend/dist/
```
`dist/` papkasini Vercel/Netlify kabi xizmatga static sayt sifatida deploy qiling —
Telegram Mini App faqat **HTTPS** manzilda ochiladi.

**Lokal test** uchun `ngrok http 5500` orqali vaqtinchalik HTTPS oling.

Deploydan keyin: `frontend/.env`dagi `VITE_API_BASE`ni backend manzilingizga,
`bot/.env`dagi `WEBAPP_URL`ni frontend manzilingizga yozing.

## 4. BotFather sozlamalari
1. @BotFather → botingiz → **Bot Settings → Menu Button** → webapp URL'ni kiriting.
2. Yoki `/start` javobida inline `WebAppInfo` tugmasidan foydalaning (allaqachon qo'shilgan).

## Texnologiyalar
- **Frontend:** Vue.js 3 (Composition API, `<script setup>`) + Vite
- **Backend:** Django 5 + Django REST Framework
- **Bot:** Python (aiogram 3)
- **DB:** SQLite (dev) / PostgreSQL (production, `dj-database-url` orqali)

## Keyingi bosqichlar (roadmap)
- [ ] "Mening kitoblarim" sahifasi (frontendda `/books/mine/list` allaqachon tayyor)
- [ ] Sevimlilar (wishlist)
- [ ] Push-bildirishnoma: yangi kitob qo'shilganda mos foydalanuvchilarga xabar
- [ ] Admin panel orqali noqonuniy e'lonlarni o'chirish (Django admin allaqachon mavjud)
- [ ] Docker Compose bilan production deploy
- [ ] Xarita orqali "yaqin atrofdagi kitoblar" (geolokatsiya)
