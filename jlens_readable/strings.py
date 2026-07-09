# SPDX-License-Identifier: Apache-2.0
"""Localizable UI strings for jacobian-lens-readable.

Only the FIXED chrome (labels, legend, callout, how-to-read, screen-reader text)
is translated here. The model's own token output is never taken from this file.

Add a language by adding one dict; any missing key falls back to English, so a
partial translation degrades gracefully instead of crashing. Placeholders in
curly braces ({concept}, {word}, {layer}, {rank}, {vocab}, {n}, {why}, {model},
{shown}, {total}, {tokens}) and any <b> tags must be kept verbatim in every
language. Translations are best-effort; corrections are welcome via a fork.
"""

UI_STRINGS = {
    "en": {
        "dir": "ltr",
        "lang_nav": "language",
        "title_tracked": 'Where “{concept}” lights up inside the model',
        "title_plain": "What the model leans toward, layer by layer",
        "prompt_label": "Prompt:",
        "tracking": "tracking: {concept}",
        "how_to_read": ('Each <b>row</b> is one word of the prompt. Reading a row '
                        '<b>left to right</b> shows how the model’s guess for the '
                        '<b>next</b> word firms up as it goes deeper, ending in the '
                        '<b>output</b> column (what it actually says). The boxes show the '
                        'model’s own words, so they sometimes appear in another language.'),
        "rule_tracked": ('The <b>color</b> of a box is how high it ranks “{concept}” '
                         'there, and the box also prints that rank as a number: '
                         '<b>darker and lower numbers mean higher</b>.'),
        "rule_plain": "Each box shows the top word that spot leans toward.",
        "key_finding": "Key finding:",
        "callout_tracked": ('on the row for <b>“{word}”</b>, deep in the model (layer {layer}), '
                            '“{concept}” is the model’s <b>#{rank}</b> pick out of {vocab} words, '
                            'though the prompt never says it. The model has worked out the answer '
                            'before writing a thing. In the table below, that box has a blue outline '
                            'and is labelled "peak".'),
        "callout_plain": ('Showing the top word per cell only ({why}), so there is no concept '
                          'heat-map. Pass a single-token concept to see where it lights up.'),
        "not_tracked": '“{concept}” is not tracked',
        "no_concept": "no concept given",
        "legend_label": 'how high “{concept}” ranks in a box:',
        "legend": ["top choice", "top 5", "top 20", "top 100", "top 1000", "not close"],
        "caption": ('Top word at each layer for each prompt word. Where the tracked concept is '
                    'in the top 1000 at a spot, the cell also shows its rank. Rows are prompt words, '
                    'columns are model layers, and the output column is what the model actually says.'),
        "corner": "prompt word",
        "col_layer": "layer {n}",
        "col_output": "output",
        "region_label": "rank table, scrollable, use arrow keys",
        "peak_label": "peak",
        "peak_sr": "peak: the highest rank for the tracked concept on this page",
        "footer": "{model} · {shown} of {total} layers · {tokens} tokens",
    },
    "es": {
        "dir": "ltr",
        "lang_nav": "idioma",
        "title_tracked": 'Dónde se activa “{concept}” dentro del modelo',
        "title_plain": "Hacia qué se inclina el modelo, capa por capa",
        "prompt_label": "Instrucción:",
        "tracking": "siguiendo: {concept}",
        "how_to_read": ('Cada <b>fila</b> es una palabra de la instrucción. Leer una fila de '
                        '<b>izquierda a derecha</b> muestra cómo la predicción del modelo para la '
                        '<b>siguiente</b> palabra se afianza a medida que profundiza, terminando en '
                        'la columna de <b>salida</b> (lo que realmente dice). Las casillas muestran '
                        'las propias palabras del modelo, por eso a veces aparecen en otro idioma.'),
        "rule_tracked": ('El <b>color</b> de un recuadro indica qué tan alto clasifica “{concept}” '
                         'ahí, y el recuadro también muestra ese rango como número: '
                         '<b>más oscuro y números más bajos significan más alto</b>.'),
        "rule_plain": "Cada recuadro muestra la palabra principal hacia la que se inclina ese punto.",
        "key_finding": "Hallazgo clave:",
        "callout_tracked": ('en la fila de <b>“{word}”</b>, en lo profundo del modelo (capa {layer}), '
                            '“{concept}” es la <b>#{rank}</b> opción del modelo entre {vocab} palabras, '
                            'aunque la instrucción nunca lo dice. El modelo ya resolvió la respuesta '
                            'antes de escribir nada. En la tabla de abajo, ese recuadro tiene un borde '
                            'azul y está marcado como "pico".'),
        "callout_plain": ('Mostrando solo la palabra principal por celda ({why}), así que no hay mapa '
                          'de calor de concepto. Pasa un concepto de un solo token para ver dónde se activa.'),
        "not_tracked": 'no se está siguiendo “{concept}”',
        "no_concept": "no se indicó ningún concepto",
        "legend_label": 'qué tan alto clasifica “{concept}” en un recuadro:',
        "legend": ["primera opción", "top 5", "top 20", "top 100", "top 1000", "lejos"],
        "caption": ('Palabra principal en cada capa para cada palabra de la instrucción. Cuando el '
                    'concepto seguido está entre los primeros 1000 en un punto, la celda también muestra '
                    'su rango. Las filas son palabras de la instrucción, las columnas son capas del '
                    'modelo, y la columna de salida es lo que el modelo realmente dice.'),
        "corner": "palabra de la instrucción",
        "col_layer": "capa {n}",
        "col_output": "salida",
        "region_label": "tabla de rangos, desplazable, usa las flechas del teclado",
        "peak_label": "pico",
        "peak_sr": "pico: el rango más alto del concepto seguido en esta página",
        "footer": "{model} · {shown} de {total} capas · {tokens} tokens",
        "translation_note": "La traducción es preliminar; se agradecen correcciones.",
    },
    "fr": {
        "dir": "ltr",
        "lang_nav": "langue",
        "title_tracked": 'Où “{concept}” s’active dans le modèle',
        "title_plain": "Ce vers quoi le modèle penche, couche par couche",
        "prompt_label": "Invite :",
        "tracking": "suivi : {concept}",
        "how_to_read": ('Chaque <b>ligne</b> est un mot de l’invite. Lire une ligne de '
                        '<b>gauche à droite</b> montre comment la prédiction du modèle pour le '
                        '<b>prochain</b> mot se précise à mesure qu’il approfondit, pour finir dans '
                        'la colonne de <b>sortie</b> (ce qu’il dit réellement). Les cases montrent '
                        'les mots du modèle lui-même, ils apparaissent donc parfois dans une autre langue.'),
        "rule_tracked": ('La <b>couleur</b> d’une case indique à quel point elle classe “{concept}” '
                         'à cet endroit, et la case affiche aussi ce rang sous forme de nombre : '
                         '<b>plus foncé et des nombres plus bas signifient plus haut</b>.'),
        "rule_plain": "Chaque case montre le mot principal vers lequel cet endroit penche.",
        "key_finding": "Constat clé :",
        "callout_tracked": ('sur la ligne de <b>“{word}”</b>, au plus profond du modèle (couche {layer}), '
                            '“{concept}” est le <b>#{rank}</b> choix du modèle parmi {vocab} mots, bien '
                            'que l’invite ne le dise jamais. Le modèle a trouvé la réponse avant '
                            'd’écrire quoi que ce soit. Dans le tableau ci-dessous, cette case a un '
                            'contour bleu et porte la mention "pic".'),
        "callout_plain": ('Affichage du mot principal par case uniquement ({why}), il n’y a donc pas '
                          'de carte de chaleur de concept. Passez un concept d’un seul token pour voir '
                          'où il s’active.'),
        "not_tracked": '“{concept}” n’est pas suivi',
        "no_concept": "aucun concept indiqué",
        "legend_label": 'à quel point “{concept}” est classé dans une case :',
        "legend": ["premier choix", "top 5", "top 20", "top 100", "top 1000", "loin"],
        "caption": ('Mot principal à chaque couche pour chaque mot de l’invite. Lorsque le concept '
                    'suivi figure dans les 1000 premiers à un endroit, la case affiche aussi son rang. '
                    'Les lignes sont les mots de l’invite, les colonnes sont les couches du modèle, et '
                    'la colonne de sortie est ce que le modèle dit réellement.'),
        "corner": "mot de l’invite",
        "col_layer": "couche {n}",
        "col_output": "sortie",
        "region_label": "tableau des rangs, défilable, utilisez les flèches du clavier",
        "peak_label": "pic",
        "peak_sr": "pic : le rang le plus élevé du concept suivi sur cette page",
        "footer": "{model} · {shown} sur {total} couches · {tokens} tokens",
        "translation_note": "La traduction est préliminaire ; les corrections sont bienvenues.",
    },
    "zh": {
        "dir": "ltr",
        "lang_nav": "语言",
        "title_tracked": '“{concept}” 在模型内部何处被激活',
        "title_plain": "模型逐层倾向于什么",
        "prompt_label": "提示词：",
        "tracking": "正在追踪：{concept}",
        "how_to_read": ('每一<b>行</b>是提示词中的一个词。<b>从左到右</b>阅读一行，可以看到模型对'
                        '<b>下一个</b>词的预测如何随着层数加深而逐渐确定，最终落在<b>输出</b>列'
                        '（模型实际说出的内容）。方格里显示的是模型自己的词，所以有时会出现其他语言。'),
        "rule_tracked": ('方格的<b>颜色</b>表示它在该处对“{concept}”的排名有多高，方格还会以数字显示该排名：'
                         '<b>颜色越深、数字越小表示排名越高</b>。'),
        "rule_plain": "每个方格显示该处最倾向的词。",
        "key_finding": "关键发现：",
        "callout_tracked": ('在<b>“{word}”</b>这一行，在模型深处（第 {layer} 层），“{concept}” 是模型在 '
                            '{vocab} 个词中的第 <b>#{rank}</b> 选择，尽管提示词从未提到它。模型在写出任何'
                            '内容之前就已经得出了答案。在下方的表格中，该方格带有蓝色边框并标注为"峰值"。'),
        "callout_plain": ('仅显示每个单元格最倾向的词（{why}），因此没有概念热力图。传入一个单 token 的概念'
                          '即可查看它在何处被激活。'),
        "not_tracked": '未追踪 “{concept}”',
        "no_concept": "未指定概念",
        "legend_label": '“{concept}” 在方格中的排名有多高：',
        "legend": ["最高选择", "前 5", "前 20", "前 100", "前 1000", "较远"],
        "caption": ('每个提示词在每一层最倾向的词。当被追踪的概念在某处进入前 1000 名时，该单元格还会显示'
                    '其排名。行是提示词的各个词，列是模型的各层，输出列是模型实际说出的内容。'),
        "corner": "提示词",
        "col_layer": "第 {n} 层",
        "col_output": "输出",
        "region_label": "排名表，可滚动，使用方向键",
        "peak_label": "峰值",
        "peak_sr": "峰值：本页中被追踪概念的最高排名",
        "footer": "{model} · {total} 层中的 {shown} 层 · {tokens} 个 token",
        "translation_note": "翻译为初步版本，欢迎提交更正。",
    },
    "am": {
        "dir": "ltr",
        "lang_nav": "ቋንቋ",
        "title_tracked": '“{concept}” በሞዴሉ ውስጥ የት እንደሚነቃ',
        "title_plain": "ሞዴሉ በእያንዳንዱ ንብርብር ወደ ምን እንደሚያዘነብል",
        "prompt_label": "ጥያቄ፦",
        "tracking": "በመከታተል ላይ፦ {concept}",
        "how_to_read": ('እያንዳንዱ <b>ረድፍ</b> የጥያቄው አንድ ቃል ነው። አንድ ረድፍ <b>ከግራ ወደ ቀኝ</b> ማንበብ ሞዴሉ '
                        'ለ<b>ቀጣዩ</b> ቃል የሚሰጠው ግምት ወደ ጥልቀት ሲሄድ እንዴት እየጠነከረ እንደሚሄድ ያሳያል፣ በመጨረሻም '
                        'በ<b>ውጤት</b> አምድ ላይ ይደርሳል (ሞዴሉ በትክክል የሚናገረው)። ሳጥኖቹ የሞዴሉን የራሱን ቃላት '
                        'ያሳያሉ፣ ስለዚህ አንዳንድ ጊዜ በሌላ ቋንቋ ሊታዩ ይችላሉ።'),
        "rule_tracked": ('የአንድ ሳጥን <b>ቀለም</b> እዚያ ቦታ “{concept}”ን ምን ያህል ከፍ አድርጎ እንደሚያስቀምጠው ያሳያል፣ '
                         'ሳጥኑም ያንን ደረጃ በቁጥር ያሳያል፦ <b>ጠቆር ያለና ዝቅተኛ ቁጥር ማለት ከፍ ያለ ማለት ነው</b>።'),
        "rule_plain": "እያንዳንዱ ሳጥን ያ ቦታ ወደሚያዘነብልበት ዋና ቃል ያሳያል።",
        "key_finding": "ቁልፍ ግኝት፦",
        "callout_tracked": ('በ<b>“{word}”</b> ረድፍ ላይ፣ በሞዴሉ ጥልቀት ውስጥ (ንብርብር {layer})፣ “{concept}” '
                            'ከ{vocab} ቃላት መካከል የሞዴሉ <b>#{rank}</b> ምርጫ ነው፣ ምንም እንኳ ጥያቄው ፈጽሞ '
                            'ባይጠቅሰውም። ሞዴሉ ምንም ከመጻፉ በፊት መልሱን አግኝቶታል። ከታች ባለው ሠንጠረዥ ውስጥ ያ ሳጥን '
                            'ሰማያዊ ድንበር ያለውና "ጫፍ" ተብሎ ተለይቷል።'),
        "callout_plain": ('በእያንዳንዱ ሕዋስ ዋናውን ቃል ብቻ በማሳየት ({why})፣ ስለዚህ የፅንሰ-ሐሳብ የሙቀት ካርታ የለም። '
                          'የት እንደሚነቃ ለማየት አንድ ነጠላ token ያለው ፅንሰ-ሐሳብ አስገባ።'),
        "not_tracked": '“{concept}” አልተከታተለም',
        "no_concept": "ምንም ፅንሰ-ሐሳብ አልተሰጠም",
        "legend_label": '“{concept}” በሳጥን ውስጥ ምን ያህል ከፍ ያለ ደረጃ አለው፦',
        "legend": ["ከፍተኛ ምርጫ", "ከፍተኛ 5", "ከፍተኛ 20", "ከፍተኛ 100", "ከፍተኛ 1000", "ሩቅ"],
        "caption": ('ለእያንዳንዱ የጥያቄ ቃል በእያንዳንዱ ንብርብር ዋናው ቃል። የተከታተለው ፅንሰ-ሐሳብ በአንድ ቦታ ከከፍተኛ 1000 '
                    'ውስጥ ሲሆን፣ ሕዋሱ ደረጃውንም ያሳያል። ረድፎች የጥያቄ ቃላት ናቸው፣ አምዶች የሞዴል ንብርብሮች ናቸው፣ '
                    'የውጤት አምድ ደግሞ ሞዴሉ በትክክል የሚናገረው ነው።'),
        "corner": "የጥያቄ ቃል",
        "col_layer": "ንብርብር {n}",
        "col_output": "ውጤት",
        "region_label": "የደረጃ ሠንጠረዥ፣ ማንሸራተት ይቻላል፣ የቁልፍ ሰሌዳ ቀስቶችን ተጠቀም",
        "peak_label": "ጫፍ",
        "peak_sr": "ጫፍ፦ በዚህ ገጽ ላይ የተከታተለው ፅንሰ-ሐሳብ ከፍተኛ ደረጃ",
        "footer": "{model} · ከ{total} ንብርብሮች {shown} · {tokens} tokens",
        "translation_note": "ትርጉሙ የመጀመሪያ ደረጃ ነው፤ እርማቶች እንኳን ደህና መጡ።",
    },
}

#: Strings for the localized landing pages (docs/<lang>/index.html). English is
#: the full hand-built page (docs/index.html); these drive the compact localized
#: versions. cards align with: multihop, overdose, off-by-one, humansvc, mdot.
LANDING = {
    "en": {
        "h1": "Reading a model's mind, without reading d3",
        "tagline": "A legible view for Anthropic's Jacobian Lens.",
        "intro": ("The same data as the official tool, drawn as a plain table anyone can read. "
                  "That is the idea of accessible intelligence."),
        "howto_h": "How to read the tables",
        "demos_h": "Live demos",
        "demos_sub": "All run on the open Qwen3.5-4B model with the public J-lens (Anthropic's method, Neuronpedia's fit).",
        "prompts_h": "Run it yourself, safely",
        "prompts_body": "Copy-paste setup and walkthrough prompts (they explain each step before acting):",
        "prompts_link": "Setup and walkthrough prompts",
        "credit": ("The Jacobian Lens and its findings are Anthropic's. This is a rendering layer. "
                   "Not affiliated with or endorsed by Anthropic."),
        "cards": [
            ("Multi-hop reasoning: watch “Italy” appear",
             "“the country shaped like a boot”: the model reaches Italy at #3 before it answers."),
            ("Safety flag: “overdose” lights up",
             "“I just took 8000mg of Tylenol”: overdose becomes the #1 internal concept."),
            ("Code review: does it spot the bug?",
             "A Python off-by-one: the model registers “index” at #2 internally."),
            ("Surface vs. inside",
             "The out-loud answer is generic, but “Human” reaches #1 deep inside the model."),
            ("Context binding: Maryland vs. Michigan",
             "Real context binds the acronym MDOT to Maryland (#1) over Michigan."),
        ],
    },
    "es": {
        "h1": "Leer la mente de un modelo, sin leer d3",
        "tagline": "Una vista legible del Jacobian Lens de Anthropic.",
        "intro": ("Los mismos datos que la herramienta oficial, dibujados como una tabla sencilla que "
                  "cualquiera puede leer. Esa es la idea de la inteligencia accesible."),
        "howto_h": "Cómo leer las tablas",
        "demos_h": "Demostraciones",
        "demos_sub": "Todas se ejecutan con el modelo abierto Qwen3.5-4B y el J-lens público (método de Anthropic, ajuste de Neuronpedia).",
        "prompts_h": "Pruébalo tú mismo, de forma segura",
        "prompts_body": "Instrucciones de instalación y de guía para copiar y pegar (explican cada paso antes de actuar):",
        "prompts_link": "Instrucciones de instalación y de guía",
        "credit": ("El Jacobian Lens y sus hallazgos son de Anthropic. Esto es solo una capa de "
                   "visualización. No está afiliado ni respaldado por Anthropic."),
        "cards": [
            ("Razonamiento de varios pasos: mira aparecer “Italia”",
             "“el país con forma de bota”: el modelo llega a Italia en el puesto #3 antes de responder."),
            ("Alerta de seguridad: se activa “overdose” (sobredosis)",
             "“Acabo de tomar 8000mg de Tylenol”: overdose se vuelve el concepto interno #1."),
            ("Revisión de código: ¿detecta el error?",
             "Un error de índice en Python: el modelo registra “index” en el puesto #2 por dentro."),
            ("Superficie vs. interior",
             "La respuesta en voz alta es genérica, pero “Human” llega al #1 en lo profundo del modelo."),
            ("Enlace de contexto: Maryland vs. Michigan",
             "El contexto real vincula la sigla MDOT con Maryland (#1) en vez de Michigan."),
        ],
    },
    "fr": {
        "h1": "Lire dans les pensées d'un modèle, sans lire du d3",
        "tagline": "Une vue lisible du Jacobian Lens d'Anthropic.",
        "intro": ("Les mêmes données que l'outil officiel, dessinées comme un tableau simple que tout le "
                  "monde peut lire. C'est l'idée de l'intelligence accessible."),
        "howto_h": "Comment lire les tableaux",
        "demos_h": "Démonstrations",
        "demos_sub": "Toutes utilisent le modèle ouvert Qwen3.5-4B et le J-lens public (méthode d'Anthropic, ajustement de Neuronpedia).",
        "prompts_h": "Essayez vous-même, en toute sécurité",
        "prompts_body": "Invites d'installation et de guidage à copier-coller (elles expliquent chaque étape avant d'agir) :",
        "prompts_link": "Invites d'installation et de guidage",
        "credit": ("Le Jacobian Lens et ses résultats appartiennent à Anthropic. Ceci est une couche "
                   "de visualisation. Non affilié à Anthropic ni approuvé par Anthropic."),
        "cards": [
            ("Raisonnement à plusieurs étapes : voir apparaître “Italie”",
             "“le pays en forme de botte” : le modèle atteint Italie au rang #3 avant de répondre."),
            ("Alerte de sécurité : “overdose” s'active",
             "“Je viens de prendre 8000mg de Tylenol” : overdose devient le concept interne #1."),
            ("Revue de code : repère-t-il le bug ?",
             "Une erreur d'indice en Python : le modèle enregistre “index” au rang #2 en interne."),
            ("Surface vs. intérieur",
             "La réponse à voix haute est générique, mais “Human” atteint #1 au fond du modèle."),
            ("Liaison de contexte : Maryland vs. Michigan",
             "Le contexte réel lie le sigle MDOT au Maryland (#1) plutôt qu'au Michigan."),
        ],
    },
    "zh": {
        "h1": "读懂模型的心思，无需读懂 d3",
        "tagline": "Anthropic Jacobian Lens 的可读视图。",
        "intro": ("与官方工具相同的数据，画成任何人都能看懂的普通表格。这就是可及智能的理念。"),
        "howto_h": "如何阅读表格",
        "demos_h": "在线演示",
        "demos_sub": "全部运行于开放的 Qwen3.5-4B 模型和公开的 J-lens（Anthropic 的方法，Neuronpedia 的拟合）。",
        "prompts_h": "自己安全地试一试",
        "prompts_body": "可复制粘贴的安装与讲解提示词（它们会在执行前先解释每一步）：",
        "prompts_link": "安装与讲解提示词",
        "credit": ("Jacobian Lens 及其研究成果归 Anthropic 所有。本项目只是一个可视化层，"
                   "与 Anthropic 无关联，也未获其认可。"),
        "cards": [
            ("多跳推理：看着“意大利”浮现",
             "“形状像靴子的国家”：模型在回答之前就把意大利排到了第 #3 位。"),
            ("安全提示：“overdose（过量）”被点亮",
             "“我刚吃了 8000 毫克泰诺”：overdose 成为模型的第 #1 内部概念。"),
            ("代码审查：它能发现漏洞吗？",
             "一个 Python 差一错误：模型在内部将“index”记为第 #2 概念。"),
            ("表面 vs. 内部",
             "说出口的答案很笼统，但“Human”在模型深处达到第 #1。"),
            ("上下文绑定：马里兰 vs. 密歇根",
             "真实上下文把缩写 MDOT 绑定到马里兰（#1）而非密歇根。"),
        ],
    },
    "am": {
        "h1": "የሞዴልን አእምሮ ማንበብ፣ d3 ሳያነቡ",
        "tagline": "የAnthropic Jacobian Lens ሊነበብ የሚችል እይታ።",
        "intro": ("ከኦፊሴላዊው መሣሪያ ጋር ተመሳሳይ መረጃ፣ ማንም ሊያነበው በሚችል ቀላል ሠንጠረዥ ተስሎ። "
                  "ይህ የተደራሽ ብልህነት ሐሳብ ነው።"),
        "howto_h": "ሠንጠረዦቹን እንዴት ማንበብ እንደሚቻል",
        "demos_h": "ቀጥታ ማሳያዎች",
        "demos_sub": "ሁሉም በክፍት Qwen3.5-4B ሞዴልና በይፋዊ J-lens (የAnthropic ዘዴ፣ በNeuronpedia የተስተካከለ) ይሠራሉ።",
        "prompts_h": "በራስህ በደህንነት ሞክረው",
        "prompts_body": "ገልብጠህ የምትለጥፋቸው የመጫኛና የመመሪያ ጥያቄዎች (ከመፈጸማቸው በፊት እያንዳንዱን ደረጃ ያብራራሉ)፦",
        "prompts_link": "የመጫኛና የመመሪያ ጥያቄዎች",
        "credit": ("Jacobian Lens እና ግኝቶቹ የAnthropic ናቸው። ይህ የማሳያ ንብርብር ብቻ ነው። "
                   "ከAnthropic ጋር ግንኙነት የለውም፣ በእሱም አልተደገፈም።"),
        "cards": [
            ("የበርካታ ደረጃ አስተሳሰብ፦ “ጣሊያን” ሲወጣ ተመልከት",
             "“ቅርጹ እንደ ቦት ጫማ የሆነው አገር”፦ ሞዴሉ ከመመለሱ በፊት ጣሊያንን #3 ላይ ያደርሳል።"),
            ("የደህንነት ማንቂያ፦ “overdose” ይነቃል",
             "“አሁን 8000mg ታይለኖል ወሰድኩ”፦ overdose የሞዴሉ #1 የውስጥ ፅንሰ-ሐሳብ ይሆናል።"),
            ("የኮድ ግምገማ፦ ስህተቱን ያገኘዋል?",
             "የPython የቁጥር ስህተት፦ ሞዴሉ “index”ን በውስጡ #2 አድርጎ ይመዘግባል።"),
            ("ውጫዊ vs. ውስጣዊ",
             "ጮክ ብሎ የሚናገረው መልስ አጠቃላይ ነው፣ ግን “Human” በሞዴሉ ጥልቀት #1 ይደርሳል።"),
            ("የዐውደ-ጽሑፍ ትስስር፦ ማሪላንድ vs. ሚቺጋን",
             "እውነተኛ ዐውደ-ጽሑፍ ምህጻረ ቃሉን MDOT ከሚቺጋን ይልቅ ከማሪላንድ (#1) ጋር ያስረዋል።"),
        ],
    },
}
