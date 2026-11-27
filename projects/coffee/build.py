"""Собирает демо-сайты кофеен: projects/coffee/<slug>/index.html.
Запуск: python build.py  (из этой папки). Авторы фото берутся из img/credits.json.
"""
import html, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).parent
import json
CRED = {c["id"]: c for c in json.loads((ROOT / "img" / "credits.json").read_text(encoding="utf-8"))["photos"]}

def credits(page_html):
    used = sorted(set(re.findall(r"photo-([a-z]?\d+)", page_html)))
    parts = []
    for i in used:
        c = CRED.get(i)
        if c:
            parts.append(f'<a href="{c["page"]}">{html.escape(c["by"])}</a>, <a href="{c["licenceUrl"]}">{c["licence"]}</a>')
    return "Фото: " + "; ".join(parts) + " (Wikimedia Commons)."

PH = {  # фото из библиотеки taste-skill (лицензии в credits.txt)
    "espresso": ("photo-m61713028", "Эспрессо стекает из рожка кофемашины"),
    "two": ("photo-m61716670", "Две струйки эспрессо в белую чашку"),
    "tray": ("photo-m189498721", "Поднос с четырьмя чашками кофе на деревянной стойке"),
    "glass": ("photo-m28146075", "Эспрессо в маленьком стакане под группой кофемашины"),
    "milk": ("photo-m201752739", "Бариста взбивает молоко в питчере"),
    "filter": ("photo-m61713103", "Фильтр-кофе капает в сервер на весах"),
    "hand": ("photo-m28989985-1200", "Чашка в руке под рожком, пока идёт эспрессо"),
    "tamp": ("photo-m187311853-1200", "Бариста темперует молотый кофе в рожке"),
    "pour": ("photo-m61714648-960", "Эспрессо из питчера в белую чашку на деревянной стойке"),
    "latte": ("photo-m61713362", "Молоко вливается в латте"),
    "terrace": ("photo-m61715560", "Чёрный кофе на столике летней веранды"),
    "art": ("photo-c141", "Латте-арт из стального питчера в тёмной чашке"),
    "green": ("photo-m62054123", "Рука перебирает зелёные зёрна кофе"),
    "roast": ("photo-m147143963", "Свежеобжаренные зёрна сыплются из барабана в охладитель"),
}

def img(key, cls="", eager=False, sizes="(max-width:900px) 100vw, 50vw"):
    f, alt = PH[key]
    src = f"../img/{f}.webp"
    if f.endswith(("-1200", "-960")):
        srcset = f"{src} {f.rsplit('-',1)[1]}w"
    else:
        srcset = f"../img/{f}-500.webp 500w, ../img/{f}-960.webp 960w, {src} 1280w"
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}" srcset="{srcset}" sizes="{sizes}" alt="{html.escape(alt)}" {load} decoding="async">'

def maps(city, street):
    return "https://yandex.ru/maps/?text=" + urllib.parse.quote(f"{city}, {street}")

CAFES = [
  dict(slug="poeziya", name="Поэзия кофе", city="Тверь", street="", district="Тверь, центр",
       hours=[("Пн–Пт", "8:30–18:30"), ("Сб–Вс", "10:00–19:00")], wa="79040171117",
       vars="--bg:#f5efe4;--surface:#ebe2d2;--ink:#1f1a16;--muted:#6b6056;--line:#d9ccb8;--accent:#a4472b;--on-accent:#fff;--r:2px;--display:Cormorant,Georgia,serif;--text:Onest,system-ui,sans-serif",
       hero="pour", h1="Кофейня «Поэзия кофе» в Твери",
       lead="Эспрессо, фильтр и выпечка к утру. С 8:30 в будни, чтобы успеть до работы.",
       fact="Открыто с 8:30 по будням",
       menu=[("Кофе", [("Эспрессо", "140 ₽"), ("Американо", "170 ₽"), ("Капучино 0,3", "220 ₽"), ("Флэт уайт", "240 ₽"), ("Раф", "270 ₽")]),
             ("Не кофе", [("Какао", "210 ₽"), ("Чай листовой", "180 ₽"), ("Матча латте", "280 ₽"), ("Лимонад", "230 ₽")]),
             ("К кофе", [("Круассан", "160 ₽"), ("Сырники", "290 ₽"), ("Чизкейк", "260 ₽"), ("Печенье", "90 ₽")])],
       type_line="Утро начинается <em>с первой строки</em> и первой чашки.", type_small="Название обязывает: тишина, хороший кофе и место, где можно дочитать главу.",
       gallery=("milk", "glass", "latte"), extra="steps"),
  dict(slug="kofeterii", name="КОфеТерий", city="Ярославль", street="", district="Ярославль",
       hours=[("Каждый день", "11:00–21:00")], wa="79807463965",
       vars="--bg:#fbf4e8;--surface:#f2e3c9;--ink:#2a1d14;--muted:#73604f;--line:#e2cfae;--accent:#985010;--on-accent:#fff;--r:14px;--display:Lora,Georgia,serif;--text:Onest,system-ui,sans-serif",
       hero="art", h1="Котокафе «КОфеТерий» в Ярославле",
       lead="Кофе, десерты и кошки, которые сами решают, к кому подойти. Каждый день с 11 до 21.",
       fact="Каждый день 11:00–21:00",
       menu=[("Кофе", [("Капучино", "220 ₽"), ("Латте", "240 ₽"), ("Раф ванильный", "280 ₽"), ("Американо", "170 ₽")]),
             ("Для детей", [("Какао с маршмеллоу", "220 ₽"), ("Молочный коктейль", "250 ₽"), ("Морс", "150 ₽")]),
             ("Посещение", [("Первый час", "400 ₽"), ("Каждые 30 минут далее", "150 ₽"), ("Дети до 7 лет", "бесплатно")])],
       type_line="Кошки здесь <em>хозяева</em>, мы просто варим кофе.", type_small="Гладить можно, будить нельзя. Остальные правила — ниже.",
       gallery=("milk", "tray", "two"), extra="rules"),
  dict(slug="coffeepie", name="Coffeepie", city="Москва", street="Наличная улица", district="Москва, Наличная улица",
       hours=[("Пн–Пт", "8:00–21:00"), ("Сб–Вс", "9:00–21:00")], wa="79037299295",
       vars="--bg:#fdf6ef;--surface:#f6e6d6;--ink:#2b1713;--muted:#77594f;--line:#ead2bf;--accent:#9e2b25;--on-accent:#fff;--r:6px;--display:Lora,Georgia,serif;--text:Onest,system-ui,sans-serif",
       hero="tray", h1="Coffeepie: кофе и пироги на Наличной",
       lead="Кофе с собой по дороге к метро и пироги, которые можно заказать целиком к празднику.",
       fact="Будни с 8:00, выходные с 9:00",
       menu=[("Кофе", [("Эспрессо", "150 ₽"), ("Капучино", "230 ₽"), ("Латте", "250 ₽"), ("Флэт уайт", "260 ₽")]),
             ("Пироги кусочком", [("Вишнёвый", "220 ₽"), ("Яблочный с корицей", "200 ₽"), ("Киш с курицей", "280 ₽"), ("Лимонный тарт", "240 ₽")]),
             ("Пироги целиком", [("Вишнёвый, 1,2 кг", "1 900 ₽"), ("Яблочный, 1,2 кг", "1 700 ₽"), ("Киш, 1 кг", "2 100 ₽")])],
       type_line="Пирог целиком — <em>за сутки</em> до праздника.", type_small="Напишите, какой пирог и к какому часу, — испечём и упакуем.",
       gallery=("espresso", "hand", "milk"), extra="steps"),
  dict(slug="lavka", name="Coffee Lavka", city="Москва", street="Зелёный проспект", district="Москва, Зелёный проспект",
       hours=[("Каждый день", "8:00–21:30")], wa="79252050747",
       vars="--bg:#f2f1ea;--surface:#e3e6da;--ink:#16241c;--muted:#56645a;--line:#cdd3c3;--accent:#2f6b47;--on-accent:#fff;--r:0px;--display:Onest,system-ui,sans-serif;--text:Onest,system-ui,sans-serif",
       hero="espresso", h1="Coffee Lavka на Зелёном проспекте",
       lead="Кофейня у дома: зерно на развес, кофе с собой и пара столиков, чтобы выпить на месте.",
       fact="Каждый день 8:00–21:30",
       menu=[("Кофе", [("Эспрессо", "130 ₽"), ("Капучино", "210 ₽"), ("Латте", "230 ₽"), ("Фильтр", "190 ₽")]),
             ("Зерно на развес", [("Бразилия, 250 г", "690 ₽"), ("Колумбия, 250 г", "790 ₽"), ("Эфиопия, 250 г", "890 ₽")]),
             ("С собой", [("Круассан", "150 ₽"), ("Сэндвич", "290 ₽"), ("Овсяное печенье", "90 ₽")])],
       type_line="Смелем зерно <em>под вашу турку</em> или кофемашину.", type_small="Скажите, чем варите дома, — подберём помол.",
       gallery=("roast", "green", "filter"), extra="steps"),
  dict(slug="bay", name="Coffe Bay", city="Москва", street="улица Генерала Белова", district="Москва, улица Генерала Белова",
       hours=[("Пн–Пт", "7:30–20:00"), ("Сб–Вс", "9:00–21:00")], wa="79264682853",
       vars="--bg:#f3f5f6;--surface:#e1e8ec;--ink:#132331;--muted:#55636f;--line:#c9d3da;--accent:#1f5f8b;--on-accent:#fff;--r:10px;--display:Cormorant,Georgia,serif;--text:Onest,system-ui,sans-serif",
       hero="two", h1="Coffe Bay на улице Генерала Белова",
       lead="Открываемся в 7:30 — раньше, чем большинство кофеен вокруг. Кофе с собой за пару минут.",
       fact="Будни с 7:30",
       menu=[("Кофе", [("Эспрессо", "140 ₽"), ("Американо", "160 ₽"), ("Капучино", "220 ₽"), ("Раф", "260 ₽")]),
             ("Холодное", [("Айс-латте", "250 ₽"), ("Эспрессо-тоник", "270 ₽"), ("Лимонад", "220 ₽")]),
             ("Завтрак", [("Круассан с ветчиной", "260 ₽"), ("Гранола", "240 ₽"), ("Сырники", "290 ₽")])],
       type_line="В 7:30 кофе уже <em>готов</em>.", type_small="Закажите заранее — заберёте без очереди по дороге к метро.",
       gallery=("terrace", "tamp", "latte"), extra="steps"),
  # Вымышленная кофейня для портфолио (та же «Корица», что в QR-меню)
  dict(slug="korica", fictional=True, name="Корица", city="Тверь", street="", district="Тверь, центр",
       hours=[("Пн–Пт", "8:00–21:00"), ("Сб–Вс", "9:00–22:00")], wa="",
       vars="--bg:#faf3ea;--surface:#f0e2cf;--ink:#2a1a10;--muted:#76604d;--line:#e3cfb6;--accent:#9c4515;--on-accent:#fff;--r:4px;--display:Cormorant,Georgia,serif;--text:Onest,system-ui,sans-serif",
       hero="hand", h1="Кофейня «Корица»: кофе и выпечка с корицей",
       lead="Синнабоны из своей печи к открытию и кофе на хорошем зерне. Предзаказ — до выхода из дома.",
       fact="Синнабоны из печи к 8:00",
       menu=[("Кофе", [("Эспрессо", "140 ₽"), ("Капучино", "220 ₽"), ("Раф с корицей", "280 ₽"), ("Фильтр", "190 ₽")]),
             ("Выпечка", [("Синнабон", "240 ₽"), ("Круассан", "190 ₽"), ("Круассан с миндалём", "260 ₽")]),
             ("Завтраки", [("Сырники", "380 ₽"), ("Омлет с сыром", "340 ₽"), ("Гранола", "290 ₽")])],
       type_line="Корица в каждом <em>третьем</em> пункте меню.", type_small="И ни одной в эспрессо — его мы не трогаем.",
       gallery=("milk", "glass", "tamp"), extra="steps"),
]

STEPS = [("Напишите заказ", "В WhatsApp: что и к какому времени."),
         ("Мы подтвердим", "Ответим за пару минут и скажем, когда будет готово."),
         ("Заберите без очереди", "Назовите имя на кассе — заказ уже ждёт.")]
RULES = [("Не будим кошек", "Если кошка спит, она спит. Подойдёт сама, когда захочет."),
         ("Угощаем только кормом от нас", "Свою еду кошкам давать нельзя — у некоторых диета."),
         ("Дети — со взрослыми", "Покажем малышам, как гладить, чтобы обоим понравилось.")]

def page(c):
    e = html.escape
    wa = f"https://wa.me/{c['wa']}" if c["wa"] else "#order"
    hrs = "".join(f"<dt>{e(d)}</dt><dd>{e(t)}</dd>" for d, t in c["hours"])
    where = c["street"] or c["district"]
    # у вымышленной кофейни карта искала бы чужое заведение с тем же названием
    fict = c.get("fictional")
    dirs = "#visit" if fict else maps(c["city"], c["street"] or c["name"])
    # без WhatsApp ссылки «Написать» вели бы по кругу на #order
    head_btn = f'<a class="btn ghost" href="{wa}">Написать</a>' if c["wa"] else '<a class="btn ghost" href="#menu">Меню</a>'
    hero_2 = '<a class="btn ghost" href="#visit">Адрес и часы</a>' if fict else f'<a class="btn ghost" href="{dirs}">Как добраться</a>'
    visit_acts = (("" if fict else f'<a class="btn" href="{dirs}">Как добраться</a>')
                  + (f'<a class="btn ghost" href="{wa}">Написать в WhatsApp</a>' if c["wa"] else '<a class="btn" href="#order">Как сделать предзаказ</a>'))
    close_btn = f'<a class="btn" href="{wa}">Написать в WhatsApp</a>' if c["wa"] else '<a class="btn" href="#menu">Посмотреть меню</a>'
    bar = ((f'<a class="btn" href="{dirs}">Маршрут</a>' if not fict else '<a class="btn" href="#visit">Адрес</a>')
           + (f'<a class="btn ghost" href="{wa}">Написать</a>' if c["wa"] else '<a class="btn ghost" href="#menu">Меню</a>'))
    menu = "".join(
        f'<div class="menu-col"><h3>{e(t)}</h3><ul>' + "".join(f"<li><span>{e(n)}</span><span>{e(p)}</span></li>" for n, p in items) + "</ul></div>"
        for t, items in c["menu"])
    g = c["gallery"]
    if c["extra"] == "rules":
        ex_t, ex_sub, ex = "Правила в гостях у кошек", "Простые, чтобы и вам, и кошкам было спокойно.", RULES
    else:
        ex_t, ex_sub, ex = "Предзаказ без очереди", "Утром каждая минута на счету — закажите заранее.", STEPS
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in ex)
    return f"""<!doctype html>
<html lang="ru" style="{c['vars']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(c['name'])} — демо-сайт кофейни, {e(c['city'])}</title>
<meta name="description" content="Демо-концепт сайта для кофейни «{e(c['name'])}» ({e(c['city'])}): меню, часы работы, предзаказ.">
<link rel="stylesheet" href="../../../fonts/fonts.css">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<a class="skip" href="#main">К содержанию</a>
<div class="demo"><div class="wrap"><span>{f"Концепт из портфолио: кофейня «{e(c['name'])}» вымышленная, меню и цены придуманы." if c.get('fictional') else f"Демо-концепт сайта для «{e(c['name'])}». Это пример, а не официальный сайт: меню и цены условные."}</span><a href="https://kiraiii-code.github.io/site-concepts/">Кто сделал</a></div></div>
<header class="top"><div class="wrap">
  <a class="logo" href="#main">{e(c['name'])}</a>
  <nav class="menu" aria-label="Разделы"><a href="#visit">Адрес и часы</a><a href="#menu">Меню</a><a href="#order">{'Правила' if c['extra']=='rules' else 'Предзаказ'}</a></nav>
  {head_btn}
</div></header>
<main id="main">
<section class="hero">
  {img(c['hero'], 'bg', eager=True, sizes='100vw')}
  <div class="wrap">
    <span class="fact">{e(c['fact'])}</span>
    <h1>{e(c['h1'])}</h1>
    <p class="lead">{e(c['lead'])}</p>
    <div class="acts"><a class="btn" href="#menu">Посмотреть меню</a>{hero_2}</div>
  </div>
</section>
<section class="s" id="visit"><div class="wrap visit">
  <div>
    <h2>Адрес и часы работы</h2>
    <p class="sub">{e(where)}. Заходите выпить на месте или возьмите с собой.</p>
    <dl>{hrs}<dt>Где</dt><dd>{e(where)}</dd></dl>
    <div class="acts">{visit_acts}</div>
  </div>
  <div class="frame">{img(g[0])}</div>
</div></section>
<section class="s alt" id="menu"><div class="wrap">
  <h2>Меню и цены</h2>
  <p class="sub">Основное, что заказывают чаще всего. Полное меню — на кассе.</p>
  <div class="menu-grid">{menu}</div>
</div></section>
<section class="type"><div class="wrap"><p>{c['type_line']}</p><small>{e(c['type_small'])}</small></div></section>
<section class="s" aria-label="Фотографии"><div class="wrap trio">
  <div class="frame">{img(g[1], sizes='(max-width:900px) 100vw, 45vw')}</div>
  <div class="frame">{img(g[2], sizes='(max-width:900px) 50vw, 28vw')}</div>
  <div class="frame">{img('pour' if c['hero']!='pour' else 'filter', sizes='(max-width:900px) 50vw, 28vw')}</div>
</div></section>
<section class="s alt" id="order"><div class="wrap">
  <h2>{e(ex_t)}</h2>
  <p class="sub">{e(ex_sub)}</p>
  <ol class="steps">{steps}</ol>
</div></section>
<section class="close"><div class="wrap">
  <h2>Заходите на кофе в «{e(c['name'])}»</h2>
  {close_btn}
</div></section>
</main>
<footer><div class="wrap">
  <span>Демо-концепт. Фотографии — иллюстрации, не из этой кофейни. __CREDITS__</span>
  <span>Сделано как пример сайта для кофейни. Если вы владелец и хотите такой сайт — напишите.</span>
</div></footer>
<div class="bar">{bar}</div>
</body>
</html>
"""

for c in CAFES:
    d = ROOT / c["slug"]
    d.mkdir(exist_ok=True)
    out = page(c)
    out = out.replace("__CREDITS__", credits(out))
    (d / "index.html").write_text(out, encoding="utf-8")
    print("ok", c["slug"])
