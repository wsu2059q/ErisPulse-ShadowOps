import pytest

from ShadowOps.Core import Main


@pytest.fixture(scope="session", autouse=True)
def _storage_teardown():
    yield
    from ErisPulse import sdk

    try:
        sdk.storage.close()
    except Exception:
        pass


@pytest.fixture
async def shadowbot(make_testbot):
    from ErisPulse import i18n

    prev_lang = i18n.get_language()
    i18n.set_language("zh-CN")

    async with make_testbot(config={"ErisPulse.master.users": {"test": ["tester"]}}) as bot:
        await bot.load_module(Main)

        from ErisPulse import module as module_mgr

        ops = module_mgr.get("ShadowOps")

        cfg = ops.cfg
        cfg.enabled = True
        cfg.diff_max_rows = 10
        cfg.audit_deep = False
        cfg.render_card = False
        ops.cfg = cfg

        from ErisPulse.Core.shadow import shadow_manager

        for real in list(getattr(shadow_manager, "_shadows", {})):
            try:
                shadow_manager.unbind(shadow_manager.shadow_owner_of(real))
            except Exception:
                pass

        bot.ops = ops
        yield bot

        for real in list(getattr(shadow_manager, "_shadows", {})):
            try:
                shadow_manager.unbind(shadow_manager.shadow_owner_of(real))
            except Exception:
                pass

    i18n.set_language(prev_lang)
