from typing import Any

from ErisPulse import i18n


def _shadow_manager():
    from ErisPulse.Core.shadow import shadow_manager

    return shadow_manager


class ShadowOpsService:

    def __init__(self, sdk, logger):
        self.sdk = sdk
        self.logger = logger

    def list_shadows(self) -> list[dict[str, str]]:
        items: list[dict[str, str]] = []
        try:
            shadows = getattr(_shadow_manager(), "_shadows", {}) or {}
        except Exception:
            shadows = {}
        for real_name, info in sorted(shadows.items()):
            items.append({
                "real_name": real_name,
                "shadow_owner": info.get("shadow_owner", ""),
            })
        return items

    def format_list_text(self) -> str:
        items = self.list_shadows()
        if not items:
            return i18n.t("ShadowOps.list_empty")
        lines = [i18n.t("ShadowOps.list_header", count=len(items))]
        for item in items:
            lines.append(f"{item['real_name']} -> {item['shadow_owner']}")
        return "\n".join(lines)

    def list_card_html(self, viz) -> str:
        import datetime

        items = self.list_shadows()
        if items:
            rows = "".join(
                viz.count_row(item["real_name"], "", f"shadow owner: {item['shadow_owner']}")
                for item in items
            )
            body = rows
            subtitle = f"共 {len(items)} 个影子在运行"
        else:
            body = "<div class='empty'>当前没有运行中的影子</div>"
            subtitle = "共 0 个影子"
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            viz.head("影子模块", subtitle)
            + f"<div class='body'>{body}</div>"
            + viz.foot(f"ShadowOps · {stamp}", "shadow_start / diff / promote / dismiss")
        )

    def diff(self, name: str) -> dict[str, Any]:
        return self.sdk.module.shadow_diff(name)

    @staticmethod
    def _entry_line(entry: dict) -> str:
        kind = entry.get("kind", "?")
        platform = entry.get("platform", "")
        method = entry.get("method", "")
        target = entry.get("target", "")
        preview = str(entry.get("preview", "") or "")
        return f"[{kind}] {platform}.{method} -> {target} {preview}".rstrip()

    def format_diff_text(self, name: str, report: dict, max_rows: int) -> str:
        if not report.get("shadow_owner"):
            return i18n.t("ShadowOps.diff_no_shadow", name=name)
        aligned = report.get("aligned") or []
        if not aligned:
            return i18n.t("ShadowOps.diff_empty")
        lines = [f"影子 {report['shadow_owner']} · 在账 {report.get('count', len(aligned))} 条"]
        for item in aligned[:max_rows]:
            shadow = item.get("shadow") or {}
            actual = item.get("actual") or []
            lines.append(self._entry_line(shadow))
            lines.append(f"  实际发送: {len(actual)} 条 (trace={shadow.get('trace_id', '-')[:8]})")
        hidden = len(aligned) - max_rows
        if hidden > 0:
            lines.append(f"…其余 {hidden} 条已省略")
        return "\n".join(lines)

    def diff_card_html(self, name: str, report: dict, max_rows: int, viz) -> str:
        import datetime

        if not report.get("shadow_owner"):
            return (
                viz.head("行为对比", f"模块 {name}")
                + "<div class='body'><div class='empty'>没有运行中的影子</div></div>"
                + viz.foot("ShadowOps", "shadow_start")
            )
        aligned = report.get("aligned") or []
        if not aligned:
            body = "<div class='empty'>影子还没有意向出站记录</div>"
        else:
            matched = sum(1 for item in aligned if item.get("actual"))
            rows = []
            for item in aligned[:max(1, max_rows)]:
                shadow = item.get("shadow") or {}
                actual = item.get("actual") or []
                line = self._entry_line(shadow)
                chips = viz.chips([
                    f"trace {str(shadow.get('trace_id', ''))[:12]}",
                    f"实际发送 {len(actual)} 条",
                ])
                rows.append(viz.count_row(
                    shadow.get("kind", "?"), "✓" if actual else "✗", line, chips,
                ))
            body = "".join(rows)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            viz.head("行为对比", f"模块 {name} · 影子 {report['shadow_owner']} · 在账 {report.get('count', 0)} 条")
            + f"<div class='body'>{body}</div>"
            + viz.foot(f"ShadowOps · {stamp}", f"展示上限 {max(1, max_rows)}")
        )

    async def start(self, name: str, source: str) -> str:
        return await self.sdk.module.shadow_start(name, source=source)

    async def promote(self, name: str) -> bool:
        return await self.sdk.module.promote_shadow(name)

    async def dismiss(self, name: str) -> bool:
        return await self.sdk.module.dismiss_shadow(name)

    def audit(self, name: str, deep: bool = False) -> dict[str, Any]:
        return self.sdk.module.audit(name, deep=deep)

    @staticmethod
    def format_audit_text(name: str, report: dict) -> str:
        lines = [f"归属审计: {name}"]
        counts = report.get("counts") or {}
        rendered = " ".join(f"{k}={v}" for k, v in sorted(counts.items()))
        lines.append(f"counts: {rendered or '-'}")
        orphans = report.get("orphans")
        if orphans:
            lines.append(f"orphans: {orphans}")
        recyclable = report.get("instance_recyclable")
        if recyclable is not None:
            lines.append(f"instance_recyclable: {recyclable}")
        return "\n".join(lines)

    def audit_card_html(self, name: str, report: dict, viz) -> str:
        import datetime

        counts = sorted((report.get("counts") or {}).items())
        body = viz.kv_section("归属资源计数", counts or [("-", "0")])
        orphans = report.get("orphans")
        if orphans:
            body += viz.kv_section("孤儿 owner", [(str(o), "") for o in orphans])
        recyclable = report.get("instance_recyclable")
        if recyclable is not None:
            body += viz.kv_section("实例可回收", [("instance_recyclable", str(recyclable))])
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            viz.head("归属权审计", f"模块 {name}")
            + f"<div class='body'>{body}</div>"
            + viz.foot(f"ShadowOps · {stamp}", "module.audit")
        )
