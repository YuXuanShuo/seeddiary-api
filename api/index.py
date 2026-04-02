"""
SeedDiary - Vercel Serverless 后端
所有 API 路由整合在一个文件，纯内存存储
"""
import os
import re
import uuid
import json
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# ── JWT 密钥 ────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "seeddiary-dev-secret-2024")


# ── Mock 词根数据 ────────────────────────────
MOCK_WORDS = {
    "interview": [
        {
            "term": "confident", "phonetic": "/ˈkɒnfɪdənt/", "translation": "自信的",
            "color": "#3B82F6",
            "context": "I'm **confident** in expressing my professional strengths.",
            "prefix": {"value": "con-", "meaning": "完全地", "note": "加强语气"},
            "root": {"value": "fid", "meaning": "信任", "note": "源自拉丁语 fides"},
            "suffix": {"value": "-ent", "meaning": "形容词后缀", "note": "表示具有某种性质的"},
            "logic": "con（完全）+ fid（信任）+ ent = 完全信任自己 → confident",
            "relatedWords": [
                {"term": "faith", "phonetic": "/feɪθ/", "translation": "信念、信任"},
                {"term": "confide", "phonetic": "/kənˈfaɪd/", "translation": "吐露、信赖"},
                {"term": "reliable", "phonetic": "/rɪˈlaɪəbl/", "translation": "可靠的"},
                {"term": "fidelity", "phonetic": "/fɪˈdeləti/", "translation": "忠诚、忠贞"},
            ],
        },
        {
            "term": "professional", "phonetic": "/prəˈfeʃənl/", "translation": "专业的",
            "color": "#22C55E",
            "context": "I have **professional** experience in project management.",
            "prefix": {"value": "pro-", "meaning": "公开地", "note": "表示公开、在之前"},
            "root": {"value": "fess", "meaning": "说", "note": "源自拉丁语 fateri"},
            "suffix": {"value": "-ion", "meaning": "名词后缀", "note": "表示行为状态"},
            "logic": "pro（公开）+ fess（说）+ ion = 公开宣称 → profess",
            "relatedWords": [
                {"term": "professor", "phonetic": "/prəˈfesər/", "translation": "教授"},
                {"term": "confess", "phonetic": "/kənˈfes/", "translation": "坦白、承认"},
                {"term": "manifest", "phonetic": "/ˈmænɪfest/", "translation": "明显的"},
            ],
        },
        {
            "term": "thoroughly", "phonetic": "/ˈθʌrəli/", "translation": "彻底地",
            "color": "#F97316",
            "context": "I conducted a **thoroughly** analysis of the market.",
            "root": {"value": "thorough", "meaning": "穿透、彻底", "note": "古英语 durch"},
            "suffix": {"value": "-ly", "meaning": "副词后缀", "note": "形容词变副词"},
            "logic": "thorough（彻底的）+ ly = 彻底地",
            "relatedWords": [
                {"term": "through", "phonetic": "/θruː/", "translation": "穿过"},
                {"term": "throughout", "phonetic": "/θruːˈaʊt/", "translation": "贯穿"},
            ],
        },
        {
            "term": "competent", "phonetic": "/ˈkɒmpɪtənt/", "translation": "有能力的",
            "color": "#A78BFA",
            "context": "I am **competent** in handling multiple projects.",
            "prefix": {"value": "com-", "meaning": "一起", "note": "表示共同"},
            "root": {"value": "pet", "meaning": "追求", "note": "源自拉丁语 petere"},
            "suffix": {"value": "-ent", "meaning": "形容词后缀", "note": "表示具有...性质的"},
            "logic": "com（共同）+ pet（追求）+ ent = 能在竞争中胜出 → competent",
            "relatedWords": [
                {"term": "compete", "phonetic": "/kəmˈpiːt/", "translation": "竞争"},
                {"term": "competition", "phonetic": "/ˌkɒmpɪˈtɪʃən/", "translation": "比赛"},
                {"term": "appetite", "phonetic": "/ˈæpɪtaɪt/", "translation": "食欲"},
            ],
        },
    ],
    "work": [
        {
            "term": "present", "phonetic": "/prɪˈzent/", "translation": "展示、呈现",
            "color": "#3B82F6",
            "context": "I need to **present** our project progress at today's meeting.",
            "prefix": {"value": "pre-", "meaning": "之前", "note": "表示在...之前"},
            "root": {"value": "sent", "meaning": "存在", "note": "源自拉丁语 esse"},
            "suffix": {"value": "-ent", "meaning": "形容词后缀", "note": "表示状态"},
            "logic": "pre（之前）+ sent（存在）= 在别人面前存在 → present（展示）",
            "relatedWords": [
                {"term": "presence", "phonetic": "/ˈprezəns/", "translation": "出席、在场"},
                {"term": "represent", "phonetic": "/ˌreprɪˈzent/", "translation": "代表"},
                {"term": "absence", "phonetic": "/ˈæbsəns/", "translation": "缺席"},
            ],
        },
        {
            "term": "concise", "phonetic": "/kənˈsaɪs/", "translation": "简洁的",
            "color": "#22C55E",
            "context": "Please keep your email **concise** and to the point.",
            "prefix": {"value": "con-", "meaning": "完全", "note": "加强语气"},
            "root": {"value": "cis", "meaning": "切", "note": "源自拉丁语 caedere"},
            "suffix": {"value": "-e", "meaning": "形容词后缀", "note": "构成形容词"},
            "logic": "con（完全）+ cis（切）+ e = 把多余的全部切掉 → concise（简洁的）",
            "relatedWords": [
                {"term": "precision", "phonetic": "/prɪˈsɪʒən/", "translation": "精确"},
                {"term": "decide", "phonetic": "/dɪˈsaɪd/", "translation": "决定"},
                {"term": "scissors", "phonetic": "/ˈsɪzəz/", "translation": "剪刀"},
            ],
        },
        {
            "term": "collaborate", "phonetic": "/kəˈlæbəreɪt/", "translation": "合作、协作",
            "color": "#F97316",
            "context": "Our team **collaborate** effectively across departments.",
            "prefix": {"value": "col-", "meaning": "一起", "note": "com- 变体"},
            "root": {"value": "labor", "meaning": "劳动", "note": "源自拉丁语 labor"},
            "suffix": {"value": "-ate", "meaning": "动词后缀", "note": "表示使成为"},
            "logic": "col（一起）+ labor（劳动）+ ate = 一起劳动 → collaborate（合作）",
            "relatedWords": [
                {"term": "collaboration", "phonetic": "/kəˌlæbəˈreɪʃən/", "translation": "合作"},
                {"term": "laboratory", "phonetic": "/ləˈbɒrətəri/", "translation": "实验室"},
                {"term": "elaborate", "phonetic": "/ɪˈlæbərət/", "translation": "精心制作的"},
            ],
        },
        {
            "term": "demonstrate", "phonetic": "/ˈdemənstreɪt/", "translation": "展示、演示",
            "color": "#A78BFA",
            "context": "I need to **demonstrate** the value of our new initiative.",
            "prefix": {"value": "de-", "meaning": "完全", "note": "加强语气"},
            "root": {"value": "monstr", "meaning": "展示", "note": "源自拉丁语 monere"},
            "suffix": {"value": "-ate", "meaning": "动词后缀", "note": "表示使成为"},
            "logic": "de（完全）+ monstr（展示）+ ate = 完全展示出来 → demonstrate",
            "relatedWords": [
                {"term": "monster", "phonetic": "/ˈmɒnstər/", "translation": "怪物"},
                {"term": "monument", "phonetic": "/ˈmɒnjʊmənt/", "translation": "纪念碑"},
            ],
        },
    ],
    "travel": [
        {
            "term": "luggage", "phonetic": "/ˈlʌɡɪdʒ/", "translation": "行李",
            "color": "#3B82F6",
            "context": "My **luggage** exceeded the weight limit at the airport.",
            "root": {"value": "lug", "meaning": "拖、拉", "note": "古英语 log"},
            "suffix": {"value": "-gage", "meaning": "担保", "note": "引申为托运的东西"},
            "logic": "lug（拖）+ gage = 需要拖着走的东西 → luggage（行李）",
            "relatedWords": [
                {"term": "baggage", "phonetic": "/ˈbæɡɪdʒ/", "translation": "行李"},
                {"term": "engage", "phonetic": "/ɪnˈɡeɪdʒ/", "translation": "从事"},
            ],
        },
        {
            "term": "airport", "phonetic": "/ˈeəpɔːt/", "translation": "机场",
            "color": "#22C55E",
            "context": "I'm checking in at the **airport**.",
            "prefix": {"value": "air-", "meaning": "天空", "note": "表示空中"},
            "root": {"value": "port", "meaning": "港口", "note": "源自拉丁语 portus"},
            "logic": "air（天空）+ port（港口）= 飞机停靠的港口 → airport（机场）",
            "relatedWords": [
                {"term": "export", "phonetic": "/ɪkˈspɔːt/", "translation": "出口"},
                {"term": "import", "phonetic": "/ɪmˈpɔːt/", "translation": "进口"},
                {"term": "transport", "phonetic": "/trænˈspɔːt/", "translation": "运输"},
            ],
        },
        {
            "term": "destination", "phonetic": "/ˌdestɪˈneɪʃən/", "translation": "目的地",
            "color": "#F97316",
            "context": "What is your final **destination** for this trip?",
            "prefix": {"value": "de-", "meaning": "从", "note": "表示从...而来"},
            "root": {"value": "stin", "meaning": "建立", "note": "源自拉丁语 stare"},
            "suffix": {"value": "-ation", "meaning": "名词后缀", "note": "表示行为结果"},
            "logic": "de（从）+ stin（建立）+ ation = 注定要到达的地方 → destination",
            "relatedWords": [
                {"term": "destiny", "phonetic": "/ˈdestɪni/", "translation": "命运"},
                {"term": "obstacle", "phonetic": "/ˈɒbstəkəl/", "translation": "障碍"},
            ],
        },
        {
            "term": "explore", "phonetic": "/ɪkˈsplɔː/", "translation": "探索",
            "color": "#A78BFA",
            "context": "I love to **explore** new places and experience local culture.",
            "prefix": {"value": "ex-", "meaning": "出来", "note": "表示从...出来"},
            "root": {"value": "plor", "meaning": "呼喊", "note": "源自拉丁语 plorare"},
            "suffix": {"value": "-e", "meaning": "动词后缀", "note": "构成动词"},
            "logic": "ex（出来）+ plor（呼喊）+ e = 发出声音去探查 → explore（探索）",
            "relatedWords": [
                {"term": "exploration", "phonetic": "/ˌekspləˈreɪʃən/", "translation": "探索"},
                {"term": "implore", "phonetic": "/ɪmˈplɔː/", "translation": "恳求"},
            ],
        },
    ],
    "daily": [
        {
            "term": "actively", "phonetic": "/ˈæktɪvli/", "translation": "积极地",
            "color": "#3B82F6",
            "context": "I **actively** learn and improve myself every day.",
            "root": {"value": "act", "meaning": "行动", "note": "源自拉丁语 agere"},
            "suffix": {"value": "-ively", "meaning": "副词后缀", "note": "形容词变副词"},
            "logic": "act（行动）+ ively = 用行动的方式 → actively（积极地）",
            "relatedWords": [
                {"term": "action", "phonetic": "/ˈækʃən/", "translation": "行动"},
                {"term": "activity", "phonetic": "/ækˈtɪvəti/", "translation": "活动"},
                {"term": "actor", "phonetic": "/ˈæktər/", "translation": "演员"},
            ],
        },
        {
            "term": "improve", "phonetic": "/ɪmˈpruːv/", "translation": "改善、提升",
            "color": "#22C55E",
            "context": "I learn and **improve** myself every day.",
            "prefix": {"value": "im-", "meaning": "向内", "note": "表示在内"},
            "root": {"value": "prov", "meaning": "利益", "note": "源自拉丁语 prodesse"},
            "suffix": {"value": "-e", "meaning": "动词后缀", "note": "构成动词"},
            "logic": "im（向内）+ prov（好处）+ e = 让内在变得更好 → improve",
            "relatedWords": [
                {"term": "improvement", "phonetic": "/ɪmˈpruːvmənt/", "translation": "改进"},
                {"term": "prove", "phonetic": "/pruːv/", "translation": "证明"},
                {"term": "approve", "phonetic": "/əˈpruːv/", "translation": "批准"},
            ],
        },
        {
            "term": "capable", "phonetic": "/ˈkeɪpəbl/", "translation": "有能力的",
            "color": "#F97316",
            "context": "I become more **capable** in facing challenges.",
            "root": {"value": "cap", "meaning": "拿、取", "note": "源自拉丁语 capere"},
            "suffix": {"value": "-able", "meaning": "能够...的", "note": "形容词后缀"},
            "logic": "cap（拿）+ able（能够）= 能够抓住机会 → capable（有能力的）",
            "relatedWords": [
                {"term": "capacity", "phonetic": "/kəˈpæsəti/", "translation": "容量、能力"},
                {"term": "capture", "phonetic": "/ˈkæptʃər/", "translation": "捕获"},
                {"term": "capital", "phonetic": "/ˈkæpɪtəl/", "translation": "首都、资本"},
            ],
        },
        {
            "term": "challenge", "phonetic": "/ˈtʃælɪndʒ/", "translation": "挑战",
            "color": "#A78BFA",
            "context": "I grow stronger in facing various **challenges**.",
            "root": {"value": "chall", "meaning": "呼叫", "note": "源自古法语 chaloir"},
            "suffix": {"value": "-enge", "meaning": "名词后缀", "note": "构成名词"},
            "logic": "chall（呼叫）+ enge = 需要勇敢应对 → challenge（挑战）",
            "relatedWords": [
                {"term": "discharge", "phonetic": "/dɪsˈtʃɑːdʒ/", "translation": "释放"},
                {"term": "recharge", "phonetic": "/riːˈtʃɑːdʒ/", "translation": "充电"},
            ],
        },
    ],
}

# 场景到翻译的映射
SCENE_TRANSLATIONS = {
    "interview": {
        "trigger": ["面试", "求职", "简历", "述职"],
        "english": "I have prepared thoroughly for tomorrow's interview, and I'm confident in expressing my professional strengths effectively.",
        "meaning": "我已经为明天的面试做了充分准备，我自信能够有效地表达我的专业优势。",
    },
    "work": {
        "trigger": ["开会", "汇报", "项目", "职场", "工作", "邮件"],
        "english": "During today's meeting, I need to present our project progress concisely and demonstrate our team's collaborative achievements.",
        "meaning": "在今天的会议中，我需要简洁地展示我们的项目进展，并展示团队的协作成果。",
    },
    "travel": {
        "trigger": ["机场", "旅行", "旅游", "出行", "行李", "酒店"],
        "english": "I'm checking in at the airport, and my luggage is slightly overweight. I'm excited to explore this new destination.",
        "meaning": "我在机场办理登机手续，行李有点超重。我很兴奋能去探索这个新的目的地。",
    },
    "daily": {
        "trigger": ["朋友", "餐厅", "吃饭", "生活", "社交"],
        "english": "Every day I actively learn and improve myself, which helps me grow stronger and more capable in facing various challenges.",
        "meaning": "每天我都在积极学习和提升自己，这让我在面对各种挑战时变得更加坚强和能力更强。",
    },
}


def detect_scene(text: str) -> str:
    text_lower = text.lower()
    max_hits = 0
    best_scene = "daily"
    for scene, data in SCENE_TRANSLATIONS.items():
        hits = sum(1 for t in data["trigger"] if t in text_lower)
        if hits > max_hits:
            max_hits = hits
            best_scene = scene
    return best_scene


# ── FastAPI 应用 ────────────────────────────────
app = FastAPI(title="SeedDiary API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求模型 ────────────────────────────────
class LoginRequest(BaseModel):
    phone: str
    code: str

class TranslateRequest(BaseModel):
    scene: str

class RecordLearningRequest(BaseModel):
    word_term: str
    scene: str


# ── 内存存储 ─────────────────────────────────
users_db: dict = {}
progress_db: dict = {}


# ── JWT 工具 ─────────────────────────────────
from jose import jwt

def create_token(user_id: str) -> str:
    return jwt.encode(
        {"sub": user_id, "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY, algorithm="HS256"
    )

def decode_token(token: str) -> Optional[str]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("sub")
    except Exception:
        return None

def get_user_from_header(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    user_id = decode_token(token)
    return users_db.get(user_id) if user_id else None


# ── API 路由 ─────────────────────────────────
@app.get("/")
def root():
    return {"app": "SeedDiary API", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    # 演示验证码：123456
    if req.code != "123456":
        raise HTTPException(status_code=400, detail="验证码错误")

    # 查找或创建用户
    user = None
    for uid, u in users_db.items():
        if u.get("phone") == req.phone:
            user = u
            break

    if user is None:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "phone": req.phone,
            "created_at": datetime.utcnow().isoformat(),
            "total_words_mastered": 0,
        }
        users_db[user_id] = user

    token = create_token(user["id"])
    return {"access_token": token, "token_type": "bearer", "user_id": user["id"]}

@app.post("/api/translate")
def translate(req: TranslateRequest):
    scene = detect_scene(req.scene)
    translation = SCENE_TRANSLATIONS[scene]
    words = MOCK_WORDS.get(scene, [])
    return {
        "english": translation["english"],
        "meaning": translation["meaning"],
        "words": words,
    }

@app.post("/api/progress/learn")
def record_learning(req: RecordLearningRequest, authorization: Optional[str] = Header(None)):
    user = get_user_from_header(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="请先登录")

    key = f"{user['id']}:{req.word_term}"
    progress_db[key] = {
        "status": "learning",
        "correct_count": 0,
        "last_reviewed_at": datetime.utcnow().isoformat(),
    }
    return {"success": True}

@app.get("/api/progress/stats")
def get_stats(authorization: Optional[str] = Header(None)):
    user = get_user_from_header(authorization)
    if not user:
        return {"total_words_mastered": 0, "total_learned": 0}

    mastered = sum(
        1 for k, v in progress_db.items()
        if k.startswith(user["id"] + ":") and v.get("status") == "mastered"
    )
    total = sum(1 for k in progress_db if k.startswith(user["id"] + ":"))

    return {
        "total_words_mastered": mastered,
        "total_learned": total,
    }

@app.get("/api/user/profile")
def get_profile(authorization: Optional[str] = Header(None)):
    user = get_user_from_header(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="请先登录")
    return user
