# MIT License

# Copyright (c) 2023 Vlad Krupinski <mrvladus@yandex.ru>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from gi.repository import Adw, Gtk, GLib
from .utils import GSettings, UserData


@Gtk.Template(resource_path="/io/github/mrvladus/List/preferences.ui")
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "PreferencesWindow"

    system_theme = Gtk.Template.Child()
    light_theme = Gtk.Template.Child()
    dark_theme = Gtk.Template.Child()
    tasks_expanded = Gtk.Template.Child()
    show_accent_colors_menu = Gtk.Template.Child()
    enable_sub_tasks = Gtk.Template.Child()
    clear_history_on_startup = Gtk.Template.Child()
    history_size = Gtk.Template.Child()

    def __init__(self, win: Adw.ApplicationWindow) -> None:
        super().__init__(transient_for=win)
        # Setup theme
        theme: int = GSettings.get("theme")
        if theme == 0:
            self.system_theme.props.active = True
        if theme == 1:
            self.light_theme.props.active = True
        if theme == 4:
            self.dark_theme.props.active = True
        # Setup tasks
        GSettings.bind("tasks-expanded", self.tasks_expanded, "active")
        GSettings.bind(
            "show-accent-colors-menu", self.show_accent_colors_menu, "active"
        )
        GSettings.bind(
            "clear-history-on-startup", self.clear_history_on_startup, "active"
        )
        GSettings.bind("history-size", self.history_size, "value")
        GSettings.bind("enable-sub-tasks", self.enable_sub_tasks, "active")

    @Gtk.Template.Callback()
    def on_theme_change(self, btn: Gtk.Button) -> None:
        id: str = btn.get_buildable_id()
        if id == "system_theme":
            theme = 0
        elif id == "light_theme":
            theme = 1
        elif id == "dark_theme":
            theme = 4
        Adw.StyleManager.get_default().set_color_scheme(theme)
        GSettings.set("theme", "i", theme)

    @Gtk.Template.Callback()
    def on_save_backup(self, _):
        UserData.backup()
        GLib.spawn_command_line_async(f"xdg-open {GLib.get_home_dir()}")
        self.hide()
