---
name: k-shoreline-ui
description: >-
  Applies the "汀線" (K案, shoreline) visual design to a web UI — pale green planes that show which things belong together, and a curved shoreline that shows where one area meets the next: a selected row whose pale green continues into the detail area (a right-hand column reserved in advance on wide screens, directly under the row on narrow ones), form chapters split into a green "land" (chapter name) and a "water" side (inputs) by a curve, Mincho titles, and — only where the app already has trends — measured points with a monotone guide curve. Use only when the user asks for 汀線, K案 or k-shoreline by name for a new or existing screen. Do not use for generic sea or beach themes, green color schemes, other design styles (糸の交点, 折本, 二色刷り), or unrelated coding.
license: MIT
compatibility: Plain HTML/CSS (optionally JS and inline SVG). Works offline; no CDN, web font or external API is required.
metadata:
  source: "YanTKYS/design-lab k-shoreline (12th comparison design, K案)"
  version: "0.2.0"
---

# 汀線（K案）UI を適用する

水際の汀線に**着想した独自のデザイン**（名称は仮称）を、Web 画面に適用する。実在の地図・海図・地形の再現や、公式のデザインシステムではない。依頼者や画面にもそう説明しない。

核は**「淡い緑の面で関連を示し、曲線で領域のつながりと境目を見せる」**こと。緑の配色に塗り替えるだけでは汀線にならない。選んだ1件と詳細、章名と入力欄、という**対になる2つの領域**を、同じ面の色と1本の曲線で結ぶ・分ける。面の色は弱い手がかりなので、選択・状態・エラーは必ず文字・記号・線でも示す。

## 使う場面

- 「汀線」「K案」「k-shoreline」の見た目を、名前を挙げて指定された依頼。
- 一覧から1件を選んで詳細を読む画面、章ごとに入力する画面、既に推移の集計がある画面。
- 既に日付やカテゴリなどのまとまりに分かれた閲覧の一覧（見出しとその下の記録・カード）。

使わない場面：このデザインの指定がない作業、海辺・水辺一般のテーマ、緑系の配色変更、ほかのデザインの適用、見た目と無関係な修正。

## 手順

1. **対象を確認する。** 技術スタック、既存の CSS、画面の目的と主要操作、一覧の件数と列、詳細の置き場所、入力の検証と保存、IME で入力する欄、画面遷移、キーボード操作（矢印キー・Tab）と、絞り込み・並べ替え・開閉・エラー後のフォーカス。動作・データ・保存・URL・ルーティングは変えない。
   - 既存のアプリに試すときは、依頼がない限り**現行のデザインを標準のまま残し**、この Skill を選べる追加のテーマとして入れる（明示的に置き換えを頼まれた場合や新しいアプリは別）。テーマを切り替える仕組みが既になく、切替の UI も頼まれていないなら、勝手に作らず依頼者に確かめる。切替を頼まれたら、標準を初期値にし、選んだテーマの保存・既存の明暗の配色モード・データ・主要操作・URL を保ち、テーマの CSS の範囲を分ける。
   - Skill のコードや素材（`tokens.css` など）を取り込むときは、MIT の著作権表示と許諾文の全文（この Skill の `LICENSE`）を、アプリの配布物にも残す（1つの HTML ならコメント、静的サイトなら配布するファイルなど）。アプリ全体のライセンスは変えない。
2. **規則と部品を選ぶ。** [references/design-principles.md](references/design-principles.md) の判断表で、対象の業務にある部品だけを選ぶ（選んだ行と続く詳細・章の陸と水際・推移の曲線・まとまりの見出しと中身）。**業務にない KPI・グラフ・右の詳細の列は足さない。**
3. **トークンと装飾を入れる。** [assets/tokens.css](assets/tokens.css) を取り込む（コピーしてよい）。表題の装飾が合う画面なら [assets/k-shore.svg](assets/k-shore.svg) を背景に使う（読み上げない）。既存の変数・クラスと衝突するなら、接頭辞を変えるか画面のルート要素に範囲を限る。
   - `tokens.css` は `:root` に変数を定義している。そのまま全体に読み込むと、アプリのほかの画面にも効く。適用する画面のルート要素に範囲を移すか、必要な変数だけを取り込む。
   - React・Vue・Tailwind CSS・CSS Modules などを使うアプリでは、既存のコンポーネントとスタイルの管理方式を保つ。トークンは既存の仕組み（テーマの設定・CSS 変数・モジュールの CSS など）に取り込み、Skill のクラス名や HTML の例をそのまま移したり、既存のスタイルやコンポーネントを全面的に置き換えたりしない。既存のラベル・`aria-*`・入力検証は消さない。
4. **型に当てはめる。** [references/patterns.md](references/patterns.md) の最小例を、対象のマークアップ・命名・フレームワークで書き直す。動作は対象アプリの仕組みを使う。
5. **点検する**（下記）。直したら 1280px 前後・中間の幅（1000px 前後）・375px でもう一度確かめる。

## 自己点検

- [ ] 淡い緑の面が「関連」を示している（選んだ行と詳細、章名と入力欄、集計の区画）。面を飾りとして画面中に塗っていない。
- [ ] 選んだ行は、面の色に加えて、濃い緑の線と文字（「表示中」・開閉ボタンの「閉じる」と `aria-expanded`）で分かる。強制カラーで面と影が消えても枠が残る。
- [ ] 詳細は、DOM と Tab の順で**選んだ行の直後**。広い幅で右の列に見せる場合は、開く前から列を確保していて、開いた瞬間に表の幅が変わらない。中間の幅・狭い幅では行の直下に開く。
- [ ] 汀線の曲線（SVG・背景）は `aria-hidden` の装飾で、文字・入力欄・操作・フォーカスの枠に重ならない。曲線だけで選択・検証・状態を示していない。曲線の場所が取れない・重なるときは省き、そのために付けた余白・背景も同じ条件で外している。
- [ ] まとまりに分かれた閲覧の一覧では、見出し（陸）とそこに属する内容（海）を面でつなぎ、新しい詳細の列・指標・グラフ・フォームを足していない。既存のタブ・二択は元の部品と `aria-selected`・`aria-pressed` のまま、陸の面＋濃い緑の下線（または枠）＋太字で示している。
- [ ] 推移の曲線を使う場合、点・縦の線・件数の文字が実測、曲線と面は目安で、そう書いてある。補間は単調（山・谷を作らない）、0件は基準線。数値は文字で1回だけ読ませる。
- [ ] フォーカスは濃い緑の外枠と淡い外光で、選択の面と別に見える。プログラムで移したフォーカスにも出る。
- [ ] エラーは具体的な文言と欄の太い枠、件数と項目名の一覧（項目名から欄へ移れる）。色だけに頼らない。
- [ ] 入力欄の枠と補助文字が地の色から読める（目安：文字 4.5:1、部品の枠 3:1）。
- [ ] 狭い幅（目安 760px 未満）で、表は行ごとに縦へ積み、並べ替えは1組だけ（並べ替えできない列の見出しは札にしない）。章名は上、入力欄は下。ページ全体が横にはみ出さない。
- [ ] キーボードだけで主要操作ができる。絞り込み・並べ替え・開閉・登録の後も、フォーカスが操作した部品か自然な移動先に残る（描き直しで操作中の部品を作り直していない）。
- [ ] IME の変換中に検索・入力が勝手に確定・再描画されない。
- [ ] 外部のフォント・画像・CDN・API を追加していない。

## 報告するときの注意

- 参照したファイル（この SKILL.md、references、assets）と、対象に合わせて変えた点・使わなかった部品とその理由を書く。Skill の部品をすべて入れることより、アプリの目的・読みやすさ・操作のしやすさを優先し、既存の機能にない部品は足さない。
- 確かめていないこと（スクリーンリーダー、実機の IME、別ブラウザ、実際の OS の強制カラー、色覚の違い）は「未確認」と書く。
- 落ち着き・業務効率・アクセシビリティ基準への適合を、確かめずに断定しない。
