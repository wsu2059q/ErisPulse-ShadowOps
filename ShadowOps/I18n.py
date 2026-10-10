from ErisPulse.Core.Bases import BaseI18n, I18nKey


class ShadowOpsI18n(BaseI18n):

    enabled: I18nKey = I18nKey(
        default="Enable module",
        zh_CN="是否启用模块",
        zh_TW="是否啟用模組",
        en="Enable module",
        ja="モジュールを有効化",
        ru="Включить модуль",
    )
    diff_max_rows: I18nKey = I18nKey(
        default="Max entries shown in one diff report",
        zh_CN="对比报告单次展示的最大条目数",
        zh_TW="對比報告單次展示的最大條目數",
        en="Max entries shown in one diff report",
        ja="差分レポート1回の最大表示件数",
        ru="Максимум записей в одном отчёте сравнения",
    )
    audit_deep: I18nKey = I18nKey(
        default="Include gc instance census in audit (has global pause cost)",
        zh_CN="审计时附带 gc 实例普查（有全局暂停开销）",
        zh_TW="審計時附帶 gc 實例普查（有全域暫停開銷）",
        en="Include gc instance census in audit (has global pause cost)",
        ja="監査に gc インスタンス調査を含める（グローバル一時停止あり）",
        ru="Включать обзор gc-экземпляров в аудит (глобальные паузы)",
    )
    render_card: I18nKey = I18nKey(
        default="Render reports as image cards via Takumi (fallback to text)",
        zh_CN="报告用 Takumi 渲染为卡片（不可用时降级文本）",
        zh_TW="報告用 Takumi 渲染為卡片（不可用時降級文本）",
        en="Render reports as image cards via Takumi (fallback to text)",
        ja="レポートを Takumi でカード画像化（不可時はテキスト）",
        ru="Рендер отчётов в карточки через Takumi (иначе текст)",
    )
    theme: I18nKey = I18nKey(
        default="Card style (doodle/editorial)",
        zh_CN="卡片风格 (doodle 手绘涂鸦风 / editorial 编辑杂志风)",
        zh_TW="卡片風格 (doodle 手繪塗鴉風 / editorial 編輯雜誌風)",
        en="Card style (doodle/editorial)",
        ja="カードスタイル（doodle/editorial）",
        ru="Стиль карточек (doodle/editorial)",
    )
    module_loaded: I18nKey = I18nKey(
        default="ShadowOps loaded: {event}",
        zh_CN="影子灰度管理已加载: {event}",
        zh_TW="影子灰度管理已載入: {event}",
        en="ShadowOps loaded: {event}",
        ja="ShadowOps を読み込みました: {event}",
        ru="ShadowOps загружен: {event}",
    )
    module_unloaded: I18nKey = I18nKey(
        default="ShadowOps unloaded: {event}",
        zh_CN="影子灰度管理已卸载: {event}",
        zh_TW="影子灰度管理已卸載: {event}",
        en="ShadowOps unloaded: {event}",
        ja="ShadowOps を解除しました: {event}",
        ru="ShadowOps выгружен: {event}",
    )
    started: I18nKey = I18nKey(
        default="Shadow started: {owner} (shadowing {name})",
        zh_CN="影子已启动: {owner}（对照模块 {name}）",
        zh_TW="影子已啟動: {owner}（對照模組 {name}）",
        en="Shadow started: {owner} (shadowing {name})",
        ja="シャドーを開始しました: {owner}（対象 {name}）",
        ru="Тень запущена: {owner} (для {name})",
    )
    promoted: I18nKey = I18nKey(
        default="Shadow promoted: {name}",
        zh_CN="影子已转正: {name}",
        zh_TW="影子已轉正: {name}",
        en="Shadow promoted: {name}",
        ja="シャドーを本番化しました: {name}",
        ru="Тень повышена: {name}",
    )
    dismissed: I18nKey = I18nKey(
        default="Shadow dismissed: {name}",
        zh_CN="影子已放弃: {name}",
        zh_TW="影子已放棄: {name}",
        en="Shadow dismissed: {name}",
        ja="シャドーを破棄しました: {name}",
        ru="Тень отклонена: {name}",
    )
    list_empty: I18nKey = I18nKey(
        default="No active shadows",
        zh_CN="当前没有运行中的影子",
        zh_TW="當前沒有運行中的影子",
        en="No active shadows",
        ja="実行中のシャドーはありません",
        ru="Нет активных теней",
    )
    list_header: I18nKey = I18nKey(
        default="Active shadows ({count}):",
        zh_CN="运行中的影子（{count} 个）：",
        zh_TW="運行中的影子（{count} 個）：",
        en="Active shadows ({count}):",
        ja="実行中のシャドー（{count} 件）：",
        ru="Активные тени ({count}):",
    )
    diff_no_shadow: I18nKey = I18nKey(
        default="Module {name} has no active shadow",
        zh_CN="模块 {name} 没有运行中的影子",
        zh_TW="模組 {name} 沒有運行中的影子",
        en="Module {name} has no active shadow",
        ja="モジュール {name} に実行中のシャドーはありません",
        ru="У модуля {name} нет активной тени",
    )
    diff_empty: I18nKey = I18nKey(
        default="Shadow has no outbound entries yet",
        zh_CN="影子还没有意向出站记录",
        zh_TW="影子還沒有意向出站記錄",
        en="Shadow has no outbound entries yet",
        ja="シャドーの出站記録はまだありません",
        ru="У тени пока нет записей исходящих",
    )
    promote_need_confirm: I18nKey = I18nKey(
        default="Promote will unload {name} and switch to the shadow version; retry with: /shadow promote {name} yes",
        zh_CN="转正会卸载 {name} 并切换到影子版本；确认请输入: /shadow promote {name} yes",
        zh_TW="轉正會卸載 {name} 並切換到影子版本；確認請輸入: /shadow promote {name} yes",
        en="Promote will unload {name} and switch to the shadow version; retry with: /shadow promote {name} yes",
        ja="本番化は {name} をアンロードしてシャドー版に切替えます。確認するには: /shadow promote {name} yes",
        ru="Повышение выгрузит {name} и переключит на версию-тень; подтвердите: /shadow promote {name} yes",
    )
