import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    action_performed,
    action_performed_with,
    attribute_value,
)


@pytest.fixture
def button():
    return toga.Button("Test Button")


def test_widget_created(button):
    """A button can be created."""
    # Round trip the impl/interface
    assert button._impl.interface == button
    assert action_performed(button, "create Button")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        (None, ""),
        (12345, "12345"),
    ],
)
def test_button_text(button, value, expected):
    """The button label can be modified."""
    assert button.text == "Test Button"

    # Clear the event log
    EventLog.reset()

    button.text = value
    assert button.text == expected

    # test backend has the right value
    assert attribute_value(button, "text") == expected

    # A rehint was performed
    assert action_performed(button, "rehint")


def test_button_on_press(button):
    """The on_press handler can be invoked."""
    # No handler initially
    assert button._on_press is None

    # Define and set a new callback
    def callback(widget, **extra):
        widget._impl._action("callback invoked", widget=widget, extra=extra)

    button.on_press = callback

    assert button.on_press._raw == callback

    # Backend has the wrapped version
    assert attribute_value(button, "on_press") == button._on_press

    # Invoke the callback
    button.on_press(button, a=1)

    # Callback was invoked
    assert action_performed_with(
        button, "callback invoked", widget=button, extra={"a": 1}
    )
