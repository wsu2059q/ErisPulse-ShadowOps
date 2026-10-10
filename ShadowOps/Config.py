from dataclasses import dataclass, field

from ErisPulse.Core.Bases import BaseConfig


@dataclass
class ShadowOpsConfig(BaseConfig):

    enabled: bool = field(
        default=True,
        metadata={
            "description": {"i18n": "ShadowOps.enabled", "default": "是否启用模块"},
            "ui": {"widget": "switch", "group": "basic", "order": 1},
        },
    )
    diff_max_rows: int = field(
        default=10,
        metadata={
            "description": {"i18n": "ShadowOps.diff_max_rows", "default": "对比报告单次展示的最大条目数"},
            "ui": {"widget": "number", "group": "report", "order": 2},
        },
    )
    audit_deep: bool = field(
        default=False,
        metadata={
            "description": {"i18n": "ShadowOps.audit_deep", "default": "审计时附带 gc 实例普查（有全局暂停开销）"},
            "ui": {"widget": "switch", "group": "report", "order": 3},
        },
    )
    render_card: bool = field(
        default=True,
        metadata={
            "description": {"i18n": "ShadowOps.render_card", "default": "报告用 Takumi 渲染为卡片（不可用时降级文本）"},
            "ui": {"widget": "switch", "group": "render", "order": 4},
        },
    )
    theme: str = field(
        default="doodle",
        metadata={
            "description": {"i18n": "ShadowOps.theme", "default": "卡片风格 (doodle/editorial)"},
            "ui": {
                "widget": "select",
                "options": ["doodle", "editorial"],
                "group": "render",
                "order": 5,
            },
        },
    )
