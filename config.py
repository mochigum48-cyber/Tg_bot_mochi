import os
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = 1831176946
OWNER_IDS = [1831176946, 7897641671]
ADMIN_IDS = []

FORCE_JOIN_CHANNELS = [
    {"id": -1003676391477, "name": "Channel 1", "link": "https://t.me/RO_Bookshelf"},
    {"id": -1003394243505, "name": "Channel 2", "link": "https://t.me/lawofpowerr"},
    {"id": -1003710354598, "name": "Group", "link": "https://t.me/readerodessey_chat"},
]

FILE_CHANNEL_ID = -1003194087750
LOG_GROUP_ID = -1003283270830

GEMINI_API_KEY = "AQ.Ab8RN6IrSMsYKP-Zy5zEeIAh-Fitdw53fYt7S2PmG7WYyPkBcQ"
MONGO_URI = "mongodb+srv://mochigum48_db_user:1PvxK6eZ0yTyEfA1@cluster0.kchfkar.mongodb.net/?appName=Cluster0"
MONGO_DB = "reader_odyssey"
SHORTLINK_API_KEY = "e5d44ced685fe5b145b4f6c5987c14f18c57f876"
SHORTLINK_SITE_URL = "https://shrinkme.io/api"

DATABASE_URL = "sqlite+aiosqlite:///data/reader_odyssey.db"
DEFAULT_LANG = "my"
LANGS = ["my", "en"]

# ==============================
# DONATION SETTINGS
# ==============================

PAYMENT_NUMBER = "09758048960"
PAYMENT_NAME = "Nang Su Thet Nway"
PHONE_BILL_NUMBER = "09758048960"

# ===== DONATE =====
DONATE_AMOUNTS = [500, 1000, 2000, 3000, 5000, 10000]

DAILY_GIFT_MIN = 1
DAILY_GIFT_MAX = 30

FREE_MAX_POINTS = 150
REFERRAL_POINTS = 10
REFERRAL_BONUS = 5
REFERRAL_BONUS_COUNT = 5

FREE_DAILY_DOWNLOADS = 5
FREE_DAILY_AI = 3

DEFAULT_LANG = "my"
LANGS = ["my", "en"]

MESSAGES = {
    "welcome": {
        "my": "မင်္ဂလာပါ {name} 👑\n\n📚 Reader Odyssey မှ ကြိုဆိုပါသည်။\n\nReader Odyssey Bot တွင်\nအခမဲ့ စာအုပ်စာပေပေါင်း ၁၀၀၀+ ကို\nစိတ်ကြိုက်ဖတ်ရှုနိုင်ပါသည်။",
        "en": "Welcome {name} 👑\n\n📚 Welcome to Reader Odyssey.\n\nPremium Myanmar Library with 1000+ free books."
    },
    "force_join": {
        "my": "ဖတ်ရှုခွင့် စစ်ဆေးခြင်း ⚠️\n\nစာအုပ်ဖတ်ရှုနိုင်ရန် အောက်ပါ\nChannel/Group များအားလုံးကို\nဦးစွာ Join ပေးရန် လိုအပ်ပါသည်။\n\n{channels}\n\n✅ Join ပြီးပါက \"အတည်ပြုရန်\" နှိပ်ပါ",
        "en": "Join Required ⚠️\n\nPlease join all channels first.\n\n{channels}\n\n✅ Press Verify after joining."
    },
    "join_done": {
        "my": "စစ်ဆေးပြီးပါပြီ ✅\n\n📥 စာအုပ်ကို ဖတ်ရှုနိုင်ပါပြီ။",
        "en": "Verified ✅\n\n📥 You can now read the book."
    },
    "daily_gift": {
        "my": "နေ့စဉ်လက်ဆောင် 🎁\n\nသင့်လက်ဆောင်ကို ဖွင့်နေပါသည်...\n\n🎉 ဂုဏ်ယူပါသည်!\n\nယနေ့ နေ့စဉ်လက်ဆောင်အဖြစ်\nခရက်ဒစ် {points} ရရှိပါသည်။\n\n🔥 ဆက်တိုက်ရယူမှု: {streak} ရက်",
        "en": "Daily Gift 🎁\n\nOpening your gift...\n\n🎉 Congratulations!\n\nYou received {points} credits.\n\n🔥 Streak: {streak} days"
    },
    "daily_gift_done": {
        "my": "နေ့စဉ်လက်ဆောင် 🎁\n\nယနေ့အတွက် လက်ဆောင်\nရယူပြီးပါပြီ။\n\n🕐 နောက်တစ်နေ့တွင်\nထပ်မံလာရောက်ပါရန်\nလေးစားစွာ ဖိတ်ခေါ်အပ်ပါသည်။",
        "en": "Daily Gift 🎁\n\nAlready claimed today.\n\n🕐 Come back tomorrow!"
    },
    "referral": {
        "my": "မိတ်ဆက်ကုဒ် 👥\n\nသင့်ကုဒ်: {code}\n\nမိတ်ဆွေများကို ဖိတ်ခေါ်ပြီး\nခရက်ဒစ်များ ရယူပါ။\n\n• ၁ ယောက် = ၅ မှတ်\n• ၅ ယောက်ပြည့် = +၅ ထပ်ဆောင်း",
        "en": "Referral 👥\n\nYour code: {code}\n\nInvite friends to earn credits.\n\n• 1 person = 5 pts\n• 5 people = +5 bonus"
    },
}

print("✅ Config loaded!")
