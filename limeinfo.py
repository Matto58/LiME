class LiMEInfo:
    version = "0.10"
    stage = "alpha1"
    devyears = "2024"
    repo = "https://github.com/Matto58/LiME"
    license = {
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "name": "CC BY-SA 4.0"
    }
    isdev = True

    def createTitle(winName: str | None = None):
        return (
            (f"{winName} | " if winName is not None else "") +
            f"LiME v{LiMEInfo.version}" + ("" if not LiMEInfo.isdev else f" (in-dev version - {LiMEInfo.stage})")
        )