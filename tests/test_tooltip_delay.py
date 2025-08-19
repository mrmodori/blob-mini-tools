import os
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.append(str(APP_DIR))

# ``core.config`` expects to be loaded with the app directory as CWD.
cwd = os.getcwd()
os.chdir(APP_DIR)
from core.config import CONFIG
from utils.tooltip import ToolTip
os.chdir(cwd)


class DummyWidget:
    def bind(self, *_args, **_kwargs):
        pass


def test_tooltip_uses_config_delay(monkeypatch):
    monkeypatch.setitem(CONFIG["tooltip"], "delay", 123)
    tt = ToolTip(DummyWidget(), "tip text")
    assert tt.delay == 123
