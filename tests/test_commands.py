from types import SimpleNamespace

from ErisPulse_Testing import create_command_event

from ErisPulse.Core.Bases import BaseModule

V2_SOURCE = '''
from ErisPulse import sdk
from ErisPulse.Core.Bases import BaseModule


class Main(BaseModule):
    def __init__(self):
        self.sdk = sdk
        self.logger = sdk.logger.get_child("ShadowDemoV2")

    @staticmethod
    def get_meta():
        from ErisPulse.Core.Bases import ModuleMeta

        return ModuleMeta(name="ShadowDemoV2", description="v2", version="2.0.0")

    async def on_load(self, event):
        return True

    async def on_unload(self, event):
        return True
'''


class ShadowDemoV1(BaseModule):
    def __init__(self):
        from ErisPulse import sdk

        self.sdk = sdk
        self.logger = sdk.logger.get_child("ShadowDemo")

    @staticmethod
    def get_meta():
        from ErisPulse.Core.Bases import ModuleMeta

        return ModuleMeta(name="ShadowDemo", description="v1", version="1.0.0")

    async def on_load(self, event):
        return True

    async def on_unload(self, event):
        return True


async def _ensure_plugin_loader(bot):
    from ErisPulse import module, sdk
    from ErisPulse.loaders.plugin_folder import PluginFolderLoader

    if getattr(module, "_sdk", None) is None:
        module.set_sdk_ref(sdk)

    loader = getattr(sdk, "_module_loader", None)
    if loader is None:
        sdk._module_loader = SimpleNamespace(_plugin_loader=PluginFolderLoader())
    elif getattr(loader, "_plugin_loader", None) is None:
        loader._plugin_loader = PluginFolderLoader()


async def _start_shadow(bot, tmp_path):
    await bot.load_module(ShadowDemoV1)
    await _ensure_plugin_loader(bot)
    src = tmp_path / "shadowdemo_v2.py"
    src.write_text(V2_SOURCE, encoding="utf-8")
    return src


async def test_shadow_usage_hint(shadowbot):
    await shadowbot.dispatch(create_command_event("shadow"))
    shadowbot.assert_reply_contains("用法")


async def test_shadow_list_empty(shadowbot):
    await shadowbot.dispatch(create_command_event("shadow list"))
    shadowbot.assert_reply_contains("没有运行中的影子")


async def test_shadow_start_and_list(shadowbot, tmp_path):
    src = await _start_shadow(shadowbot, tmp_path)
    await shadowbot.dispatch(create_command_event(f"shadow start ShadowDemo {src}"))
    reply = shadowbot.last_reply.text
    assert "影子已启动" in reply
    assert "shadowdemo_v2" in reply

    await shadowbot.dispatch(create_command_event("shadow list"))
    reply = shadowbot.last_reply.text
    assert "运行中的影子（1 个）" in reply
    assert "ShadowDemo -> shadowdemo_v2" in reply


async def test_shadow_start_not_loaded(shadowbot, tmp_path):
    src = tmp_path / "whatever.py"
    src.write_text(V2_SOURCE, encoding="utf-8")
    await shadowbot.dispatch(create_command_event(f"shadow start NoSuch {src}"))
    shadowbot.assert_reply_contains("ShadowStateError")


async def test_shadow_start_bad_path(shadowbot, tmp_path):
    await shadowbot.load_module(ShadowDemoV1)
    await shadowbot.dispatch(create_command_event("shadow start ShadowDemo no/such/path"))
    shadowbot.assert_reply_contains("ShadowSourceError")


async def test_shadow_diff_without_shadow(shadowbot):
    await shadowbot.dispatch(create_command_event("shadow diff ShadowDemo"))
    shadowbot.assert_reply_contains("没有运行中的影子")


async def test_shadow_diff_with_ledger_entries(shadowbot, tmp_path):
    src = await _start_shadow(shadowbot, tmp_path)
    await shadowbot.dispatch(create_command_event(f"shadow start ShadowDemo {src}"))
    from ErisPulse.Core.shadow import shadow_ledger, shadow_manager

    owner = shadow_manager.shadow_owner_of("ShadowDemo")
    shadow_ledger.record(owner, {
        "kind": "send", "platform": "test", "method": "Text",
        "target": "user/u1", "trace_id": "trace-abc123", "preview": "hello v2",
    })
    await shadowbot.dispatch(create_command_event("shadow diff ShadowDemo"))
    reply = shadowbot.last_reply.text
    assert "在账 1 条" in reply
    assert "hello v2" in reply


async def test_shadow_dismiss(shadowbot, tmp_path):
    src = await _start_shadow(shadowbot, tmp_path)
    await shadowbot.dispatch(create_command_event(f"shadow start ShadowDemo {src}"))
    await shadowbot.dispatch(create_command_event("shadow dismiss ShadowDemo"))
    shadowbot.assert_reply_contains("影子已放弃")

    from ErisPulse.Core.shadow import shadow_manager

    assert shadow_manager.shadow_owner_of("ShadowDemo") is None


async def test_shadow_promote_needs_confirm(shadowbot, tmp_path):
    src = await _start_shadow(shadowbot, tmp_path)
    await shadowbot.dispatch(create_command_event(f"shadow start ShadowDemo {src}"))
    await shadowbot.dispatch(create_command_event("shadow promote ShadowDemo"))
    shadowbot.assert_reply_contains("确认请输入")
    from ErisPulse.Core.shadow import shadow_manager

    assert shadow_manager.shadow_owner_of("ShadowDemo") is not None


async def test_shadow_audit(shadowbot):
    await shadowbot.dispatch(create_command_event("shadow audit ShadowOps"))
    reply = shadowbot.last_reply.text
    assert "归属审计" in reply
    assert "counts:" in reply
