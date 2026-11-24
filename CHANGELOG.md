# 変更履歴

配布版ごとの、利用者に関係する変更をまとめます。新しい版が上です。版の付け方は README の「[版（バージョン）](README.md#版バージョン)」を、詳しい議論と確認の記録は各 Issue・プルリクエストを見てください。

## [Unreleased]

### Added

- 5つの Skill すべてに、別のセッションによる独立した適用の実績（README の「検証の状況」）。[since PR #9](https://github.com/YanTKYS/since/pull/9)（折本）、[devlog PR #32](https://github.com/YanTKYS/devlog/pull/32)（汀線）、[clock PR #35](https://github.com/YanTKYS/clock/pull/35)（標示盤）を追加。
- 5つの `SKILL.md` に共通の進め方：既存のアプリには現行のデザインを標準のまま残し、選べる追加のテーマとして試す（依頼のない切替の UI は作らない）。Skill のコード・素材を取り込むときは MIT の著作権表示と許諾文をアプリの配布物にも残す。使わなかった部品とその理由を報告する。
- 汀線（`k-shoreline-ui`）：まとまりに分かれた閲覧の一覧（見出しを陸、内容を海）と、既存のタブ・二択の選択の表し方（`patterns.md` の 10）。

### Changed

- 標示盤（`l-signage-ui`）：ドット文字を任意にした。時計・タイマーなど数値そのものを読ませる主な表示や頻繁に変わる値には普通の数字を使い、同じ数値を二重に見せない。主な数値を一律に琥珀にしない。
- 折本（`h-prime-ui`）：数値を比べる面で、主な数値と共通の操作の位置をそろえる。`clip-path` の傾きでフォーカスの枠が切れないよう、余白を取って Tab で確かめる。中間の幅の読む順を明確にした。
- 汀線（`k-shoreline-ui`）：曲線を省くときは、そのための余白・背景も外す。CSS 変数は定義してから使う。
- 4つの Skill の `design-principles.md` の「原本から変えた値」を、今の値とその根拠（コントラスト）の表にした。

## [0.1.0] - 2026-11-23

初回の配布版。

### Added

- 5つの Skill：糸の交点（`okinawa-thread-ui`）、折本（`h-prime-ui`）、二色刷り（`j-risograph-ui`）、汀線（`k-shoreline-ui`）、標示盤（`l-signage-ui`）。
- MIT License。リポジトリ直下と各 Skill のフォルダーに `LICENSE`、`SKILL.md` に `license: MIT`。
- 配布内容の検査（`scripts/validate-skills.py`、GitHub Actions）：YAML の frontmatter、参照ファイル、README の掲載、`LICENSE` の一致。
- README：Claude Code・Codex への導入（Bash・PowerShell）と更新のしかた、適用の実績、版の付け方。全 Skill の `metadata.version` を `0.1.0` にそろえた。

### Fixed

- UI の例の不具合：表示の重なり（汀線の右の列）、コントラスト（折本の「詳細を閉じる」、標示盤の並べ替えの矢印）、入力欄（必須の `required`、糸の交点の幅とテーマの範囲）、汀線のグラフ（0期間・1期間）。

[Unreleased]: https://github.com/YanTKYS/design-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YanTKYS/design-skills/releases/tag/v0.1.0
