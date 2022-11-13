import subprocess
import sys
import json
import os
from datetime import timedelta
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Adw, Gio

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

# Settings dialog
class Dialog_settings(Gtk.Dialog):
    def __init__(self, parent, **kwargs):
        super().__init__(use_header_bar=True, transient_for=app.get_active_window())

        self.set_title(title=jT["preferences"])
        self.use_header_bar = True
        self.set_modal(modal=True)
        self.connect('response', self.dialog_response)
        self.set_default_size(500, 460)

        # Buttons
        self.add_buttons(
            jT["close"], Gtk.ResponseType.CANCEL,
        )

        # Close button response ID
        btn_cancel = self.get_widget_for_response(
            response_id=Gtk.ResponseType.CANCEL,
        )
        btn_cancel.get_style_context().add_class(class_name='destructive-action')
        
        # Layout
        content_area = self.get_content_area()
        content_area.set_orientation(orientation=Gtk.Orientation.VERTICAL)
        content_area.set_spacing(spacing=12)
        content_area.set_margin_top(margin=12)
        content_area.set_margin_end(margin=12)
        content_area.set_margin_bottom(margin=12)
        content_area.set_margin_start(margin=12)
        
        # Preferences Page
        adw_preferences_page = Adw.PreferencesPage.new()
        content_area.append(child=adw_preferences_page)
        
        adw_preferences_group = Adw.PreferencesGroup.new()
        #adw_preferences_group.set_title(title=preferences)
        #adw_preferences_group.set_description(description=restart_timer_desc)
        #adw_preferences_group.set_header_suffix(suffix=button_flat)
        adw_preferences_page.add(group=adw_preferences_group)
        
        # ComboBox - spinner size
        sizes = [
            '5', '10', '15', '20', '25', '30', '35', '40 (%s)' % jT["default"], '45', '50', '55', '60', '65', '70', '75', '80'
        ]
        combobox_text = Gtk.ComboBoxText.new()
        for text in sizes:
            combobox_text.append_text(text=text)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["spinner-size"]
            if combobox_s == "5":
                combobox_text.set_active(index_=0)
            elif combobox_s == "10":
                combobox_text.set_active(index_=1)
            elif combobox_s == "15":
                combobox_text.set_active(index_=2)
            elif combobox_s == "20":
                combobox_text.set_active(index_=3)
            elif combobox_s == "25":
                combobox_text.set_active(index_=4)
            elif combobox_s == "30":
                combobox_text.set_active(index_=5)
            elif combobox_s == "35":
                combobox_text.set_active(index_=6)
            elif combobox_s == "40 (%s)" % jT["default"]:
                combobox_text.set_active(index_=7)
            elif combobox_s == "45":
                combobox_text.set_active(index_=8)
            elif combobox_s == "50":
                combobox_text.set_active(index_=9)
            elif combobox_s == "55":
                combobox_text.set_active(index_=10)
            elif combobox_s == "60":
                combobox_text.set_active(index_=11)
            elif combobox_s == "65":
                combobox_text.set_active(index_=12)
            elif combobox_s == "70":
                combobox_text.set_active(index_=13)
            elif combobox_s == "75":
                combobox_text.set_active(index_=14)
            elif combobox_s == "80":
                combobox_text.set_active(index_=15)
        else:
            combobox_text.set_active(index_=7)
        combobox_text.connect('changed', self.on_combo_box_text_changed)
        
        adw_action_row_00 = Adw.ActionRow.new()
        adw_action_row_00.set_icon_name(icon_name='content-loading-symbolic')
        adw_action_row_00.set_title(title=jT["spinner"])
        adw_action_row_00.set_subtitle(subtitle=jT["spinner_size_desc"])
        adw_action_row_00.add_suffix(widget=combobox_text)
        adw_preferences_group.add(child=adw_action_row_00)
        
        # ComboBox - Actions
        actions = [
            jT["default"], jT["shut_down"], jT["reboot"], jT["suspend"]
        ]
        combobox_text_s = Gtk.ComboBoxText.new()
        for text in actions:
            combobox_text_s.append_text(text=text)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/actions.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/actions.json') as p:
                jsonSpinner = json.load(p)
            combobox_s = jsonSpinner["action"]
            if combobox_s == jT["default"]:
                combobox_text_s.set_active(index_=0)
            elif combobox_s == jT["shut_down"]:
                combobox_text_s.set_active(index_=1)
            elif combobox_s == jT["reboot"]:
                combobox_text_s.set_active(index_=2)
            elif combobox_s == jT["mute_volume"]:
                combobox_text_s.set_active(index_=3)
            elif combobox_s == jT["suspend"]:
                combobox_text_s.set_active(index_=4)
        else:
            combobox_text_s.set_active(index_=0)
        combobox_text_s.connect('changed', self.on_combo_box_text_s_changed)
        
        adw_action_row_01 = Adw.ActionRow.new()
        adw_action_row_01.set_icon_name(icon_name='timer-symbolic')
        adw_action_row_01.set_title(title=jT["action_after_timing"])
        adw_action_row_01.add_suffix(widget=combobox_text_s)
        adw_preferences_group.add(child=adw_action_row_01)
        
        # Adw ActionRow - Theme configuration
        ## Gtk.Switch
        switch_01 = Gtk.Switch.new()
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json') as r:
                jR = json.load(r)
            dark = jR["theme"]
            if dark == "dark":
                switch_01.set_active(True)
        switch_01.set_valign(align=Gtk.Align.CENTER)
        switch_01.connect('notify::active', self.on_switch_01_toggled)
        
        ## Adw.ActionRow
        adw_action_row_02 = Adw.ActionRow.new()
        adw_action_row_02.set_icon_name(icon_name='weather-clear-night-symbolic')
        adw_action_row_02.set_title(title=jT["dark_theme"])
        adw_action_row_02.set_subtitle(subtitle=jT["theme_desc"])
        adw_action_row_02.add_suffix(widget=switch_01)
        adw_preferences_group.add(child=adw_action_row_02)
        
        # Adw ActionRow - Resizable of Window configuration
        ## Gtk.Switch
        switch_02 = Gtk.Switch.new()
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json') as r:
                jR = json.load(r)
            resizable = jR["resizable"]
            if resizable == "true":
                switch_02.set_active(True)
        switch_02.set_valign(align=Gtk.Align.CENTER)
        switch_02.connect('notify::active', self.on_switch_02_toggled)
        
        ## Adw.ActionRow
        adw_action_row_03 = Adw.ActionRow.new()
        adw_action_row_03.set_icon_name(icon_name='window-maximize-symbolic')
        adw_action_row_03.set_title(title=jT["resizable_of_window"])
        #adw_action_row_03.set_subtitle(subtitle=resizable_of_window)
        adw_action_row_03.add_suffix(widget=switch_02)
        adw_action_row_03.set_activatable_widget(widget=switch_02)
        adw_preferences_group.add(child=adw_action_row_03)
        
        # Adw ActionRow - custom notification
        ## Adw.EntryRow
        self.entry = Adw.EntryRow()
        self.apply_entry_text()
        self.entry.set_show_apply_button(True)
        self.entry.set_enable_emoji_completion(True)
        self.entry.connect('changed', self.on_entry_text_changed)
        
        ## Adw.ActionRow
        adw_action_row_04 = Adw.ActionRow.new()
        adw_action_row_04.set_icon_name(icon_name='notification-symbolic')
        adw_action_row_04.set_title(title=jT["custom_notification"])
        adw_action_row_04.add_suffix(widget=self.entry)
        adw_action_row_04.set_activatable_widget(widget=self.entry)
        adw_preferences_group.add(child=adw_action_row_04)
        
        # Adw ActionRow - play beep
        ## Gtk.Switch
        switch_03 = Gtk.Switch.new()
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                switch_03.set_active(False)
            else:
                switch_03.set_active(True)
        else:
            switch_03.set_active(True)
        switch_03.set_valign(align=Gtk.Align.CENTER)
        switch_03.connect('notify::active', self.on_switch_03_toggled)
        
        ## Adw.ActionRow
        adw_action_row_05 = Adw.ActionRow.new()
        adw_action_row_05.set_icon_name(icon_name='sound-symbolic')
        adw_action_row_05.set_title(title=jT["play_beep"])
        #adw_action_row_05.set_subtitle(subtitle=)
        adw_action_row_05.add_suffix(widget=switch_03)
        adw_action_row_05.set_activatable_widget(widget=switch_03)
        adw_preferences_group.add(child=adw_action_row_05)
        
        self.show()
    
    # Save app theme configuration
    def on_switch_01_toggled(self, switch01, GParamBoolean):
        if switch01.get_active():
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json', 'w') as t:
                t.write('{\n "theme": "dark"\n}')
        else:
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json', 'w') as t:
                t.write('{\n "theme": "system"\n}')

    # Save entry text (custom notification text)
    def on_entry_text_changed(self, entry):
        entry = self.entry.get_text()
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/notification.json', 'w') as n:
            n.write('{\n "custom-notification": "true",\n "text": "%s"\n}' % entry)
    
    # Apply entry text (custom notification text)
    def apply_entry_text(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/notification.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/notification.json') as n:
                jN = json.load(n)
            text = jN["text"]
            self.entry.set_text(text)
    
    # Save resizable window configuration
    def on_switch_02_toggled(self, switch02, GParamBoolean):
        if switch02.get_active():
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json', 'w') as w:
                w.write('{\n "resizable": "true"\n}')
        else:
            os.remove(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json')
    
    # Save playing beep configuration
    def on_switch_03_toggled(self, switch03, GParamBoolean):
        if switch03.get_active():
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json', 'w') as t:
                t.write('{\n "play-beep": "true"\n}')
        else:
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json', 'w') as t:
                t.write('{\n "play-beep": "false"\n}')
    
    # Save Combobox (actions) configuration
    def on_combo_box_text_s_changed(self, comboboxtexts):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/actions.json', 'w') as a:
            a.write('{\n "action": "%s"\n}' % comboboxtexts.get_active_text())
    
    # Save Combobox (spinner size) configuration
    def on_combo_box_text_changed(self, comboboxtext):
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json', 'w') as s:
            s.write('{\n "spinner-size": "%s"\n}' % comboboxtext.get_active_text())
    
    # Close button clicked action
    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.CANCEL:
            dialog.close()
            self.restart_timer()
            print(jT["preferences_saved"])
    
    # restart timer function
    def restart_timer(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

print(jT["timer_running"])
# Timer Application window
class TimerWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable()
        self.application = kwargs.get('application')
        self.style_manager = self.application.get_style_manager()
        self.theme()
        self.set_title(title=jT["timer_title"])
        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)
        
        # Gtk.Box() layout
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.mainBox.set_margin_start(10)
        self.mainBox.set_margin_end(10)
        self.set_child(self.mainBox)
        
        # App menu
        menu_button_model = Gio.Menu()
        menu_button_model.append(jT["preferences"], 'app.settings')
        menu_button_model.append(jT["about_app"], 'app.about')
        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)
        
        # Spinner
        self.spinner = Gtk.Spinner()
        self.spinner_size()
        self.mainBox.append(self.spinner)
        
        self.label = Gtk.Label()
        self.mainBox.append(self.label)
        
        # Entry
        self.make_timer_box()
        
        # Gtk.ListBox layout for start and stop button
        self.listbox = Gtk.ListBox.new()
        self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.listbox.get_style_context().add_class(class_name='boxed-list')
        self.mainBox.append(self.listbox)
        
        # Start timer button
        self.buttonStart = Gtk.Button(label=jT["run_timer"])
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        self.button1_style_context = self.buttonStart.get_style_context()
        self.button1_style_context.add_class('suggested-action')
        self.listbox.append(self.buttonStart)
        
        # Stop timer button
        self.buttonStop = Gtk.Button(label=jT["stop_timer"])
        self.buttonStop.set_sensitive(False)
        self.button2_style_context = self.buttonStop.get_style_context()
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        self.listbox.append(self.buttonStop)

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)
    
    # Entries of seconds, minutes and hours
    def make_timer_box(self):
        # Load counter.json (config file with time counter values)
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json') as jc:
                jC = json.load(jc)
            hour_e = jC["hour"]
            min_e = jC["minutes"]
            sec_e = jC["seconds"]
        else:
            hour_e = "0"
            min_e = "1"
            sec_e = "0"
        # Layout
        self.timerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.timerBox.set_margin_start(50)
        self.timerBox.set_margin_end(50)
        
        # Hour entry and label
        self.hour_entry = Gtk.Entry()
        self.hour_entry.set_text(hour_e)
        self.hour_entry.set_alignment(xalign=1)
        self.timerBox.append(self.hour_entry)
        label = Gtk.Label(label = jT["hours"])
        label.set_hexpand(False)
        self.timerBox.append(label)
        
        # Minute entry and label
        self.minute_entry = Gtk.Entry()
        self.minute_entry.set_text(min_e)
        self.minute_entry.set_alignment(xalign=1)
        self.timerBox.append(self.minute_entry)
        label = Gtk.Label(label = jT["mins"])        
        label.set_hexpand(False)
        self.timerBox.append(label)
        
        # Second entry and label
        self.secs_entry = Gtk.Entry()
        self.secs_entry.set_text(sec_e)
        self.secs_entry.set_alignment(xalign=1)
        self.timerBox.append(self.secs_entry)
        label = Gtk.Label(label = jT["secs"])        
        label.set_hexpand(False)
        self.timerBox.append(label)
        
        self.mainBox.append(self.timerBox)

    # Theme setup
    def theme(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/theme.json') as jt:
                t = json.load(jt)
            theme = t["theme"]
            if theme == "dark":
                self.style_manager.set_color_scheme(
                    color_scheme=Adw.ColorScheme.PREFER_DARK
                )
                
    # Resizable of Window
    def resizable(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/window.json') as jr:
                rezisable = json.load(jr)
            if rezisable == "true":
                self.set_resizable(True)
        else:
            self.set_resizable(False)
    
    # Spinner size
    def spinner_size(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/spinner.json') as j:
                jsonObject = json.load(j)
            spinner = jsonObject["spinner-size"]
            if spinner == "5":
                self.spinner.set_size_request(5,5)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "10":
                self.spinner.set_size_request(10,10)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "15":
                self.spinner.set_size_request(15,15)
                self.set_default_size(300, 300)
                self.set_size_request(300, 300)
            if spinner == "20":
                self.spinner.set_size_request(20,20)
                self.set_default_size(320, 320)
                self.set_size_request(320, 320)
            if spinner == "25":
                self.spinner.set_size_request(25,25)
                self.set_default_size(320, 320)
                self.set_size_request(320, 320)
            if spinner == "30":
                self.spinner.set_size_request(30,30)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "35":
                self.spinner.set_size_request(35,35)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "40 (%s)" % (jT["default"]):
                self.spinner.set_size_request(40,40)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "45":
                self.spinner.set_size_request(45,45)
                self.set_default_size(340, 340)
                self.set_size_request(340, 340)
            if spinner == "50":
                self.spinner.set_size_request(50,50)
                self.set_default_size(350, 350)
                self.set_size_request(350, 350)
            if spinner == "55":
                self.spinner.set_size_request(55,55)
                self.set_default_size(350, 350)
                self.set_size_request(350, 350)
            if spinner == "60":
                self.spinner.set_size_request(60,60)
                self.set_default_size(360, 360)
                self.set_size_request(360, 360)
            if spinner == "65":
                self.spinner.set_size_request(65,65)
                self.set_default_size(360, 360)
                self.set_size_request(360, 360)
            if spinner == "70":
                self.spinner.set_size_request(70,70)
                self.set_default_size(370, 370)
                self.set_size_request(370, 370)
            if spinner == "75":
                self.spinner.set_size_request(75,75)
                self.set_default_size(370, 370)
                self.set_size_request(370, 370)
            if spinner == "80":
                self.spinner.set_size_request(80,80)
                self.set_default_size(400, 400)
                self.set_size_request(400, 400)
        else:
            # default spinner size
            self.spinner.set_size_request(40,40)
            # default size of Window
            self.set_default_size(340, 340)
            self.set_size_request(340, 340)
    
    # Start button action
    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.start_timer()
    
    # Stop button action
    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.stop_timer(jT["timing_ended"])
        print(jT["timing_ended"])

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()
    
    # On timeout function
    tick_counter = timedelta(milliseconds = 250) # static object so we don't recreate the object every time
    zero_counter = timedelta()
    def on_timeout(self, *args, **kwargs):
        self.counter -= self.tick_counter
        if self.counter <= self.zero_counter:
            self.stop_timer(jT["timing_finished"])
            self.label.set_markup("<b>" + jT["timing_finished"]+ "</b>")
            self.session()
            print(jT["timing_finished"])
            return False
        self.label.set_markup("<big><b>{}</b></big>".format(
            strfdelta(self.counter, "{hours} %s {minutes} %s {seconds} %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        return True
    
    # Start timer function
    def start_timer(self):
        """ Run Timer. """
        self.check_and_save()
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
        self.button2_style_context.add_class('destructive-action')
        self.button1_style_context.remove_class('suggested-action')
        self.counter = timedelta(hours = int(self.hour_entry.get_text()), minutes = int(self.minute_entry.get_text()), seconds = int(self.secs_entry.get_text()))
        self.play_beep()
        self.label.set_markup("<big><b>{}</b></big>".format(
            strfdelta(self.counter, "{hours} %s {minutes} %s {seconds} %s" % (jT["hours"], jT["mins"], jT["secs"]))
        ))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        
    # Stop timer function
    def stop_timer(self, alabeltext):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.buttonStart.set_sensitive(True)
        self.buttonStop.set_sensitive(False)
        self.button2_style_context.remove_class('destructive-action')
        self.button1_style_context.add_class('suggested-action')
        self.label.set_label(alabeltext)
        #self.play_beep()
    
    # Session
    def session(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/actions.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/actions.json') as a:
                jA = json.load(a)
            action = jA["action"]
            if action == jT["default"]:
                self.play_beep()
                self.notification()
            elif action == jT["shut_down"]:
                self.play_beep()
                os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.PowerOff" boolean:true')
            elif action == jT["reboot"]:
                self.play_beep()
                os.system('dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Reboot" boolean:true')
            elif action == jT["suspend"]:
                self.play_beep()
                os.system('dbus-send --system --print-reply \
        --dest=org.freedesktop.login1 /org/freedesktop/login1 \
        "org.freedesktop.login1.Manager.Suspend" boolean:true')
        else:
            self.play_beep()
            self.notification()
    
    # Notification function
    def notification(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/notification.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/notification.json') as r:
                jR = json.load(r)
            notification = jR["text"]
            if notification == "":
                subprocess.call(['notify-send',jT["timer_title"],jT["timing_finished"],'-i','com.github.vikdevelop.timer'])
            else:
                subprocess.call(['notify-send',jT["timer_title"],notification,'-i','com.github.vikdevelop.timer'])
        else:
            subprocess.call(['notify-send',jT["timer_title"],jT["timing_finished"],'-i','com.github.vikdevelop.timer'])
    
    # Checking whether the entered values are correct and then saving them
    def check_and_save(self):
        hour = self.hour_entry.get_text()
        minute = self.minute_entry.get_text()
        sec = self.secs_entry.get_text()
        if hour == "":
            subprocess.call(['notify-send',jT["blank_value"],jT["blank_values_desc"],'-i','com.github.vikdevelop.timer'])
        elif minute == "":
            subprocess.call(['notify-send',jT["blank_value"],jT["blank_values_desc"],'-i','com.github.vikdevelop.timer'])
        elif sec == "":
            subprocess.call(['notify-send',jT["blank_value"],jT["blank_values_desc"],'-i','com.github.vikdevelop.timer'])
        # Save time counter values
        with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/counter.json', 'w') as c:
            c.write('{\n "hour": "%s",\n "minutes": "%s",\n "seconds": "%s"\n}' % (hour, minute, sec))
            
    # Play beep          
    def play_beep(self):
        if os.path.exists(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json'):
            with open(os.path.expanduser('~') + '/.var/app/com.github.vikdevelop.timer/data/beep.json') as r:
                jR = json.load(r)
            beep = jR["play-beep"]
            if beep == "false":
                print("")
            else:
                os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")
        else:
            os.popen("ffplay -nodisp -autoexit /app/share/beeps/Oxygen.ogg > /dev/null 2>&1")

# Adw Application class
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.create_action('about', self.on_about_action)
        self.create_action('settings', self.on_settings_action)
    
    # Run About dialog
    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name(jT["timer_title"])
        dialog.set_version("2.4")
        dialog.set_developer_name("vikdevelop")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments(jT["app_desc"])
        dialog.set_website("https://github.com/vikdevelop/timer")
        dialog.set_issue_url("https://github.com/vikdevelop/timer/issues")
        dialog.add_credit_section(jT["contributors"], ["KenyC https://github.com/KenyC", "Albano Battistella https://github.com/albanobattistella", "ViktorOn https://github.com/ViktorOn", "Allan Nordhøy https://github.com/comradekingu"])
        dialog.set_translator_credits(jT["translator_credits"])
        dialog.set_copyright("© 2022 vikdevelop")
        dialog.set_developers(["vikdevelop https://github.com/vikdevelop"])
        dialog.set_application_icon("com.github.vikdevelop.timer")
        dialog.show()
    
    # Run settings dialog
    def on_settings_action(self, action, param):
        self.dialog = Dialog_settings(self)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)
    
    def on_activate(self, app):
        self.win = TimerWindow(application=app)
        self.win.present()
app = MyApp(application_id="com.github.vikdevelop.timer")
app.run(sys.argv)
print(jT["timer_quit"])
