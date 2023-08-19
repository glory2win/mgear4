from mgear.vendor.Qt import QtCore


class WidgetSettingsManager(QtCore.QSettings):
    widget_map = {
        'QCheckBox': ('isChecked', 'setChecked', False),
        'QComboBox': ('currentIndex', 'setCurrentIndex', 0),
        'QLineEdit': ('text', 'setText', ""),
        'QListWidget': (None, 'addItems', [])
    }

    def __init__(self, ui_name, parent=None):
        super(WidgetSettingsManager, self).__init__(parent)
        self.settings = QtCore.QSettings(
            QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            "mcsGear",
            ui_name
        )

    def _get_listwidget_item_names(self, listwidget):
        return [listwidget.item(i).text() for i in range(listwidget.count())]

    def save_ui_state(self, widget_dict):
        for name, widget in widget_dict.items():
            class_name = widget.__class__.__name__
            if class_name == 'QListWidget':
                value = self._get_listwidget_item_names(widget)
                self.settings.setValue(name, value)
                continue
            getter, _, _ = self.widget_map.get(class_name)
            if not getter:
                return
            get_function = getattr(widget, getter)
            value = get_function()
            if value is not None:
                self.settings.setValue(name, value)

    def load_ui_state(self, widget_dict, reset=False):
        for name, widget in widget_dict.items():
            class_name = widget.__class__.__name__
            _, setter, default_value = self.widget_map.get(class_name)
            if not setter:
                return
            set_function = getattr(widget, setter)
            value = self.settings.value(name) if not reset else default_value
            if value is not None:
                try:
                    set_function(value)
                except Exception as e:
                    print(e)

