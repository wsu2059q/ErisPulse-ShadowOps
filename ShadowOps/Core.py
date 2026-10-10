from ErisPulse import i18n, sdk
from ErisPulse.Core.Bases import BaseModule, ModuleMeta
from ErisPulse.Core.Event import command
from ErisPulse.loaders import ModuleLoadStrategy

from .Config import ShadowOpsConfig
from .I18n import ShadowOpsI18n
from .Service import ShadowOpsService
from .Visualizer import CardVisualizer


class Main(BaseModule):

    ConfigClass = ShadowOpsConfig
    I18nClass = ShadowOpsI18n

    def __init__(self):
        self.sdk = sdk
        self.logger = sdk.logger.get_child("ShadowOps")
        self._service = ShadowOpsService(sdk, self.logger)
        self._viz = CardVisualizer(sdk, self.logger)

    @staticmethod
    def get_load_strategy() -> ModuleLoadStrategy:
        return ModuleLoadStrategy(lazy_load=False, priority=20)

    @staticmethod
    def get_meta() -> ModuleMeta:
        return ModuleMeta(
            name="ShadowOps",
            description="影子灰度管理模块：启动/对比/转正/放弃影子模块，附归属权审计",
            version="0.1.2",
            author="ErisPulse-devs",
            group="运维",
            tags=["影子模块", "灰度", "热更新", "审计"],
            min_sdk_version="2.9.0",
        )

    async def on_load(self, event: dict) -> bool:
        self._register_commands()
        self.logger.info(i18n.t("ShadowOps.module_loaded", event=event))
        return True

    async def on_unload(self, event: dict) -> bool:
        self.logger.info(i18n.t("ShadowOps.module_unloaded", event=event))
        return True

    async def _reply_card(self, event, html, fallback_text: str):
        if self.cfg.render_card:
            png = await self._viz.render(html, theme=self.cfg.theme)
            if png is not None:
                try:
                    await event.reply(png, method="Image")
                    return
                except Exception as e:
                    self.logger.warning(f"图片回复失败，降级文本: {e}")
        await event.reply(fallback_text)

    def _shadow_error_text(self, error: Exception, name: str) -> str:
        from ErisPulse.Core.Bases.errors import ShadowError

        if isinstance(error, ShadowError):
            return f"{type(error).__name__}: {error}"
        return f"{type(error).__name__}: {error}"

    def _register_commands(self):
        @command("shadow", master=True, help="影子灰度管理")
        async def shadow_handler(event):
            await event.reply(
                "用法: /shadow start <模块名> <v2路径> | /shadow list | /shadow diff <模块名> | "
                "/shadow promote <模块名> confirm | /shadow dismiss <模块名> | /shadow audit <模块名>"
            )

        @command("shadow start", master=True, help="启动影子（新版代码以独立 owner 并存试运行）",
                 args="<name:str> <source:rest>")
        async def shadow_start_handler(event, name: str, source: str):
            source = source.strip()
            if not source:
                await event.reply("缺少 v2 路径")
                return
            try:
                owner = await self._service.start(name, source)
            except Exception as e:
                await event.reply(self._shadow_error_text(e, name))
                return
            await event.reply(i18n.t("ShadowOps.started", owner=owner, name=name))

        @command("shadow list", master=True, help="列出运行中的影子")
        async def shadow_list_handler(event):
            await self._reply_card(
                event,
                self._service.list_card_html(self._viz),
                self._service.format_list_text(),
            )

        @command("shadow diff", master=True, help="对比 v1 实际发送 × v2 意向发送", args="<name:str>")
        async def shadow_diff_handler(event, name: str):
            report = self._service.diff(name)
            await self._reply_card(
                event,
                self._service.diff_card_html(name, report, self.cfg.diff_max_rows, self._viz),
                self._service.format_diff_text(name, report, self.cfg.diff_max_rows),
            )

        @command("shadow promote", master=True, help="转正影子（需 yes 确认）",
                 args="<name:str> [confirm:literal=no|yes]")
        async def shadow_promote_handler(event, name: str, confirm: str = "no"):
            if confirm != "yes":
                await event.reply(i18n.t("ShadowOps.promote_need_confirm", name=name))
                return
            try:
                ok = await self._service.promote(name)
            except Exception as e:
                await event.reply(self._shadow_error_text(e, name))
                return
            if ok:
                await event.reply(i18n.t("ShadowOps.promoted", name=name))
            else:
                await event.reply(f"promote returned False: {name}")

        @command("shadow dismiss", master=True, help="放弃影子", args="<name:str>")
        async def shadow_dismiss_handler(event, name: str):
            try:
                ok = await self._service.dismiss(name)
            except Exception as e:
                await event.reply(self._shadow_error_text(e, name))
                return
            if ok:
                await event.reply(i18n.t("ShadowOps.dismissed", name=name))
            else:
                await event.reply(f"dismiss returned False: {name}")

        @command("shadow audit", master=True, help="归属权审计", args="<name:str>")
        async def shadow_audit_handler(event, name: str):
            try:
                report = self._service.audit(name, deep=self.cfg.audit_deep)
            except Exception as e:
                await event.reply(self._shadow_error_text(e, name))
                return
            await self._reply_card(
                event,
                self._service.audit_card_html(name, report, self._viz),
                self._service.format_audit_text(name, report),
            )
