# -*- coding: utf-8 -*-
import json
import os
import re
import ssl
import sys
import threading
import time
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta

# 💡 메인 운영 Raw 주소 및 버전 세팅
UPDATE_CHECK_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/version.txt"
UPDATE_CODE_URL = "https://raw.githubusercontent.com/hmyang-crypto/hm-rep/refs/heads/main/main.py"
CURRENT_VERSION = "2.0.0"


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

import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = "replacement-463907-07ae6e152f37.json"
SPREADSHEET_NAME = "보충시트"
USER_SHEET_NAME = "사용자_목록"
TASK_SHEET_NAME = "보충작업_지시서"
LOG_SHEET_NAME = "작업완료_로그"
RETURN_TASK_SHEET_NAME = "원복작업_지시서"
RETURN_LOG_SHEET_NAME = "원복작업_로그"
FCM_TOKEN_SHEET_NAME = "FCM_토큰"
LOCATION_CAPA_SHEET_NAME = "로케이션별재고 raw"

RETURN_DRIVE_FOLDER_ID = "1_EafaL8qZ-g8nYGxDvhhpROIUHZmwFRJ"

SHEET_RANGES = {
    USER_SHEET_NAME: "A:AZ",
    TASK_SHEET_NAME: "A:AZ",
    LOG_SHEET_NAME: "A:AZ",
    RETURN_TASK_SHEET_NAME: "A:Z",
    RETURN_LOG_SHEET_NAME: "A:Z",
    FCM_TOKEN_SHEET_NAME: "A:AZ",
    LOCATION_CAPA_SHEET_NAME: "A:J",
}

try:
    LabelBase.register(name="Nanum", fn_regular="NanumSquareRoundEB.ttf")
    FONT_NAME = "Nanum"
except Exception:
    FONT_NAME = "Roboto"

PRIMARY_BLUE = get_color_from_hex("#1E88E5")
LIGHT_BLUE = get_color_from_hex("#E3F2FD")
FILTER_BG_GRAY = get_color_from_hex("#CFD8DC")
BG_GRAY = get_color_from_hex("#F4F7FA")
TEXT_DARK = get_color_from_hex("#212121")
TEXT_MUTED = get_color_from_hex("#757575")

Window.clearcolor = BG_GRAY
g_recent_completed_tasks = []


def safe_int(val, default=0):
    if val is None:
        return default
    try:
        clean_str = re.sub(r"[^\d]", "", str(val))
        return int(clean_str) if clean_str else default
    except Exception:
        return default


def get_barcode_from_task(task_dict):
    for key in ["상품바코드", "바코드", "상품 바코드", "BARCODE", "Barcode"]:
        val = task_dict.get(key)
        if val and str(val).strip():
            return str(val).strip()
    return "N/A"


def t(d, k, default=""):
    return d.get(k, default) if isinstance(d, dict) else default


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
                time.sleep(base_delay * (2**attempt))
            else:
                raise e
        except Exception as e:
            raise e
    raise Exception("🚨 구글 API 트래픽 초과 오류 누적")


def invalidate_cache(sheet_name):
    g_cached_sheets.pop(sheet_name, None)
    g_cache_timestamps.pop(sheet_name, None)


def initialize_gspread():
    global g_sheet_client, g_spreadsheet, GSPREAD_LOADED, GSPREAD_ERROR_MSG
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        GSPREAD_LOADED = False
        GSPREAD_ERROR_MSG = f"키 파일 없음: '{SERVICE_ACCOUNT_FILE}'"
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

    ws = execute_with_retry(g_spreadsheet.worksheet, worksheet_name)
    g_worksheet_objects[worksheet_name] = ws
    return ws


def get_sheet_data(sheet_name, force_refresh=False):
    now = time.time()
    if (
        not force_refresh
        and (now - g_cache_timestamps.get(sheet_name, 0)) < CACHE_DURATION
    ):
        if sheet_name in g_cached_sheets:
            return g_cached_sheets[sheet_name]
    try:
        sheet = get_worksheet(sheet_name)
        target_range = SHEET_RANGES.get(sheet_name, "A:Z")
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


def upload_photo_to_drive_async(
    file_path, file_name, task_id, sheet_name, callback_success=None
):
    def _async_upload():
        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            scope = ["https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                SERVICE_ACCOUNT_FILE, scope
            )
            drive_service = build("drive", "v3", credentials=creds)

            file_metadata = {
                "name": file_name,
                "parents": [RETURN_DRIVE_FOLDER_ID],
            }
            media = MediaFileUpload(
                file_path, mimetype="image/jpeg", resumable=True
            )
            uploaded_file = (
                drive_service.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    fields="id, webViewLink",
                )
                .execute()
            )

            web_link = uploaded_file.get(
                "webViewLink",
                f"https://drive.google.com/file/d/{uploaded_file.get('id')}/view",
            )

            sheet = get_worksheet(sheet_name)
            headers = [str(h).strip() for h in sheet.row_values(1)]
            if "사진" in headers and "작업ID" in headers:
                task_id_col = headers.index("작업ID") + 1
                photo_col = headers.index("사진") + 1
                all_ids = sheet.col_values(task_id_col)
                if task_id in all_ids:
                    row_idx = all_ids.index(task_id) + 1
                    sheet.update_cell(row_idx, photo_col, web_link)
                    invalidate_cache(sheet_name)

            if callback_success:
                Clock.schedule_once(lambda dt: callback_success(web_link))
        except Exception as e:
            print(f"🔴 사진 업로드 오류: {e}")

    threading.Thread(target=_async_upload, daemon=True).start()


class LoadingPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "처리 중"
        self.title_font = FONT_NAME
        self.content = Label(
            text="데이터를 처리 중입니다...",
            font_name=FONT_NAME,
            font_size=dp(16),
        )
        self.size_hint = (0.8, 0.3)
        self.auto_dismiss = False


class InfoPopup(Popup):

    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.title_font = FONT_NAME
        self.size_hint = (0.85, 0.4)
        content = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(10)
        )
        content.add_widget(
            Label(
                text=str(message),
                font_name=FONT_NAME,
                font_size=dp(14),
                halign="center",
            )
        )
        ok_button = StyledButton(
            text="확인", size_hint_y=None, height=dp(40)
        )
        ok_button.bind(on_press=self.dismiss)
        content.add_widget(ok_button)
        self.content = content


# --- 원복 전용 카드 UI ---
class ReturnTaskCard(RecycleDataViewBehavior, BoxLayout):
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
        is_unassigned = t(self.task_data, "지정구분", "") == "미지정"

        if is_urgent:
            self.card_bg_color = get_color_from_hex("#FFCDD2")
        elif is_unassigned:
            self.card_bg_color = get_color_from_hex("#FFF9C4")
        else:
            self.card_bg_color = [1, 1, 1, 1]

        raw_equip = str(t(self.task_data, "장비", ""))
        display_tag = (
            f"[color=D32F2F][{raw_equip}][/color]" if raw_equip else ""
        )
        client_name = str(t(self.task_data, "고객사", "")).strip()
        client_tag = (
            f" [color=555555][{client_name}][/color]" if client_name else ""
        )

        self.ids.lbl_equip.text = f"[b]{display_tag}{client_tag}[/b]"

        req_qty = safe_int(t(self.task_data, "지시수량", 0))
        product_name = t(self.task_data, "상품명", "N/A")
        assign_type = t(self.task_data, "지정구분", "지정")

        tag_prefix = f"[color=2E7D32][원복-{assign_type}][/color] "
        if is_urgent:
            tag_prefix += "[color=D32F2F][긴급][/color] "

        self.ids.lbl_product.text = f"[b]{tag_prefix}{product_name}[/b]"
        self.ids.lbl_barcode.text = (
            f"바코드: {get_barcode_from_task(self.task_data)}"
        )

        raw_target_loc = str(t(self.task_data, "원복로케이션", "")).strip()
        target_loc = raw_target_loc if raw_target_loc else "[자율적치/QR스캔]"
        actual_scanned_loc = str(t(self.task_data, "최종적치", "")).strip() or "-"

        self.ids.lbl_loc.text = f"목표: [color=D32F2F]{target_loc}[/color] ➔ 실적: [color=1E88E5]{actual_scanned_loc}[/color]"

        conf_qty_val = self.task_data.get(
            "confirmed_quantity", t(self.task_data, "확인수량", "")
        )
        active_count = (
            safe_int(conf_qty_val, 0) if str(conf_qty_val).isdigit() else 0
        )

        if self.is_claimed:
            self.ids.lbl_main_qty.text = (
                f"원복지시: {req_qty} / [color=D32F2F]확인 {active_count}[/color]"
            )
        else:
            self.ids.lbl_main_qty.text = f"원복지시: [b]{req_qty}[/b]"

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
            self.card_screen.handle_return_task_action(
                action_name, self.task_data
            )


# --- 원복 작업 메인 컨트롤 화면 ---
class ReturnReplenishScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_main_tab = "PENDING"
        self.raw_all_tasks = []
        self.raw_inventory = []
        self.checked_task_ids = set()

        self.layout = BoxLayout(
            orientation="vertical", padding=dp(8), spacing=dp(4)
        )

        header = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(6))
        btn_back = StyledButton(
            text="< 메인",
            size_hint_x=0.18,
            bg_color=get_color_from_hex("#78909C"),
        )
        btn_back.bind(
            on_press=lambda x: setattr(self.manager, "current", "main_menu")
        )

        lbl_title = Label(
            text="🔄 원복 작업 컨트롤",
            font_name=FONT_NAME,
            font_size=dp(15),
            bold=True,
            color=TEXT_DARK,
        )

        btn_refresh = StyledButton(
            text="갱신", size_hint_x=0.20, font_size=dp(12)
        )
        btn_refresh.bind(on_press=lambda x: self.fetch_data())

        header.add_widget(btn_back)
        header.add_widget(lbl_title)
        header.add_widget(btn_refresh)
        self.layout.add_widget(header)

        main_tab_box = BoxLayout(
            size_hint_y=None, height=dp(36), spacing=dp(5)
        )
        self.btn_tab_pending = StyledToggleButton(
            text="원복 대기", group="return_tab", state="down", size_hint_x=0.5
        )
        self.btn_tab_pending.bind(
            on_press=lambda x: self.switch_main_tab("PENDING")
        )

        self.btn_tab_my = StyledToggleButton(
            text="내 원복작업", group="return_tab", state="normal", size_hint_x=0.5
        )
        self.btn_tab_my.bind(on_press=lambda x: self.switch_main_tab("MY"))

        main_tab_box.add_widget(self.btn_tab_pending)
        main_tab_box.add_widget(self.btn_tab_my)
        self.layout.add_widget(main_tab_box)

        list_header = BoxLayout(
            size_hint_y=None, height=dp(26), padding=(dp(5), 0)
        )
        self.lbl_status_count = Label(
            text="원복 대기 : 0건",
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
        lbl_chk_all = Label(
            text="전체선택",
            font_name=FONT_NAME,
            font_size=dp(12),
            color=TEXT_DARK,
            size_hint_x=None,
            width=dp(55),
        )

        list_header.add_widget(self.lbl_status_count)
        list_header.add_widget(self.chk_all)
        list_header.add_widget(lbl_chk_all)
        self.layout.add_widget(list_header)

        self.rv = RecycleView()
        self.rv_layout = RecycleBoxLayout(
            default_size=(None, dp(218)),
            default_size_hint=(1, None),
            size_hint_y=None,
            orientation="vertical",
            spacing=dp(8),
        )
        self.rv_layout.bind(minimum_height=self.rv_layout.setter("height"))
        self.rv.add_widget(self.rv_layout)
        self.rv.viewclass = "ReturnTaskCard"
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

    def on_enter(self):
        self.fetch_data()

    def fetch_data(self):
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_fetch_data, daemon=True).start()

    def _async_fetch_data(self):
        try:
            tasks = get_sheet_data(RETURN_TASK_SHEET_NAME, force_refresh=True)
            inventory = get_sheet_data(
                LOCATION_CAPA_SHEET_NAME, force_refresh=False
            )
            self.raw_all_tasks = tasks
            self.raw_inventory = inventory
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
        self.checked_task_ids.clear()
        self.chk_all.active = False

        if tab_mode == "MY":
            self.btn_main_action.text = "↩ 선택 항목 일괄 반납 (0)"
            self.btn_main_action.set_bg_color(get_color_from_hex("#FF7043"))
        else:
            self.btn_main_action.text = "+ 선택 항목 할당받기 (0)"
            self.btn_main_action.set_bg_color(PRIMARY_BLUE)

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

        filtered_list = []
        for task in self.raw_all_tasks:
            status = str(t(task, "상태")).strip()
            assignee = (
                str(
                    t(
                        task,
                        "보충담당자",
                        t(task, "작업자", t(task, "작업 담당자", "")),
                    )
                )
                .strip()
                .lower()
            )

            if self.active_main_tab == "PENDING":
                if status != "대기" or assignee != "":
                    continue
            else:
                if status != "작업중" or assignee != user_name:
                    continue

            filtered_list.append(task)

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

        tab_name = "원복 대기" if not is_my_mode else "내 원복작업"
        self.lbl_status_count.text = f"{tab_name} : {len(filtered_list)}건"

    def handle_main_action(self, instance):
        if self.active_main_tab == "PENDING":
            self.claim_checked_tasks(instance)
        else:
            self.batch_return_checked_tasks(instance)

    def claim_checked_tasks(self, instance):
        if not self.checked_task_ids:
            App.get_running_app().show_info_popup(
                "알림", "할당받을 원복 작업을 선택해주세요."
            )
            return
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_claim_tasks, daemon=True).start()

    def _async_claim_tasks(self):
        try:
            app = App.get_running_app()
            sheet = get_worksheet(RETURN_TASK_SHEET_NAME)
            all_rows = execute_with_retry(sheet.get, "A:Z")
            headers = [str(h).strip() for h in all_rows[0]]

            assignee_col = 14
            for target_name in ["보충담당자", "작업자", "작업 담당자"]:
                if target_name in headers:
                    assignee_col = headers.index(target_name) + 1
                    break

            status_col = headers.index("상태") + 1 if "상태" in headers else 2

            cells_to_update = []
            for row_idx, row in enumerate(all_rows[1:], start=2):
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                row_dict = {headers[i]: row[i] for i in range(len(headers))}
                task_id = str(t(row_dict, "작업ID")).strip()

                if task_id in self.checked_task_ids:
                    cells_to_update.append(
                        gspread.Cell(row_idx, assignee_col, app.user_real_name)
                    )
                    cells_to_update.append(
                        gspread.Cell(row_idx, status_col, "작업중")
                    )

            if cells_to_update:
                sheet.update_cells(cells_to_update)

            invalidate_cache(RETURN_TASK_SHEET_NAME)
            self.checked_task_ids.clear()
            Clock.schedule_once(
                lambda dt: app.show_toast("원복 작업이 할당되었습니다.")
            )
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

    def batch_return_checked_tasks(self, instance):
        if not self.checked_task_ids:
            App.get_running_app().show_info_popup(
                "알림", "반납할 작업을 선택해주세요."
            )
            return
        App.get_running_app().show_loading_popup()
        threading.Thread(target=self._async_batch_return, daemon=True).start()

    def _async_batch_return(self):
        try:
            sheet = get_worksheet(RETURN_TASK_SHEET_NAME)
            all_rows = execute_with_retry(sheet.get, "A:Z")
            headers = [str(h).strip() for h in all_rows[0]]

            assignee_col = 14
            for target_name in ["보충담당자", "작업자", "작업 담당자"]:
                if target_name in headers:
                    assignee_col = headers.index(target_name) + 1
                    break

            status_col = headers.index("상태") + 1 if "상태" in headers else 2

            cells_to_update = []
            for row_idx, row in enumerate(all_rows[1:], start=2):
                row_dict = {
                    headers[i]: row[i]
                    for i in range(min(len(headers), len(row)))
                }
                task_id = str(t(row_dict, "작업ID")).strip()
                if task_id in self.checked_task_ids:
                    cells_to_update.append(
                        gspread.Cell(row_idx, assignee_col, "")
                    )
                    cells_to_update.append(
                        gspread.Cell(row_idx, status_col, "대기")
                    )

            if cells_to_update:
                sheet.update_cells(cells_to_update)

            invalidate_cache(RETURN_TASK_SHEET_NAME)
            self.checked_task_ids.clear()
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

    def handle_return_task_action(self, action_name, task_data):
        if action_name == "complete":
            ReturnExecutionPopup(
                task_data=task_data, return_screen=self
            ).open()


# --- 원복 적치 및 사진 촬영 수행 팝업 ---
class ReturnExecutionPopup(Popup):

    def __init__(self, task_data, return_screen, **kwargs):
        super().__init__(**kwargs)
        self.task_data = task_data
        self.return_screen = return_screen
        self.title = "원복 적치 & 사진 촬영"
        self.title_font = FONT_NAME
        self.size_hint = (0.95, 0.9)
        self.auto_dismiss = False

        self.scanned_barcode = ""
        self.scanned_location = ""
        self.photo_file_path = None

        main_layout = BoxLayout(
            orientation="vertical", padding=dp(10), spacing=dp(8)
        )

        prod_name = t(task_data, "상품명", "N/A")
        client_name = t(task_data, "고객사", "")
        assign_type = t(task_data, "지정구분", "지정")
        raw_target_loc = str(t(task_data, "원복로케이션", "")).strip()
        target_loc = raw_target_loc if raw_target_loc else "[자율적치/QR스캔]"

        lbl_info = Label(
            text=f"[b][{client_name}] {prod_name}[/b]\n목표 로케이션: [color=D32F2F][b]{target_loc}[/b][/color] ({assign_type})",
            font_name=FONT_NAME,
            font_size=dp(14),
            markup=True,
            size_hint_y=None,
            height=dp(40),
            halign="left",
        )
        lbl_info.bind(size=lambda i, s: setattr(i, "text_size", s))
        main_layout.add_widget(lbl_info)

        if assign_type == "미지정":
            dist_text = self._get_client_location_distribution(client_name)
            lbl_guide = Label(
                text=f"💡 [color=1E88E5][b]{client_name}[/b] 주요 보관 존 분포:[/color]\n{dist_text}",
                font_name=FONT_NAME,
                font_size=dp(12),
                markup=True,
                size_hint_y=None,
                height=dp(45),
            )
            lbl_guide.bind(size=lambda i, s: setattr(i, "text_size", s))
            main_layout.add_widget(lbl_guide)

        self.lbl_bc_status = Label(
            text="1. 상품 바코드: [color=D32F2F]미스캔[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            halign="left",
            size_hint_y=None,
            height=dp(25),
        )
        self.lbl_bc_status.bind(size=lambda i, s: setattr(i, "text_size", s))
        main_layout.add_widget(self.lbl_bc_status)

        self.lbl_loc_status = Label(
            text="2. 적치 로케이션 QR: [color=D32F2F]미스캔[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            halign="left",
            size_hint_y=None,
            height=dp(25),
        )
        self.lbl_loc_status.bind(size=lambda i, s: setattr(i, "text_size", s))
        main_layout.add_widget(self.lbl_loc_status)

        qty_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        qty_box.add_widget(
            Label(
                text="원복 확인수량:", font_name=FONT_NAME, font_size=dp(13)
            )
        )
        self.input_qty = TextInput(
            text=str(t(task_data, "지시수량", "1")),
            multiline=False,
            input_type="number",
            font_name=FONT_NAME,
            font_size=dp(16),
            halign="center",
        )
        qty_box.add_widget(self.input_qty)
        main_layout.add_widget(qty_box)

        self.lbl_photo_status = Label(
            text="3. 증적 사진: [color=D32F2F]미촬영[/color]",
            font_name=FONT_NAME,
            font_size=dp(13),
            markup=True,
            halign="left",
            size_hint_y=None,
            height=dp(25),
        )
        self.lbl_photo_status.bind(size=lambda i, s: setattr(i, "text_size", s))
        main_layout.add_widget(self.lbl_photo_status)

        btn_photo = StyledButton(
            text="📷 적치 상태 사진 촬영하기",
            size_hint_y=None,
            height=dp(45),
            bg_color=get_color_from_hex("#00897B"),
        )
        btn_photo.bind(on_press=self.take_photo)
        main_layout.add_widget(btn_photo)

        btn_grid = GridLayout(
            cols=2, size_hint_y=None, height=dp(45), spacing=dp(10)
        )
        btn_cancel = StyledButton(text="취소", bg_color=(0.6, 0.6, 0.6, 1))
        btn_cancel.bind(on_press=self.dismiss)

        btn_submit = StyledButton(text="원복 최종 완료", bg_color=PRIMARY_BLUE)
        btn_submit.bind(on_press=self.submit_completion)

        btn_grid.add_widget(btn_cancel)
        btn_grid.add_widget(btn_submit)
        main_layout.add_widget(btn_grid)

        self.content = main_layout

    def _get_client_location_distribution(self, client_name):
        if not client_name or not self.return_screen.raw_inventory:
            return "정보 없음"
        zone_counts = Counter()
        for row in self.return_screen.raw_inventory:
            c = str(t(row, "고객사", t(row, "화주사", ""))).strip()
            loc = str(t(row, "로케이션", "")).strip().upper()
            if c == client_name and loc:
                zone_counts[f"{loc[0]}존"] += safe_int(
                    t(row, "로케이션 수량", 1)
                )

        top_zones = zone_counts.most_common(2)
        if not top_zones:
            return "보관 재고 존 정보 없음"
        return " / ".join([f"• {z}: {cnt}개" for z, cnt in top_zones])

    def take_photo(self, instance):
        date_str = datetime.now().strftime("%Y%m%d")
        bc = get_barcode_from_task(self.task_data)
        loc = self.scanned_location or "NOLOC"
        file_name = f"{date_str}_{bc}_{loc}.jpg"

        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.photo_file_path = os.path.join(app_dir, file_name)

        try:
            with open(self.photo_file_path, "wb") as f:
                f.write(b"IMAGE_DATA")
            self.lbl_photo_status.text = (
                f"3. 증적 사진: [color=2E7D32]촬영 완료 ({file_name})[/color]"
            )
            App.get_running_app().show_toast("사진이 준비되었습니다.")
        except Exception as e:
            App.get_running_app().show_info_popup("오류", f"사진 저장 오류: {e}")

    def submit_completion(self, instance):
        app = App.get_running_app()
        target_bc = get_barcode_from_task(self.task_data)
        target_loc = str(t(self.task_data, "원복로케이션", "")).strip()
        assign_type = t(self.task_data, "지정구분", "지정")

        if not self.scanned_barcode:
            app.show_info_popup("검증 오류", "상품 바코드를 먼저 스캔해주세요.")
            return

        if self.scanned_barcode != target_bc:
            app.show_info_popup(
                "바코드 불일치 🚨",
                f"스캔한 바코드[{self.scanned_barcode}]가 대상[{target_bc}]과 일치하지 않습니다.",
            )
            return

        if not self.scanned_location:
            app.show_info_popup("검증 오류", "적치 로케이션 QR을 스캔해주세요.")
            return

        if (
            assign_type == "지정"
            and target_loc
            and self.scanned_location != target_loc
        ):
            app.show_info_popup(
                "로케이션 불일치 🚨",
                f"지정된 위치[{target_loc}]와 스캔한 위치[{self.scanned_location}]가 다릅니다!",
            )
            return

        if not self.photo_file_path or not os.path.exists(self.photo_file_path):
            app.show_info_popup(
                "사진 필요", "적치 상태 증적 사진을 촬영해야 합니다."
            )
            return

        conf_qty = self.input_qty.text.strip()
        if not conf_qty.isdigit():
            app.show_info_popup("오류", "확인 수량은 숫자로 입력해주세요.")
            return

        task_id = t(self.task_data, "작업ID")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%Y%m%d")
        photo_name = f"{date_str}_{target_bc}_{self.scanned_location}.jpg"

        updates = {
            "상태": "원복완료",
            "보충담당자": app.user_real_name,
            "작업자": app.user_real_name,  # X열(작업자) 업데이트
            "최종적치": self.scanned_location,
            "확인수량": conf_qty,
            "완료일시": now_str,
        }

        app.show_loading_popup()

        def _async_finalize():
            try:
                sheet = get_worksheet(RETURN_TASK_SHEET_NAME)
                headers = [str(h).strip() for h in sheet.row_values(1)]
                task_id_col = headers.index("작업ID") + 1
                all_ids = sheet.col_values(task_id_col)

                if task_id in all_ids:
                    row_idx = all_ids.index(task_id) + 1
                    cells = []
                    for k, v in updates.items():
                        if k in headers:
                            c_idx = headers.index(k) + 1
                            cells.append(gspread.Cell(row_idx, c_idx, str(v)))
                    if cells:
                        sheet.update_cells(cells)

                try:
                    log_sheet = get_worksheet(RETURN_LOG_SHEET_NAME)
                    log_headers = [
                        str(h).strip() for h in log_sheet.row_values(1)
                    ]
                    full_task = dict(self.task_data)
                    full_task.update(updates)
                    log_row = [str(full_task.get(h, "")) for h in log_headers]
                    log_sheet.append_row(log_row)
                except Exception as log_e:
                    print(f"⚠️ 원복 로그 기록 에러: {log_e}")

                invalidate_cache(RETURN_TASK_SHEET_NAME)
                invalidate_cache(RETURN_LOG_SHEET_NAME)

                upload_photo_to_drive_async(
                    self.photo_file_path,
                    photo_name,
                    task_id,
                    RETURN_TASK_SHEET_NAME,
                )

                Clock.schedule_once(
                    lambda dt: app.show_toast(
                        "원복 작업이 최종 완료되었습니다!"
                    )
                )
                Clock.schedule_once(lambda dt: self.return_screen.fetch_data())

            except Exception as e:
                Clock.schedule_once(
                    lambda dt, err=str(e): app.show_info_popup("오류", str(err))
                )
            finally:
                Clock.schedule_once(lambda dt: app.dismiss_loading_popup())

        threading.Thread(target=_async_finalize, daemon=True).start()
        self.dismiss()


# --- 메인 메뉴 화면 ---
class MainMenuScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(
            orientation="vertical", padding=dp(15), spacing=dp(8)
        )
        self.add_widget(self.layout)

    def on_enter(self, *args):
        self.layout.clear_widgets()
        app = App.get_running_app()

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
        top_bar.add_widget(welcome_box)
        self.layout.add_widget(top_bar)

        menu_box = BoxLayout(
            orientation="vertical", spacing=dp(6), size_hint_y=None
        )
        menu_box.bind(minimum_height=menu_box.setter("height"))

        def create_compact_menu_row(btn_widget):
            row = BoxLayout(size_hint_y=None, height=dp(42))
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

        # 💡 [신규] 원복 작업 버튼
        btn_return = StyledButton(
            text="[원복] 원복 작업",
            bg_color=get_color_from_hex("#D32F2F"),
            size_hint_x=None,
            width=dp(220),
        )
        btn_return.bind(
            on_press=lambda x: setattr(
                self.manager, "current", "return_replenish"
            )
        )
        menu_box.add_widget(create_compact_menu_row(btn_return))

        self.layout.add_widget(menu_box)


# --- [원복 Task Card UI] KV 구문 ---
Builder.load_string(
    """
<ReturnTaskCard>:
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
            size_hint_x: 0.8
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
            font_size: dp(15)
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
            font_size: dp(16)
            bold: True
            halign: 'left'
            valign: 'middle'
            markup: True
            color: (0.12, 0.53, 0.9, 1)
            text_size: self.width, None

    GridLayout:
        id: btn_action_box
        cols: 1
        size_hint_y: None
        height: dp(40)
        opacity: 0
        disabled: True

        StyledButton:
            text: "원복 적치 & 사진촬영 완료"
            font_size: dp(13)
            bg_color: (0.8, 0.2, 0.2, 1)
            on_press: root.handle_card_btn('complete')
"""
)


class MainApp(App):
    FONT_NAME = FONT_NAME

    def build(self):
        self.user_real_name = "테스트작업자"
        self.loading_popup = LoadingPopup()

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(ReturnReplenishScreen(name="return_replenish"))
        sm.current = "main_menu"
        return sm

    def show_loading_popup(self):
        if not self.loading_popup.parent:
            self.loading_popup.open()

    def dismiss_loading_popup(self):
        self.loading_popup.dismiss()

    def show_info_popup(self, title, message):
        InfoPopup(title, message).open()

    def show_toast(self, message):
        print(f"🍞 [TOAST]: {message}")


if __name__ == "__main__":
    MainApp().run()
