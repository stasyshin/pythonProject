from uvicorn import run

from app.config.config import Settings, Config

if __name__ == "__main__":
    config: Settings = Config.get_config()
    run("app.main:create_app", port=8000, factory=True, reload=config.app.DEBUG)
