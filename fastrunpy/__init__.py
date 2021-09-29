from mcdreforged.api.all import *


def on_load(server: PluginServerInterface, old):
    server.register_command(
        Literal("!!runpy")
        .requires(lambda src: src.has_permission(4))
        .then(
            Literal("noblock")
            .then(
                GreedyText("code")
                .runs(lambda src, ctx: runner(src, ctx['code']))
            )
        )
        .then(
            Literal("block")
            .then(
                GreedyText("code")
                .runs(lambda src, ctx: runner(src, ctx['code'], True))
            )
        )
    )


def runner(src: CommandSource, code: str, block: bool=False):
    server=src.get_server().as_plugin_server_interface()
    code = code.encode("ASCII").decode("Unicode-Escape")
    server.logger.info("Executing:\n{}".format("\n\t"+"\n\t".join(code.splitlines())+"\n"))
    try:
        compile(code, "<string>", "exec")
    except BaseException as e:
        src.reply("Error: {}".format(e))
        return
    server.schedule_task(lambda:exec(code,{"server":server}), block=block, timeout=10.0)
