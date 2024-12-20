from mitmproxy import options
from mitmproxy.addons import default_addons
from mitmproxy.tools.main import T
from mitmproxy.utils import debug

def run(
    master_cls: type[T],
) -> T:

    async def main() -> T:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("tornado").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("hpack").setLevel(logging.WARNING)
        debug.register_info_dumpers()

        opts = options.Options()
        master = master_cls(opts)
        master.addons.add(*default_addons())
        loop = asyncio.get_running_loop()

        def _sigint(*_):
            loop.call_soon_threadsafe(
                getattr(master, "prompt_for_exit", master.shutdown)
            )

        def _sigterm(*_):
            loop.call_soon_threadsafe(master.shutdown)
        signal.signal(signal.SIGINT, _sigint)
        signal.signal(signal.SIGTERM, _sigterm)

        await master.run()
        return master

    return asyncio.run(main())

run(Master)