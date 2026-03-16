import streamlit as st
import pandas as pd
from typing import List, Dict

st.set_page_config(
    page_title="Webste 個別相談デモ",
    page_icon="🧭",
    layout="wide",
)

# -----------------------------
# 初期化
# -----------------------------
DEFAULT_EXPERIENCES = pd.DataFrame([
    {
        "経験タイトル": "",
        "カテゴリ": "仕事",
        "経験内容": "",
        "一次情報": 3,
        "ニーズ変換": 3,
        "生活相性": 3,
        "想定市場": "",
    }
])

DEFAULT_MARKETS = pd.DataFrame([
    {
        "市場名": "",
        "一次情報の強さ": 3,
        "企業ニーズ": 3,
        "継続しやすさ": 3,
        "案件化しやすさ": 3,
    }
])

DEFAULT_COMPANIES = pd.DataFrame([
    {
        "企業名": "",
        "企業URL": "",
        "対象市場": "",
        "型の見えやすさ": 3,
        "改善余地": 3,
        "案件化しやすさ": 3,
        "盗む型": "",
        "最初に見る場所": "",
    }
])

if "master" not in st.session_state:
    st.session_state.master = {
        "氏名": "",
        "現職": "",
        "副業経験": "なし",
        "発信経験": "なし",
        "既存スキル": [],
        "可処分時間_週": 5,
        "作業タイプ": "平日型",
        "目標": "最短回収",
        "最大の不安": "",
    }

if "experiences" not in st.session_state:
    st.session_state.experiences = DEFAULT_EXPERIENCES.copy()

if "markets" not in st.session_state:
    st.session_state.markets = DEFAULT_MARKETS.copy()

if "companies" not in st.session_state:
    st.session_state.companies = DEFAULT_COMPANIES.copy()

if "do_not_list" not in st.session_state:
    st.session_state.do_not_list = []


# -----------------------------
# 判定ロジック
# -----------------------------
def classify_user(master: Dict) -> str:
    hours = int(master.get("可処分時間_週", 5))
    has_side = master.get("副業経験") == "あり"
    has_posting = master.get("発信経験") == "あり"
    skills = master.get("既存スキル", [])

    if not has_side and not has_posting and hours <= 5 and len(skills) == 0:
        return "T1_完全未経験_週5時間前後"
    if not has_side and hours >= 10:
        return "T2_未経験_週10時間以上"
    if has_posting and len(skills) == 0:
        return "T3_発信やブログ等の経験あり"
    if len(skills) > 0:
        return "T4_既存スキルあり"
    return "T2_未経験_週10時間以上"


def calc_experience_table(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    for col in ["一次情報", "ニーズ変換", "生活相性"]:
        temp[col] = pd.to_numeric(temp[col], errors="coerce").fillna(0)
    temp["総合点"] = temp["一次情報"] + temp["ニーズ変換"] + temp["生活相性"]

    def rank(score: float) -> str:
        if score >= 12:
            return "A"
        if score >= 9:
            return "B"
        return "C"

    temp["判定"] = temp["総合点"].apply(rank)
    return temp


def calc_market_table(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    score_cols = ["一次情報の強さ", "企業ニーズ", "継続しやすさ", "案件化しやすさ"]
    for col in score_cols:
        temp[col] = pd.to_numeric(temp[col], errors="coerce").fillna(0)
    temp["総合点"] = temp[score_cols].sum(axis=1)

    def rank(score: float) -> str:
        if score >= 16:
            return "A"
        if score >= 12:
            return "B"
        return "C"

    temp["判定"] = temp["総合点"].apply(rank)
    return temp.sort_values(["判定", "総合点"], ascending=[True, False])


def calc_company_table(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    score_cols = ["型の見えやすさ", "改善余地", "案件化しやすさ"]
    for col in score_cols:
        temp[col] = pd.to_numeric(temp[col], errors="coerce").fillna(0)
    temp["総合点"] = temp[score_cols].sum(axis=1)

    def classify(score: float) -> str:
        if score >= 12:
            return "A_先に型を盗む"
        if score >= 9:
            return "B_入口提案"
        return "C_参考"

    temp["分類"] = temp["総合点"].apply(classify)
    return temp.sort_values(["総合点"], ascending=False)


def get_revenue_ranges(user_type: str) -> Dict[str, str]:
    if user_type == "T1_完全未経験_週5時間前後":
        return {
            "慎重ライン": "0〜1万円",
            "現実ライン": "1〜3万円",
            "上振れライン": "3万円前後",
            "到達状態": "市場と企業の方向性が固まり、成果物1つ＋小さな収益化の入口が見え始める段階",
            "6ヶ月回収見込み": "小さな案件・提案の継続化が見え始める",
            "10ヶ月回収見込み": "回収ライン到達の現実性が高まる",
        }
    if user_type == "T2_未経験_週10時間以上":
        return {
            "慎重ライン": "0〜3万円",
            "現実ライン": "1〜5万円",
            "上振れライン": "5万円前後",
            "到達状態": "成果物1〜2個、接触や提案の入口、小さな案件化が条件次第で見え始める段階",
            "6ヶ月回収見込み": "案件化・改善提案の再現性が出てくる",
            "10ヶ月回収見込み": "回収ライン到達の現実性がかなり高まる",
        }
    if user_type == "T3_発信やブログ等の経験あり":
        return {
            "慎重ライン": "1〜3万円",
            "現実ライン": "3〜7万円",
            "上振れライン": "7万円前後",
            "到達状態": "既存経験を企業ニーズへ接続し、自己流を修正しながら小さな継続導線が見え始める段階",
            "6ヶ月回収見込み": "企業型の型が定着し、回収速度が上がりやすい",
            "10ヶ月回収見込み": "回収ライン到達の現実性が高い",
        }
    return {
        "慎重ライン": "3〜7万円",
        "現実ライン": "5〜10万円",
        "上振れライン": "10〜15万円",
        "到達状態": "既存スキルを市場に再定義し、小さな案件化または継続導線が見え始める段階",
        "6ヶ月回収見込み": "回収初動がかなり見えやすい",
        "10ヶ月回収見込み": "回収ライン到達の現実性が高い",
    }


def build_roadmap(user_type: str, market: str, company: str) -> pd.DataFrame:
    rows = [
        ["Week1", "経験棚卸し", "使える経験を3つ以上抽出", "人生棚卸しシート初稿", "市場候補の種が出ている"],
        ["Week2", "市場比較", "A市場を1〜2個に絞る", "市場選定マップ", "今すぐ狙う市場が明確"],
        ["Week3", "企業比較", "先に見る企業を2〜3社決める", "企業選定シート", "型を盗む企業が決定"],
        ["Week4", "型抽出", "盗む型を3つ言語化", "型抽出メモ", "何を真似するか曖昧でない"],
        ["Week5", "初回制作", "小さな成果物を1つ作る", "初回アウトプット", "人に見せられる形になっている"],
        ["Week6", "改善", "改善前後の差を説明できる", "改善版アウトプット", "改善理由が言語化できる"],
        ["Week7", "別形式展開", "2つ目の成果物を作る", "2つ目の成果物", "型の横展開ができる"],
        ["Week8", "提案視点化", "改善提案を3つ出す", "提案メモ", "惜しい点と改善案を言える"],
        ["Week9", "実績整理", "見せられる材料を整える", "簡易ポートフォリオ", "相談や提案に使える"],
        ["Week10", "接触準備", "送る先と文面を決める", "接触リスト", "誰にどう出すか明確"],
        ["Week11", "小さく接触", "1〜3件接触する", "接触記録", "ゼロ行動で終わっていない"],
        ["Week12", "次の3ヶ月設計", "継続方針を明確化", "次期方針メモ", "次の一手が明確"],
    ]
    roadmap = pd.DataFrame(rows, columns=["週", "テーマ", "今週のゴール", "成果物", "完了基準"])
    roadmap["市場"] = market
    roadmap["対象企業"] = company
    roadmap["タイプ"] = user_type
    roadmap["今週やらないこと"] = [
        "いきなりSNS多面展開をしない",
        "稼げそうだけで市場を決めない",
        "有名企業だけを追わない",
        "AI大量生成を目的化しない",
        "自分ブログ収益化を主軸にしない",
        "新ノウハウを探し続けない",
        "全部を同時に極めない",
        "高単価案件だけを狙わない",
        "作って満足しない",
        "準備だけで終わらない",
        "反応ゼロで止まらない",
        "次の計画を曖昧にしない",
    ]
    return roadmap


def get_default_do_not_list(user_type: str) -> List[Dict[str, str]]:
    common = [
        {
            "やらないこと": "最初から自分ブログの収益化を主軸にしない",
            "理由": "正解が見えないまま続けると、独学の自腹に戻りやすいから",
            "代わりに集中": "企業コンテンツで型を学ぶ",
            "再開条件": "企業の型を1〜2個再現できた後",
        },
        {
            "やらないこと": "SNSを全部同時に伸ばそうとしない",
            "理由": "発信・導線・案件化が全部中途半端になるから",
            "代わりに集中": "市場・企業・型の確定",
            "再開条件": "提案材料とコンテンツ軸が固まった後",
        },
        {
            "やらないこと": "AIで大量生成すること自体を目的にしない",
            "理由": "市場選定と企業選定がズレると、速く遠回りするだけだから",
            "代わりに集中": "何を書くか、何を改善するかの判断",
            "再開条件": "テーマと型が固まった後",
        },
        {
            "やらないこと": "新しいノウハウを次々つまみ食いしない",
            "理由": "判断コストが増え、実行が止まるから",
            "代わりに集中": "今決めた市場と企業で3ヶ月やり切る",
            "再開条件": "3ヶ月の振り返り後",
        },
    ]

    if user_type.startswith("T1"):
        common.append(
            {
                "やらないこと": "最初から世界観発信に時間をかけない",
                "理由": "土台がない状態だと、反応の取り方が分からず止まりやすいから",
                "代わりに集中": "企業型の型を1つ真似する",
                "再開条件": "市場とコンテンツ軸が決まった後",
            }
        )
    elif user_type.startswith("T4"):
        common.append(
            {
                "やらないこと": "自分のスキルをそのまま売ろうとしない",
                "理由": "市場に合わせて再定義しないと、刺さらないから",
                "代わりに集中": "既存スキルを企業ニーズに接続する",
                "再開条件": "対象市場と企業の型が見えた後",
            }
        )

    return common


# -----------------------------
# サイドバー
# -----------------------------
st.sidebar.title("Webste 個別相談デモ")
step = st.sidebar.radio(
    "表示ステップ",
    [
        "0. 基本情報",
        "1. 人生棚卸し",
        "2. 市場選定",
        "3. 企業選定",
        "4. 3ヶ月ロードマップ",
        "5. 収益シミュレーション",
        "6. やらないこと",
        "7. 最終サマリー",
    ],
)

user_type = classify_user(st.session_state.master)
st.sidebar.info(f"現在のタイプ判定: {user_type}")

# -----------------------------
# 0 基本情報
# -----------------------------
if step == "0. 基本情報":
    st.title("0. 基本情報")
    st.caption("まずは前提条件を揃えます。")

    with st.form("master_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("氏名", value=st.session_state.master["氏名"])
            job = st.text_input("現職", value=st.session_state.master["現職"])
            side = st.selectbox("副業経験", ["なし", "あり"], index=0 if st.session_state.master["副業経験"] == "なし" else 1)
            posting = st.selectbox("発信経験", ["なし", "あり"], index=0 if st.session_state.master["発信経験"] == "なし" else 1)
        with col2:
            skills = st.multiselect(
                "既存スキル",
                ["文章", "デザイン", "営業", "資料作成", "AI活用"],
                default=st.session_state.master["既存スキル"],
            )
            hours = st.slider("週の可処分時間", 1, 30, int(st.session_state.master["可処分時間_週"]))
            work_type = st.radio("作業タイプ", ["平日型", "土日型"], index=0 if st.session_state.master["作業タイプ"] == "平日型" else 1)
            goal = st.selectbox("目標", ["最短回収", "安定収益", "資産形成"], index=["最短回収", "安定収益", "資産形成"].index(st.session_state.master["目標"]))
        anxiety = st.text_area("最大の不安", value=st.session_state.master["最大の不安"], height=120)

        submitted = st.form_submit_button("保存する")
        if submitted:
            st.session_state.master = {
                "氏名": name,
                "現職": job,
                "副業経験": side,
                "発信経験": posting,
                "既存スキル": skills,
                "可処分時間_週": hours,
                "作業タイプ": work_type,
                "目標": goal,
                "最大の不安": anxiety,
            }
            st.success("基本情報を保存しました。")

    st.subheader("現在の判定")
    st.write(f"**タイプ**: {classify_user(st.session_state.master)}")


# -----------------------------
# 1 人生棚卸し
# -----------------------------
elif step == "1. 人生棚卸し":
    st.title("1. 人生棚卸し")
    st.caption("経験を価値の素材として抽出します。")

    edited = st.data_editor(
        st.session_state.experiences,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "カテゴリ": st.column_config.SelectboxColumn("カテゴリ", options=["仕事", "生活", "失敗", "継続", "学習"]),
            "一次情報": st.column_config.NumberColumn("一次情報", min_value=1, max_value=5, step=1),
            "ニーズ変換": st.column_config.NumberColumn("ニーズ変換", min_value=1, max_value=5, step=1),
            "生活相性": st.column_config.NumberColumn("生活相性", min_value=1, max_value=5, step=1),
        },
    )
    st.session_state.experiences = edited

    result = calc_experience_table(edited)
    st.subheader("判定結果")
    st.dataframe(result, use_container_width=True)

    top_exp = result[result["判定"] == "A"]
    if not top_exp.empty:
        st.success("A判定の経験は、次の市場選定に渡す候補です。")
    else:
        st.warning("まずは A か B の経験候補を最低1つ作るのが先です。")


# -----------------------------
# 2 市場選定
# -----------------------------
elif step == "2. 市場選定":
    st.title("2. 市場選定")
    st.caption("好きな市場ではなく、勝ち筋がある市場を絞ります。")

    exp_result = calc_experience_table(st.session_state.experiences)
    candidate_markets = sorted({m for m in exp_result["想定市場"].fillna("").tolist() if str(m).strip()})

    if candidate_markets:
        st.info(f"人生棚卸しから出た市場候補: {', '.join(candidate_markets)}")

    edited = st.data_editor(
        st.session_state.markets,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "一次情報の強さ": st.column_config.NumberColumn("一次情報の強さ", min_value=1, max_value=5, step=1),
            "企業ニーズ": st.column_config.NumberColumn("企業ニーズ", min_value=1, max_value=5, step=1),
            "継続しやすさ": st.column_config.NumberColumn("継続しやすさ", min_value=1, max_value=5, step=1),
            "案件化しやすさ": st.column_config.NumberColumn("案件化しやすさ", min_value=1, max_value=5, step=1),
        },
    )
    st.session_state.markets = edited

    result = calc_market_table(edited)
    st.subheader("市場判定")
    st.dataframe(result, use_container_width=True)

    a_markets = result[result["判定"] == "A"]["市場名"].dropna().tolist()
    if a_markets:
        st.success(f"A市場: {', '.join([m for m in a_markets if str(m).strip()])}")
    else:
        st.warning("A市場がまだありません。スコアを見直してください。")


# -----------------------------
# 3 企業選定
# -----------------------------
elif step == "3. 企業選定":
    st.title("3. 企業選定")
    st.caption("営業先探しではなく、先に盗む型を決めます。")

    market_result = calc_market_table(st.session_state.markets)
    a_markets = market_result[market_result["判定"] == "A"]["市場名"].dropna().tolist()
    if a_markets:
        st.info(f"優先市場候補: {', '.join([m for m in a_markets if str(m).strip()])}")

    edited = st.data_editor(
        st.session_state.companies,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "型の見えやすさ": st.column_config.NumberColumn("型の見えやすさ", min_value=1, max_value=5, step=1),
            "改善余地": st.column_config.NumberColumn("改善余地", min_value=1, max_value=5, step=1),
            "案件化しやすさ": st.column_config.NumberColumn("案件化しやすさ", min_value=1, max_value=5, step=1),
        },
    )
    st.session_state.companies = edited

    result = calc_company_table(edited)
    st.subheader("企業判定")
    st.dataframe(result, use_container_width=True)

    top = result[result["分類"] == "A_先に型を盗む"]
    if not top.empty:
        st.success("A分類の企業は、先に観察する企業候補です。")
    else:
        st.warning("まずは1社でも『先に型を盗む企業』を置けると強いです。")


# -----------------------------
# 4 3ヶ月ロードマップ
# -----------------------------
elif step == "4. 3ヶ月ロードマップ":
    st.title("4. 3ヶ月ロードマップ")
    st.caption("今の生活で、何を・どの順番で・どこまで進めるかを見ます。")

    market_result = calc_market_table(st.session_state.markets)
    company_result = calc_company_table(st.session_state.companies)

    market = ""
    company = ""

    a_market_rows = market_result[market_result["判定"] == "A"]
    if not a_market_rows.empty:
        market = str(a_market_rows.iloc[0]["市場名"])

    a_company_rows = company_result[company_result["分類"] == "A_先に型を盗む"]
    if not a_company_rows.empty:
        company = str(a_company_rows.iloc[0]["企業名"])

    roadmap = build_roadmap(user_type, market, company)
    st.dataframe(roadmap, use_container_width=True)

    st.subheader("ガント風の全体像")
    for _, row in roadmap.iterrows():
        week_num = int(str(row["週"]).replace("Week", ""))
        width = min(95, 18 + week_num * 5)
        st.markdown(
            f"""
            <div style="margin-bottom:8px;">
              <div style="font-size:14px; font-weight:600;">{row['週']}｜{row['テーマ']}</div>
              <div style="background:#E9EEF5; border-radius:10px; height:12px; width:100%;">
                <div style="background:#4A6CF7; height:12px; width:{width}%; border-radius:10px;"></div>
              </div>
              <div style="font-size:12px; color:#666;">{row['今週のゴール']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------
# 5 収益シミュレーション
# -----------------------------
elif step == "5. 収益シミュレーション":
    st.title("5. 収益シミュレーション")
    st.caption("夢を煽るためではなく、現実ラインを確認するための表示です。")

    ranges = get_revenue_ranges(user_type)
    c1, c2, c3 = st.columns(3)
    c1.metric("慎重ライン", ranges["慎重ライン"])
    c2.metric("現実ライン", ranges["現実ライン"])
    c3.metric("上振れライン", ranges["上振れライン"])

    st.subheader("3ヶ月の到達状態")
    st.info(ranges["到達状態"])

    col1, col2 = st.columns(2)
    with col1:
        st.write("**6ヶ月回収見込み**")
        st.write(ranges["6ヶ月回収見込み"])
    with col2:
        st.write("**10ヶ月回収見込み**")
        st.write(ranges["10ヶ月回収見込み"])

    st.subheader("この人の主な収益化ルート")
    if user_type.startswith("T4"):
        st.write("- 既存スキル × 企業ニーズ")
        st.write("- 小さな改善提案")
        st.write("- 継続化しやすい実務導線")
    elif user_type.startswith("T3"):
        st.write("- 発信経験の企業型への転用")
        st.write("- 記事 / 図解 / 比較整理")
        st.write("- 小さな継続導線")
    else:
        st.write("- 企業コンテンツで型を学ぶ")
        st.write("- 小さな成果物の作成")
        st.write("- 提案入口の確保")


# -----------------------------
# 6 やらないこと
# -----------------------------
elif step == "6. やらないこと":
    st.title("6. やらないことリスト")
    st.caption("やることを増やすより、今は切ることを決めます。")

    items = get_default_do_not_list(user_type)
    selected = []

    for idx, item in enumerate(items):
        with st.container(border=True):
            checked = st.checkbox(item["やらないこと"], value=True, key=f"dnd_{idx}")
            st.write(f"**理由**: {item['理由']}")
            st.write(f"**代わりに集中**: {item['代わりに集中']}")
            st.write(f"**再開条件**: {item['再開条件']}")
            if checked:
                selected.append(item)

    st.session_state.do_not_list = selected
    st.success(f"現在 {len(selected)} 件を『今はやらないこと』として採用しています。")


# -----------------------------
# 7 最終サマリー
# -----------------------------
elif step == "7. 最終サマリー":
    st.title("7. 最終サマリー")
    st.caption("個別相談の最後に渡す1枚イメージです。")

    exp_result = calc_experience_table(st.session_state.experiences)
    market_result = calc_market_table(st.session_state.markets)
    company_result = calc_company_table(st.session_state.companies)
    ranges = get_revenue_ranges(user_type)

    top_exp = exp_result.sort_values("総合点", ascending=False)
    top_market = market_result.sort_values("総合点", ascending=False)
    top_company = company_result.sort_values("総合点", ascending=False)

    picked_exp = top_exp.iloc[0]["経験タイトル"] if not top_exp.empty else ""
    picked_market = top_market.iloc[0]["市場名"] if not top_market.empty else ""
    picked_company = top_company.iloc[0]["企業名"] if not top_company.empty else ""

    recommend_course = "エキスパートコース"
    reason = "判断量が多く、個別設計と伴走の価値が高い状態のため"
    if user_type == "T4_既存スキルあり":
        recommend_course = "スタンダード or エキスパート要判定"
        reason = "既存スキルがあり自走余地はあるが、接続設計の精度次第で変わるため"

    st.markdown("## あなた専用の勝ち筋設計サマリー")
    st.write(f"**タイプ判定**: {user_type}")
    st.write(f"**今回使う経験**: {picked_exp if picked_exp else '未設定'}")
    st.write(f"**狙う市場**: {picked_market if picked_market else '未設定'}")
    st.write(f"**先に型を盗む企業**: {picked_company if picked_company else '未設定'}")
    st.write("**3ヶ月の重点テーマ**: 市場確定 → 企業選定 → 型抽出 → 小さな成果物 → 接触")
    st.write(f"**3ヶ月現実ライン**: {ranges['現実ライン']}")
    st.write(f"**6ヶ月回収見込み**: {ranges['6ヶ月回収見込み']}")
    st.write(f"**10ヶ月回収見込み**: {ranges['10ヶ月回収見込み']}")

    st.subheader("今やらないこと")
    if st.session_state.do_not_list:
        for item in st.session_state.do_not_list:
            st.write(f"- {item['やらないこと']}")
    else:
        st.write("- 未設定")

    st.subheader("推奨コース")
    st.success(f"{recommend_course}")
    st.write(reason)

    st.subheader("次回アクション")
    st.write("1. A市場を1つ確定する")
    st.write("2. 先に型を盗む企業を2〜3社決める")
    st.write("3. Week1〜4を実行して初回成果物まで持っていく")
