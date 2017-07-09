# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2017 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Test Backforward widget."""

import pytest

from qutebrowser.mainwindow.statusbar import backforward


@pytest.fixture
def backforward_widget(qtbot):
    widget = backforward.Backforward()
    qtbot.add_widget(widget)
    return widget


@pytest.mark.parametrize('can_go_back, can_go_forward, expected_text', [
    (False, False, ''),
    (True, False, '[<]'),
    (False, True, '[>]'),
    (True, True, '[<>]'),
])
def test_backforward_widget(backforward_widget, stubs,
                            fake_web_tab, can_go_back, can_go_forward,
                            expected_text):
    """Ensure the Backforward widget shows the correct text."""
    tab = fake_web_tab(can_go_back=can_go_back, can_go_forward=can_go_forward)
    tabbed_browser = stubs.TabbedBrowserStub()
    tabbed_browser.current_index = 1
    tabbed_browser.tabs = [tab]
    backforward_widget.on_tab_cur_url_changed(tabbed_browser)
    assert backforward_widget.text() == expected_text

    # Check that the widget gets reset if empty.
    if can_go_back and can_go_forward:
        tab = fake_web_tab(can_go_back=False, can_go_forward=False)
        tabbed_browser.tabs = [tab]
        backforward_widget.on_tab_cur_url_changed(tabbed_browser)
        assert backforward_widget.text() == ''
