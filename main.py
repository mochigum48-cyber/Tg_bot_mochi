import asyncio
import logging
import uuid
import aiohttp
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from motor.motor_asyncio import AsyncIOMotorClient
import google.generativeai as genai

# ==========================================
# 1. CONFIGURATION (HARDCODED)
# ==========================================
BOT_TOKEN = "8932194744:AAEz6iv7dPhP6KJg1SIwVGmlpH7ISI8ybdc"
ADMIN_IDS = [1831176946, 7897641671]

GROUP_ID = -1003283270830
MAIN_CHANNEL = -1003676391477
FILE_CHANNEL = -1003899149079
FORCE_JOIN_GROUP = -1003710354598
FORCE_JOIN_CHANNEL = -1003676391477

GEMINI_API_KEY = "AQ.Ab8RN6IrSMsYKP-Zy5zEeIAh-Fitdw53fYt7S2PmG7WYyPkBcQ"
MONGO_URI = "mongodb+srv://mochigum48_db_user:itismemochigun@cluster0.kchfkar.mongodb.net/?appName=Cluster0"
SHORTLINK_API_KEY = "2d77152a987921c3e5015e4519daeaa9e2e285e5"

# ==========================================
# 2. DATABASE SETUP (MONGODB)
# ==========================================
client = AsyncIOMotorClient(MONGO_URI)
db = client["telegram_ai_bot"]

users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
books_col = db["books"]

async def get_or_create_user(user_id: int, username: str = None, referrer_id: int = None):
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        user_data = {
            "user_id": user_id,
            "username": username,
            "status": "free_user",
            "mode": "library_mode",
            "task": "idle",
            "pid": None,
            "mark": [],
            "reputation": 100,
            "points": 0,
            "referral_count": 0,
            "referrer_id": referrer_id,
            "last_claim": None,
            "created_at": datetime.now(timezone.utc)
        }
        await users_col.insert_one(user_data)
        return user_data
    return user

async def add_points(user_id: int, points: int):
    await users_col.update_one({"user_id": user_id}, {"$inc": {"points": points}})

# ==========================================
# 3. FSM STATES
# ==========================================
class UserStates(StatesGroup):
    awaiting_slip = State()

class AdminStates(StatesGroup):
    uploading_pdf = State()
    adding_product_name = State()
    adding_product_price = State()

# ==========================================
# 4. EXTERNAL SERVICES (AI & SHORTLINK)
# ==========================================
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

async def generate_book_summary(text_content: str) -> str:
    prompt = f"Read this book excerpt and provide a review in Myanmar and English:\n{text_content[:4000]}"
    try:
        res = await ai_model.generate_content_async(prompt)
        return res.text
    except Exception as e:
        return f"Summary Error: {e}"

async def create_shortlink(destination_url: str) -> str:
    api_url = f"https://gplinks.in/api?api={SHORTLINK_API_KEY}&url={destination_url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as res:
                if res.status == 200:
                    data = await res.json()
                    if data.get("status") == "success":
                        return data.get("shortenedUrl")
    except Exception:
        pass
    return destination_url

# ==========================================
# 5. MIDDLEWARE (FORCE JOIN)
# ==========================================
class ForceJoinMiddleware(BaseMiddleware):
    async def call(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if not user or user.id in ADMIN_IDS:
            return await handler(event, data)

        try:
            bot = data['bot']
            ch = await bot.get_chat_member(FORCE_JOIN_CHANNEL, user.id)
            gp = await bot.get_chat_member(FORCE_JOIN_GROUP, user.id)
            
            if not (ch.status in ['member', 'administrator', 'creator'] and gp.status in ['member', 'administrator', 'creator']):
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="📢 Join Channel", url=f"https://t.me/c/{str(FORCE_JOIN_CHANNEL).replace('-100', '')}"),
                    InlineKeyboardButton(text="💬 Join Group", url=f"https://t.me/c/{str(FORCE_JOIN_GROUP).replace('-100', '')}")
                ]])
                msg = "⚠️ ဘော့ကို အသုံးပြုရန် အောက်ပါ Channel နှင့် Group သို့ Join ပေးပါရန်။"
                if isinstance(event, Message):
                    await event.answer(msg, reply_markup=kb, parse_mode="Markdown")
                elif isinstance(event, CallbackQuery):
                    await event.message.answer(msg, reply_markup=kb, parse_mode="Markdown")
                return
        except Exception:
            pass

        return await handler(event, data)

# ==========================================
# 6. ROUTERS & HANDLERS
# ==========================================
router = Router()

# --- START & USER DASHBOARD ---
@router.message(CommandStart())
async def start_cmd(message: Message):
    args = message.text.split()
    ref_id = int(args[1]) if len(args) > 1 and args[1].isdigit() and int(args[1]) != message.from_user.id else None
    
    user = await get_or_create_user(message.from_user.id, message.from_user.username, ref_id)
    
    if ref_id and user.get("referrer_id") == ref_id:
        await add_points(ref_id, 15)
        await users_col.update_one({"user_id": ref_id}, {"$inc": {"referral_count": 1}})

    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"

    text = (
        f"👋 မင်္ဂလာပါ {message.from_user.full_name}!\n\n"
        f"🆔 User ID: {user['user_id']}\n"
        f"💎 Points: {user['points']} Points\n"
        f"👥 Referrals: {user['referral_count']} ယောက်\n\n"
        f"🔗 Referral Link:\n{ref_link}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍️ VISIT SHOP", callback_data="open_shop")],
        [InlineKeyboardButton(text="🎁 Daily Claim (+15)", callback_data="claim_daily")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

# --- DAILY CLAIM ---
@router.callback_query(F.data == "claim_daily")
async def claim_daily_cb(cb: CallbackQuery):
    user = await get_or_create_user(cb.from_user.id)
    last_claim = user.get("last_claim")
    now = datetime.now(timezone.utc)

    if last_claim and (now - last_claim) < timedelta(hours=24):
        await cb.answer("⏳ 24 နာရီ မပြည့်သေးပါခင်ဗျာ!", show_alert=True)
        return

    await add_points(cb.from_user.id, 15)
    await users_col.update_one({"user_id": cb.from_user.id}, {"$set": {"last_claim": now}})
    await cb.message.answer("🎉 Daily Bonus +15 Points ရရှိသွားပါပြီ!")
    await cb.answer()

# --- SHOP & CHECKOUT ---
@router.callback_query(F.data == "open_shop")
async def open_shop_cb(cb: CallbackQuery):
    products = await products_col.find({}).to_list(length=10)
    if not products:
        await cb.message.answer("🛍️ ပစ္စည်းများ မရှိသေးပါခင်ဗျာ။")
        await cb.answer()
        return

    buttons = [[InlineKeyboardButton(text=f"{p['name']} - {p['price']} MMK", callback_data=f"buy_{p['pid']}")] for p in products]
    await cb.message.answer("🛍️ SHOP CATALOG", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await cb.answer()

@router.callback_query(F.data.startswith("buy_"))
async def buy_product_cb(cb: CallbackQuery, state: FSMContext):
  pid = cb.data.replace("buy_", "")
    product = await products_col.find_one({"pid": pid})
    if product:
        await state.update_data(checkout_pid=pid, price=product['price'])
        await state.set_state(UserStates.awaiting_slip)
        await cb.message.answer(
            f"📦 {product['name']}\n💰 စျေးနှုန်း: {product['price']} MMK\n\n"
            "💳 KPay/Wave မှ ငွေလွှဲပြီး Slip Screenshot ပို့ပေးပါရန် -",
            parse_mode="Markdown"
        )
    await cb.answer()

@router.message(UserStates.awaiting_slip, F.photo)
async def process_slip(message: Message, state: FSMContext):
    data = await state.get_data()
    order_id = str(uuid.uuid4())[:8]
    
    await orders_col.insert_one({
        "order_id": order_id,
        "user_id": message.from_user.id,
        "pid": data.get("checkout_pid"),
        "price": data.get("price"),
        "status": "pending"
    })
    
    if ADMIN_IDS:
        await message.bot.send_photo(
            chat_id=ADMIN_IDS[0],
            photo=message.photo[-1].file_id,
            caption=f"🛍️ **NEW ORDER (#{order_id})**\nFrom: {message.from_user.id}",
            parse_mode="Markdown"
        )
    await message.answerငွေလွှဲပြေစာ လက်ခံရရှိပါပြီ!ီ!**")
    await state.clear()

# --- ADMIN COMMANDS ---
@router.message(Command("stats"), F.from_user.id.in_(ADMIN_IDS))
async def admin_stats_cmd(message: Message):
    users = await users_col.count_documents({})
    books = await books_col.count_documents({})
    await message.answer(fSTATSTS**\n\n👥 Users: {users}\n📚 Books: {books}", parse_mode="Markdown")

@router.message(Command("addbook"), F.from_user.id.in_(ADMIN_IDS))
async def add_book_cmd(message: Message, state: FSMContext):
    await state.set_state(AdminStates.uploading_pdf)
    await message.answer(စာအုပ် PDF ပို့ပေးပါရန် - -**")

@router.message(AdminStates.uploading_pdf, F.document)
async def process_pdf(message: Message, state: FSMContext):
    doc = message.document
    await message.answer(Gemini AI အလုပ်လုပ်နေပါသည်.....**")
    
    summary = await generate_book_summary(doc.file_name)
    file_msg = await message.bot.send_document(chat_id=FILE_CHANNEL, document=doc.file_id)
    
    pid = str(uuid.uuid4())[:8]
    raw_url = f"https://t.me/c/{str(FILE_CHANNEL).replace('-100', '')}/{file_msg.message_id}"
    short_url = await create_shortlink(raw_url)

    await books_col.insert_one({"pid": pid, "title": doc.file_name, "file_id": doc.file_id})
    
    post_text = f{doc.file_nam\n\n{summary}\n\Download:d:d:** {short_url}"
    await message.bot.send_message(chat_id=MAIN_CHANNEL, text=post_text, parse_mode="Markdown")
    await message.answer(f"✅ **အောင်မြင်စွာ တင်ပြီးပါပြီ! (PID: {pid})**", parse_mode="Markdown")
    await state.clear()

# ==========================================
# 7. MAIN ENTRY POINT
# ==========================================
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ForceJoinMiddleware())
    dp.callback_query.middleware(ForceJoinMiddleware())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    # Admin ဆီ တိုက်ရိုက် Message ပို့ခြင်း
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, tBot က စတင် အလုပ်လုပ်နေပါပြီဗျာ!ြီဗျာ!**")
        except Exception:
            pass

    print("\n" + "="*40)
    print("🚀 BOT IS RUNNING SUCCESSFULLY!")
    print("="*40 + "\n")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if name == "main":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
