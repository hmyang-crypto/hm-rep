# -*- coding: utf-8 -*-
import json
import os
import re
import ssl
import sys
import threading
import time
import urllib.request
from collections import defaultdict, Counter
from datetime import datetime
from functools import partial

UPDATE_CHECK_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/version.txt"
UPDATE_CODE_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/main.py"
CURRENT_VERSION = "1.3.0"


def check_and_apply_update():
    try:
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
    except Exception as e:
        print(f"⚠️ 업데이트 확인 중 오류 (무시하고 앱 실행): {e}")


if "updated_main.py" not in os.path.basename(__file__):
    check_and_apply_update()

    _app_dir = os.path.dirname(os.path.abspath(__file__))
    _updated_script = os.path.join(_app_dir, "updated_main.py")

    if os.path.exists(_updated_script) and __name__ == "__main__":
        try:
            with open(_updated_script, "r", encoding="utf-8") as _f:
                _code = _f.read()
            exec(
                compile(_code, _updated_script, "exec"),
                {"__name__": "__main__", "__file__": _updated_script},
            )
            sys.exit(0)
        except Exception as _exec_err:
            print(f"⚠️ 업데이트 코드 실행 실패: {_exec_err}")

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
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
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
    from jnius import autoclass

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

Window.clearcolor = BG_GRAY


def safe_int(val, default=0):
    if val is None:
        return default
    try:
        clean_str = re.sub(r"[^\d]", "", str(val))
        return int(clean_str) if clean_str else default
    except Exception:
        return default


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


# 💡 [기존 드롭다운 스타일 100% 복원] 체크박스 + 수량 표기 결합 클래스
class ZoneMultiSelectDropDown(DropDown):

    def __init__(self, zone_counts_dict, selected_zones, on_apply, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = True
        self.on_apply = on_apply
        self.checkboxes = {}

        container = BoxLayout(
            orientation="vertical",
            padding=dp(6),
            spacing=dp(4),
            size_hint=(None, None),
            width=dp(200),
        )
        container.bind(minimum_height=container.setter("height"))

        with container.canvas.before:
            Color(0.2, 0.2, 0.2, 0.98)
            self.bg_rect = RoundedRectangle(
                pos=container.pos, size=container.size, radius=[dp(8)]
            )
        container.bind(
            pos=lambda i, p: setattr(self.bg_rect, "pos", p),
            size=lambda i, s: setattr(self.bg_rect, "size", s),
        )

        scroll = ScrollView(size_hint_y=None, height=dp(200))
        grid = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for zone_name, count in zone_counts_dict.items():
            item_box = BoxLayout(
                size_hint_y=None, height=dp(36), spacing=dp(6), padding=(dp(4), 0)
            )
            chk = CheckBox(
                active=(zone_name in selected_zones or "전체" in selected_zones),
                size_hint_x=None,
                width=dp(28),
                color=PRIMARY_BLUE,
            )
            lbl = Label(
                text=f"{zone_name} ({count})",
                font_name=FONT_NAME,
                font_size=dp(13),
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle",
            )
            lbl.bind(size=lambda i, s: setattr(i, "text_size", s))

            item_box.add_widget(chk)
            item_box.add_widget(lbl)
            grid.add_widget(item_box)
            self.checkboxes[zone_name] = chk

        scroll.add_widget(grid)
        container.add_widget(scroll)

        btn_apply = StyledButton(
            text="적용",
            size_hint_y=None,
            height=dp(34),
            font_size=dp(12),
            bg_color=PRIMARY_BLUE,
        )
        btn_apply.bind(on_press=self._on_apply_press)
        container.add_widget(btn_apply)

        self.add_widget(container)

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
    raise Exception("🚨 구글 API 오류로 작업이 최종 실패했습니다.")


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


# --- 올인원 통합 보충 작업 카드 뷰어 ---
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
        display_tag = (
            "[color=0000FF][리치][/color]"
            if raw_equip == "리치"
            else ("[color=1E88E5][오더피커][/color]" if raw_equip == "오더피커" else "")
        )
        self.ids.lbl_equip.text = f"[b]{display_tag}[/b]"

        existing_qty = safe_int(t(self.task_data, "기존수량", 0))
        req_qty = safe_int(t(self.task_data, "지시수량", 0))
        remaining_qty = existing_qty - req_qty
        self.ids.lbl_stock_info.text = f"기존: [b]{existing_qty}[/b]\n보충후: [b][color=1E88E5]{remaining_qty}[/color][/b]"

        qty_per_box = safe_int(
            t(self.task_data, "박스입수량", t(self.task_data, "박스 입수량", 0))
        )
        product_name = t(self.task_data, "상품명", "N/A")

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

        self.ids.box_check.opacity = 1
        self.ids.box_check.disabled = False
        self.ids.box_check.active = self.is_checked


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

        self.filter_panel = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(112),
            spacing=dp(4),
        )

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

        opt_toolbar.add_widget(self.btn_from_zone)
        opt_toolbar.add_widget(self.btn_to_zone)
        self.filter_panel.add_widget(opt_toolbar)
        self.layout.add_widget(self.filter_panel)

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

        self.add_widget(self.layout)

    def open_from_zone_popup(self, instance):
        # 💡 [동적 수량 집계] 보관 로케이션 기반 존별 개수 파싱
        from_counts = Counter()
        for task in self.raw_all_tasks:
            loc = str(t(task, "기존로케이션")).strip().upper()
            if loc:
                from_counts[f"{loc[0]}존"] += 1

        if not from_counts:
            from_counts = Counter({"I존": 0, "J존": 0, "K존": 0})

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
        # 💡 [동적 수량 집계] 이동 로케이션 기반 존별 개수 파싱 (E, F존 자동 대응)
        to_counts = Counter()
        for task in self.raw_all_tasks:
            loc = str(t(task, "보충로케이션")).strip().upper()
            if loc:
                to_counts[f"{loc[0]}존"] += 1

        if not to_counts:
            to_counts = Counter({"A존": 0, "B존": 0, "E존": 0, "F존": 0})

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

    def fetch_data(self):
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_fetch_data, daemon=True).start()

    def _async_fetch_data(self):
        try:
            tasks = get_sheet_data(TASK_SHEET_NAME, force_refresh=True)
            self.raw_all_tasks = tasks
            Clock.schedule_once(lambda dt: self.apply_filters_and_render())
        except Exception as e:
            pass
        finally:
            Clock.schedule_once(
                lambda dt: App.get_running_app().dismiss_loading_popup()
            )

    def apply_filters_and_render(self):
        filtered_list = []
        for task in self.raw_all_tasks:
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

            filtered_list.append(task)

        rv_items = [
            {"task_data": task, "is_claimed": False, "is_checked": False, "card_screen": self}
            for task in filtered_list
        ]
        self.rv.data = rv_items
        self.rv.refresh_from_data()


class MainApp(App):
    FONT_NAME = FONT_NAME

    def build(self):
        self.user_real_name = "테스터"
        self.loading_popup = LoadingPopup()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(UnifiedReplenishScreen(name="unified_replenish"))
        return sm

    def process_global_scan(self, barcode):
        clean_barcode = re.sub(r'[\r\n\t]', '', str(barcode)).strip()
        if self.root and clean_barcode:
            curr_screen = self.root.current_screen
            if hasattr(curr_screen, "handle_barcode_scan"):
                curr_screen.handle_barcode_scan(clean_barcode)

    def show_loading_popup(self):
        if not self.loading_popup.parent:
            self.loading_popup.open()

    def dismiss_loading_popup(self):
        self.loading_popup.dismiss()


if __name__ == "__main__":
    MainApp().run()
