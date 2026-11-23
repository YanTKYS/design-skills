# design-skills

AI エージェント（Claude Code、Codex など）に、独自デザインを別の Web アプリへ適用させるための Agent Skill を配布するリポジトリです。形式は [Agent Skills の仕様](https://agentskills.io/specification)（`SKILL.md` と任意の `references/`・`assets/`）に合わせています。

## このリポジトリと design-lab の役割

| リポジトリ | 役割 |
| --- | --- |
| **design-skills**（ここ） | 配布する Skill の**正本**。Skill の更新はここで行う |
| [design-lab](https://github.com/YanTKYS/design-lab) | 13デザインの調査・比較サイト（[公開ページ](https://yantkys.github.io/design-lab/)）と、Skill を作ったときの固定の適用見本・検証記録の正本 |

Skill は design-lab の [skills/](https://github.com/YanTKYS/design-lab/tree/main/skills) から移行しました（移行元のコミットは移行の PR に記載）。

## Skill の一覧

5つの Skill は、**依頼の中でデザインの名前を指定したときだけ**使う想定です。「ダークな UI に」「緑系の UI に」「印刷物風に」のような一般的な依頼では使いません（各 `SKILL.md` の `description` で使う場面を分けています）。

| Skill | デザイン（いずれも仮称） | 内容 | 依頼での呼び方の例 |
| --- | --- | --- | --- |
| [okinawa-thread-ui](skills/okinawa-thread-ui/SKILL.md) | 糸の交点 | 宮古上布に着想した独自の沖縄テーマ。濃藍の地、本文左の格子帯、章の二重罫、「章｜項目名｜値」の軸 | 「糸の交点で」「沖縄テーマ（糸の交点）で」 |
| [h-prime-ui](skills/h-prime-ui/SKILL.md) | 折本（H′案） | 生成りと葡萄色、右から左へ読む縦組みの面、右頁→左頁の見開きのフォーム、狭い幅では横組みへ | 「折本で」「H′で」 |
| [j-risograph-ui](skills/j-risograph-ui/SKILL.md) | 二色刷り（J案） | 生成りの紙に青の版（文字・罫・操作）と蛍光ピンクの版（版ずれ・網点・影の飾りと選択の地）、点線罫の表、青の反転札と二重罫のエラー | 「二色刷りで」「J案で」 |
| [k-shoreline-ui](skills/k-shoreline-ui/SKILL.md) | 汀線（K案） | 淡い緑の面で関連を示し、曲線で領域のつながりと境目を見せる。選んだ行から続く詳細、章名の陸と入力欄の水際 | 「汀線で」「K案で」 |
| [l-signage-ui](skills/l-signage-ui/SKILL.md) | 標示盤（L案） | 暗い盤面を区画に分け、今の状態だけを琥珀で点灯させる。状態の盤面、5×7 のドット文字（装飾。数値は文字でも1回）、1目盛り＝1件 | 「標示盤で」「L案で」 |

依頼の例：

```text
この画面（src/pages/memo.html）を「糸の交点」の見た目に改修してください。
保存・検証の処理は変えないでください。375px と 1280px で崩れないか確認してください。
```

```text
窓口の呼び出し画面（src/counter/）を「標示盤」（L案）の見た目にしてください。
呼び出し・保存・権限は変えないでください。琥珀は呼び出し中の窓口と選んだ状態だけにし、
ドット文字の件数と読み上げる文字の件数が同じか、強制カラーでも選択が分かるか確認してください。
```

## 導入する

Skill は**使うアプリのリポジトリ（またはユーザーの設定フォルダー）にコピーしたときだけ**読み込まれます。このリポジトリが GitHub にあるだけでは、エージェントがほかのリポジトリの作業で自動的に使うことはありません。

使う Skill のフォルダーを、`references/` と `assets/` を含めて**丸ごと**コピーします（シンボリックリンクは不要です。Windows でもエクスプローラーでのコピーで足ります）。

| エージェント | 対象のリポジトリだけで使う | 自分の全リポジトリで使う |
| --- | --- | --- |
| Claude Code | `<アプリのリポジトリ>/.claude/skills/<Skill 名>/` | `~/.claude/skills/<Skill 名>/` |
| Codex | `<アプリのリポジトリ>/.agents/skills/<Skill 名>/` | `~/.agents/skills/<Skill 名>/` |

コマンドでコピーする場合（アプリのリポジトリの直下で。`<design-skills>` はこのリポジトリを置いた場所、`h-prime-ui` は使う Skill 名に読み替え）：

```bash
mkdir -p .claude/skills && cp -R <design-skills>/skills/h-prime-ui .claude/skills/
```

```bash
mkdir -p .agents/skills && cp -R <design-skills>/skills/h-prime-ui .agents/skills/
```

コピー後の構成（例）：

```text
.claude/skills/h-prime-ui/     （Codex は .agents/skills/h-prime-ui/）
├── SKILL.md
├── references/
│   ├── design-principles.md
│   └── patterns.md
└── assets/
    └── tokens.css
```

各 Skill の `assets/` に入っているもの：

| Skill | assets |
| --- | --- |
| okinawa-thread-ui | `tokens.css`、`thread-pattern.svg`（見出しの模様） |
| h-prime-ui | `tokens.css` |
| j-risograph-ui | `tokens.css` |
| k-shoreline-ui | `tokens.css`、`k-shore.svg`（表題の等高線） |
| l-signage-ui | `tokens.css`、`dot-digits.js`（5×7 のドット文字を描く小さな関数） |

Skill を更新したときは、コピー先も同じフォルダーで上書きします。コピーした側で値を変えた場合は、どちらを正とするかを対象リポジトリの設計メモなどに書いておきます。

## 検証の状況

### 確かめたこと

- **Agent Skills の形式**：5つの `SKILL.md` の frontmatter（`name` とフォルダー名の一致、`name` の文字種、`description` の長さ）、`references/`・`assets/` への相対リンク、参照しているアセットの存在。各フォルダーを単独でコピーしても、リンクとアセットが切れないこと。
- **独立したセッションでの適用（糸の交点のみ）**：`okinawa-thread-ui` は、別の Codex のセッションが Skill だけをデザインの資料として、2つのアプリに適用しました（markdown-library の PR #11、okinawa-watch の PR #12。どちらもマージ済み）。
- **Skill を書いた本人による適用見本（5つとも）**：Skill を書いた同じ作業の中で、比較サイトにない別の業務に当てはめた見本です。作り手が原本の実装を知っているため、**独立した適用の評価ではありません**。見本と検証記録は design-lab にあります。

| Skill | 見本（design-lab） | 検証記録 |
| --- | --- | --- |
| okinawa-thread-ui | 業務メモ | [VERIFICATION.md](https://github.com/YanTKYS/design-lab/blob/main/examples/okinawa-thread-memo/VERIFICATION.md) |
| h-prime-ui | 部屋の予約台帳 | [VERIFICATION.md](https://github.com/YanTKYS/design-lab/blob/main/examples/h-prime-room-booking/VERIFICATION.md) |
| j-risograph-ui | 備品の貸出台帳 | [VERIFICATION.md](https://github.com/YanTKYS/design-lab/blob/main/examples/j-risograph-equipment-lending/VERIFICATION.md) |
| k-shoreline-ui | 照会の進捗 | [VERIFICATION.md](https://github.com/YanTKYS/design-lab/blob/main/examples/k-shoreline-inquiry-tracker/VERIFICATION.md) |
| l-signage-ui | 窓口の呼び出し | [VERIFICATION.md](https://github.com/YanTKYS/design-lab/blob/main/examples/l-signage-counter-queue/VERIFICATION.md) |

デザインの元になった画面は、design-lab の[比較サイト](https://yantkys.github.io/design-lab/)で見比べられます。

### まだ確かめていないこと

- `h-prime-ui`・`j-risograph-ui`・`k-shoreline-ui`・`l-signage-ui` を、別のセッションに Skill だけを渡して適用させたときの再現性。
- Claude Code・Codex で、セッションの開始時に Skill が自動で認識され、依頼に応じて選ばれること。
- スクリーンリーダー、実機の IME、Chromium 以外のブラウザ、実際の OS の強制カラーなど、実機での確認。

## 注意

- 5つはいずれも design-lab で作った**独自のデザイン**（名称は仮称）です。公式のデザインシステム、伝統工芸・実在の印刷物・地図・表示器の再現ではありません。
- Skill に入っているのは、色・書体・罫のトークンと規則、最小の例、小さな自作の素材だけです。design-lab の比較サイトの CSS・HTML・JavaScript は含まず、対象アプリの仕組みに合わせて書く前提です。
- 模様・等高線・ドット文字の字形は、第三者の素材を含まない自作のものです。
- **再配布の条件は未定**です。このリポジトリには LICENSE ファイルがありません。組織の外へ再配布するときや、商用で使うときの条件は、リポジトリの所有者に確認してください。販売やマーケットプレイスへの掲載は想定していません。
