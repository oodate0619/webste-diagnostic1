import math
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Webste 個別設計ロードマップ",
    page_icon="📘",
    layout="wide"
)

# =========================
# 必要に応じて差し替える定数
# =========================
CTA_URL = "https://example.com"
COURSE_FEE_6_DEFAULT = 600000
COURSE_FEE_10_DEFAULT = 900000
TEN_MONTH_SUPPORT_NOTE = "10ヶ月プランは、必要に応じて費用回収を目指す段階まで延長サポートを想定した設計です。実際の保証条件に合わせて文言は調整してください。"

STEP_TITLES = [
    "1. 人生棚卸しシート",
    "2. 市場選定マップ",
    "3. 企業選定シート",
    "4. 3ヶ月ロードマップ",
    "5. 収益シミュレーション",
    "6. やらないことリスト",
    "7. 最終サマリー"
]

JOB_OPTIONS = [
    "会社員",
    "パート・アルバイト",
    "主婦・主夫",
    "営業職",
    "事務職",
    "接客・販売",
    "医療従事者",
    "介護・福祉職",
    "工場勤務",
    "教育・保育",
    "美容・サロン",
    "ジム・フィットネス関連",
    "フリーランス",
    "自営業",
    "その他"
]

EXPERIENCE_OPTIONS = [
    "文章を書く",
    "Canvaなどで画像を作る",
    "SNS投稿を作る",
    "ブログやサイトを触る",
    "接客・営業をする",
    "事務作業を進める",
    "人に説明する",
    "リサーチする",
    "Excel / スプレッドシートを使う",
    "AIツールを少し触ったことがある"
]

MARKET_PROFILES = {
    "コンテンツ・Web運用支援": {
        "fit": "文章・Canva・SNS・ブログなど、発信や見せ方に近い経験を活かしやすい方向です。",
        "service": "記事構成、SNS投稿設計、LP改善、簡易ディレクション",
        "company_profiles": [
            {
                "name": "情報発信を強化したい中小企業",
                "typical_companies": "士業、教育サービス、BtoB支援会社、小規模ブランド",
                "typical_issues": [
                    "発信が止まりがち",
                    "伝えたいことはあるが整理されていない",
                    "SNSや記事の更新が属人化している"
                ],
                "starter_projects": [
                    "記事構成案の整理",
                    "SNS投稿の型づくり",
                    "LP改善のたたき台作成"
                ],
                "good_signals": [
                    "すでに発信意欲がある",
                    "改善したいテーマが明確",
                    "意思決定が比較的早い"
                ],
                "avoid_signals": [
                    "成果責任だけ重く、素材提供がない",
                    "役割範囲が曖昧",
                    "最初から全部やってほしい前提"
                ]
            },
            {
                "name": "オウンドメディア・SNS運用に課題がある事業者",
                "typical_companies": "採用強化中の会社、メディア運営企業、集客に悩む中小企業",
                "typical_issues": [
                    "投稿が続かない",
                    "訴求軸がぶれている",
                    "見せ方が整理されていない"
                ],
                "starter_projects": [
                    "投稿テーマの整理",
                    "コンテンツカレンダー作成",
                    "見出し・導線の改善提案"
                ],
                "good_signals": [
                    "担当者がいる",
                    "改善対象がはっきりしている",
                    "すでに運用の土台が少しある"
                ],
                "avoid_signals": [
                    "現状データがない",
                    "全部丸投げしたい",
                    "期待値だけが高い"
                ]
            }
        ]
    },
    "営業支援・顧客対応改善": {
        "fit": "接客・営業・説明など、対人コミュニケーションの経験を収益化しやすい方向です。",
        "service": "問い合わせ導線改善、営業資料整理、LINE・顧客対応フロー設計",
        "company_profiles": [
            {
                "name": "営業の型が整っていない中小企業",
                "typical_companies": "地場サービス業、紹介営業中心の会社、拡大途中の小規模企業",
                "typical_issues": [
                    "提案内容が担当者ごとに違う",
                    "問い合わせ後の流れが整っていない",
                    "資料や説明が属人化している"
                ],
                "starter_projects": [
                    "営業資料の整理",
                    "初回案内フローの可視化",
                    "問い合わせ対応テンプレート作成"
                ],
                "good_signals": [
                    "社長や責任者が改善意欲を持っている",
                    "現場で困りごとが言語化されている",
                    "まずは一部から試したい姿勢がある"
                ],
                "avoid_signals": [
                    "成果責任のみ求める",
                    "社内協力が得られない",
                    "現状把握なしで即結果だけ求める"
                ]
            },
            {
                "name": "問い合わせ対応が属人化している会社",
                "typical_companies": "店舗型事業、サロン、スクール、BtoCサービス業",
                "typical_issues": [
                    "担当者によって案内内容が違う",
                    "見込み客の取りこぼしがある",
                    "LINEや電話の流れが整理されていない"
                ],
                "starter_projects": [
                    "問い合わせ導線の棚卸し",
                    "案内文の整備",
                    "見込み客フォローの流れ設計"
                ],
                "good_signals": [
                    "現場の手間を減らしたい意図がある",
                    "改善対象が目に見えている",
                    "小さく始める余地がある"
                ],
                "avoid_signals": [
                    "誰も情報を出せない",
                    "改善範囲が広すぎる",
                    "価格だけで判断される"
                ]
            }
        ]
    },
    "バックオフィス・業務整理支援": {
        "fit": "事務・リサーチ・スプレッドシート・業務整理の経験を活かしやすい方向です。",
        "service": "業務フロー整理、資料整理、マニュアル化、AI活用の下準備",
        "company_profiles": [
            {
                "name": "業務が人依存になっている会社",
                "typical_companies": "少人数の中小企業、家族経営、拡大途中の小規模事業者",
                "typical_issues": [
                    "やり方が人によって違う",
                    "引き継ぎが難しい",
                    "資料やデータの置き場がバラバラ"
                ],
                "starter_projects": [
                    "業務フローの整理",
                    "資料・データの棚卸し",
                    "マニュアルのたたき台作成"
                ],
                "good_signals": [
                    "社内で困っていることが明確",
                    "現場協力が得られそう",
                    "一部業務から始められる"
                ],
                "avoid_signals": [
                    "何を整理したいか曖昧",
                    "現場が全く協力しない",
                    "最初から大規模改善を求める"
                ]
            },
            {
                "name": "管理業務が煩雑な小規模事業者",
                "typical_companies": "店舗複数展開企業、事務スタッフが少ない会社、在庫や顧客管理が混在する事業者",
                "typical_issues": [
                    "同じ入力や確認作業が多い",
                    "ミスや漏れが起きやすい",
                    "業務全体が見えていない"
                ],
                "starter_projects": [
                    "定型業務の洗い出し",
                    "スプレッドシート整理",
                    "AI導入前の下準備支援"
                ],
                "good_signals": [
                    "手間削減のニーズが強い",
                    "現状のやり方が見えている",
                    "まずは一部業務で試せる"
                ],
                "avoid_signals": [
                    "IT拒否が強い",
                    "現状把握がまったくない",
                    "丸投げ前提で役割が曖昧"
                ]
            }
        ]
    },
    "店舗・専門サービス業向け支援": {
        "fit": "医療・介護・美容・ジムなど、現場理解がある人ほど提案が刺さりやすい方向です。",
        "service": "集客導線の整理、顧客フォロー改善、情報発信支援、業務改善補助",
        "company_profiles": [
            {
                "name": "地域密着型の店舗・クリニック・サロン",
                "typical_companies": "整体院、ジム、サロン、歯科・クリニック、小規模教室",
                "typical_issues": [
                    "紹介頼みで新規導線が弱い",
                    "来店後フォローが整っていない",
                    "WebやSNSが更新できていない"
                ],
                "starter_projects": [
                    "顧客フォローの流れ整理",
                    "来店導線の見直し",
                    "発信ネタ・案内導線の整理"
                ],
                "good_signals": [
                    "現場課題が具体的",
                    "改善の必要性を感じている",
                    "小さな施策から試せる"
                ],
                "avoid_signals": [
                    "現場理解を求めるのに情報共有がない",
                    "成果だけ急ぐ",
                    "業務範囲が広すぎる"
                ]
            },
            {
                "name": "専門性は高いが導線が弱い事業者",
                "typical_companies": "技術力はあるが集客や説明が弱い専門職サービス",
                "typical_issues": [
                    "価値がうまく伝わっていない",
                    "案内の順番が整理されていない",
                    "見込み客の離脱が多い"
                ],
                "starter_projects": [
                    "案内順の整理",
                    "よくある質問の整備",
                    "サービス説明の言語化支援"
                ],
                "good_signals": [
                    "強みがはっきりしている",
                    "伝え方に課題がある自覚がある",
                    "改善テーマが絞れている"
                ],
                "avoid_signals": [
                    "何を変えたいか不明確",
                    "全部お任せ前提",
                    "価格だけで依頼先を決める"
                ]
            }
        ]
    }
}

NOT_TO_DO_ITEMS = [
    ("最初から手を広げすぎない", "市場・企業・サービスを同時に広げすぎない"),
    ("単価だけで案件を選ばない", "継続しづらい案件に入るとズレやすい"),
    ("実績づくりを飛ばさない", "最初の信用づくりを省かない"),
    ("発信だけで満足しない", "見せ方だけで終わらず、提案までつなげる"),
    ("学ぶだけで終わらせない", "インプットだけで止まらない"),
    ("自分に合わない市場へ無理に入らない", "向いていない領域は消耗しやすい"),
    ("企業選定を感覚で決めない", "条件を見ずに選ぶとズレやすい"),
    ("提案の順番を自己流で決めない", "順番がズレると成約率が落ちやすい"),
    ("ツール集めだけで止まらない", "環境づくりだけで進んだ気にならない"),
    ("『とりあえず全部やる』をやらない", "優先順位を決めて進める")
]

LOW_SCORE_REASSURANCE = {
    "コンテンツ適性": "文章や発信は、最初から得意でなくても型を使えば補いやすい領域です。",
    "対人・提案適性": "提案は勢いより順番設計の方が重要なので、最初から営業力が高くなくても問題ありません。",
    "整理・運用適性": "整理力はテンプレートや進め方で補いやすく、実務の中で伸ばしやすい部分です。",
    "デジタル適性": "ツール操作は後から覚えやすいので、最初は最低限で十分です。"
}

# =========================
# 共通UI
# =========================
def inject_css():
    st.markdown("""
    <style>
        .app-title {
            font-size: 32px;
            font-weight: 800;
            line-height: 1.3;
            margin-bottom: 8px;
        }
        .app-subtitle {
            font-size: 15px;
            color: #475569;
            margin-bottom: 20px;
        }
        .panel {
            padding: 18px 20px;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            background: #FFFFFF;
            margin-bottom: 16px;
        }
        .panel-soft {
            padding: 18px 20px;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            background: #F8FAFC;
            margin-bottom: 16px;
        }
        .panel-highlight {
            padding: 18px 20px;
            border: 1px solid #DBEAFE;
            border-radius: 16px;
            background: #EFF6FF;
            margin-bottom: 16px;
        }
        .mini-card {
            padding: 14px 16px;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            background: #FFFFFF;
            margin-bottom: 10px;
        }
        .summary-chip {
            display: inline-block;
            padding: 6px 10px;
            margin: 0 8px 8px 0;
            border-radius: 999px;
            background: #EFF6FF;
            border: 1px solid #DBEAFE;
            font-size: 13px;
        }
        .cta-box {
            padding: 22px;
            border: 1px solid #D1D5DB;
            border-radius: 18px;
            background: #FFFFFF;
            text-align: center;
            margin-top: 18px;
        }
        .cta-title {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .cta-sub {
            font-size: 14px;
            color: #6B7280;
            margin-bottom: 16px;
        }
        .cta-button {
            display: inline-block;
            padding: 12px 22px;
            border-radius: 12px;
            background: #111827;
            color: #FFFFFF !important;
            text-decoration: none;
            font-weight: 700;
        }
        .section-label {
            font-size: 13px;
            color: #64748B;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .small-muted {
            font-size: 13px;
            color: #64748B;
        }
    </style>
    """, unsafe_allow_html=True)

def init_state():
    defaults = {
        "job_type": "会社員",
        "available_hours": 5,
        "experience_items": [],
        "priority_type": "今後の不安を減らしたい",
        "market_selected": None,
        "company_selected": None,
        "target_monthly_revenue": 150000,
        "monthly_clients": 2,
        "start_month": 3,
        "course_fee_6": COURSE_FEE_6_DEFAULT,
        "course_fee_10": COURSE_FEE_10_DEFAULT
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_header():
    st.markdown('<div class="app-title">Webste 個別設計ロードマップ</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">自分で判断するとズレやすい「市場選定 × 企業選定 × 順番設計」を、先に整理して見える化するための個別設計デモです。</div>',
        unsafe_allow_html=True
    )

def render_step_intro(step_no, title, what_decides, next_step):
    st.markdown(
        f"""
        <div class="panel-soft">
            <div class="section-label">STEP {step_no}</div>
            <div style="font-size:24px; font-weight:800; margin-bottom:10px;">{title}</div>
            <div style="font-size:14px; margin-bottom:8px;"><strong>この画面で整理すること：</strong>{what_decides}</div>
            <div style="font-size:14px; color:#475569;"><strong>次に見るポイント：</strong>{next_step}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_sidebar(profile):
    with st.sidebar:
        st.markdown("### 表示するステップ")
        current_step = st.radio(
            "step",
            STEP_TITLES,
            label_visibility="collapsed"
        )

        current_index = STEP_TITLES.index(current_step) + 1
        st.progress(current_index / len(STEP_TITLES))
        st.caption(f"{current_index} / {len(STEP_TITLES)}")

        st.markdown("---")
        st.markdown("### 今の仮設計")
        chips = [
            f"現職：{st.session_state.job_type}",
            f"優先度：{st.session_state.priority_type}",
            f"推奨市場：{profile['recommended_market']}",
            f"推奨企業：{profile['recommended_company']}"
        ]
        for chip in chips:
            st.markdown(f'<div class="summary-chip">{chip}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.caption("上の基本情報を変えると、下の各ステップの内容にも自動で反映されます。")

    return current_step

def render_basic_info():
    with st.expander("基本情報（ここを更新すると、下の各ステップに反映されます）", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("現職", JOB_OPTIONS, key="job_type")
            st.number_input(
                "1週間に使える時間（目安）",
                min_value=1,
                max_value=40,
                step=1,
                key="available_hours"
            )

        with col2:
            st.multiselect(
                "経験のあること（仕事・副業・趣味で少しでも触れたことがあれば選択してください）",
                EXPERIENCE_OPTIONS,
                key="experience_items"
            )
            st.radio(
                "今の優先度に近いもの",
                ["収入を増やしたい", "働き方を整えたい", "今後の不安を減らしたい"],
                key="priority_type"
            )

# =========================
# ロジック
# =========================
def compute_profile():
    job = st.session_state.job_type
    experiences = set(st.session_state.experience_items)
    hours = st.session_state.available_hours
    priority = st.session_state.priority_type

    score_content = 20
    score_communication = 20
    score_operations = 20
    score_digital = 20

    if "文章を書く" in experiences:
        score_content += 18
    if "Canvaなどで画像を作る" in experiences:
        score_content += 12
        score_digital += 8
    if "SNS投稿を作る" in experiences:
        score_content += 14
        score_digital += 8
    if "ブログやサイトを触る" in experiences:
        score_content += 12
        score_digital += 12
    if "接客・営業をする" in experiences:
        score_communication += 18
    if "人に説明する" in experiences:
        score_communication += 14
    if "事務作業を進める" in experiences:
        score_operations += 16
    if "リサーチする" in experiences:
        score_operations += 12
        score_digital += 6
    if "Excel / スプレッドシートを使う" in experiences:
        score_operations += 14
        score_digital += 8
    if "AIツールを少し触ったことがある" in experiences:
        score_digital += 16

    if job == "営業職":
        score_communication += 16
    elif job == "事務職":
        score_operations += 14
    elif job == "接客・販売":
        score_communication += 12
    elif job == "医療従事者":
        score_communication += 10
        score_operations += 8
    elif job == "介護・福祉職":
        score_communication += 10
        score_operations += 8
    elif job == "工場勤務":
        score_operations += 12
    elif job == "教育・保育":
        score_communication += 12
    elif job == "美容・サロン":
        score_communication += 12
        score_content += 6
    elif job == "ジム・フィットネス関連":
        score_communication += 12
    elif job == "主婦・主夫":
        score_operations += 8
    elif job == "フリーランス":
        score_content += 6
        score_digital += 6

    if hours >= 10:
        time_label = "週10時間以上を確保しやすく、試行回数を作りやすい状態です。"
    elif hours >= 5:
        time_label = "週5時間前後を確保しながら、無理なく進めやすい状態です。"
    else:
        time_label = "使える時間が限られるため、手を広げず順番設計を先に固める方がズレにくい状態です。"

    scores = {
        "コンテンツ適性": min(score_content, 100),
        "対人・提案適性": min(score_communication, 100),
        "整理・運用適性": min(score_operations, 100),
        "デジタル適性": min(score_digital, 100)
    }

    if job in ["医療従事者", "介護・福祉職", "美容・サロン", "ジム・フィットネス関連"]:
        recommended_market = "店舗・専門サービス業向け支援"
    else:
        score_map = {
            "コンテンツ・Web運用支援": scores["コンテンツ適性"] + scores["デジタル適性"],
            "営業支援・顧客対応改善": scores["対人・提案適性"] + 10,
            "バックオフィス・業務整理支援": scores["整理・運用適性"] + scores["デジタル適性"],
            "店舗・専門サービス業向け支援": scores["対人・提案適性"] + scores["整理・運用適性"]
        }
        recommended_market = max(score_map, key=score_map.get)

    market_profiles = MARKET_PROFILES[recommended_market]["company_profiles"]
    recommended_company = market_profiles[0]["name"]

    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    low_scores = sorted(scores.items(), key=lambda x: x[1])[:2]
    strengths = [top_scores[0][0], top_scores[1][0]]

    base_observation = [
        f"現職と経験から見ると、まずは「{recommended_market}」の方向から入る方が自然です。",
        f"使いやすい強みは「{strengths[0]}」と「{strengths[1]}」です。",
        time_label
    ]

    if priority == "収入を増やしたい":
        base_observation.append("最初から高単価だけを追うより、実績づくり → 継続支援の順で進める方がズレにくいです。")
    elif priority == "働き方を整えたい":
        base_observation.append("短期で広げるより、再現しやすい流れを先に固める方が安定しやすいです。")
    else:
        base_observation.append("不安を減らす目的なら、向いている市場と企業を先に絞る方が遠回りを防ぎやすいです。")

    reassurance = [(label, LOW_SCORE_REASSURANCE[label]) for label, _ in low_scores]

    return {
        "scores": scores,
        "recommended_market": recommended_market,
        "recommended_company": recommended_company,
        "strengths": strengths,
        "base_observation": base_observation,
        "low_scores": low_scores,
        "reassurance": reassurance
    }

def sync_recommendations(profile):
    if st.session_state.market_selected is None:
        st.session_state.market_selected = profile["recommended_market"]

    market = st.session_state.market_selected
    company_options = [c["name"] for c in MARKET_PROFILES[market]["company_profiles"]]

    if st.session_state.company_selected not in company_options:
        if profile["recommended_company"] in company_options:
            st.session_state.company_selected = profile["recommended_company"]
        else:
            st.session_state.company_selected = company_options[0]

def get_market_data():
    return MARKET_PROFILES[st.session_state.market_selected]

def get_company_data():
    company_name = st.session_state.company_selected
    company_profiles = MARKET_PROFILES[st.session_state.market_selected]["company_profiles"]
    for company in company_profiles:
        if company["name"] == company_name:
            return company
    return company_profiles[0]

def get_primary_offer():
    market = st.session_state.market_selected
    if market == "コンテンツ・Web運用支援":
        return "コンテンツ改善・発信支援"
    if market == "営業支援・顧客対応改善":
        return "営業導線・顧客対応改善"
    if market == "バックオフィス・業務整理支援":
        return "業務整理・運用改善"
    return "店舗導線・顧客フォロー支援"

def get_roadmap_plan():
    market = st.session_state.market_selected
    company = get_company_data()
    offer = get_primary_offer()

    starter = " / ".join(company["starter_projects"][:2])

    month_details = {
        "1ヶ月目": f"狙う市場を『{market}』に絞り、提案先として『{company['name']}』のような企業タイプを固定します。まずは広げず、どこを見に行くかを先に決める段階です。",
        "2ヶ月目": f"最初に出す提案を『{offer}』に寄せて整理します。たとえば {starter} のように、入りやすい案件から入口を作る想定です。",
        "3ヶ月目": "実績づくりと提案開始のフェーズです。案件候補を絞り、何を先に見せて、どの順番で提案するかまで固めます。"
    }

    tasks = [
        {"Task": "市場を1つに絞る", "Start": 1.0, "End": 1.7},
        {"Task": "企業タイプを確定する", "Start": 1.2, "End": 2.0},
        {"Task": "最初の案件を整理する", "Start": 1.8, "End": 2.6},
        {"Task": "実績づくりの動線を作る", "Start": 2.2, "End": 3.0},
        {"Task": "提案開始と改善", "Start": 2.7, "End": 3.4},
    ]

    reach_state = [
        "自分に合う市場と企業タイプが絞れている",
        "提案するサービス内容と順番が整理できている",
        "最初に狙う案件候補が見えている",
        "実績づくりの動き方が明確になっている",
        "『何をやるか』より『何をやらないか』が決まっている"
    ]

    return offer, month_details, tasks, reach_state

def build_roadmap_chart(tasks):
    df = pd.DataFrame(tasks)
    chart = alt.Chart(df).mark_bar(size=26).encode(
        x=alt.X(
            "Start:Q",
            title="月",
            scale=alt.Scale(domain=[0.9, 3.6]),
            axis=alt.Axis(values=[1, 2, 3], labelExpr="datum.value + 'ヶ月目'")
        ),
        x2="End:Q",
        y=alt.Y("Task:N", sort=list(reversed(df["Task"].tolist())), title=None),
        tooltip=["Task", "Start", "End"]
    ).properties(height=260)
    return chart

def round_to_5000(value):
    return int(math.ceil(value / 5000) * 5000)

def get_unit_price_from_target(target_monthly_revenue, monthly_clients):
    raw = target_monthly_revenue / max(monthly_clients, 1)
    return round_to_5000(raw)

def build_revenue_df(unit_price, monthly_clients, start_month):
    months = list(range(1, 11))
    sales = []

    for m in months:
        if m < start_month:
            sales.append(0)
        elif m == start_month:
            sales.append(unit_price)
        elif m == start_month + 1:
            sales.append(unit_price * min(2, monthly_clients))
        else:
            sales.append(unit_price * monthly_clients)

    df = pd.DataFrame({"月": months, "月売上": sales})
    df["累計売上"] = df["月売上"].cumsum()
    return df

def build_revenue_chart(df):
    base = alt.Chart(df).encode(
        x=alt.X("月:O", title="月")
    )

    bar = base.mark_bar(opacity=0.75).encode(
        y=alt.Y("月売上:Q", title="月売上（円）"),
        tooltip=["月", "月売上", "累計売上"]
    )

    line = base.mark_line(point=True, strokeWidth=3).encode(
        y=alt.Y("累計売上:Q", title="累計売上（円）"),
        tooltip=["月", "月売上", "累計売上"]
    )

    return alt.layer(bar, line).resolve_scale(y="independent").properties(height=360)

def find_recovery_month(fee, df):
    matched = df[df["累計売上"] >= fee]
    if matched.empty:
        return "10ヶ月以降"
    return f"{int(matched.iloc[0]['月'])}ヶ月目"

def get_revenue_routes():
    market = st.session_state.market_selected

    if market == "コンテンツ・Web運用支援":
        return [
            "既存経験を活かした記事・SNS・Canvaまわりの支援から入る",
            "小さな改善提案を挟みながら、継続支援へつなげる",
            "実績づくり後に、導線改善や設計寄りの提案へ広げる"
        ]
    if market == "営業支援・顧客対応改善":
        return [
            "問い合わせ対応や営業資料整理など、改善しやすい入口から入る",
            "LINE導線や顧客対応フローの見直しへつなげる",
            "継続支援として運用改善や提案設計に広げる"
        ]
    if market == "バックオフィス・業務整理支援":
        return [
            "業務整理・資料整理・マニュアル化など、必要性が高い支援から入る",
            "スプレッドシートや簡易AI活用の下準備につなげる",
            "継続支援として運用改善や仕組み化に広げる"
        ]
    return [
        "現場理解を活かし、店舗や専門サービス業の課題に近い支援から入る",
        "集客導線・顧客フォロー・情報発信の改善につなげる",
        "継続支援として運用改善や導線設計へ広げる"
    ]

# =========================
# 各ステップ描画
# =========================
def render_step_1(profile):
    render_step_intro(
        1,
        "人生棚卸しシート",
        "最初に入力した基本情報をもとに、今の経験・使いやすい強み・優先したい方向を整理します。",
        "次の『市場選定マップ』で、相性のよい方向を見ていきます。"
    )

    st.info(
        "この画面は、向き不向きの判定ではなく『今の状態で使いやすい強みの目安』を見るためのものです。"
        " 点数が低い項目も、最初から全部揃っている必要はありません。順番を決めて補えば十分です。"
    )

    st.markdown("### 今の使いやすさの目安")
    score_cols = st.columns(4)
    for idx, (label, score) in enumerate(profile["scores"].items()):
        with score_cols[idx]:
            st.metric(label, f"{score}点")

    st.markdown("### 今の土台から見えること")
    st.markdown('<div class="panel-highlight">', unsafe_allow_html=True)
    for text in profile["base_observation"]:
        st.markdown(f"- {text}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 使いやすい強み")
    st.markdown(
        f"""
        <div class="panel">
            <span class="summary-chip">{profile['strengths'][0]}</span>
            <span class="summary-chip">{profile['strengths'][1]}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 低い項目があっても大丈夫な理由")
    for label, message in profile["reassurance"]:
        st.markdown(
            f"""
            <div class="mini-card">
                <div style="font-weight:800; margin-bottom:6px;">{label}</div>
                <div class="small-muted">{message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_step_2(profile):
    render_step_intro(
        2,
        "市場選定マップ",
        "どの市場から入るとズレにくいかを整理し、最初に狙う方向を絞ります。",
        "次の『企業選定シート』で、どの企業タイプに当てると自然かを見ます。"
    )

    market_keys = list(MARKET_PROFILES.keys())
    recommended = profile["recommended_market"]
    default_index = market_keys.index(st.session_state.market_selected) if st.session_state.market_selected in market_keys else market_keys.index(recommended)

    selected_market = st.selectbox(
        "最初に狙う市場",
        market_keys,
        index=default_index
    )
    st.session_state.market_selected = selected_market
    sync_recommendations(profile)

    market_info = get_market_data()

    st.markdown("### この市場が合いやすい理由")
    st.markdown(f'<div class="panel">{market_info["fit"]}</div>', unsafe_allow_html=True)

    st.markdown("### この市場で出会いやすい企業と案件イメージ")
    for company in market_info["company_profiles"]:
        issues_html = "".join([f"<li>{i}</li>" for i in company["typical_issues"]])
        projects_html = "".join([f"<li>{p}</li>" for p in company["starter_projects"]])
        st.markdown(
            f"""
            <div class="panel-soft">
                <div style="font-size:18px; font-weight:800; margin-bottom:8px;">{company["name"]}</div>
                <div style="margin-bottom:8px;"><strong>企業例：</strong>{company["typical_companies"]}</div>
                <div style="margin-bottom:8px;"><strong>よくある課題：</strong><ul>{issues_html}</ul></div>
                <div><strong>最初に入りやすい案件例：</strong><ul>{projects_html}</ul></div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_step_3(profile):
    render_step_intro(
        3,
        "企業選定シート",
        "市場の中でも、どの企業タイプから入ると提案が通りやすいかを整理します。",
        "次の『3ヶ月ロードマップ』で、何をどの順番でやるかを固めます。"
    )

    company_options = [c["name"] for c in get_market_data()["company_profiles"]]
    default_company_index = company_options.index(st.session_state.company_selected) if st.session_state.company_selected in company_options else 0

    selected_company = st.selectbox(
        "最初に狙う企業タイプ",
        company_options,
        index=default_company_index
    )
    st.session_state.company_selected = selected_company
    company = get_company_data()

    st.markdown("### この企業タイプから入る理由")
    st.markdown(
        f"""
        <div class="panel">
            今の状態では、<strong>{company["name"]}</strong> のように、課題が見えやすく、改善の入口を作りやすい相手から入る方が自然です。<br><br>
            いきなり難易度の高い案件に行くより、まずは「課題が見えやすい」「意思決定が比較的早い」「小さく始められる」相手から入る方が、実績づくりと提案精度の両方でズレにくくなります。
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 最初に入りやすい案件の選び方")
        good_html = "".join([f"<li>{g}</li>" for g in company["good_signals"]])
        projects_html = "".join([f"<li>{p}</li>" for p in company["starter_projects"]])
        st.markdown(
            f"""
            <div class="panel-soft">
                <div style="font-weight:800; margin-bottom:8px;">見ておきたい条件</div>
                <ul>{good_html}</ul>
                <div style="font-weight:800; margin:12px 0 8px;">最初の案件例</div>
                <ul>{projects_html}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("### 最初に避けたい案件")
        avoid_html = "".join([f"<li>{a}</li>" for a in company["avoid_signals"]])
        st.markdown(
            f"""
            <div class="panel-soft">
                <div style="font-weight:800; margin-bottom:8px;">避けたいサイン</div>
                <ul>{avoid_html}</ul>
                <div class="small-muted">最初から範囲が広すぎる案件や、成果責任だけ重い案件はズレやすくなります。</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_step_4():
    render_step_intro(
        4,
        "3ヶ月ロードマップ",
        "最初の3ヶ月で、何をどの順番で進めるかを整理します。",
        "次の『収益シミュレーション』で、現実的な見通しを見ます。"
    )

    offer, month_details, tasks, reach_state = get_roadmap_plan()

    st.markdown(
        f"""
        <div class="panel-highlight">
            <div style="font-weight:800; margin-bottom:8px;">このロードマップの前提</div>
            <span class="summary-chip">市場：{st.session_state.market_selected}</span>
            <span class="summary-chip">企業：{st.session_state.company_selected}</span>
            <span class="summary-chip">入口提案：{offer}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 3ヶ月後の到達イメージ")
    for item in reach_state:
        st.markdown(f'<div class="mini-card">• {item}</div>', unsafe_allow_html=True)

    st.caption("3ヶ月後には、『誰に・何を・どの順番で提案するか』が言語化され、最初の案件獲得に向けた動き方がはっきりしている状態を目指します。")

    st.markdown("### 月ごとの進め方")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="panel-soft"><strong>1ヶ月目</strong><br><br>{month_details["1ヶ月目"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="panel-soft"><strong>2ヶ月目</strong><br><br>{month_details["2ヶ月目"]}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="panel-soft"><strong>3ヶ月目</strong><br><br>{month_details["3ヶ月目"]}</div>', unsafe_allow_html=True)

    st.markdown("### ロードマップの見える化")
    st.altair_chart(build_roadmap_chart(tasks), use_container_width=True)

def render_step_5():
    render_step_intro(
        5,
        "収益シミュレーション",
        "最初に狙いやすい収益ルートと、現実的な見通しの目安を整理します。",
        "次の『やらないことリスト』で、遠回りしやすい動きを止めます。"
    )

    st.caption("このデモでは、期待値を上げすぎないために、初期表示は『3ヶ月目から売上が立ち始める前提』で計算しています。必要なら詳細設定で変更できます。")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "目標月収の目安（円）",
            min_value=50000,
            max_value=1000000,
            step=10000,
            key="target_monthly_revenue"
        )
    with col2:
        st.slider(
            "月の想定案件数",
            min_value=1,
            max_value=10,
            key="monthly_clients"
        )

    with st.expander("詳細設定", expanded=False):
        st.slider(
            "売上が立ち始める月",
            min_value=1,
            max_value=6,
            key="start_month"
        )

        c1, c2 = st.columns(2)
        with c1:
            st.number_input(
                "6ヶ月サポート費用（円）",
                min_value=100000,
                max_value=3000000,
                step=50000,
                key="course_fee_6"
            )
        with c2:
            st.number_input(
                "10ヶ月サポート費用（円）",
                min_value=100000,
                max_value=3000000,
                step=50000,
                key="course_fee_10"
            )

    unit_price = get_unit_price_from_target(
        st.session_state.target_monthly_revenue,
        st.session_state.monthly_clients
    )

    df = build_revenue_df(
        unit_price=unit_price,
        monthly_clients=st.session_state.monthly_clients,
        start_month=st.session_state.start_month
    )

    recovery_6 = find_recovery_month(st.session_state.course_fee_6, df)
    recovery_10 = find_recovery_month(st.session_state.course_fee_10, df)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("1件あたり目安単価", f"{unit_price:,.0f}円")
    with m2:
        st.metric("目標月収", f"{st.session_state.target_monthly_revenue:,.0f}円")
    with m3:
        st.metric("6ヶ月費用の回収目安", recovery_6)
    with m4:
        st.metric("10ヶ月費用の回収目安", recovery_10)

    st.altair_chart(build_revenue_chart(df), use_container_width=True)

    st.markdown("### あなたが最初に狙いやすい収益ルート")
    st.write(
        "あなたの経験や今の状況をもとに、最初に現実的に狙いやすい収益ルートを整理しています。"
        " 最初から広げすぎず、順番を決めて進める前提です。"
    )
    for route in get_revenue_routes():
        st.markdown(f"- {route}")

    st.markdown("### 6ヶ月 / 10ヶ月の考え方")
    st.write(
        "6ヶ月でも前に進めますが、未経験から始める場合は、途中で市場選定や提案の順番がズレやすくなります。"
        " そのため、仕事や家庭と両立しながら、無理なく実践と修正を重ねるなら10ヶ月の方が現実的です。"
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="panel">
                <div style="font-size:20px; font-weight:800; margin-bottom:8px;">6ヶ月</div>
                <div style="font-size:14px; color:#475569;">
                    ・すでに経験がある人<br>
                    ・短期間で集中して動ける人<br>
                    ・自分で改善しながら進めやすい人
                </div>
                <div style="margin-top:12px;" class="small-muted">
                    ある程度動ける前提がある人向けです。
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="panel-soft">
                <div style="font-size:20px; font-weight:800; margin-bottom:8px;">10ヶ月</div>
                <div style="font-size:14px; color:#475569;">
                    ・未経験から始める人<br>
                    ・仕事や家庭と両立しながら進めたい人<br>
                    ・市場選定や提案の順番で迷いやすい人<br>
                    ・無理に急いで遠回りしたくない人
                </div>
                <div style="margin-top:12px; font-size:13px; font-weight:700;">
                    迷いやすいポイントを途中で修正しながら進めやすい設計です。
                </div>
                <div style="margin-top:10px;" class="small-muted">
                    {TEN_MONTH_SUPPORT_NOTE}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_step_6():
    render_step_intro(
        6,
        "やらないことリスト",
        "遠回りしやすい判断を先に止め、ズレた努力を減らします。",
        "最後の『最終サマリー』で、ここまでの設計をまとめます。"
    )

    for title, desc in NOT_TO_DO_ITEMS:
        st.markdown(
            f"""
            <div class="mini-card">
                <div style="font-weight:800;">{title}</div>
                <div class="small-muted">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_step_7(profile):
    render_step_intro(
        7,
        "最終サマリー",
        "市場選定・企業選定・順番設計の結論を、見える形でまとめます。",
        "この先は、伴走で具体化するかどうかを判断します。"
    )

    offer, month_details, tasks, _ = get_roadmap_plan()
    company = get_company_data()

    unit_price = get_unit_price_from_target(
        st.session_state.target_monthly_revenue,
        st.session_state.monthly_clients
    )
    revenue_df = build_revenue_df(
        unit_price=unit_price,
        monthly_clients=st.session_state.monthly_clients,
        start_month=st.session_state.start_month
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### あなたの現在地")
        st.markdown(
            f"""
            <div class="panel">
                今の経験・使いやすい強み・使える時間を踏まえると、最初は広げすぎず、<strong>{st.session_state.market_selected}</strong> を軸に、
                <strong>{st.session_state.company_selected}</strong> のような相手から入る方がズレにくい状態です。
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 相性のよい方向")
        st.markdown(
            f"""
            - 狙う市場：{st.session_state.market_selected}  
            - 最初に狙う企業タイプ：{st.session_state.company_selected}  
            - 入口になりやすい提案：{offer}  
            - 最初の案件例：{company["starter_projects"][0]} / {company["starter_projects"][1]}  
            - 使いやすい強み：{profile['strengths'][0]} / {profile['strengths'][1]}  
            """
        )

        st.markdown("### 最初の3ヶ月でやること")
        st.markdown(
            """
            - 狙う市場と企業タイプを絞る  
            - 最初に提案するサービス内容を決める  
            - 最初の案件例をもとに実績づくりの動き方を整理する  
            - やらないことを決めて、手を広げすぎない  
            """
        )

        st.markdown("### ここまでの要点")
        st.markdown(
            f"""
            <div class="panel-soft">
                このデモで出しているのは「何でもできる可能性」ではなく、<strong>最初にどこへ行くとズレにくいか</strong>です。<br><br>
                一人で進めるとブレやすいのは、能力不足というより、<strong>市場選定・企業選定・提案の順番</strong>を感覚で決めてしまいやすいからです。<br><br>
                特に未経験から進める場合は、短く急ぐより、<strong>10ヶ月のように途中で修正しながら費用回収を目指せる設計</strong>の方が安心して進めやすくなります。
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown("### ロードマップの見える化")
        st.altair_chart(build_roadmap_chart(tasks), use_container_width=True)

        st.markdown("### 収益イメージ")
        st.altair_chart(build_revenue_chart(revenue_df).properties(height=260), use_container_width=True)

    st.markdown(
        f"""
        <div class="cta-box">
            <div class="cta-title">この設計を、Websteの伴走型サポートで具体化する</div>
            <div class="cta-sub">
                市場選定・企業選定・順番設計を、一人で曖昧に決めずに進めたい方向けです。
            </div>
            <a class="cta-button" href="{CTA_URL}" target="_blank">Websteの伴走型サポートで進める</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# メイン
# =========================
def main():
    inject_css()
    init_state()
    render_header()
    render_basic_info()

    profile = compute_profile()
    sync_recommendations(profile)
    current_step = render_sidebar(profile)

    if current_step == "1. 人生棚卸しシート":
        render_step_1(profile)
    elif current_step == "2. 市場選定マップ":
        render_step_2(profile)
    elif current_step == "3. 企業選定シート":
        render_step_3(profile)
    elif current_step == "4. 3ヶ月ロードマップ":
        render_step_4()
    elif current_step == "5. 収益シミュレーション":
        render_step_5()
    elif current_step == "6. やらないことリスト":
        render_step_6()
    elif current_step == "7. 最終サマリー":
        render_step_7(profile)

if __name__ == "__main__":
    main()
