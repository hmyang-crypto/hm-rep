# -*- coding: utf-8 -*-
import json
import os
import re
import ssl
import sys
import threading
import time
import traceback
import urllib.request
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from functools import partial

# 💡 GitHub Raw 주소
UPDATE_CHECK_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/version.txt"
UPDATE_CODE_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/main.py"
CURRENT_VERSION = "1.4.5"


def check_and_apply_update():
    try:
        print("🔍 서버에서 최신 업데이트 확인 중...")
        ssl_context = ssl._create_unverified_context()
        req = urllib.request.Request(
            UPDATE_CHECK_URL, headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(
            req, timeout=5, context=ssl_context
        ) as response:
            if response.status == 200:
                server_version = response.read().decode("utf-8").strip()

                if server_version > CURRENT_VERSION:
                    print(
                        f"🚀 새 버전 발견 ({server_version})! 코드를 다운로드합니다."
                    )
                    code_req = urllib.request.Request(
                        UPDATE_CODE_URL, headers={"User-Agent": "Mozilla/5.0"}
                    )
                    with urllib.request.urlopen(
                        code_req, timeout=10, context=ssl_context
                    ) as new_code_response:
                        if new_code_response.status == 200:
                            app_dir = os.path.dirname(
                                os.path.abspath(__file__)
                            )
                            updated_file_path = os.path.join(
                                app_dir, "updated_main.py"
                            )

                            with open(
                                updated_file_path, "w", encoding="utf-8"
                            ) as f:
                                f.write(
                                    new_code_response.read().decode("utf-8")
                                )

                            print("✅ updated_main.py 최신 스크립트 저장 완료!")
    except Exception as e:
        print(f"⚠️ 업데이트 확인 중 오류 (무시하고 앱 실행): {e}")


if "updated_main.py" not in os.path.basename(__file__):
    check_and_apply_update()

    _app_dir = os.path.dirname(os.path.abspath(__file__))
    _updated_script = os.path.join(_app_dir, "updated_main.py")

    if os.path.exists(_updated_script) and __name__ == "__main__":
        try:
            print("🔄 최신 업데이트 스크립트(updated_main.py)로 실행합니다...")
            with open(_updated_script, "r", encoding="utf-8") as _f:
                _code = _f.read()
            exec(
                compile(_code, _updated_script, "exec"),
                {"__name__": "__main__", "__file__": _updated_script},
            )
            sys.exit(0)
        except Exception as _exec_err:
            print(
                f"⚠️ 업데이트 코드 실행 실패 (기본 main.py로 대체 실행): {_exec_err}"
            )

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex, platform

if platform == "android":
    try:
        from jnius import autoclass

        current_app = autoclass(
            "android.app.ActivityThread"
        ).currentApplication()
        context = current_app.getApplicationContext()
        user_data_dir = context.getFilesDir().getAbsolutePath()
        kivy_home_dir = os.path.join(user_data_dir, ".kivy")
        os.environ["KIVY_HOME"] = kivy_home_dir
        if not os.path.exists(kivy_home_dir):
            os.makedirs(kivy_home_dir)
    except Exception as e:
        print(f"🚨 KIVY_HOME 설정 오류: {e}")

if platform == "android":
    Window.softinput_mode = "below_target"
    from android.permissions import Permission, request_permissions
    from android.runnable import run_on_ui_thread
    from jnius import JavaException, PythonJavaClass, autoclass, java_method

import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = "replacement-463907-07ae6e152f37.json"
SPREADSHEET_NAME = "보충시트"
USER_SHEET_NAME = "사용자_목록"
TASK_SHEET_NAME = "보충작업_지시서"
LOG_SHEET_NAME = "작업완료_로그"
FCM_TOKEN_SHEET_NAME = "FCM_토큰"
LOCATION_CAPA_SHEET_NAME = "로케이션 케파 시트"

SHEET_RANGES = {
    USER_SHEET_NAME: "A:AA",
    TASK_SHEET_NAME: "A:AA",
    LOG_SHEET_NAME: "A:AA",
    FCM_TOKEN_SHEET_NAME: "A:AA",
    LOCATION_CAPA_SHEET_NAME: "A:AA",
}

try:
    LabelBase.register(name="Nanum", fn_regular="NanumSquareRoundEB.ttf")
    FONT_NAME = "Nanum"
except Exception as e:
    FONT_NAME = "Roboto"

PRIMARY_BLUE = get_color_from_hex("#1E88E5")
LIGHT_BLUE = get_color_from_hex("#E3F2FD")
FILTER_BG_GRAY = get_color_from_hex("#CFD8DC")
BG_GRAY = get_color_from_hex("#F4F7FA")
TEXT_DARK = get_color_from_hex("#212121")
TEXT_MUTED = get_color_from_hex("#757575")

DEFAULT_FONT_STYLE = {
    "font_name": FONT_NAME,
    "font_size": dp(15),
    "color": TEXT_DARK,
}
Window.clearcolor = BG_GRAY


def safe_int(val, default=0):
    if val is None:
        return default
    try:
        clean_str = re.sub(r"[^\d]", "", str(val))
        return int(clean_str) if clean_str else default
    except Exception:
        return default


# 💡 [핵심 구현] 안드로이드 시스템 대화상자(AlertDialog) 호출로 한/영 전환 및 한글 완전 지원
def open_native_korean_input(title, hint, initial_text, callback, is_number=False):
    if platform == "android":
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            AlertDialog = autoclass("android.app.AlertDialog$Builder")
            EditText = autoclass("android.widget.EditText")
            InputType = autoclass("android.text.InputType")

            context = PythonActivity.mActivity
            builder = AlertDialog(context)
            builder.setTitle(title)

            input_field = EditText(context)
            input_field.setHint(hint)
            if initial_text:
                input_field.setText(str(initial_text))
            
            if is_number:
                input_field.setInputType(InputType.TYPE_CLASS_NUMBER)

            builder.setView(input_field)

            # Positive Button Event Listener
            class PositiveClickListener(PythonJavaClass):
                __javainterfaces__ = ["android/content/DialogInterface$OnClickListener"]

                def __init__(self, cb, field):
                    super().__init__()
                    self.cb = cb
                    self.field = field

                @java_method("(Landroid/content/DialogInterface;I)V")
                def onClick(self, dialog, which):
                    res = self.field.getText().toString()
                    Clock.schedule_once(lambda dt: self.cb(res), 0.1)

            builder.setPositiveButton("확인", PositiveClickListener(callback, input_field))
            builder.setNegativeButton("취소", None)

            dialog = builder.create()
            dialog.show()
            return
        except Exception as e:
            print(f"⚠️ 안드로이드 시스템 입력창 오류 (Kivy fallback 사용): {e}")

    # 안드로이드 실패 시 Kivy SingleInputPopup 팝업 호출
    SingleInputPopup(
        title=title,
        hint_text=hint,
        initial_text=initial_text,
        input_type="number" if is_number else "text",
        on_confirm=callback,
    ).open()


class StyledButton(Button):

    def __init__(self, **kwargs):
        self.btn_bg_color = kwargs.pop("bg_color", PRIMARY_BLUE)
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        if "font_size" not in kwargs:
            self.font_size = dp(14)
        with self.canvas.before:
            self.bg_color_inst = Color(*self.btn_bg_color)
            self.bg_rounded_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(12)]
            )
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, instance, value):
        self.bg_rounded_rect.pos = instance.pos
        self.bg_rounded_rect.size = instance.size

    def set_bg_color(self, color):
        self.btn_bg_color = color
        self.bg_color_inst.rgba = color


class StyledToggleButton(ToggleButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        if "font_size" not in kwargs:
            self.font_size = dp(14)
        with self.canvas.before:
            initial_bg = PRIMARY_BLUE if self.state == "down" else LIGHT_BLUE
            self.bg_color_inst = Color(*initial_bg)
            self.bg_rounded_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(12)]
            )
        self.color = (1, 1, 1, 1) if self.state == "down" else TEXT_DARK
        self.bold = True if self.state == "down" else False
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            state=self._update_state,
        )

    def _update_canvas(self, instance, value):
        self.bg_rounded_rect.pos = instance.pos
        self.bg_rounded_rect.size = instance.size

    def _update_state(self, instance, value):
        if value == "down":
            self.bg_color_inst.rgba = PRIMARY_BLUE
            self.color = (1, 1, 1, 1)
            self.bold = True
        else:
            self.bg_color_inst.rgba = LIGHT_BLUE
            self.color = TEXT_DARK
            self.bold = False

    def set_active_visual(self, is_active):
        if is_active:
            self.state = "down"
            self.bg_color_inst.rgba = PRIMARY_BLUE
            self.color = (1, 1, 1, 1)
            self.bold = True
        else:
            self.state = "normal"
            self.bg_color_inst.rgba = LIGHT_BLUE
            self.color = TEXT_DARK
            self.bold = False


class StyledSpinner(Spinner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = TEXT_DARK
        if "font_size" not in kwargs:
            self.font_size = dp(13)
        with self.canvas.before:
            self.bg_color_inst = Color(*FILTER_BG_GRAY)
            self.bg_rounded_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(12)]
            )
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, instance, value):
        self.bg_rounded_rect.pos = instance.pos
        self.bg_rounded_rect.size = instance.size


class KoreanSpinnerOption(SpinnerOption):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = FONT_NAME
        self.font_size = dp(13)
        self.background_normal = ""
        self.background_color = get_color_from_hex("#37474F")


class TouchableBox(ButtonBehavior, BoxLayout):
    pass


class NotificationBanner(ButtonBehavior, BoxLayout):

    def __init__(self, text, on_press_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (0.95, None)
        self.height = dp(50)
        self.pos_hint = {"center_x": 0.5, "top": 1.2}
        self.padding = (dp(15), dp(5))
        self.spacing = dp(10)
        self.on_press_callback = on_press_callback

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.95)
            self.bg_rect = RoundedRectangle(
                size=self.size, pos=self.pos, radius=[dp(10)]
            )

        self.bind(pos=self._update_rect, size=self._update_rect)

        icon_label = Label(
            text="🔔",
            font_name=FONT_NAME,
            font_size=dp(20),
            size_hint_x=None,
            width=dp(30),
        )
        self.add_widget(icon_label)

        self.message_label = Label(
            text=text,
            font_name=FONT_NAME,
            font_size=dp(14),
            halign="left",
            valign="middle",
            markup=True,
            color=(1, 1, 1, 1),
        )
        self.message_label.bind(size=self.message_label.setter("text_size"))
        self.add_widget(self.message_label)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_press(self):
        if self.on_press_callback:
            self.on_press_callback()
        self.dismiss()

    def show(self, target_widget):
        target_widget.add_widget(self)
        anim = Animation(
            pos_hint={"center_x": 0.5, "top": 0.98}, duration=0.4, t="out_quad"
        )
        anim.start(self)
        Clock.schedule_once(self.dismiss, 6)

    def dismiss(self, *args):
        Clock.unschedule(self.dismiss)
        if not self.parent:
            return

        anim = Animation(
            pos_hint={"center_x": 0.5, "top": 1.2}, duration=0.4, t="in_quad"
        )
        anim.bind(on_complete=self._remove_widget)
        anim.start(self)

    def _remove_widget(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


# Native CheckBox 적용 다중 선택 드롭다운
class ZoneMultiSelectDropDown(DropDown):

    def __init__(self, zone_counts_dict, selected_zones, on_apply, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = True
        self.on_apply = on_apply
        self.checkboxes = {}

        self.auto_width = False
        self.width = dp(150)

        container = BoxLayout(
            orientation="vertical",
            padding=dp(6),
            spacing=dp(3),
            size_hint=(None, None),
            width=dp(150),
            height=dp(280),
        )

        with container.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.bg_rect = RoundedRectangle(
                pos=container.pos, size=container.size, radius=[dp(8)]
            )
        container.bind(
            pos=lambda i, p: setattr(self.bg_rect, "pos", p),
            size=lambda i, s: setattr(self.bg_rect, "size", s),
        )

        all_active = len(selected_zones) == len(zone_counts_dict) or "전체" in selected_zones
        self.btn_toggle_all = Button(
            text="전체해제" if all_active else "전체선택",
            font_name=FONT_NAME,
            font_size=dp(11),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            background_normal="",
            background_color=get_color_from_hex("#78909C"),
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
        )
        self.btn_toggle_all.bind(size=lambda i, s: setattr(i, "text_size", s))
        self.btn_toggle_all.bind(on_press=self._on_toggle_all_press)
        container.add_widget(self.btn_toggle_all)

        scroll = ScrollView(size_hint_y=None, height=dp(190))
        grid = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for zone_name, count in zone_counts_dict.items():
            is_active = (zone_name in selected_zones or "전체" in selected_zones)

            item_box = TouchableBox(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(34),
                padding=(dp(8), 0),
                spacing=dp(4),
            )
            with item_box.canvas.before:
                Color(*get_color_from_hex("#EEEEEE"))
                bg = RoundedRectangle(pos=item_box.pos, size=item_box.size, radius=[dp(4)])
            item_box.bind(
                pos=lambda i, p, b=bg: setattr(b, "pos", p),
                size=lambda i, s, b=bg: setattr(b, "size", s),
            )

            lbl = Label(
                text=f"{zone_name} ({count}건)",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=get_color_from_hex("#212121"),
                halign="left",
                valign="middle",
            )
            lbl.bind(size=lambda i, s: setattr(i, "text_size", s))

            chk = CheckBox(
                active=is_active,
                size_hint_x=None,
                width=dp(26),
                color=PRIMARY_BLUE,
            )

            item_box.add_widget(lbl)
            item_box.add_widget(chk)

            item_box.bind(on_press=lambda instance, c=chk: setattr(c, "active", not c.active))
            chk.bind(active=self._on_check_change)

            grid.add_widget(item_box)
            self.checkboxes[zone_name] = chk

        scroll.add_widget(grid)
        container.add_widget(scroll)

        btn_apply = Button(
            text="적용",
            font_name=FONT_NAME,
            font_size=dp(12),
            bold=True,
            size_hint_y=None,
            height=dp(34),
            background_normal="",
            background_color=PRIMARY_BLUE,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
        )
        btn_apply.bind(size=lambda i, s: setattr(i, "text_size", s))
        btn_apply.bind(on_press=self._on_apply_press)
        container.add_widget(btn_apply)

        self.add_widget(container)

    def _on_check_change(self, checkbox, value):
        self._update_toggle_all_btn_text()

    def _on_toggle_all_press(self, instance):
        target_state = not all(chk.active for chk in self.checkboxes.values())
        for chk in self.checkboxes.values():
            chk.active = target_state
        self._update_toggle_all_btn_text()

    def _update_toggle_all_btn_text(self):
        all_selected = all(chk.active for chk in self.checkboxes.values())
        self.btn_toggle_all.text = "전체해제" if all_selected else "전체선택"

    def _on_apply_press(self, instance):
        selected = {
            zone for zone, chk in self.checkboxes.items() if chk.active
        }
        if not selected or len(selected) == len(self.checkboxes):
            selected = {"전체"}
        self.on_apply(selected)
        self.dismiss()


g_sheet_client = None
g_spreadsheet = None
g_worksheet_objects = {}
GSPREAD_LOADED = False
GSPREAD_ERROR_MSG = ""
g_cached_sheets = {}
g_cache_timestamps = {}
CACHE_DURATION = 60


def execute_with_retry(func, *args, **kwargs):
    max_retries = 5
    base_delay = 1.5
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            if e.code in [429, 503]:
                delay = base_delay * (2**attempt)
                time.sleep(delay)
            else:
                raise e
        except Exception as e:
            raise e
    raise Exception(
        "🚨 구글 API 트래픽 초과 오류 누적으로 작업이 최종 실패했습니다."
    )


def invalidate_cache(sheet_name):
    if sheet_name in g_cached_sheets:
        del g_cached_sheets[sheet_name]
    if sheet_name in g_cache_timestamps:
        del g_cache_timestamps[sheet_name]


def initialize_gspread():
    global g_sheet_client, g_spreadsheet, GSPREAD_LOADED, GSPREAD_ERROR_MSG, g_worksheet_objects
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        GSPREAD_LOADED = False
        GSPREAD_ERROR_MSG = f"인증 키 파일 '{SERVICE_ACCOUNT_FILE}'을(를) 찾을 수 없습니다."
        print(f"\n🚨 '{SERVICE_ACCOUNT_FILE}' 파일이 없습니다!\n")
        return

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, scope
        )
        g_sheet_client = gspread.authorize(creds)
        g_spreadsheet = g_sheet_client.open(SPREADSHEET_NAME)
        g_worksheet_objects.clear()
        GSPREAD_LOADED = True
        print(f"✅ 구글 시트 연결 성공: [{SPREADSHEET_NAME}]")
    except Exception as e:
        GSPREAD_ERROR_MSG = str(e)
        GSPREAD_LOADED = False


def get_worksheet(worksheet_name):
    global g_spreadsheet, g_worksheet_objects
    if not GSPREAD_LOADED:
        initialize_gspread()
        if not GSPREAD_LOADED or not g_spreadsheet:
            raise Exception(f"구글 연결 실패: {GSPREAD_ERROR_MSG}")

    if worksheet_name in g_worksheet_objects:
        return g_worksheet_objects[worksheet_name]

    try:
        ws = execute_with_retry(g_spreadsheet.worksheet, worksheet_name)
        g_worksheet_objects[worksheet_name] = ws
        return ws
    except Exception:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, scope
        )
        client = gspread.authorize(creds)
        g_spreadsheet = client.open(SPREADSHEET_NAME)
        g_worksheet_objects.clear()
        ws = execute_with_retry(g_spreadsheet.worksheet, worksheet_name)
        g_worksheet_objects[worksheet_name] = ws
        return ws


def get_sheet_data(sheet_name, force_refresh=False):
    now = time.time()
    last_updated = g_cache_timestamps.get(sheet_name, 0)
    if not force_refresh and (now - last_updated) < CACHE_DURATION:
        if sheet_name in g_cached_sheets:
            return g_cached_sheets[sheet_name]
    try:
        sheet = get_worksheet(sheet_name)
        target_range = SHEET_RANGES.get(sheet_name, "A:AA")
        raw_rows = execute_with_retry(sheet.get, target_range)
        records = []
        if raw_rows and len(raw_rows) > 0:
            headers = [str(h).strip() for h in raw_rows[0]]
            for row in raw_rows[1:]:
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                record_dict = {
                    headers[i]: row[i] for i in range(len(headers))
                }
                records.append(record_dict)
        g_cached_sheets[sheet_name] = records
        g_cache_timestamps[sheet_name] = now
        return records
    except Exception as e:
        if sheet_name in g_cached_sheets:
            return g_cached_sheets[sheet_name]
        raise e


def t(d, k, default=""):
    return d.get(k, default)


class LoadingPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "처리 중"
        self.title_font = FONT_NAME
        self.content = Label(
            text="데이터를 처리하는 중입니다...\n잠시만 기다려주세요.",
            font_name=FONT_NAME,
            font_size=dp(16),
        )
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False


class InfoPopup(Popup):

    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.title_font = FONT_NAME
        self.size_hint = (0.9, 0.5)
        content = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        message_label = Label(
            text=str(message),
            font_name=FONT_NAME,
            font_size=dp(14),
            halign="center",
            valign="top",
        )
        message_label.bind(
            width=lambda *x: message_label.setter("text_size")(
                message_label, (message_label.width, None)
            )
        )
        scroll_view = ScrollView(size_hint_y=1)
        scroll_view.add_widget(message_label)
        content.add_widget(scroll_view)
        ok_button = StyledButton(
            text="확인", size_hint_y=None, height=dp(45)
        )
        ok_button.bind(on_press=self.dismiss)
        content.add_widget(ok_button)
        self.content = content


class SingleInputPopup(Popup):

    def __init__(
        self,
        title,
        hint_text,
        on_confirm,
        initial_text="",
        input_type="text",
        warning_text=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.title_font = FONT_NAME
        self.size_hint = (0.9, None)
        self.auto_dismiss = False
        self.on_confirm = on_confirm

        main_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None,
        )
        main_layout.bind(minimum_height=main_layout.setter("height"))
        main_layout.bind(
            height=lambda instance, value: setattr(
                self, "height", value + dp(60)
            )
        )

        if warning_text:
            warning_label = Label(
                text=warning_text,
                font_name=FONT_NAME,
                font_size=dp(15),
                color=get_color_from_hex("#D32F2F"),
                markup=True,
                halign="center",
                size_hint_y=None,
            )
            warning_label.bind(
                width=lambda *x: warning_label.setter("text_size")(
                    warning_label, (warning_label.width, None)
                ),
                texture_size=lambda *x: warning_label.setter("height")(
                    warning_label, warning_label.texture_size[1]
                ),
            )
            main_layout.add_widget(warning_label)

        self.text_input = TextInput(
            text=initial_text,
            hint_text=hint_text,
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=dp(18),
            font_name=FONT_NAME,
            input_type=input_type,
        )
        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10),
        )
        cancel_button = StyledButton(text="취소", bg_color=(0.6, 0.6, 0.6, 1))
        cancel_button.bind(on_press=self.dismiss)
        ok_button = StyledButton(text="확인")
        ok_button.bind(on_press=self._on_ok_press)

        button_layout.add_widget(cancel_button)
        button_layout.add_widget(ok_button)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(button_layout)
        self.content = main_layout
        self.bind(on_open=lambda *a: setattr(self.text_input, "focus", True))

    def _on_ok_press(self, instance):
        self.on_confirm(self.text_input.text)
        self.dismiss()


class MultipleSkuSelectPopup(Popup):

    def __init__(self, matches, on_select, **kwargs):
        super().__init__(**kwargs)
        self.title = "검수 대상 선택 (중복 SKU)"
        self.size_hint = (0.9, 0.7)
        layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        layout.add_widget(
            Label(
                text="스캔한 바코드가 여러 건 존재합니다.\n대상을 선택해주세요.",
                font_name=FONT_NAME,
                size_hint_y=None,
                height=dp(40),
            )
        )

        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        grid.bind(minimum_height=grid.setter("height"))

        for item in matches:
            task = item["task_data"]
            loc = t(task, "기존로케이션", t(task, "보충로케이션", "N/A"))
            qty = t(task, "지시수량", "0")
            btn = StyledButton(
                text=f"보관위치: {loc} | 지시수량: {qty}",
                size_hint_y=None,
                height=dp(55),
            )
            btn.bind(
                on_release=lambda instance, i=item: (
                    on_select(i),
                    self.dismiss(),
                )
            )
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.content = layout


class InspectionPopup(Popup):

    def __init__(self, card, task_list_screen, **kwargs):
        super().__init__(**kwargs)
        self.card = card
        self.task_data = card.task_data
        self.task_list_screen = task_list_screen
        self.current_remarks = str(t(self.task_data, "비고", ""))

        self.title = "검수 및 최종 처리"
        self.title_font = FONT_NAME
        self.size_hint = (0.95, None)
        self.height = dp(580)
        self.auto_dismiss = False

        main_layout = BoxLayout(
            orientation="vertical", padding=dp(15), spacing=dp(10)
        )

        total_qty = safe_int(t(self.task_data, "지시수량", 0))
        default_box_size = safe_int(
            t(self.task_data, "박스입수량", t(self.task_data, "박스 입수량", 1))
        )
        if default_box_size <= 0:
            default_box_size = 1

        product_name = str(t(self.task_data, "상품명", ""))
        is_invoice_only = default_box_size == 1 or "송장" in product_name

        info_label = Label(
            text=f"지시수량: [b]{total_qty}[/b] / 기본입수량: [b]{default_box_size}[/b]",
            font_name=FONT_NAME,
            font_size=dp(15),
            markup=True,
            size_hint_y=None,
            height=dp(25),
        )
        main_layout.add_widget(info_label)

        if is_invoice_only:
            warn_lbl = Label(
                text="[color=D32F2F][b]⚠️ [송장만 부착 항목] - 로케이션을 적지 마세요![/b][/color]",
                font_name=FONT_NAME,
                font_size=dp(13),
                markup=True,
                size_hint_y=None,
                height=dp(22),
            )
            main_layout.add_widget(warn_lbl)

        input_grid = GridLayout(
            cols=2, spacing=dp(10), size_hint_y=None, height=dp(150)
        )

        input_grid.add_widget(
            Label(
                text=f"박스 입수량 (기존 {default_box_size}):",
                font_name=FONT_NAME,
                font_size=dp(14),
            )
        )
        self.box_size_input = TextInput(
            text=str(default_box_size),
            multiline=False,
            input_type="number",
            font_name=FONT_NAME,
            font_size=dp(18),
            halign="center",
            readonly=True,
        )
        self.box_size_input.bind(
            on_touch_down=lambda instance, touch: self._touch_input(
                instance, touch, "박스 입수량 입력", True
            )
        )
        input_grid.add_widget(self.box_size_input)

        input_grid.add_widget(
            Label(text="박스 수량:", font_name=FONT_NAME, font_size=dp(14))
        )
        self.box_count_input = TextInput(
            hint_text="0",
            multiline=False,
            input_type="number",
            font_name=FONT_NAME,
            font_size=dp(18),
            halign="center",
            readonly=True,
        )
        self.box_count_input.bind(
            on_touch_down=lambda instance, touch: self._touch_input(
                instance, touch, "박스 수량 입력", True
            )
        )
        input_grid.add_widget(self.box_count_input)

        input_grid.add_widget(
            Label(text="낱개 수량:", font_name=FONT_NAME, font_size=dp(14))
        )
        self.rem_qty_input = TextInput(
            hint_text="0",
            multiline=False,
            input_type="number",
            font_name=FONT_NAME,
            font_size=dp(18),
            halign="center",
            readonly=True,
        )
        self.rem_qty_input.bind(
            on_touch_down=lambda instance, touch: self._touch_input(
                instance, touch, "낱개 수량 입력", True
            )
        )
        input_grid.add_widget(self.rem_qty_input)

        main_layout.add_widget(input_grid)

        loc_box = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_y=None, height=dp(70)
        )
        loc_box.add_widget(
            Label(
                text="최종 적치위치",
                font_name=FONT_NAME,
                font_size=dp(14),
                size_hint_y=None,
                height=dp(20),
                halign="left",
            )
        )
        self.final_location_input = TextInput(
            text=str(t(self.task_data, "보충로케이션", "")),
            hint_text="적치위치 입력",
            multiline=False,
            font_name=FONT_NAME,
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
            readonly=True,
        )
        self.final_location_input.bind(
            on_touch_down=lambda instance, touch: self._touch_input(
                instance, touch, "최종 적치위치 입력", False
            )
        )
        loc_box.add_widget(self.final_location_input)
        main_layout.add_widget(loc_box)

        top_button_grid = GridLayout(
            cols=2, size_hint_y=None, height=dp(50), spacing=dp(10)
        )
        cancel_button = StyledButton(text="취소", bg_color=(0.6, 0.6, 0.6, 1))
        cancel_button.bind(on_press=self.dismiss)
        ok_button = StyledButton(
            text="최종 완료", bg_color=get_color_from_hex("#00897B")
        )
        ok_button.bind(on_press=self.confirm_inspection)

        top_button_grid.add_widget(cancel_button)
        top_button_grid.add_widget(ok_button)
        main_layout.add_widget(top_button_grid)

        self.content = main_layout

    def _touch_input(self, instance, touch, title, is_num):
        if instance.collide_point(*touch.pos):
            def set_val(val):
                instance.text = str(val).strip()

            open_native_korean_input(title, title, instance.text, set_val, is_number=is_num)
            return True
        return False

    def confirm_inspection(self, instance):
        app = App.get_running_app()

        box_size_str = self.box_size_input.text.strip()
        box_count_str = self.box_count_input.text.strip() or "0"
        rem_qty_str = self.rem_qty_input.text.strip() or "0"
        final_location = self.final_location_input.text.strip()

        if not box_size_str.isdigit() or not box_count_str.isdigit() or not rem_qty_str.isdigit():
            app.show_info_popup(
                "입력 오류", "박스 입수량, 박스 수량, 낱개 수량을 숫자로 입력해야 합니다."
            )
            return

        box_size = int(box_size_str)
        box_count = int(box_count_str)
        rem_qty = int(rem_qty_str)

        calculated_total_qty = (box_size * box_count) + rem_qty

        if calculated_total_qty <= 0:
            app.show_info_popup("입력 오류", "최종 수량이 0개 이상이어야 합니다.")
            return

        if not final_location:
            app.show_info_popup("오류", "최종 적치위치를 입력해야 합니다.")
            return

        self.task_list_screen._finalize_task_processing(
            card=self.card,
            final_qty=calculated_total_qty,
            split_qty=0,
            final_location=final_location,
            updated_remarks=self.current_remarks,
        )
        self.dismiss()


class NameEntryScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(
            orientation="vertical", padding=dp(30), spacing=dp(15)
        )

        layout.add_widget(
            Label(
                text="보충 업무 자동화",
                font_name=FONT_NAME,
                font_size=dp(28),
                bold=True,
                color=PRIMARY_BLUE,
                size_hint_y=0.2,
            )
        )

        layout.add_widget(
            Label(
                text=f"App Version: v{CURRENT_VERSION}",
                font_name=FONT_NAME,
                font_size=dp(13),
                color=TEXT_MUTED,
                size_hint_y=0.1,
            )
        )

        input_box = BoxLayout(
            orientation="vertical", spacing=dp(10), size_hint_y=0.3
        )
        input_box.add_widget(
            Label(
                text="작업자 이름을 입력해주세요",
                font_name=FONT_NAME,
                font_size=dp(16),
                color=TEXT_DARK,
            )
        )
        self.name_input = TextInput(
            hint_text="터치하여 이름 입력",
            multiline=False,
            font_name=FONT_NAME,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50),
            halign="center",
            readonly=True,
        )
        self.name_input.bind(on_touch_down=self.on_input_touch)
        input_box.add_widget(self.name_input)

        start_btn = StyledButton(
            text="작업 시작하기", size_hint_y=None, height=dp(55)
        )
        start_btn.bind(on_press=self.start_app)

        layout.add_widget(input_box)
        layout.add_widget(start_btn)
        layout.add_widget(Widget(size_hint_y=0.2))
        self.add_widget(layout)

    def on_input_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            def set_name(val):
                if val.strip():
                    self.name_input.text = val.strip()

            open_native_korean_input(
                "작업자 이름 입력", "이름을 입력하세요", self.name_input.text, set_name
            )
            return True
        return False

    def on_enter(self, *args):
        app = App.get_running_app()
        saved_name = app.load_saved_user_name()
        if saved_name:
            self.name_input.text = saved_name

    def start_app(self, instance):
        name = self.name_input.text.strip()
        if not name:
            App.get_running_app().show_info_popup(
                "알림", "이름을 입력해야 합니다."
            )
            return
        app = App.get_running_app()
        app.user_real_name = name
        app.save_user_name(name)
        self.manager.current = "main_menu"


class MainMenuScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(
            orientation="vertical", padding=dp(15), spacing=dp(10)
        )
        self.add_widget(self.layout)

    def on_enter(self, *args):
        self.layout.clear_widgets()
        app = App.get_running_app()

        if not app.user_real_name:
            app.user_real_name = app.load_saved_user_name() or ""
            if not app.user_real_name:
                self.manager.current = "name_entry"
                return

        top_bar = BoxLayout(size_hint_y=None, height=dp(40))
        welcome_box = BoxLayout(orientation="vertical", size_hint_x=0.75)
        welcome_box.add_widget(
            Label(
                text=f'"{app.user_real_name}"님',
                font_name=FONT_NAME,
                font_size=dp(18),
                bold=True,
                color=PRIMARY_BLUE,
                halign="left",
            )
        )
        welcome_box.add_widget(
            Label(
                text="오늘도 안전 작업하세요!",
                font_name=FONT_NAME,
                font_size=dp(13),
                color=TEXT_MUTED,
                halign="left",
            )
        )
        for child in welcome_box.children:
            child.bind(size=lambda i, s: setattr(i, "text_size", s))

        btn_printer = StyledButton(
            text="프린터",
            size_hint_x=None,
            width=dp(70),
            font_size=dp(12),
            bg_color=get_color_from_hex("#78909C"),
        )
        btn_printer.bind(
            on_press=lambda x: Factory.PrinterSettingsPopup().open()
        )

        top_bar.add_widget(welcome_box)
        top_bar.add_widget(btn_printer)
        self.layout.add_widget(top_bar)

        dash_card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(140),
            padding=dp(10),
            spacing=dp(4),
        )
        with dash_card.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=dash_card.pos, size=dash_card.size, radius=[dp(12)]
            )
        dash_card.bind(
            pos=lambda i, p: setattr(i.canvas.before.children[-1], "pos", p),
            size=lambda i, s: setattr(i.canvas.before.children[-1], "size", s),
        )

        lbl_dash_title = Label(
            text="📊 실시간 보충 현황 요약",
            font_name=FONT_NAME,
            font_size=dp(13),
            bold=True,
            color=PRIMARY_BLUE,
            size_hint_y=None,
            height=dp(20),
            halign="left",
        )
        lbl_dash_title.bind(size=lambda i, s: setattr(i, "text_size", s))
        dash_card.add_widget(lbl_dash_title)

        grid = GridLayout(cols=3, spacing=dp(2))
        grid.add_widget(
            Label(
                text="구분",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_MUTED,
                bold=True,
            )
        )
        grid.add_widget(
            Label(
                text="대기중 (긴급)",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_MUTED,
                bold=True,
            )
        )
        grid.add_widget(
            Label(
                text="작업중 (긴급)",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_MUTED,
                bold=True,
            )
        )

        self.lbl_op_pending = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            color=TEXT_DARK,
        )
        self.lbl_op_working = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            color=PRIMARY_BLUE,
        )
        grid.add_widget(
            Label(
                text="오더피커",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_DARK,
                bold=True,
            )
        )
        grid.add_widget(self.lbl_op_pending)
        grid.add_widget(self.lbl_op_working)

        self.lbl_reach_pending = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            color=TEXT_DARK,
        )
        self.lbl_reach_working = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            color=PRIMARY_BLUE,
        )
        grid.add_widget(
            Label(
                text="리치",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_DARK,
                bold=True,
            )
        )
        grid.add_widget(self.lbl_reach_pending)
        grid.add_widget(self.lbl_reach_working)

        dash_card.add_widget(grid)

        sep = Widget(size_hint_y=None, height=dp(1))
        with sep.canvas:
            Color(0.85, 0.85, 0.85, 1)
            rect = Rectangle(pos=sep.pos, size=sep.size)
        sep.bind(
            pos=lambda i, p: setattr(rect, "pos", p),
            size=lambda i, s: setattr(rect, "size", s),
        )
        dash_card.add_widget(sep)

        grid_tot = GridLayout(
            cols=3, size_hint_y=None, height=dp(25), spacing=dp(2)
        )
        self.lbl_all_pending = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            bold=True,
            markup=True,
            color=TEXT_DARK,
        )
        self.lbl_all_working = Label(
            text="0 [color=D32F2F](0)[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            bold=True,
            markup=True,
            color=PRIMARY_BLUE,
        )
        grid_tot.add_widget(
            Label(
                text="전체합계",
                font_name=FONT_NAME,
                font_size=dp(12),
                color=TEXT_DARK,
                bold=True,
            )
        )
        grid_tot.add_widget(self.lbl_all_pending)
        grid_tot.add_widget(self.lbl_all_working)
        dash_card.add_widget(grid_tot)

        self.layout.add_widget(dash_card)
        self.layout.add_widget(Widget(size_hint_y=None, height=dp(15)))

        menu_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        menu_box.bind(minimum_height=menu_box.setter("height"))

        def create_compact_menu_row(btn_widget):
            row = BoxLayout(size_hint_y=None, height=dp(46))
            row.add_widget(Widget())
            row.add_widget(btn_widget)
            row.add_widget(Widget())
            return row

        btn_replenish = StyledButton(
            text="[보충] 보충 작업",
            bg_color=PRIMARY_BLUE,
            size_hint_x=None,
            width=dp(220),
        )
        btn_replenish.bind(
            on_press=lambda x: setattr(
                self.manager, "current", "unified_replenish"
            )
        )
        menu_box.add_widget(create_compact_menu_row(btn_replenish))

        btn_inspect = StyledButton(
            text="[검수] 검수 목록 보기",
            bg_color=get_color_from_hex("#00897B"),
            size_hint_x=None,
            width=dp(220),
        )
        btn_inspect.bind(on_press=self.go_to_inspect)
        menu_box.add_widget(create_compact_menu_row(btn_inspect))

        btn_dashboard = StyledButton(
            text="[현황] 전체 작업 현황판",
            bg_color=get_color_from_hex("#3F51B5"),
            size_hint_x=None,
            width=dp(220),
        )
        btn_dashboard.bind(
            on_press=lambda x: setattr(
                self.manager, "current", "admin_dashboard"
            )
        )
        menu_box.add_widget(create_compact_menu_row(btn_dashboard))

        self.layout.add_widget(menu_box)
        self.layout.add_widget(Widget())

        bottom_box = BoxLayout(size_hint_y=None, height=dp(36))
        bottom_box.add_widget(Widget())
        change_btn = StyledButton(
            text="작업자 이름 변경",
            size_hint_x=None,
            width=dp(140),
            bg_color=get_color_from_hex("#FF7043"),
            font_size=dp(12),
        )
        change_btn.bind(
            on_press=lambda x: setattr(self.manager, "current", "name_entry")
        )
        bottom_box.add_widget(change_btn)
        self.layout.add_widget(bottom_box)

        threading.Thread(
            target=self._fetch_summary_counts, daemon=True
        ).start()

    def _fetch_summary_counts(self):
        try:
            tasks = get_sheet_data(TASK_SHEET_NAME, force_refresh=False)
            op_p, op_pu, op_w, op_wu = 0, 0, 0, 0
            rc_p, rc_pu, rc_w, rc_wu = 0, 0, 0, 0

            for task in tasks:
                st = str(t(task, "상태")).strip()
                eq = str(t(task, "장비")).strip()
                is_urg = t(task, "긴급여부") == "Y"

                if st == "대기":
                    if eq == "오더피커":
                        op_p += 1
                        if is_urg:
                            op_pu += 1
                    elif eq == "리치":
                        rc_p += 1
                        if is_urg:
                            rc_pu += 1
                elif st == "작업중":
                    if eq == "오더피커":
                        op_w += 1
                        if is_urg:
                            op_wu += 1
                    elif eq == "리치":
                        rc_w += 1
                        if is_urg:
                            rc_wu += 1

            tot_p, tot_pu = op_p + rc_p, op_pu + rc_pu
            tot_w, tot_wu = op_w + rc_w, op_wu + rc_wu

            Clock.schedule_once(
                lambda dt: self._update_summary_labels(
                    f"{op_p} [color=D32F2F]({op_pu})[/color]",
                    f"{op_w} [color=D32F2F]({op_wu})[/color]",
                    f"{rc_p} [color=D32F2F]({rc_pu})[/color]",
                    f"{rc_w} [color=D32F2F]({rc_wu})[/color]",
                    f"{tot_p} [color=D32F2F]({tot_pu})[/color]",
                    f"{tot_w} [color=D32F2F]({tot_wu})[/color]",
                )
            )
        except Exception:
            pass

    def _update_summary_labels(self, op_p, op_w, rc_p, rc_w, tot_p, tot_w):
        if hasattr(self, "lbl_op_pending") and self.lbl_op_pending.parent:
            self.lbl_op_pending.text = op_p
            self.lbl_op_working.text = op_w
            self.lbl_reach_pending.text = rc_p
            self.lbl_reach_working.text = rc_w
            self.lbl_all_pending.text = tot_p
            self.lbl_all_working.text = tot_w

    def go_to_inspect(self, instance):
        app = App.get_running_app()
        app.current_list_type = "검수인원"
        self.manager.current = "task_list"


# --- 통합 보충 작업 카드 뷰어 ---
class UnifiedTaskCard(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(0)
    task_data = DictProperty({})
    is_claimed = BooleanProperty(False)
    is_checked = BooleanProperty(False)
    card_screen = ObjectProperty(None)
    card_bg_color = ListProperty([1, 1, 1, 1])

    def refresh_view_attrs(self, rv, index, data):
        super().refresh_view_attrs(rv, index, data)
        self.index = index
        self.task_data = data.get("task_data", {})
        self.is_claimed = data.get("is_claimed", False)
        self.is_checked = data.get("is_checked", False)
        self.card_screen = data.get("card_screen", None)

        is_urgent = self.task_data.get("긴급여부") == "Y"
        is_shelf_rack = t(self.task_data, "선반랙 여부", "").upper() == "Y"

        if is_urgent:
            self.card_bg_color = get_color_from_hex("#FFEBEE")
        elif is_shelf_rack:
            self.card_bg_color = get_color_from_hex("#E3F2FD")
        else:
            self.card_bg_color = [1, 1, 1, 1]

        raw_equip = str(t(self.task_data, "장비", ""))
        if raw_equip == "리치":
            display_tag = "[color=0000FF][리치][/color]"
        elif raw_equip == "오더피커":
            display_tag = "[color=1E88E5][오더피커][/color]"
        else:
            display_tag = ""
        self.ids.lbl_equip.text = f"[b]{display_tag}[/b]"

        existing_qty = safe_int(t(self.task_data, "기존수량", 0))
        req_qty = safe_int(t(self.task_data, "지시수량", 0))
        remaining_qty = existing_qty - req_qty
        self.ids.lbl_stock_info.text = f"기존: [b]{existing_qty}[/b]\n보충후: [b][color=1E88E5]{remaining_qty}[/color][/b]"

        qty_per_box = safe_int(
            t(self.task_data, "박스입수량", t(self.task_data, "박스 입수량", 0))
        )
        product_name = t(self.task_data, "상품명", "N/A")
        is_invoice_only = qty_per_box == 1 or "송장" in product_name
        is_inbox = str(t(self.task_data, "인박스여부", "")).strip().upper() == "Y"

        tag_prefix = ""
        if is_urgent:
            tag_prefix += "[color=D32F2F][긴급][/color] "
        if is_shelf_rack:
            tag_prefix += "[color=1565C0][선반랙][/color] "

        self.ids.lbl_product.text = f"[b]{tag_prefix}{product_name}[/b]"
        self.ids.lbl_barcode.text = f"바코드: {t(self.task_data, '상품바코드', t(self.task_data, '바코드', 'N/A'))}"

        from_loc = str(t(self.task_data, "기존로케이션", "-"))
        to_loc = str(t(self.task_data, "보충로케이션", "-"))
        self.ids.lbl_loc.text = (
            f"[color=D32F2F]{from_loc}[/color] ➔ [color=1E88E5]{to_loc}[/color]"
        )

        conf_qty_val = self.task_data.get("confirmed_quantity", t(self.task_data, "확인수량", ""))
        active_count = safe_int(conf_qty_val, 0) if str(conf_qty_val).isdigit() else 0

        target_box_ea_calc = (
            f"({req_qty // qty_per_box}B / {req_qty % qty_per_box}E)"
            if qty_per_box > 0
            else f"({req_qty}E)"
        )

        if self.is_claimed:
            self.ids.lbl_main_qty.text = f"지시: {req_qty} / [color=D32F2F]{active_count}[/color] [color=1E88E5]{target_box_ea_calc}[/color]"
        else:
            self.ids.lbl_main_qty.text = f"지시: [b]{req_qty}[/b] [color=1E88E5]{target_box_ea_calc}[/color]"

        box_notice_str = f"박스입수: {qty_per_box}"
        if is_inbox:
            box_notice_str += "  [color=D32F2F][b][인박스 확인 필요][/b][/color]"
        if is_invoice_only:
            box_notice_str += "  [color=D32F2F][b][송장만 부착 - 로케이션 적지 말 것][/b][/color]"

        self.ids.lbl_box_info.text = box_notice_str

        self.ids.box_check.opacity = 1
        self.ids.box_check.disabled = False
        self.ids.box_check.active = self.is_checked

        if self.is_claimed:
            self.ids.btn_action_box.height = dp(40)
            self.ids.btn_action_box.opacity = 1
            self.ids.btn_action_box.disabled = False
        else:
            self.ids.btn_action_box.height = 0
            self.ids.btn_action_box.opacity = 0
            self.ids.btn_action_box.disabled = True

    def on_checkbox_active(self, checkbox, value):
        if self.card_screen:
            self.card_screen.toggle_card_check(self.task_data, value)

    def handle_card_btn(self, action_name):
        if self.card_screen:
            self.card_screen.handle_my_task_action(action_name, self.task_data)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            if app and app.root and app.root.current == "task_list":
                task_list_screen = app.root.get_screen("task_list")
                task_list_screen.open_task_from_scan({"task_data": self.task_data})
                return True
        return super().on_touch_down(touch)


# --- 올인원 통합 보충 작업 화면 ---
class UnifiedReplenishScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_main_tab = "PENDING"
        self.active_equip_filter = "ALL"
        self.only_urgent = False
        self.selected_from_zones = {"전체"}
        self.selected_to_zones = {"전체"}
        self.sort_asc = True
        self.is_filter_expanded = True

        self.raw_all_tasks = []
        self.checked_task_ids = set()

        self.layout = BoxLayout(
            orientation="vertical", padding=dp(8), spacing=dp(4)
        )

        header = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        btn_back = StyledButton(
            text="< 뒤로",
            size_hint_x=0.2,
            bg_color=get_color_from_hex("#78909C"),
        )
        btn_back.bind(
            on_press=lambda x: setattr(self.manager, "current", "main_menu")
        )

        lbl_title = Label(
            text="보충 작업 통합 컨트롤",
            font_name=FONT_NAME,
            font_size=dp(16),
            bold=True,
            color=TEXT_DARK,
        )

        btn_refresh = StyledButton(text="갱신", size_hint_x=0.2)
        btn_refresh.bind(on_press=lambda x: self.fetch_data())

        header.add_widget(btn_back)
        header.add_widget(lbl_title)
        header.add_widget(btn_refresh)
        self.layout.add_widget(header)

        self.btn_toggle_filter = StyledButton(
            text="🔍 필터 설정 닫기 ▲ (대기작업 / 전체)",
            size_hint_y=None,
            height=dp(32),
            bg_color=get_color_from_hex("#546E7A"),
            font_size=dp(12),
        )
        self.btn_toggle_filter.bind(on_press=self.toggle_filter_panel)
        self.layout.add_widget(self.btn_toggle_filter)

        self.filter_panel = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(112),
            spacing=dp(4),
        )

        main_tab_box = BoxLayout(
            size_hint_y=None, height=dp(36), spacing=dp(5)
        )
        self.btn_tab_pending = StyledToggleButton(
            text="대기 작업",
            group="main_tab",
            state="down",
            size_hint_x=0.5,
            font_size=dp(14),
        )
        self.btn_tab_pending.bind(
            on_press=lambda x: self.switch_main_tab("PENDING")
        )

        self.btn_tab_my = StyledToggleButton(
            text="내 작업",
            group="main_tab",
            state="normal",
            size_hint_x=0.5,
            font_size=dp(14),
        )
        self.btn_tab_my.bind(on_press=lambda x: self.switch_main_tab("MY"))

        main_tab_box.add_widget(self.btn_tab_pending)
        main_tab_box.add_widget(self.btn_tab_my)
        self.filter_panel.add_widget(main_tab_box)

        equip_filter_box = BoxLayout(
            size_hint_y=None, height=dp(32), spacing=dp(5)
        )
        self.btn_eq_all = StyledToggleButton(
            text="전체", group="equip_filter", state="down", font_size=dp(12)
        )
        self.btn_eq_all.bind(
            on_press=lambda x: self.switch_equip_filter("ALL")
        )

        self.btn_eq_op = StyledToggleButton(
            text="오더피커",
            group="equip_filter",
            state="normal",
            font_size=dp(12),
        )
        self.btn_eq_op.bind(
            on_press=lambda x: self.switch_equip_filter("ORDERPICKER")
        )

        self.btn_eq_reach = StyledToggleButton(
            text="리치", group="equip_filter", state="normal", font_size=dp(12)
        )
        self.btn_eq_reach.bind(
            on_press=lambda x: self.switch_equip_filter("REACH")
        )

        equip_filter_box.add_widget(self.btn_eq_all)
        equip_filter_box.add_widget(self.btn_eq_op)
        equip_filter_box.add_widget(self.btn_eq_reach)
        self.filter_panel.add_widget(equip_filter_box)

        opt_toolbar = BoxLayout(
            size_hint_y=None, height=dp(32), spacing=dp(3)
        )

        self.btn_from_zone = StyledButton(
            text="보관: 전체", size_hint_x=0.30, font_size=dp(11)
        )
        self.btn_from_zone.bind(on_press=self.open_from_zone_popup)

        self.btn_to_zone = StyledButton(
            text="이동: 전체", size_hint_x=0.30, font_size=dp(11)
        )
        self.btn_to_zone.bind(on_press=self.open_to_zone_popup)

        self.btn_sort = StyledButton(
            text="▲",
            size_hint_x=0.12,
            font_size=dp(12),
            bg_color=get_color_from_hex("#546E7A"),
        )
        self.btn_sort.bind(on_press=self.toggle_sort_order)

        chk_box = BoxLayout(size_hint_x=0.28, spacing=dp(2))
        self.chk_urgent = CheckBox(
            active=False, size_hint_x=None, width=dp(20), color=PRIMARY_BLUE
        )
        self.chk_urgent.bind(active=self.on_urgent_check_change)
        lbl_urg = Label(
            text="긴급만",
            font_name=FONT_NAME,
            font_size=dp(12),
            color=TEXT_DARK,
            halign="left",
            valign="middle",
        )
        lbl_urg.bind(size=lambda i, s: setattr(i, "text_size", s))

        chk_box.add_widget(self.chk_urgent)
        chk_box.add_widget(lbl_urg)
        opt_toolbar.add_widget(self.btn_from_zone)
        opt_toolbar.add_widget(self.btn_to_zone)
        opt_toolbar.add_widget(self.btn_sort)
        opt_toolbar.add_widget(chk_box)
        self.filter_panel.add_widget(opt_toolbar)

        self.layout.add_widget(self.filter_panel)

        list_header = BoxLayout(
            size_hint_y=None, height=dp(26), padding=(dp(5), 0)
        )
        self.lbl_status_count = Label(
            text="대기 작업 (전체) : 0건",
            font_name=FONT_NAME,
            font_size=dp(13),
            color=TEXT_MUTED,
            halign="left",
        )
        self.lbl_status_count.bind(
            size=lambda i, s: setattr(i, "text_size", s)
        )

        self.chk_all = CheckBox(
            size_hint_x=None, width=dp(26), color=PRIMARY_BLUE
        )
        self.chk_all.bind(active=self.on_check_all_change)
        self.lbl_chk_all = Label(
            text="전체선택",
            font_name=FONT_NAME,
            font_size=dp(12),
            color=TEXT_DARK,
            size_hint_x=None,
            width=dp(55),
        )

        list_header.add_widget(self.lbl_status_count)
        list_header.add_widget(self.chk_all)
        list_header.add_widget(self.lbl_chk_all)
        self.layout.add_widget(list_header)

        self.rv = RecycleView()
        self.rv_layout = RecycleBoxLayout(
            default_size=(None, dp(205)),
            default_size_hint=(1, None),
            size_hint_y=None,
            orientation="vertical",
            spacing=dp(8),
        )
        self.rv_layout.bind(minimum_height=self.rv_layout.setter("height"))
        self.rv.add_widget(self.rv_layout)
        self.rv.viewclass = "UnifiedTaskCard"
        self.layout.add_widget(self.rv)

        self.action_bar = BoxLayout(
            size_hint_y=None, height=dp(42), padding=(dp(5), 0)
        )
        self.action_bar.add_widget(Widget())

        self.btn_main_action = StyledButton(
            text="+ 선택 항목 할당받기 (0)",
            size_hint_x=None,
            width=dp(210),
            bg_color=PRIMARY_BLUE,
            bold=True,
            font_size=dp(13),
        )
        self.btn_main_action.bind(on_press=self.handle_main_action)
        self.action_bar.add_widget(self.btn_main_action)
        self.layout.add_widget(self.action_bar)

        self.add_widget(self.layout)

    def open_from_zone_popup(self, instance):
        app = App.get_running_app()
        user_name = str(app.user_real_name).strip().lower()

        from_counts = Counter()
        for task in self.raw_all_tasks:
            status = str(t(task, "상태")).strip()
            assignee = str(t(task, "작업 담당자")).strip().lower()
            if self.active_main_tab == "PENDING":
                if status != "대기" or assignee != "":
                    continue
            else:
                if status != "작업중" or assignee != user_name:
                    continue

            loc = str(t(task, "기존로케이션")).strip().upper()
            if loc:
                from_counts[f"{loc[0]}존"] += 1

        def apply_from_zones(selected_set):
            self.selected_from_zones = selected_set
            if "전체" in selected_set or not selected_set:
                self.btn_from_zone.text = "보관: 전체"
            else:
                zones_str = ",".join(sorted(selected_set)).replace("존", "")
                self.btn_from_zone.text = f"보관: {zones_str}"
            self.apply_filters_and_render()

        dropdown = ZoneMultiSelectDropDown(
            dict(sorted(from_counts.items())), self.selected_from_zones, apply_from_zones
        )
        dropdown.open(instance)

    def open_to_zone_popup(self, instance):
        app = App.get_running_app()
        user_name = str(app.user_real_name).strip().lower()

        to_counts = Counter()
        for task in self.raw_all_tasks:
            status = str(t(task, "상태")).strip()
            assignee = str(t(task, "작업 담당자")).strip().lower()
            if self.active_main_tab == "PENDING":
                if status != "대기" or assignee != "":
                    continue
            else:
                if status != "작업중" or assignee != user_name:
                    continue

            loc = str(t(task, "보충로케이션")).strip().upper()
            if loc:
                to_counts[f"{loc[0]}존"] += 1

        def apply_to_zones(selected_set):
            self.selected_to_zones = selected_set
            if "전체" in selected_set or not selected_set:
                self.btn_to_zone.text = "이동: 전체"
            else:
                zones_str = ",".join(sorted(selected_set)).replace("존", "")
                self.btn_to_zone.text = f"이동: {zones_str}"
            self.apply_filters_and_render()

        dropdown = ZoneMultiSelectDropDown(
            dict(sorted(to_counts.items())), self.selected_to_zones, apply_to_zones
        )
        dropdown.open(instance)

    def toggle_sort_order(self, instance):
        self.sort_asc = not self.sort_asc
        self.btn_sort.text = "▲" if self.sort_asc else "▼"
        self.apply_filters_and_render()

    def toggle_filter_panel(self, instance=None):
        self.is_filter_expanded = not self.is_filter_expanded
        if self.is_filter_expanded:
            if self.filter_panel not in self.layout.children:
                target_idx = len(self.layout.children) - 2
                self.layout.add_widget(self.filter_panel, index=target_idx)
            self._update_filter_button_text("닫기 ▲")
        else:
            if self.filter_panel in self.layout.children:
                self.layout.remove_widget(self.filter_panel)
            self._update_filter_button_text("열기 ▼")

    def _update_filter_button_text(self, arrow):
        tab_str = "대기작업" if self.active_main_tab == "PENDING" else "내 작업"
        eq_str = (
            "전체"
            if self.active_equip_filter == "ALL"
            else (
                "오더피커"
                if self.active_equip_filter == "ORDERPICKER"
                else "리치"
            )
        )
        self.btn_toggle_filter.text = (
            f"🔍 필터 설정 {arrow} ({tab_str} / {eq_str})"
        )

    def on_enter(self):
        app = App.get_running_app()
        if not app.user_real_name:
            app.user_real_name = app.load_saved_user_name() or ""
            if not app.user_real_name:
                self.manager.current = "name_entry"
                return

        self.active_main_tab = "PENDING"
        self.active_equip_filter = "ALL"
        self.btn_tab_pending.set_active_visual(True)
        self.btn_tab_my.set_active_visual(False)
        self.btn_eq_all.set_active_visual(True)
        self.btn_eq_op.set_active_visual(False)
        self.btn_eq_reach.set_active_visual(False)

        self.is_filter_expanded = True
        if self.filter_panel not in self.layout.children:
            target_idx = len(self.layout.children) - 2
            self.layout.add_widget(self.filter_panel, index=target_idx)
        self._update_filter_button_text("닫기 ▲")

        self.fetch_data()

    def handle_barcode_scan(self, barcode):
        clean_bc = str(barcode).strip().upper()
        app = App.get_running_app()
        user_name = str(app.user_real_name).strip().lower()

        my_matches = [
            t_item
            for t_item in self.raw_all_tasks
            if str(t(t_item, "상태")).strip() == "작업중"
            and str(t(t_item, "작업 담당자")).strip().lower() == user_name
            and str(
                t(t_item, "상품바코드", t(t_item, "바코드", ""))
            ).strip().upper()
            == clean_bc
        ]

        if my_matches:
            if self.active_main_tab != "MY":
                self.switch_main_tab("MY")
            target_task = my_matches[0]
            task_list_screen = self.manager.get_screen("task_list")
            dummy_card = type(
                "DummyCard", (), {"task_data": target_task}
            )()
            task_list_screen.open_quantity_popup(dummy_card, card_ref=self)
        else:
            pending_matches = [
                t_item
                for t_item in self.raw_all_tasks
                if str(t(t_item, "상태")).strip() == "대기"
                and str(
                    t(t_item, "상품바코드", t(t_item, "바코드", ""))
                ).strip().upper()
                == clean_bc
            ]
            if pending_matches:
                task_id = t(pending_matches[0], "작업ID")
                self.checked_task_ids.add(task_id)
                self.apply_filters_and_render()
                app.show_info_popup(
                    "스캔 알림",
                    f"['내 작업' 목록에 없는 상품입니다]\n대기 목록의 [{clean_bc}] 항목이 체크 선택되었습니다.\n하단의 [할당받기]를 먼저 눌러주세요.",
                )
            else:
                app.show_info_popup(
                    "스캔 오류",
                    f"스캔한 바코드 [{clean_bc}] 에 해당하는 작업을 찾을 수 없습니다.",
                )

    def fetch_data(self):
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_fetch_data, daemon=True).start()

    def _async_fetch_data(self):
        try:
            tasks = get_sheet_data(TASK_SHEET_NAME, force_refresh=True)
            self.raw_all_tasks = tasks
            Clock.schedule_once(lambda dt: self.apply_filters_and_render())
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def switch_main_tab(self, tab_mode):
        self.active_main_tab = tab_mode
        self.btn_tab_pending.set_active_visual(tab_mode == "PENDING")
        self.btn_tab_my.set_active_visual(tab_mode == "MY")
        self.checked_task_ids.clear()
        self.chk_all.active = False

        if tab_mode == "MY":
            self.btn_main_action.text = "↩ 선택 항목 일괄 반납 (0)"
            self.btn_main_action.set_bg_color(get_color_from_hex("#FF7043"))
        else:
            self.btn_main_action.text = "+ 선택 항목 할당받기 (0)"
            self.btn_main_action.set_bg_color(PRIMARY_BLUE)

        self._update_filter_button_text(
            "닫기 ▲" if self.is_filter_expanded else "열기 ▼"
        )
        self.apply_filters_and_render()

    def switch_equip_filter(self, eq_mode):
        self.active_equip_filter = eq_mode
        self.btn_eq_all.set_active_visual(eq_mode == "ALL")
        self.btn_eq_op.set_active_visual(eq_mode == "ORDERPICKER")
        self.btn_eq_reach.set_active_visual(eq_mode == "REACH")
        self._update_filter_button_text(
            "닫기 ▲" if self.is_filter_expanded else "열기 ▼"
        )
        self.apply_filters_and_render()

    def on_urgent_check_change(self, checkbox, value):
        self.only_urgent = value
        self.apply_filters_and_render()

    def toggle_card_check(self, task_data, is_checked):
        task_id = t(task_data, "작업ID")
        if is_checked:
            self.checked_task_ids.add(task_id)
        else:
            self.checked_task_ids.discard(task_id)

        action_prefix = (
            "↩ 선택 항목 일괄 반납"
            if self.active_main_tab == "MY"
            else "+ 선택 항목 할당받기"
        )
        self.btn_main_action.text = (
            f"{action_prefix} ({len(self.checked_task_ids)})"
        )

    def on_check_all_change(self, checkbox, value):
        self.rv.data = [{**item, "is_checked": value} for item in self.rv.data]
        self.rv.refresh_from_data()
        if value:
            for item in self.rv.data:
                self.checked_task_ids.add(t(item["task_data"], "작업ID"))
        else:
            self.checked_task_ids.clear()

        action_prefix = (
            "↩ 선택 항목 일괄 반납"
            if self.active_main_tab == "MY"
            else "+ 선택 항목 할당받기"
        )
        self.btn_main_action.text = (
            f"{action_prefix} ({len(self.checked_task_ids)})"
        )

    def apply_filters_and_render(self):
        app = App.get_running_app()
        user_name = str(app.user_real_name).strip().lower()

        eq_all_tot, eq_all_urg = 0, 0
        eq_op_tot, eq_op_urg = 0, 0
        eq_reach_tot, eq_reach_urg = 0, 0

        for task in self.raw_all_tasks:
            status = str(t(task, "상태")).strip()
            assignee = str(t(task, "작업 담당자")).strip().lower()

            if self.active_main_tab == "PENDING":
                if status != "대기" or assignee != "":
                    continue
            else:
                if status != "작업중" or assignee != user_name:
                    continue

            equip = str(t(task, "장비")).strip()
            is_urg = t(task, "긴급여부") == "Y"

            eq_all_tot += 1
            if is_urg:
                eq_all_urg += 1

            if equip == "오더피커":
                eq_op_tot += 1
                if is_urg:
                    eq_op_urg += 1
            elif equip == "리치":
                eq_reach_tot += 1
                if is_urg:
                    eq_reach_urg += 1

        self.btn_eq_all.markup = True
        self.btn_eq_all.text = f"전체 ({eq_all_tot} / [color=D32F2F]{eq_all_urg}[/color])"

        self.btn_eq_op.markup = True
        self.btn_eq_op.text = f"오더피커 ({eq_op_tot} / [color=D32F2F]{eq_op_urg}[/color])"

        self.btn_eq_reach.markup = True
        self.btn_eq_reach.text = f"리치 ({eq_reach_tot} / [color=D32F2F]{eq_reach_urg}[/color])"

        filtered_list = []
        for task in self.raw_all_tasks:
            status = str(t(task, "상태")).strip()
            assignee = str(t(task, "작업 담당자")).strip().lower()
            equip = str(t(task, "장비")).strip()

            if self.active_main_tab == "PENDING":
                if status != "대기" or assignee != "":
                    continue
            else:
                if status != "작업중" or assignee != user_name:
                    continue

            if (
                self.active_equip_filter == "ORDERPICKER"
                and equip != "오더피커"
            ):
                continue
            if self.active_equip_filter == "REACH" and equip != "리치":
                continue

            from_loc = str(t(task, "기존로케이션")).strip().upper()
            to_loc = str(t(task, "보충로케이션")).strip().upper()

            if "전체" not in self.selected_from_zones:
                from_zone = f"{from_loc[0]}존" if from_loc else ""
                if from_zone not in self.selected_from_zones:
                    continue

            if "전체" not in self.selected_to_zones:
                to_zone = f"{to_loc[0]}존" if to_loc else ""
                if to_zone not in self.selected_to_zones:
                    continue

            if self.only_urgent and t(task, "긴급여부") != "Y":
                continue

            filtered_list.append(task)

        filtered_list.sort(
            key=lambda x: (
                t(x, "긴급여부") != "Y",
                t(x, "기존로케이션", ""),
            ),
            reverse=not self.sort_asc,
        )

        rv_items = []
        is_my_mode = self.active_main_tab == "MY"
        for task in filtered_list:
            task_id = t(task, "작업ID")
            rv_items.append(
                {
                    "task_data": task,
                    "is_claimed": is_my_mode,
                    "is_checked": (task_id in self.checked_task_ids),
                    "card_screen": self,
                }
            )

        self.rv.data = rv_items
        self.rv.refresh_from_data()

        tab_name = "대기 작업" if not is_my_mode else "내 작업"
        eq_name = (
            "전체"
            if self.active_equip_filter == "ALL"
            else (
                "오더피커"
                if self.active_equip_filter == "ORDERPICKER"
                else "리치"
            )
        )
        self.lbl_status_count.text = (
            f"{tab_name} ({eq_name}) : {len(filtered_list)}건"
        )

    def handle_main_action(self, instance):
        if self.active_main_tab == "PENDING":
            self.claim_checked_tasks(instance)
        else:
            self.batch_return_checked_tasks(instance)

    def claim_checked_tasks(self, instance):
        if not self.checked_task_ids:
            App.get_running_app().show_info_popup(
                "알림", "할당받을 작업을 선택해주세요."
            )
            return
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_claim_tasks, daemon=True).start()

    def _async_claim_tasks(self):
        try:
            app = App.get_running_app()
            sheet = get_worksheet(TASK_SHEET_NAME)
            
            all_rows = execute_with_retry(sheet.get, "A:AA")
            if not all_rows or len(all_rows) < 2:
                raise Exception("시트 데이터를 불러올 수 없습니다.")

            headers = [str(h).strip() for h in all_rows[0]]
            assignee_col = headers.index("작업 담당자") + 1
            status_col = headers.index("상태") + 1

            cells_to_update = []
            already_taken_count = 0

            for row_idx, row in enumerate(all_rows[1:], start=2):
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                
                row_dict = {headers[i]: row[i] for i in range(len(headers))}
                task_id = str(t(row_dict, "작업ID")).strip()

                if task_id in self.checked_task_ids:
                    curr_status = str(t(row_dict, "상태")).strip()
                    curr_assignee = str(t(row_dict, "작업 담당자", t(row_dict, "담당자", ""))).strip()

                    if curr_status in ["대기", ""] and curr_assignee == "":
                        cells_to_update.append(
                            gspread.Cell(row_idx, assignee_col, app.user_real_name)
                        )
                        cells_to_update.append(
                            gspread.Cell(row_idx, status_col, "작업중")
                        )
                    else:
                        already_taken_count += 1

            if cells_to_update:
                sheet.update_cells(cells_to_update)

            invalidate_cache(TASK_SHEET_NAME)
            self.checked_task_ids.clear()

            if already_taken_count > 0 and len(cells_to_update) == 0:
                Clock.schedule_once(
                    lambda dt: app.show_info_popup(
                        "할당 실패", "선택하신 작업이 이미 다른 작업자에게 할당되었습니다.\n목록을 자동으로 갱신합니다."
                    )
                )
            elif already_taken_count > 0:
                Clock.schedule_once(
                    lambda dt: app.show_info_popup(
                        "부분 할당 완료", f"이미 다른 사용자가 가져간 {already_taken_count}건을 제외하고 할당되었습니다."
                    )
                )
            else:
                Clock.schedule_once(lambda dt: self.on_claim_success())

            Clock.schedule_once(lambda dt: self.fetch_data())

        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def on_claim_success(self):
        App.get_running_app().show_info_popup(
            "성공", "선택한 작업이 '내 작업'으로 할당되었습니다."
        )
        self.switch_main_tab("MY")

    def batch_return_checked_tasks(self, instance):
        if not self.checked_task_ids:
            App.get_running_app().show_info_popup(
                "알림", "반납할 작업을 선택해주세요."
            )
            return
        App.get_running_app().show_confirmation_popup(
            "일괄 반납 확인",
            f"선택한 {len(self.checked_task_ids)}건의 작업을 반납하시겠습니까?",
            lambda: self._start_async_batch_return(),
        )

    def _start_async_batch_return(self):
        App.get_running_app().show_loading_popup()
        threading.Thread(
            target=self._async_batch_return, daemon=True
        ).start()

    def _async_batch_return(self):
        try:
            sheet = get_worksheet(TASK_SHEET_NAME)
            all_rows = execute_with_retry(sheet.get, "A:AA")
            if not all_rows or len(all_rows) < 2:
                raise Exception("시트 데이터를 불러올 수 없습니다.")

            headers = [str(h).strip() for h in all_rows[0]]
            assignee_col = headers.index("작업 담당자") + 1
            status_col = headers.index("상태") + 1
            task_id_col = headers.index("작업ID") + 1

            all_ids = sheet.col_values(task_id_col)
            cells_to_update = []

            for task_id in self.checked_task_ids:
                if task_id in all_ids:
                    row_idx = all_ids.index(task_id) + 1
                    cells_to_update.append(
                        gspread.Cell(row_idx, assignee_col, "")
                    )
                    cells_to_update.append(
                        gspread.Cell(row_idx, status_col, "대기")
                    )

            if cells_to_update:
                sheet.update_cells(cells_to_update)

            for task in self.raw_all_tasks:
                if t(task, "작업ID") in self.checked_task_ids:
                    task["상태"] = "대기"
                    task["작업 담당자"] = ""

            invalidate_cache(TASK_SHEET_NAME)
            self.checked_task_ids.clear()

            Clock.schedule_once(
                lambda dt: App.get_running_app().show_info_popup(
                    "성공", "선택한 작업이 일괄 반납되었습니다."
                )
            )
            Clock.schedule_once(lambda dt: self.apply_filters_and_render())
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def handle_my_task_action(self, action_name, task_data):
        task_list_screen = self.manager.get_screen("task_list")
        dummy_card = type("DummyCard", (), {"task_data": task_data})()

        if action_name == "return":
            task_list_screen.return_task(dummy_card)
        elif action_name == "qty":
            task_list_screen.open_quantity_popup(dummy_card, card_ref=self)
        elif action_name == "fail":
            task_list_screen.process_failure(dummy_card)
        elif action_name == "remarks":
            task_list_screen.prompt_for_remarks(dummy_card)
        elif action_name == "complete":
            App.get_running_app().current_list_type = "보충인원"
            task_list_screen.process_task(dummy_card)


# --- 검수 및 액션 처리 전용 화면 ---
class TaskListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_tasks_data = []

    def on_enter(self, *args):
        app = App.get_running_app()
        if not app.user_real_name:
            app.user_real_name = app.load_saved_user_name() or ""
            if not app.user_real_name:
                self.manager.current = "name_entry"
                return
        self.refresh_list(force_refresh=True)

    def refresh_list(self, force_refresh=True):
        App.get_running_app().show_loading_popup()
        threading.Thread(
            target=self._perform_get_tasks,
            args=(force_refresh,),
            daemon=True,
        ).start()

    def _perform_get_tasks(self, force_refresh):
        try:
            all_tasks = get_sheet_data(
                TASK_SHEET_NAME, force_refresh=force_refresh
            )
            filtered_task_data = [
                task
                for task in all_tasks
                if str(t(task, "상태")).strip() == "보충완료"
            ]

            task_map = {
                t(task, "작업ID"): (i + 2, task)
                for i, task in enumerate(all_tasks)
            }
            my_tasks = [
                {
                    "task_data": task,
                    "task_screen": self,
                    "row_index": task_map.get(t(task, "작업ID"), (0, None))[0],
                }
                for task in filtered_task_data
                if t(task, "작업ID") in task_map
            ]

            self.all_tasks_data = my_tasks
            Clock.schedule_once(lambda dt: self.update_recycle_view())
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def update_recycle_view(self):
        query = (
            self.ids.search_input.text.strip().lower()
            if "search_input" in self.ids
            else ""
        )
        filtered_data = []
        for item in self.all_tasks_data:
            task = item["task_data"]
            product_name = str(t(task, "상품명", "")).lower()
            barcode = str(
                t(task, "상품바코드", t(task, "바코드", ""))
            ).lower()
            if not query or query in product_name or query in barcode:
                filtered_data.append(item)

        if hasattr(self.ids, "task_list_rv"):
            self.ids.task_list_rv.data = filtered_data
            self.ids.task_list_rv.refresh_from_data()

    def search_tasks(self, instance=None):
        self.update_recycle_view()

    def handle_barcode_scan(self, barcode):
        matches = [
            item
            for item in self.all_tasks_data
            if str(
                t(item["task_data"], "상품바코드", t(item["task_data"], "바코드", ""))
            ).strip().upper()
            == barcode
        ]
        if not matches:
            App.get_running_app().show_info_popup(
                "알림", f"스캔한 바코드[{barcode}]는 검수 대상 목록에 없습니다."
            )
            return
        if len(matches) == 1:
            self.open_task_from_scan(matches[0])
        else:
            MultipleSkuSelectPopup(
                matches=matches, on_select=self.open_task_from_scan
            ).open()

    def open_task_from_scan(self, item_data):
        dummy_card = type(
            "DummyCard", (), {"task_data": item_data["task_data"]}
        )()
        InspectionPopup(card=dummy_card, task_list_screen=self).open()

    def return_task(self, card):
        App.get_running_app().show_confirmation_popup(
            "작업 반납",
            "이 작업을 반납하시겠습니까?",
            lambda: self._perform_return(card),
        )

    def _perform_return(self, card):
        App.get_running_app().show_loading_popup()
        threading.Thread(
            target=self._async_return, args=(card,), daemon=True
        ).start()

    def _async_return(self, card):
        try:
            sheet = get_worksheet(TASK_SHEET_NAME)
            task_id = str(t(card.task_data, "작업ID"))
            headers = sheet.row_values(1)
            row_idx = (
                sheet.col_values(headers.index("작업ID") + 1).index(task_id) + 1
            )
            sheet.update_cells(
                [
                    gspread.Cell(row_idx, headers.index("상태") + 1, "대기"),
                    gspread.Cell(
                        row_idx, headers.index("작업 담당자") + 1, ""
                    ),
                ]
            )
            invalidate_cache(TASK_SHEET_NAME)
            Clock.schedule_once(
                lambda dt: self.on_action_success("작업이 반납되었습니다.")
            )
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def open_quantity_popup(self, card, card_ref=None):
        ordered_qty = str(t(card.task_data, "지시수량", "0")).strip()
        existing_conf_qty = str(card.task_data.get("confirmed_quantity", "")).strip()
        initial_val = (
            existing_conf_qty if existing_conf_qty.isdigit() else ordered_qty
        )

        def on_confirm_qty(text):
            val = text.strip()
            if val.isdigit():
                task_id = t(card.task_data, "작업ID")
                
                if card_ref and hasattr(card_ref, "raw_all_tasks"):
                    for task in card_ref.raw_all_tasks:
                        if t(task, "작업ID") == task_id:
                            task["confirmed_quantity"] = val
                            task["확인수량"] = val
                            break

                card.task_data["confirmed_quantity"] = val
                card.task_data["확인수량"] = val

                if card_ref and hasattr(card_ref, "apply_filters_and_render"):
                    card_ref.apply_filters_and_render()

                App.get_running_app().show_info_popup(
                    "알림", f"수량 '{val}'(이)가 임시 저장되었습니다."
                )
            else:
                App.get_running_app().show_info_popup(
                    "오류", "숫자만 입력해야 합니다."
                )

        open_native_korean_input(
            "확인 수량 입력", "수량 입력", initial_val, on_confirm_qty, is_number=True
        )

    def prompt_for_remarks(self, card):

        def on_confirm_rem(text):
            if not text.strip():
                return
            app = App.get_running_app()
            ts = datetime.now().strftime("%y-%m-%d %H:%M")
            formatted = f"[{ts} {app.user_real_name}] {text.strip()}"
            curr = card.task_data.get(
                "remarks_text", t(card.task_data, "비고", "")
            )
            card.task_data["remarks_text"] = (
                f"{curr}\n{formatted}" if curr else formatted
            )
            app.show_info_popup("알림", "비고가 추가되었습니다.")

        open_native_korean_input("비고 추가", "비고 내용 입력", "", on_confirm_rem)

    def process_failure(self, card):

        def on_confirm_fail(reason):
            if not reason.strip():
                return
            app = App.get_running_app()
            updates = {
                "상태": "보충실패",
                "실패사유": reason.strip(),
                "보충담당자": app.user_real_name,
                "완료일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            app.show_loading_popup()
            threading.Thread(
                target=self._perform_update,
                args=(card, updates, "보충 실패 처리 되었습니다."),
                daemon=True,
            ).start()

        open_native_korean_input("실패 사유 입력", "사유 입력", "", on_confirm_fail)

    def process_task(self, card):
        app = App.get_running_app()

        if app.current_list_type == "검수인원":
            InspectionPopup(card=card, task_list_screen=self).open()
            return

        qty_val = str(
            card.task_data.get("confirmed_quantity", t(card.task_data, "확인수량", ""))
        ).strip()
        if not qty_val.isdigit() or int(qty_val) == 0:
            app.show_info_popup(
                "입력 오류",
                "수량입력 버튼을 눌러 확인 수량을 먼저 입력해주세요.",
            )
            return

        conf_q = int(qty_val)
        card.task_data["확인수량"] = conf_q

        self._finalize_task_processing(
            card,
            conf_q,
            0,
            None,
            card.task_data.get("remarks_text", t(card.task_data, "비고", "")),
        )

    def _start_print_job(self, card_data):
        try:
            app = App.get_running_app()
            default_printer = app.load_default_printer()
            if not default_printer:
                return

            qty_per_box = safe_int(t(card_data, "박스입수량", t(card_data, "박스 입수량", 0)))
            prod_name = str(t(card_data, "상품명", ""))
            is_invoice_only = qty_per_box == 1 or "송장" in prod_name

            label_info = {
                "바코드": str(t(card_data, "상품바코드", t(card_data, "바코드", "N/A"))),
                "출고 로케이션": str(t(card_data, "보충로케이션", "N/A")),
                "긴급여부": (t(card_data, "긴급여부") == "Y"),
                "송장전용": is_invoice_only,
            }
            threading.Thread(
                target=self._print_thread,
                args=(default_printer, label_info, 1),
                daemon=True,
            ).start()
        except Exception as e:
            print(f"🔴 프린터 작업 에러 무시됨: {e}")

    def _print_thread(self, address, label_info, quantity):
        try:
            printer = BluetoothPrinter(address)
            if printer.connect():
                try:
                    printer.print_outbound_label_cpcl(label_info, quantity)
                except Exception:
                    pass
                finally:
                    printer.disconnect()
        except Exception as e:
            print(f"🔴 블루투스 인쇄 실패: {e}")

    def _finalize_task_processing(
        self, card, final_qty, split_qty, final_location, updated_remarks
    ):
        app = App.get_running_app()

        if app.current_list_type == "검수인원":
            updates = {
                "상태": "최종완료",
                "검수담당자": app.user_real_name,
                "최종완료일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "확인수량": str(final_qty),
                "비고": updated_remarks,
                "최종적치위치": final_location,
            }
            app.show_loading_popup()
            threading.Thread(
                target=self._perform_update,
                args=(card, updates, "검수 작업이 '최종완료' 처리 되었습니다."),
                daemon=True,
            ).start()
            return

        updates = {
            "상태": "보충완료",
            "보충담당자": app.user_real_name,
            "완료일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "확인수량": str(final_qty),
            "비고": updated_remarks,
        }

        def run_sheet_update():
            app.show_loading_popup()
            threading.Thread(
                target=self._perform_update,
                args=(card, updates, "보충완료 처리 되었습니다."),
                daemon=True,
            ).start()

        def on_yes_print():
            try:
                self._start_print_job(card.task_data)
            except Exception:
                pass
            run_sheet_update()

        app.show_confirmation_popup(
            title="인쇄 및 완료",
            message="[color=ffffff]보충완료 처리합니다.\n라벨 1장을 인쇄하시겠습니까?[/color]",
            on_yes=on_yes_print,
            on_no=run_sheet_update,
        )

    def _perform_update(self, card, updates, msg):
        try:
            sheet = get_worksheet(TASK_SHEET_NAME)
            headers = [str(h).strip() for h in sheet.row_values(1)]
            task_id = str(t(card.task_data, "작업ID"))

            task_id_col_idx = headers.index("작업ID") + 1
            all_task_ids = sheet.col_values(task_id_col_idx)

            if task_id not in all_task_ids:
                raise Exception(f"작업ID [{task_id}]를 시트에서 찾을 수 없습니다.")

            row_idx = all_task_ids.index(task_id) + 1
            cells = []

            for key, val in updates.items():
                if key in headers:
                    col_idx = headers.index(key) + 1
                    cells.append(gspread.Cell(row_idx, col_idx, str(val)))

            if cells:
                sheet.update_cells(cells)

            invalidate_cache(TASK_SHEET_NAME)
            Clock.schedule_once(lambda dt: self.on_action_success(msg))
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def on_action_success(self, msg):
        App.get_running_app().dismiss_loading_popup()
        App.get_running_app().show_info_popup("성공", msg)

        def _safe_refresh_ui(dt):
            try:
                app = App.get_running_app()
                if app and app.root:
                    curr_screen = app.root.current_screen
                    if hasattr(curr_screen, "fetch_data"):
                        curr_screen.fetch_data()
                    elif hasattr(curr_screen, "refresh_list"):
                        curr_screen.refresh_list(force_refresh=True)
            except Exception as e:
                print(f"🔴 UI 리프레시 예외 무시: {e}")

        Clock.schedule_once(_safe_refresh_ui, 0.2)


class AdminDashboardScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_tasks = []
        self.layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )

        top_bar = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
        top_bar.add_widget(
            StyledButton(
                text="< 메인",
                size_hint_x=0.2,
                bg_color=get_color_from_hex("#78909C"),
                on_press=lambda x: setattr(self.manager, "current", "main_menu"),
            )
        )
        top_bar.add_widget(
            Label(
                text="전체 작업 현황판",
                font_name=FONT_NAME,
                font_size=dp(18),
                bold=True,
                color=TEXT_DARK,
            )
        )
        top_bar.add_widget(
            StyledButton(
                text="갱신", size_hint_x=0.2, on_press=lambda x: self.refresh()
            )
        )
        self.layout.add_widget(top_bar)

        search_bar = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
        self.search_input = TextInput(
            hint_text="터치하여 바코드/SKU 검색",
            multiline=False,
            font_name=FONT_NAME,
            font_size=dp(15),
            size_hint_x=0.8,
            readonly=True,
        )
        self.search_input.bind(on_touch_down=self.on_search_touch)

        btn_search = StyledButton(
            text="검색", size_hint_x=0.2, font_size=dp(14)
        )
        btn_search.bind(on_press=self.search_tasks)

        search_bar.add_widget(self.search_input)
        search_bar.add_widget(btn_search)
        self.layout.add_widget(search_bar)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def on_search_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            def set_query(val):
                self.search_input.text = val
                self.search_tasks()

            open_native_korean_input(
                "검색어 입력", "바코드 또는 SKU 검색", self.search_input.text, set_query
            )
            return True
        return False

    def on_enter(self):
        app = App.get_running_app()
        if not app.user_real_name:
            app.user_real_name = app.load_saved_user_name() or ""
            if not app.user_real_name:
                self.manager.current = "name_entry"
                return

        self.search_input.text = ""
        self.grid.clear_widgets()
        self.grid.add_widget(
            Label(
                text="바코드를 스캔하거나 입력 후 검색해 주세요.",
                font_name=FONT_NAME,
                font_size=dp(15),
                color=TEXT_MUTED,
                size_hint_y=None,
                height=dp(100),
            )
        )

        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_fetch_all, daemon=True).start()

    def refresh(self, instance=None):
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_fetch_all, daemon=True).start()

    def _async_fetch_all(self):
        try:
            tasks = get_sheet_data(TASK_SHEET_NAME, force_refresh=True)
            self.all_tasks = tasks
            Clock.schedule_once(lambda dt: self.search_tasks())
        except Exception as e:
            Clock.schedule_once(
                lambda dt, err=str(e): App.get_running_app().show_info_popup(
                    "오류", str(err)
                )
            )
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def handle_barcode_scan(self, barcode):
        self.search_input.text = barcode
        self.search_tasks()

    def search_tasks(self, instance=None):
        query = self.search_input.text.strip().lower()
        self.grid.clear_widgets()

        if not query:
            self.grid.add_widget(
                Label(
                    text="바코드를 스캔하거나 입력 후 검색해 주세요.",
                    font_name=FONT_NAME,
                    font_size=dp(15),
                    color=TEXT_MUTED,
                    size_hint_y=None,
                    height=dp(100),
                )
            )
            return

        matches = []
        for task in self.all_tasks:
            bc = (
                str(t(task, "상품바코드", t(task, "바코드", "")))
                .strip()
                .lower()
            )
            if query in bc:
                matches.append(task)

        if not matches:
            self.grid.add_widget(
                Label(
                    text=f"검색어 [{query}] 에 해당하는 작업 건이 없습니다.",
                    font_name=FONT_NAME,
                    font_size=dp(14),
                    color=TEXT_MUTED,
                    size_hint_y=None,
                    height=dp(100),
                )
            )
            return

        for task in matches:
            self.grid.add_widget(self._create_dashboard_card(task))

    def _create_dashboard_card(self, task):
        status = str(t(task, "상태", "미지정")).strip()
        is_urgent = t(task, "긴급여부") == "Y"

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(110),
            padding=dp(10),
            spacing=dp(4),
        )
        with card.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(10)]
            )
        card.bind(
            pos=lambda i, p: setattr(i.canvas.before.children[-1], "pos", p),
            size=lambda i, s: setattr(i.canvas.before.children[-1], "size", s),
        )

        top_row = BoxLayout(size_hint_y=None, height=dp(25))
        st_color = (
            "[color=3366ff]"
            if status == "작업중"
            else (
                "[color=00897B]"
                if status in ["보충완료", "최종완료"]
                else "[color=757575]"
            )
        )
        urg_tag = "[color=D32F2F][긴급][/color] " if is_urgent else ""

        lbl_prod = Label(
            text=f"{st_color}[b][{status}][/b][/color] {urg_tag}{t(task, '상품명')}",
            font_name=FONT_NAME,
            font_size=dp(14),
            markup=True,
            halign="left",
        )
        lbl_prod.bind(size=lambda i, s: setattr(i, "text_size", s))
        top_row.add_widget(lbl_prod)
        card.add_widget(top_row)

        lbl_info = Label(
            text=f"바코드: {t(task, '상품바코드', t(task, '바코드'))} | {t(task, '기존로케이션')} ➔ {t(task, '보충로케이션')}",
            font_name=FONT_NAME,
            font_size=dp(13),
            color=TEXT_DARK,
            halign="left",
        )
        lbl_info.bind(size=lambda i, s: setattr(i, "text_size", s))
        card.add_widget(lbl_info)

        raw_time = str(
            t(task, "최종완료일시", t(task, "완료일시", ""))
        ).strip()
        time_str = ""
        if status in ["최종완료", "완료"] and raw_time:
            time_str = f" | [color=2E7D32][b]완료시간: {raw_time}[/b][/color]"

        assignee = t(
            task,
            "검수담당자",
            t(task, "보충담당자", t(task, "작업 담당자", "미할당")),
        )
        lbl_sub = Label(
            text=f"담당: {assignee} / 수량: {t(task, '확인수량', t(task, '지시수량', 0))}{time_str}",
            font_name=FONT_NAME,
            font_size=dp(12),
            color=TEXT_MUTED,
            markup=True,
            halign="left",
        )
        lbl_sub.bind(size=lambda i, s: setattr(i, "text_size", s))
        card.add_widget(lbl_sub)

        return card


class CompletedHistoryScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        top = BoxLayout(size_hint_y=None, height=dp(45))
        top.add_widget(
            StyledButton(
                text="< 메인",
                size_hint_x=0.2,
                bg_color=get_color_from_hex("#78909C"),
                on_press=lambda x: setattr(self.manager, "current", "main_menu"),
            )
        )
        top.add_widget(
            Label(
                text="금일 완료 이력",
                font_name=FONT_NAME,
                font_size=dp(18),
                bold=True,
                color=TEXT_DARK,
            )
        )
        layout.add_widget(top)
        self.add_widget(layout)


class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        header = BoxLayout(size_hint_y=None, height=dp(45))
        header.add_widget(
            StyledButton(
                text="< 메인",
                size_hint_x=0.2,
                bg_color=get_color_from_hex("#78909C"),
                on_press=lambda x: setattr(self.manager, "current", "main_menu"),
            )
        )
        header.add_widget(
            Label(
                text="프린터 설정",
                font_name=FONT_NAME,
                font_size=dp(18),
                bold=True,
                color=TEXT_DARK,
            )
        )
        layout.add_widget(header)
        layout.add_widget(
            StyledButton(
                text="프린터 연결 설정",
                size_hint_y=None,
                height=dp(55),
                on_press=lambda x: Factory.PrinterSettingsPopup().open(),
            )
        )
        self.add_widget(layout)


class PrinterSettingsPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "프린터 설정"
        self.title_font = FONT_NAME
        self.size_hint = (0.9, None)
        self.height = dp(350)
        self.auto_dismiss = False
        self.found_devices = {}
        layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        self.current_lbl = Label(
            text="현재 프린터: "
            + (App.get_running_app().load_default_printer() or "미설정"),
            font_name=FONT_NAME,
        )
        layout.add_widget(self.current_lbl)
        self.spinner = StyledSpinner(
            text="기기를 선택하세요",
            font_name=FONT_NAME,
            option_cls=KoreanSpinnerOption,
            size_hint_y=None,
            height=dp(45),
        )
        layout.add_widget(self.spinner)

        btn_scan = StyledButton(
            text="주변 기기 검색",
            on_press=self.scan_devices,
            size_hint_y=None,
            height=dp(45),
        )
        btn_save = StyledButton(
            text="기본 프린터로 저장",
            on_press=self.save_printer,
            size_hint_y=None,
            height=dp(45),
        )
        btn_close = StyledButton(
            text="닫기",
            on_press=self.dismiss,
            size_hint_y=None,
            height=dp(45),
            bg_color=(0.6, 0.6, 0.6, 1),
        )
        layout.add_widget(btn_scan)
        layout.add_widget(btn_save)
        layout.add_widget(btn_close)
        self.content = layout

    def scan_devices(self, instance):
        if platform != "android" or not autoclass:
            return
        try:
            adapter = autoclass(
                "android.bluetooth.BluetoothAdapter"
            ).getDefaultAdapter()
            if not adapter.isEnabled():
                return
            self.found_devices.clear()
            for dev in adapter.getBondedDevices().toArray():
                self.found_devices[dev.getName()] = dev.getAddress()
            self.spinner.values = (
                list(self.found_devices.keys())
                if self.found_devices
                else ["페어링된 기기 없음"]
            )
        except Exception:
            pass

    def save_printer(self, instance):
        name = self.spinner.text
        if name in self.found_devices:
            App.get_running_app().save_default_printer(
                self.found_devices[name]
            )
            self.current_lbl.text = "현재 프린터: " + self.found_devices[name]
            self.dismiss()


class BluetoothPrinter:

    def __init__(self, device_address):
        self.mac_address = device_address
        self.socket = None
        self.stream = None

    def connect(self):
        if platform != "android":
            return False

        for attempt in range(2):
            try:
                BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
                UUID = autoclass("java.util.UUID")
                device = BluetoothAdapter.getDefaultAdapter().getRemoteDevice(
                    self.mac_address
                )
                spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                self.socket = device.createRfcommSocketToServiceRecord(spp_uuid)
                self.socket.connect()
                self.stream = self.socket.getOutputStream()
                time.sleep(0.3)
                return True
            except Exception as e:
                print(f"⚠️ 블루투스 연결 시도 {attempt + 1}회 실패: {e}")
                self.disconnect()
                time.sleep(0.5)
        return False

    def disconnect(self):
        try:
            if self.stream:
                self.stream.close()
        except Exception:
            pass
        try:
            if self.socket:
                self.socket.close()
        except Exception:
            pass
        self.stream = None
        self.socket = None

    def print_outbound_label_cpcl(self, label_info: dict, quantity: int):
        if not self.stream:
            return False

        try:
            barcode_suffix = label_info.get("바코드", "N/A")[-6:]
            loc_raw = label_info.get("출고 로케이션", "N/A")
            loc1 = loc_raw.split("-", 1)[0] if "-" in loc_raw else loc_raw
            loc2 = loc_raw.split("-", 1)[1] if "-" in loc_raw else ""

            is_urgent = label_info.get("긴급여부", False)
            is_invoice_only = label_info.get("송장전용", False)

            tag_str = ""
            if is_urgent:
                tag_str += "[긴급건] "
            if is_invoice_only:
                tag_str += "[송장만]"

            cmd = f"! 0 200 200 800 {quantity}\r\nLEFT\r\nSETMAG 2 2\r\nTEXT 4 1 20 50 {barcode_suffix}\r\n"
            if tag_str:
                cmd += f"RIGHT\r\nSETMAG 2 2\r\nTEXT 4 1 500 50 {tag_str}\r\nLEFT\r\n"

            cmd += f"LINE 20 150 556 150 4\r\nCENTER\r\nSETMAG 4 4\r\nTEXT 4 1 0 220 {loc1}\r\nSETMAG 3 3\r\nTEXT 4 1 0 410 {loc2}\r\nSETMAG 1 1\r\nFORM\r\nPRINT\r\n"

            self.stream.write(cmd.encode("cp949"))
            self.stream.flush()
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"🔴 CPCL 전송 중 에러: {e}")
            return False
        finally:
            self.disconnect()


Builder.load_string(
    """
<TaskListScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(10)
            
            StyledButton:
                text: '< 메인'
                size_hint_x: 0.25
                on_press: root.manager.current = 'main_menu'
            Label:
                text: '검수 목록 보기'
                size_hint_x: 0.5
                font_name: app.FONT_NAME
                font_size: dp(18)
                bold: True
                color: (0.1, 0.1, 0.1, 1)
            StyledButton:
                text: '새로고침'
                size_hint_x: 0.25
                on_press: root.refresh_list(True)

        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(5)
            TextInput:
                id: search_input
                hint_text: 'SKU명 또는 바코드 검색'
                multiline: False
                font_name: app.FONT_NAME
                size_hint_x: 0.8
                on_text_validate: root.search_tasks()
            StyledButton:
                text: '검색'
                size_hint_x: 0.2
                on_press: root.search_tasks()

        RecycleView:
            id: task_list_rv
            viewclass: 'UnifiedTaskCard'
            RecycleBoxLayout:
                default_size: None, dp(205)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: dp(8)

<UnifiedTaskCard>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: dp(10)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: root.card_bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]

    BoxLayout:
        size_hint_y: None
        height: dp(26)
        spacing: dp(5)
        Label:
            id: lbl_equip
            font_name: app.FONT_NAME
            font_size: dp(14)
            halign: 'left'
            valign: 'middle'
            markup: True
            size_hint_x: 0.35
            text_size: self.width, None
        Label:
            id: lbl_stock_info
            font_name: app.FONT_NAME
            font_size: dp(12)
            color: (0.3, 0.3, 0.3, 1)
            halign: 'right'
            valign: 'middle'
            markup: True
            size_hint_x: 0.55
            text_size: self.width, None
        CheckBox:
            id: box_check
            size_hint_x: None
            width: dp(30)
            color: (0.12, 0.53, 0.9, 1)
            on_active: root.on_checkbox_active(self, self.active)

    Label:
        id: lbl_product
        font_name: app.FONT_NAME
        font_size: dp(15)
        color: (0,0,0,1)
        halign: 'left'
        valign: 'middle'
        markup: True
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]

    BoxLayout:
        size_hint_y: None
        height: dp(18)
        Label:
            id: lbl_barcode
            font_name: app.FONT_NAME
            font_size: dp(12)
            color: (0.4, 0.4, 0.4, 1)
            halign: 'left'
            text_size: self.width, None

    BoxLayout:
        size_hint_y: None
        height: dp(25)
        Label:
            id: lbl_loc
            font_name: app.FONT_NAME
            font_size: dp(16)
            bold: True
            markup: True
            halign: 'left'
            text_size: self.width, None

    BoxLayout:
        size_hint_y: None
        height: dp(26)
        Label:
            id: lbl_main_qty
            font_name: app.FONT_NAME
            font_size: dp(18)
            bold: True
            halign: 'left'
            valign: 'middle'
            markup: True
            color: (0.12, 0.53, 0.9, 1)
            text_size: self.width, None

    BoxLayout:
        size_hint_y: None
        height: dp(18)
        Label:
            id: lbl_box_info
            font_name: app.FONT_NAME
            font_size: dp(12)
            color: (0.3, 0.3, 0.3, 1)
            markup: True
            halign: 'left'
            text_size: self.width, None

    GridLayout:
        id: btn_action_box
        cols: 5
        size_hint_y: None
        height: dp(40)
        spacing: dp(4)
        opacity: 0
        disabled: True

        StyledButton:
            text: "반납"
            font_size: dp(12)
            bg_color: (0.9, 0.6, 0, 1)
            on_press: root.handle_card_btn('return')
        StyledButton:
            text: "수량입력"
            font_size: dp(12)
            on_press: root.handle_card_btn('qty')
        StyledButton:
            text: "실패"
            font_size: dp(12)
            bg_color: (1, 0.3, 0.3, 1)
            on_press: root.handle_card_btn('fail')
        StyledButton:
            text: "비고"
            font_size: dp(12)
            on_press: root.handle_card_btn('remarks')
        StyledButton:
            text: "완료"
            font_size: dp(12)
            bg_color: (0.1, 0.8, 0.5, 1)
            on_press: root.handle_card_btn('complete')
"""
)

Factory.register("PrinterSettingsPopup", cls=PrinterSettingsPopup)


class MainApp(App):
    FONT_NAME = FONT_NAME

    def build(self):
        self.user_real_name = self.load_saved_user_name() or ""
        self.current_list_type = None
        self.loading_popup = LoadingPopup()
        self._scan_buffer = ""
        self._last_keystroke_time = 0
        self.last_known_pending_task_ids = set()

        Window.bind(on_key_down=self._on_keyboard_down)

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(NameEntryScreen(name="name_entry"))
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(UnifiedReplenishScreen(name="unified_replenish"))
        sm.add_widget(TaskListScreen(name="task_list"))
        sm.add_widget(AdminDashboardScreen(name="admin_dashboard"))
        sm.add_widget(CompletedHistoryScreen(name="completed_history"))
        sm.add_widget(SettingsScreen(name="settings"))

        if self.user_real_name:
            sm.current = "main_menu"

        return sm

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifier):
        try:
            kb = getattr(window, "_system_keyboard", None)
            focused_widget = getattr(kb, "widget", None) if kb else None
            if focused_widget is not None and isinstance(focused_widget, TextInput):
                return False
        except Exception:
            pass

        current_time = time.time()
        if current_time - self._last_keystroke_time > 0.25:
            self._scan_buffer = ""
        self._last_keystroke_time = current_time

        if key in [13, 40]:
            if self._scan_buffer:
                self.process_global_scan(self._scan_buffer)
                self._scan_buffer = ""
            return True

        if codepoint and 32 <= ord(codepoint) <= 126:
            self._scan_buffer += codepoint
        return False

    def on_start(self):
        threading.Thread(target=initialize_gspread, daemon=True).start()
        Clock.schedule_interval(self.check_for_new_tasks, 30)

        if platform == "android":
            try:
                request_permissions(
                    [
                        Permission.POST_NOTIFICATIONS,
                        Permission.BLUETOOTH_SCAN,
                        Permission.BLUETOOTH_CONNECT,
                        Permission.BLUETOOTH_ADMIN,
                        Permission.ACCESS_FINE_LOCATION,
                    ]
                )
            except Exception as e:
                print(f"🔴 권한 요청 오류: {e}")

    def check_for_new_tasks(self, *args):
        if self.root and any(
            isinstance(w, NotificationBanner) for w in Window.children
        ):
            return
        threading.Thread(target=self._perform_task_check, daemon=True).start()

    def _perform_task_check(self):
        try:
            all_tasks = get_sheet_data(TASK_SHEET_NAME, force_refresh=True)

            pending_tasks = [
                task
                for task in all_tasks
                if str(t(task, "상태")).strip() == "대기"
            ]
            current_pending_task_ids = {
                str(t(task, "작업ID")) for task in pending_tasks
            }

            if not self.last_known_pending_task_ids:
                if self.root and self.root.current != "name_entry":
                    self.last_known_pending_task_ids = current_pending_task_ids
                return

            new_task_ids = (
                current_pending_task_ids - self.last_known_pending_task_ids
            )

            if new_task_ids:
                new_tasks = [
                    task
                    for task in pending_tasks
                    if str(t(task, "작업ID")) in new_task_ids
                ]
                if new_tasks:
                    Clock.schedule_once(
                        lambda dt: self.show_notification_banner(new_tasks)
                    )

            self.last_known_pending_task_ids = current_pending_task_ids
        except Exception as e:
            print(f"⚠️ 신규 작업 알림 확인 중 에러 (무시): {e}")

    def play_notification_sound(self):
        if platform != "android":
            return
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            RingtoneManager = autoclass("android.media.RingtoneManager")
            context = PythonActivity.mActivity.getApplicationContext()
            notification_uri = RingtoneManager.getDefaultUri(
                RingtoneManager.TYPE_NOTIFICATION
            )
            if notification_uri:
                ringtone = RingtoneManager.getRingtone(
                    context, notification_uri
                )
                ringtone.play()
        except Exception as e:
            print(f"🔴 시스템 소리 재생 예외: {e}")

    def show_notification_banner(self, new_tasks):
        if not self.root or self.root.current == "name_entry":
            return

        self.play_notification_sound()

        has_urgent = any(t(task, "긴급여부") == "Y" for task in new_tasks)
        equipment_counts = defaultdict(int)
        for task in new_tasks:
            equip = t(task, "장비", "기타")
            equipment_counts[equip] += 1

        summary_parts = [
            f"{eq} {num}건" for eq, num in equipment_counts.items()
        ]
        summary_text = ", ".join(summary_parts)

        message = "새로운 "
        if has_urgent:
            message += "[color=FF3333][긴급][/color] "
        message += f"작업 발생: {summary_text}"

        def go_to_replenish_screen():
            if self.root:
                self.root.current = "unified_replenish"

        banner = NotificationBanner(
            text=message, on_press_callback=go_to_replenish_screen
        )
        banner.show(Window)

    def process_global_scan(self, barcode):
        clean_barcode = re.sub(r'[\r\n\t]', '', str(barcode)).strip()
        if self.root and clean_barcode:
            curr_screen = self.root.current_screen
            if hasattr(curr_screen, "handle_barcode_scan"):
                curr_screen.handle_barcode_scan(clean_barcode)

    def get_config_path(self):
        return "user_config.json"

    def save_user_name(self, name):
        try:
            with open(self.get_config_path(), "w") as f:
                json.dump({"user_name": name}, f)
        except Exception:
            pass

    def load_saved_user_name(self):
        path = self.get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f).get("user_name")
            except Exception:
                None
        return None

    def save_default_printer(self, address):
        try:
            with open("printer_config.json", "w") as f:
                json.dump({"default_printer": address}, f)
        except Exception:
            pass

    def load_default_printer(self):
        if os.path.exists("printer_config.json"):
            try:
                with open("printer_config.json", "r") as f:
                    return json.load(f).get("default_printer")
            except Exception:
                None
        return None

    def show_loading_popup(self):
        if not self.loading_popup.parent:
            self.loading_popup.open()

    def dismiss_loading_popup(self):
        self.loading_popup.dismiss()

    def show_info_popup(self, title, message):
        InfoPopup(title, message).open()

    def show_confirmation_popup(self, title, message, on_yes, on_no=None):
        popup_content = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(20)
        )
        msg_label = Label(
            text=str(message),
            halign="center",
            valign="middle",
            markup=True,
            color=(1, 1, 1, 1),
            size_hint_y=1,
            font_size=dp(18),
            font_name=FONT_NAME,
        )
        msg_label.bind(size=msg_label.setter("text_size"))
        button_layout = BoxLayout(
            size_hint_y=None, height=dp(45), spacing=dp(10)
        )
        btn_yes = StyledButton(text="예")
        btn_no = StyledButton(text="아니오")
        button_layout.add_widget(btn_yes)
        button_layout.add_widget(btn_no)
        popup_content.add_widget(msg_label)
        popup_content.add_widget(button_layout)
        popup = Popup(
            title=title,
            title_font=FONT_NAME,
            content=popup_content,
            size_hint=(0.8, None),
            height=dp(280),
            auto_dismiss=False,
            background_color=(0.3, 0.3, 0.3, 0.95),
        )

        def yes_action(instance):
            popup.dismiss()
            if on_yes:
                Clock.schedule_once(lambda dt: on_yes(), 0.1)

        def no_action(instance):
            popup.dismiss()
            if on_no:
                Clock.schedule_once(lambda dt: on_no(), 0.1)

        btn_yes.bind(on_press=yes_action)
        btn_no.bind(on_press=no_action)
        popup.open()


if __name__ == "__main__":
    MainApp().run()
