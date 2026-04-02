/**
 * SeedDiary - Vercel Serverless Backend (Node.js)
 */
const crypto = require('crypto');

// ── JWT 密钥 ─────────────────────────────────
const SECRET_KEY = process.env.SECRET_KEY || 'seeddiary-dev-secret-2024';

// ── Mock 词根数据 ────────────────────────────
const MOCK_WORDS = {
    interview: [
        {
            term: "confident", phonetic: "/ˈkɒnfɪdənt/", translation: "自信的",
            color: "#3B82F6",
            context: "I'm **confident** in expressing my professional strengths.",
            prefix: { value: "con-", meaning: "完全地", note: "加强语气" },
            root: { value: "fid", meaning: "信任", note: "源自拉丁语 fides" },
            suffix: { value: "-ent", meaning: "形容词后缀", note: "表示具有某种性质的" },
            logic: "con（完全）+ fid（信任）+ ent = 完全信任自己 → confident",
            relatedWords: [
                { term: "faith", phonetic: "/feɪθ/", translation: "信念、信任" },
                { term: "confide", phonetic: "/kənˈfaɪd/", translation: "吐露、信赖" },
                { term: "reliable", phonetic: "/rɪˈlaɪəbl/", translation: "可靠的" },
                { term: "fidelity", phonetic: "/fɪˈdeləti/", translation: "忠诚、忠贞" },
            ],
        },
        {
            term: "professional", phonetic: "/prəˈfeʃənl/", translation: "专业的",
            color: "#22C55E",
            context: "I have **professional** experience in project management.",
            prefix: { value: "pro-", meaning: "公开地", note: "表示公开、在之前" },
            root: { value: "fess", meaning: "说", note: "源自拉丁语 fateri" },
            suffix: { value: "-ion", meaning: "名词后缀", note: "表示行为状态" },
            logic: "pro（公开）+ fess（说）+ ion = 公开宣称 → profess",
            relatedWords: [
                { term: "professor", phonetic: "/prəˈfesər/", translation: "教授" },
                { term: "confess", phonetic: "/kənˈfes/", translation: "坦白、承认" },
                { term: "manifest", phonetic: "/ˈmænɪfest/", translation: "明显的" },
            ],
        },
        {
            term: "thoroughly", phonetic: "/ˈθʌrəli/", translation: "彻底地",
            color: "#F97316",
            context: "I conducted a **thoroughly** analysis of the market.",
            root: { value: "thorough", meaning: "穿透、彻底", note: "古英语 durch" },
            suffix: { value: "-ly", meaning: "副词后缀", note: "形容词变副词" },
            logic: "thorough（彻底的）+ ly = 彻底地",
            relatedWords: [
                { term: "through", phonetic: "/θruː/", translation: "穿过" },
                { term: "throughout", phonetic: "/θruːˈaʊt/", translation: "贯穿" },
            ],
        },
        {
            term: "competent", phonetic: "/ˈkɒmpɪtənt/", translation: "有能力的",
            color: "#A78BFA",
            context: "I am **competent** in handling multiple projects.",
            prefix: { value: "com-", meaning: "一起", note: "表示共同" },
            root: { value: "pet", meaning: "追求", note: "源自拉丁语 petere" },
            suffix: { value: "-ent", meaning: "形容词后缀", note: "表示具有...性质的" },
            logic: "com（共同）+ pet（追求）+ ent = 能在竞争中胜出 → competent",
            relatedWords: [
                { term: "compete", phonetic: "/kəmˈpiːt/", translation: "竞争" },
                { term: "competition", phonetic: "/ˌkɒmpɪˈtɪʃən/", translation: "比赛" },
                { term: "appetite", phonetic: "/ˈæpɪtaɪt/", translation: "食欲" },
            ],
        },
    ],
    work: [
        {
            term: "present", phonetic: "/prɪˈzent/", translation: "展示、呈现",
            color: "#3B82F6",
            context: "I need to **present** our project progress at today's meeting.",
            prefix: { value: "pre-", meaning: "之前", note: "表示在...之前" },
            root: { value: "sent", meaning: "存在", note: "源自拉丁语 esse" },
            suffix: { value: "-ent", meaning: "形容词后缀", note: "表示状态" },
            logic: "pre（之前）+ sent（存在）= 在别人面前存在 → present（展示）",
            relatedWords: [
                { term: "presence", phonetic: "/ˈprezəns/", translation: "出席、在场" },
                { term: "represent", phonetic: "/ˌreprɪˈzent/", translation: "代表" },
                { term: "absence", phonetic: "/ˈæbsəns/", translation: "缺席" },
            ],
        },
        {
            term: "concise", phonetic: "/kənˈsaɪs/", translation: "简洁的",
            color: "#22C55E",
            context: "Please keep your email **concise** and to the point.",
            prefix: { value: "con-", meaning: "完全", note: "加强语气" },
            root: { value: "cis", meaning: "切", note: "源自拉丁语 caedere" },
            suffix: { value: "-e", meaning: "形容词后缀", note: "构成形容词" },
            logic: "con（完全）+ cis（切）+ e = 把多余的全部切掉 → concise（简洁的）",
            relatedWords: [
                { term: "precision", phonetic: "/prɪˈsɪʒən/", translation: "精确" },
                { term: "decide", phonetic: "/dɪˈsaɪd/", translation: "决定" },
                { term: "scissors", phonetic: "/ˈsɪzəz/", translation: "剪刀" },
            ],
        },
        {
            term: "collaborate", phonetic: "/kəˈlæbəreɪt/", translation: "合作、协作",
            color: "#F97316",
            context: "Our team **collaborate** effectively across departments.",
            prefix: { value: "col-", meaning: "一起", note: "com- 变体" },
            root: { value: "labor", meaning: "劳动", note: "源自拉丁语 labor" },
            suffix: { value: "-ate", meaning: "动词后缀", note: "表示使成为" },
            logic: "col（一起）+ labor（劳动）+ ate = 一起劳动 → collaborate（合作）",
            relatedWords: [
                { term: "collaboration", phonetic: "/kəˌlæbəˈreɪʃən/", translation: "合作" },
                { term: "laboratory", phonetic: "/ləˈbɒrətəri/", translation: "实验室" },
                { term: "elaborate", phonetic: "/ɪˈlæbərət/", translation: "精心制作的" },
            ],
        },
        {
            term: "demonstrate", phonetic: "/ˈdemənstreɪt/", translation: "展示、演示",
            color: "#A78BFA",
            context: "I need to **demonstrate** the value of our new initiative.",
            prefix: { value: "de-", meaning: "完全", note: "加强语气" },
            root: { value: "monstr", meaning: "展示", note: "源自拉丁语 monere" },
            suffix: { value: "-ate", meaning: "动词后缀", note: "表示使成为" },
            logic: "de（完全）+ monstr（展示）+ ate = 完全展示出来 → demonstrate",
            relatedWords: [
                { term: "monster", phonetic: "/ˈmɒnstər/", translation: "怪物" },
                { term: "monument", phonetic: "/ˈmɒnjʊmənt/", translation: "纪念碑" },
            ],
        },
    ],
    travel: [
        {
            term: "luggage", phonetic: "/ˈlʌɡɪdʒ/", translation: "行李",
            color: "#3B82F6",
            context: "My **luggage** exceeded the weight limit at the airport.",
            root: { value: "lug", meaning: "拖、拉", note: "古英语 log" },
            suffix: { value: "-gage", meaning: "担保", note: "引申为托运的东西" },
            logic: "lug（拖）+ gage = 需要拖着走的东西 → luggage（行李）",
            relatedWords: [
                { term: "baggage", phonetic: "/ˈbæɡɪdʒ/", translation: "行李" },
                { term: "engage", phonetic: "/ɪnˈɡeɪdʒ/", translation: "从事" },
            ],
        },
        {
            term: "airport", phonetic: "/ˈeəpɔːt/", translation: "机场",
            color: "#22C55E",
            context: "I'm checking in at the **airport**.",
            prefix: { value: "air-", meaning: "天空", note: "表示空中" },
            root: { value: "port", meaning: "港口", note: "源自拉丁语 portus" },
            logic: "air（天空）+ port（港口）= 飞机停靠的港口 → airport（机场）",
            relatedWords: [
                { term: "export", phonetic: "/ɪkˈspɔːt/", translation: "出口" },
                { term: "import", phonetic: "/ɪmˈpɔːt/", translation: "进口" },
                { term: "transport", phonetic: "/trænˈspɔːt/", translation: "运输" },
            ],
        },
        {
            term: "destination", phonetic: "/ˌdestɪˈneɪʃən/", translation: "目的地",
            color: "#F97316",
            context: "What is your final **destination** for this trip?",
            prefix: { value: "de-", meaning: "从", note: "表示从...而来" },
            root: { value: "stin", meaning: "建立", note: "源自拉丁语 stare" },
            suffix: { value: "-ation", meaning: "名词后缀", note: "表示行为结果" },
            logic: "de（从）+ stin（建立）+ ation = 注定要到达的地方 → destination",
            relatedWords: [
                { term: "destiny", phonetic: "/ˈdestɪni/", translation: "命运" },
                { term: "obstacle", phonetic: "/ˈɒbstəkəl/", translation: "障碍" },
            ],
        },
        {
            term: "explore", phonetic: "/ɪkˈsplɔː/", translation: "探索",
            color: "#A78BFA",
            context: "I love to **explore** new places and experience local culture.",
            prefix: { value: "ex-", meaning: "出来", note: "表示从...出来" },
            root: { value: "plor", meaning: "呼喊", note: "源自拉丁语 plorare" },
            suffix: { value: "-e", meaning: "动词后缀", note: "构成动词" },
            logic: "ex（出来）+ plor（呼喊）+ e = 发出声音去探查 → explore（探索）",
            relatedWords: [
                { term: "exploration", phonetic: "/ˌekspləˈreɪʃən/", translation: "探索" },
                { term: "implore", phonetic: "/ɪmˈplɔː/", translation: "恳求" },
            ],
        },
    ],
    daily: [
        {
            term: "actively", phonetic: "/ˈæktɪvli/", translation: "积极地",
            color: "#3B82F6",
            context: "I **actively** learn and improve myself every day.",
            root: { value: "act", meaning: "行动", note: "源自拉丁语 agere" },
            suffix: { value: "-ively", meaning: "副词后缀", note: "形容词变副词" },
            logic: "act（行动）+ ively = 用行动的方式 → actively（积极地）",
            relatedWords: [
                { term: "action", phonetic: "/ˈækʃən/", translation: "行动" },
                { term: "activity", phonetic: "/ækˈtɪvəti/", translation: "活动" },
                { term: "actor", phonetic: "/ˈæktər/", translation: "演员" },
            ],
        },
        {
            term: "improve", phonetic: "/ɪmˈpruːv/", translation: "改善、提升",
            color: "#22C55E",
            context: "I learn and **improve** myself every day.",
            prefix: { value: "im-", meaning: "向内", note: "表示在内" },
            root: { value: "prov", meaning: "利益", note: "源自拉丁语 prodesse" },
            suffix: { value: "-e", meaning: "动词后缀", note: "构成动词" },
            logic: "im（向内）+ prov（好处）+ e = 让内在变得更好 → improve",
            relatedWords: [
                { term: "improvement", phonetic: "/ɪmˈpruːvmənt/", translation: "改进" },
                { term: "prove", phonetic: "/pruːv/", translation: "证明" },
                { term: "approve", phonetic: "/əˈpruːv/", translation: "批准" },
            ],
        },
        {
            term: "capable", phonetic: "/ˈkeɪpəbl/", translation: "有能力的",
            color: "#F97316",
            context: "I become more **capable** in facing challenges.",
            root: { value: "cap", meaning: "拿、取", note: "源自拉丁语 capere" },
            suffix: { value: "-able", meaning: "能够...的", note: "形容词后缀" },
            logic: "cap（拿）+ able（能够）= 能够抓住机会 → capable（有能力的）",
            relatedWords: [
                { term: "capacity", phonetic: "/kəˈpæsəti/", translation: "容量、能力" },
                { term: "capture", phonetic: "/ˈkæptʃər/", translation: "捕获" },
                { term: "capital", phonetic: "/ˈkæpɪtəl/", translation: "首都、资本" },
            ],
        },
        {
            term: "challenge", phonetic: "/ˈtʃælɪndʒ/", translation: "挑战",
            color: "#A78BFA",
            context: "I grow stronger in facing various **challenges**.",
            root: { value: "chall", meaning: "呼叫", note: "源自古法语 chaloir" },
            suffix: { value: "-enge", meaning: "名词后缀", note: "构成名词" },
            logic: "chall（呼叫）+ enge = 需要勇敢应对 → challenge（挑战）",
            relatedWords: [
                { term: "discharge", phonetic: "/dɪsˈtʃɑːdʒ/", translation: "释放" },
                { term: "recharge", phonetic: "/riːˈtʃɑːdʒ/", translation: "充电" },
            ],
        },
    ],
};

// 场景到翻译的映射
const SCENE_TRANSLATIONS = {
    interview: {
        trigger: ["面试", "求职", "简历", "述职"],
        english: "I have prepared thoroughly for tomorrow's interview, and I'm confident in expressing my professional strengths effectively.",
        meaning: "我已经为明天的面试做了充分准备，我自信能够有效地表达我的专业优势。",
    },
    work: {
        trigger: ["开会", "汇报", "项目", "职场", "工作", "邮件"],
        english: "During today's meeting, I need to present our project progress concisely and demonstrate our team's collaborative achievements.",
        meaning: "在今天的会议中，我需要简洁地展示我们的项目进展，并展示团队的协作成果。",
    },
    travel: {
        trigger: ["机场", "旅行", "旅游", "出行", "行李", "酒店"],
        english: "I'm checking in at the airport, and my luggage is slightly overweight. I'm excited to explore this new destination.",
        meaning: "我在机场办理登机手续，行李有点超重。我很兴奋能去探索这个新的目的地。",
    },
    daily: {
        trigger: ["朋友", "餐厅", "吃饭", "生活", "社交"],
        english: "Every day I actively learn and improve myself, which helps me grow stronger and more capable in facing various challenges.",
        meaning: "每天我都在积极学习和提升自己，这让我在面对各种挑战时变得更加坚强和能力更强。",
    },
};

// ── 内存存储 ─────────────────────────────────
const usersDb = {};
const progressDb = {};

// ── JWT 工具 ─────────────────────────────────
function createToken(userId) {
    const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
    const payload = Buffer.from(JSON.stringify({
        sub: userId,
        exp: Math.floor(Date.now() / 1000) + 7 * 24 * 60 * 60,
    })).toString('base64url');
    const signature = crypto.createHmac('sha256', SECRET_KEY)
        .update(`${header}.${payload}`).digest('base64url');
    return `${header}.${payload}.${signature}`;
}

function decodeToken(token) {
    try {
        const [header, payload, signature] = token.split('.');
        const expectedSig = crypto.createHmac('sha256', SECRET_KEY)
            .update(`${header}.${payload}`).digest('base64url');
        if (signature !== expectedSig) return null;
        const data = JSON.parse(Buffer.from(payload, 'base64url').toString());
        return data.sub;
    } catch {
        return null;
    }
}

function getUserFromHeader(authHeader) {
    if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
    const userId = decodeToken(authHeader.slice(7));
    return userId ? usersDb[userId] : null;
}

function detectScene(text) {
    text = text.toLowerCase();
    let maxHits = 0, bestScene = 'daily';
    for (const [scene, data] of Object.entries(SCENE_TRANSLATIONS)) {
        const hits = data.trigger.filter(t => text.includes(t)).length;
        if (hits > maxHits) { maxHits = hits; bestScene = scene; }
    }
    return bestScene;
}

// ── CORS Headers ─────────────────────────────
const CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

// ── 主 Handler ──────────────────────────────
module.exports = async function handler(req, res) {
    // CORS preflight
    if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Origin', '*');
        return res.status(200).end();
    }

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');

    const { url, method, headers, body } = req;
    const path = url.split('?')[0];

    try {
        // GET /
        if (path === '/' && method === 'GET') {
            return res.status(200).json({ app: "SeedDiary API", version: "1.0.0", status: "running" });
        }

        // GET /api/health
        if (path === '/api/health' && method === 'GET') {
            return res.status(200).json({ status: "ok" });
        }

        // POST /api/auth/login
        if (path === '/api/auth/login' && method === 'POST') {
            const { phone, code } = body;
            if (!phone || code !== '123456') {
                return res.status(400).json({ detail: "验证码错误" });
            }
            let user = Object.values(usersDb).find(u => u.phone === phone);
            if (!user) {
                const id = crypto.randomUUID();
                user = { id, phone, created_at: new Date().toISOString(), total_words_mastered: 0 };
                usersDb[id] = user;
            }
            const token = createToken(user.id);
            return res.status(200).json({ access_token: token, token_type: 'bearer', user_id: user.id });
        }

        // POST /api/translate
        if (path === '/api/translate' && method === 'POST') {
            const { scene } = body;
            const detected = detectScene(scene || '');
            const translation = SCENE_TRANSLATIONS[detected];
            const words = MOCK_WORDS[detected] || [];
            return res.status(200).json({
                english: translation.english,
                meaning: translation.meaning,
                words,
            });
        }

        // POST /api/progress/learn
        if (path === '/api/progress/learn' && method === 'POST') {
            const user = getUserFromHeader(headers.authorization);
            if (!user) return res.status(401).json({ detail: "请先登录" });
            const { word_term, scene } = body;
            const key = `${user.id}:${word_term}`;
            progressDb[key] = { status: 'learning', correct_count: 0, last_reviewed_at: new Date().toISOString() };
            return res.status(200).json({ success: true });
        }

        // GET /api/progress/stats
        if (path === '/api/progress/stats' && method === 'GET') {
            const user = getUserFromHeader(headers.authorization);
            if (!user) return res.status(200).json({ total_words_mastered: 0, total_learned: 0 });
            const keys = Object.keys(progressDb).filter(k => k.startsWith(user.id + ':'));
            const mastered = keys.filter(k => progressDb[k].status === 'mastered').length;
            return res.status(200).json({ total_words_mastered: mastered, total_learned: keys.length });
        }

        // GET /api/user/profile
        if (path === '/api/user/profile' && method === 'GET') {
            const user = getUserFromHeader(headers.authorization);
            if (!user) return res.status(401).json({ detail: "请先登录" });
            return res.status(200).json(user);
        }

        // 404
        return res.status(404).json({ detail: "Not found" });

    } catch (err) {
        return res.status(500).json({ detail: err.message });
    }
};
