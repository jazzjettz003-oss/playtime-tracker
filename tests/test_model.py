from playtime_tracker.model import GameApp


def test_gameapp_from_dict_and_to_dict_with_time_key():
    data = {"display": "My App", "time": 45, "is_tracking": True, "category": "Game", "color_tag": "#00c896"}
    app = GameApp.from_dict("myapp.exe", data)

    assert app.name == "myapp.exe"
    assert app.display == "My App"
    assert app.total_time == 45
    assert app.is_tracking is True
    assert app.category == "Game"
    assert app.color_tag == "#00c896"

    payload = app.to_dict()
    assert payload["time"] == 45
    assert payload["display"] == "My App"


def test_gameapp_from_dict_supports_legacy_cumulative_seconds():
    legacy = {"display": "LegacyApp", "cumulative_seconds": 180}
    app = GameApp.from_dict("legacy.exe", legacy)

    assert app.total_time == 180
    assert app.display == "LegacyApp"
    assert app.name == "legacy.exe"
