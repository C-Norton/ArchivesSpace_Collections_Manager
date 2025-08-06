"""
Tests for the updated MenuButton system using pytest and pytest-mock
"""
import pytest
import tkinter as tk
from tkinter import ttk

from view.MenuFrame import MenuFrame
from view.menu_buttons.ConfigureConnection import (
    ConfigureConnectionButtonImpl,
    create_configure_connection_button,
)
# Import the classes we're testing
from view.menu_buttons.MenuButton import (
    MenuButton,
    PopupButton,
    BaseMenuButtonImpl,
    MenuButtonWidget,
    FunctionMenuButtonImpl,
    MenuButtonFactory,
    MenuButtonObserver
)
from view.menu_buttons.SaveConnection import (
    SaveConnectionButtonImpl,
    create_save_connection_button,
)
from view.menu_buttons.TestConnection import (
    TestConnectionButtonImpl,
    create_test_connection_button,
)


class TestMenuButtonProtocol:
    """Test the MenuButton protocol compliance"""

    def test_protocol_compliance(self, mocker):
        """Test that our implementations satisfy the MenuButton protocol"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        # Create implementations
        configure_impl = ConfigureConnectionButtonImpl(parent, connection_manager)
        save_impl = SaveConnectionButtonImpl(parent, connection_manager)
        test_impl = TestConnectionButtonImpl(parent, connection_manager)

        # Test that they satisfy the MenuButton protocol
        assert isinstance(configure_impl, MenuButton)
        assert isinstance(save_impl, MenuButton)
        assert isinstance(test_impl, MenuButton)

        # Test that save_impl also satisfies PopupButton protocol
        assert isinstance(save_impl, PopupButton)

    def test_protocol_properties_exist(self, mocker):
        """Test that all required protocol properties exist"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        impl = ConfigureConnectionButtonImpl(parent, connection_manager)

        # Protocol properties and methods must exist
        assert hasattr(impl, 'clickable')
        assert hasattr(impl, 'on_click')
        assert callable(impl.on_click)

        # clickable should be a bool
        assert isinstance(impl.clickable, bool)


class TestBaseMenuButtonImpl:
    """Test the base implementation class"""

    class ConcreteMenuButton(BaseMenuButtonImpl):
        """Concrete implementation for testing"""
        def on_click(self):
            return "clicked"

    def test_initialization(self, mocker):
        """Test base class initialization"""
        parent = mocker.Mock()
        button = self.ConcreteMenuButton(parent, "Test Button")

        assert button.parent == parent
        assert button.text == "Test Button"
        assert button._clickable is True
        assert button.clickable is True

    def test_clickable_property(self, mocker):
        """Test clickable property getter and setter"""
        parent = mocker.Mock()
        button = self.ConcreteMenuButton(parent, "Test Button")

        # Initially clickable
        assert button.clickable is True

        # Set to False
        button.clickable = False
        assert button.clickable is False
        assert button._clickable is False

        # Set back to True
        button.clickable = True
        assert button.clickable is True
        assert button._clickable is True

    def test_set_enabled_convenience_method(self, mocker):
        """Test set_enabled convenience method"""
        parent = mocker.Mock()
        button = self.ConcreteMenuButton(parent, "Test Button")

        # Initially enabled
        assert button.clickable is True

        # Disable
        button.set_enabled(False)
        assert button.clickable is False

        # Re-enable
        button.set_enabled(True)
        assert button.clickable is True

    def test_abstract_method_enforcement(self, mocker):
        """Test that on_click must be implemented"""
        parent = mocker.Mock()

        # Should not be able to instantiate BaseMenuButtonImpl directly
        with pytest.raises(TypeError):
            BaseMenuButtonImpl(parent, "Test")


class TestMenuButtonWidget:
    """Test the MenuButtonWidget wrapper"""

    def test_widget_creation(self, mocker):
        """Test MenuButtonWidget creation"""
        parent = mocker.Mock()
        mock_button_impl = mocker.Mock(spec=MenuButton)
        mock_button_impl.text = "Test Button"
        mock_button_impl.clickable = True

        # Mock ttk.Button
        mock_ttk_button = mocker.Mock()
        mocker.patch('tkinter.ttk.Button', return_value=mock_ttk_button)

        widget = MenuButtonWidget(parent, mock_button_impl)

        # Should create ttk.Button with correct parameters
        ttk.Button.assert_called_once_with(
            parent,
            text="Test Button",
            command=widget._handle_click
        )

        # Should configure button state
        mock_ttk_button.configure.assert_called_with(state='normal')

    def test_click_delegation(self, mocker):
        """Test that clicks are delegated to implementation"""
        parent = mocker.Mock()
        mock_button_impl = mocker.Mock(spec=MenuButton)
        mock_button_impl.clickable = True
        mock_button_impl.text = "Test"

        mocker.patch('tkinter.ttk.Button')

        widget = MenuButtonWidget(parent, mock_button_impl)

        # Simulate click
        widget._handle_click()

        # Should call on_click when clickable
        mock_button_impl.on_click.assert_called_once()

    def test_click_blocked_when_not_clickable(self, mocker):
        """Test that clicks are blocked when button is not clickable"""
        parent = mocker.Mock()
        mock_button_impl = mocker.Mock(spec=MenuButton)
        mock_button_impl.clickable = False
        mock_button_impl.text = "Test"

        mocker.patch('tkinter.ttk.Button')

        widget = MenuButtonWidget(parent, mock_button_impl)

        # Simulate click
        widget._handle_click()

        # Should not call on_click when not clickable
        mock_button_impl.on_click.assert_not_called()

    def test_state_refresh(self, mocker):
        """Test refreshing button state"""
        parent = mocker.Mock()
        mock_button_impl = mocker.Mock(spec=MenuButton)
        mock_button_impl.text = "Test"
        mock_button_impl.clickable = True

        mock_ttk_button = mocker.Mock()
        mocker.patch('tkinter.ttk.Button', return_value=mock_ttk_button)

        widget = MenuButtonWidget(parent, mock_button_impl)
        mock_ttk_button.configure.reset_mock()

        # Change implementation state and refresh
        mock_button_impl.clickable = False
        widget.refresh()

        # Should update button state
        mock_ttk_button.configure.assert_called_with(state='disabled')

    def test_tkinter_method_delegation(self, mocker):
        """Test that tkinter methods are properly delegated"""
        parent = mocker.Mock()
        mock_button_impl = mocker.Mock(spec=MenuButton)
        mock_button_impl.text = "Test"
        mock_button_impl.clickable = True

        mock_ttk_button = mocker.Mock()
        mocker.patch('tkinter.ttk.Button', return_value=mock_ttk_button)

        widget = MenuButtonWidget(parent, mock_button_impl)

        # Test delegation of common methods
        widget.grid(row=0, column=0)
        mock_ttk_button.grid.assert_called_once_with(row=0, column=0)

        widget.pack(side='left')
        mock_ttk_button.pack.assert_called_once_with(side='left')

        widget.configure(width=100)
        mock_ttk_button.configure.assert_called_with(width=100)


class TestConcreteImplementations:
    """Test concrete button implementations"""

    def test_configure_connection_button(self, mocker):
        """Test ConfigureConnectionButtonImpl"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        button = ConfigureConnectionButtonImpl(parent, connection_manager)

        assert button.text == "Configure Connection"
        assert button.clickable is True
        assert button.connection_manager == connection_manager

    def test_configure_connection_on_click(self, mocker):
        """Test ConfigureConnectionButtonImpl click handling"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mock_dialog = mocker.patch('view.menu_buttons.ConfigureConnection.ConnectionDialog')

        button = ConfigureConnectionButtonImpl(parent, connection_manager)
        button.on_click()

        # Should create connection dialog
        mock_dialog.assert_called_once_with(parent, connection_manager)

    def test_configure_connection_dialog_reuse(self, mocker):
        """Test that existing dialog is reused if still open"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mock_dialog_class = mocker.patch('view.menu_buttons.ConfigureConnection.ConnectionDialog')
        mock_dialog = mocker.Mock()
        mock_dialog.winfo_exists.return_value = True
        mock_dialog_class.return_value = mock_dialog

        button = ConfigureConnectionButtonImpl(parent, connection_manager)

        # First click creates dialog
        button.on_click()
        mock_dialog_class.assert_called_once_with(parent, connection_manager)

        # Second click reuses existing dialog
        mock_dialog_class.reset_mock()
        button.on_click()

        mock_dialog_class.assert_not_called()
        mock_dialog.lift.assert_called_once()
        mock_dialog.focus_force.assert_called_once()

    def test_save_connection_button_clickability(self, mocker):
        """Test SaveConnectionButtonImpl clickability logic"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        button = SaveConnectionButtonImpl(parent, connection_manager)

        # Not clickable when no connection
        connection_manager.connection = None
        assert button.clickable is False

        # Not clickable when connection not validated
        mock_connection = mocker.Mock()
        mock_connection.validated = False
        connection_manager.connection = mock_connection
        assert button.clickable is False

        # Clickable when connection exists and is validated
        mock_connection.validated = True
        assert button.clickable is True

    def test_save_connection_clickable_with_disabled_base(self, mocker):
        """Test SaveConnectionButtonImpl when base clickable is disabled"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()
        mock_connection = mocker.Mock()
        mock_connection.validated = True
        connection_manager.connection = mock_connection

        button = SaveConnectionButtonImpl(parent, connection_manager)

        # Should be clickable initially
        assert button.clickable is True

        # Disable at base level
        button.clickable = False
        assert button.clickable is False

        # Re-enable at base level
        button.clickable = True
        assert button.clickable is True

    def test_save_connection_on_click(self, mocker):
        """Test SaveConnectionButtonImpl click handling"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()
        mock_connection = mocker.Mock()
        connection_manager.connection = mock_connection

        mock_save = mocker.patch('view.menu_buttons.SaveConnection.save_connection')

        button = SaveConnectionButtonImpl(parent, connection_manager)
        button.on_click()

        # Should call save_connection
        mock_save.assert_called_once_with(mock_connection)

    def test_save_connection_implements_popup_button(self, mocker):
        """Test that SaveConnectionButtonImpl implements PopupButton protocol"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        button = SaveConnectionButtonImpl(parent, connection_manager)

        # Should implement PopupButton
        assert isinstance(button, PopupButton)
        assert hasattr(button, 'on_close')
        assert callable(button.on_close)

        # on_close should not raise
        button.on_close()

    def test_test_connection_button_clickability(self, mocker):
        """Test TestConnectionButtonImpl clickability logic"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        button = TestConnectionButtonImpl(parent, connection_manager)

        # Not clickable when no connection
        connection_manager.connection = None
        assert button.clickable is False

        # Clickable when connection exists
        connection_manager.connection = mocker.Mock()
        assert button.clickable is True

    def test_test_connection_clickable_with_disabled_base(self, mocker):
        """Test TestConnectionButtonImpl when base clickable is disabled"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()
        connection_manager.connection = mocker.Mock()

        button = TestConnectionButtonImpl(parent, connection_manager)

        # Should be clickable initially
        assert button.clickable is True

        # Disable at base level
        button.clickable = False
        assert button.clickable is False

        # Re-enable at base level
        button.clickable = True
        assert button.clickable is True

    def test_test_connection_on_click(self, mocker):
        """Test TestConnectionButtonImpl click handling"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()
        mock_connection = mocker.Mock()
        connection_manager.connection = mock_connection

        mock_test = mocker.patch('view.menu_buttons.TestConnection.TestConnection')

        button = TestConnectionButtonImpl(parent, connection_manager)
        button.on_click()

        # Should create TestConnection dialog
        mock_test.assert_called_once_with(mock_connection)


class TestFunctionMenuButtonImpl:
    """Test the generic function-based menu button implementation"""

    def test_initialization(self, mocker):
        """Test FunctionMenuButtonImpl initialization"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        button = FunctionMenuButtonImpl(parent, "Test Button", mock_func, False)

        assert button.parent == parent
        assert button.text == "Test Button"
        assert button._on_click_func == mock_func
        assert button.clickable is False

    def test_initialization_with_defaults(self, mocker):
        """Test FunctionMenuButtonImpl initialization with defaults"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        button = FunctionMenuButtonImpl(parent, "Test Button", mock_func)

        assert button.clickable is True

    def test_on_click_execution(self, mocker):
        """Test that on_click executes the provided function"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        button = FunctionMenuButtonImpl(parent, "Test Button", mock_func)
        button.on_click()

        mock_func.assert_called_once()

    def test_on_click_with_none_function(self, mocker):
        """Test that on_click handles None function gracefully"""
        parent = mocker.Mock()

        button = FunctionMenuButtonImpl(parent, "Test Button", None)

        # Should not raise an exception
        button.on_click()

    def test_protocol_compliance(self, mocker):
        """Test that FunctionMenuButtonImpl satisfies MenuButton protocol"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        button = FunctionMenuButtonImpl(parent, "Test Button", mock_func)

        assert isinstance(button, MenuButton)
        assert hasattr(button, 'clickable')
        assert hasattr(button, 'on_click')
        assert callable(button.on_click)


class TestMenuButtonFactory:
    """Test the MenuButtonFactory"""

    def test_create_function_button(self, mocker):
        """Test creating a function button"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_function_button(
            parent, "Test Button", mock_func, initial_clickable=False, width=200
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, FunctionMenuButtonImpl)
        assert button_widget.impl.text == "Test Button"
        assert button_widget.impl._on_click_func == mock_func
        assert button_widget.impl.clickable is False

    def test_create_function_button_with_defaults(self, mocker):
        """Test creating function button with default parameters"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_function_button(
            parent, "Test Button", mock_func
        )

        assert button_widget.impl.clickable is True

    def test_create_lambda_button(self, mocker):
        """Test creating a lambda button"""
        parent = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_lambda_button(
            parent, "Lambda Test", lambda: print("clicked"), width=150
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, FunctionMenuButtonImpl)
        assert button_widget.impl.text == "Lambda Test"
        assert callable(button_widget.impl._on_click_func)

    def test_create_method_button(self, mocker):
        """Test creating a method button"""
        parent = mocker.Mock()
        test_obj = mocker.Mock()
        test_obj.test_method = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_method_button(
            parent, "Method Test", test_obj, "test_method", width=100
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, FunctionMenuButtonImpl)
        assert button_widget.impl.text == "Method Test"

        # Test that clicking calls the method
        button_widget.impl.on_click()
        test_obj.test_method.assert_called_once()

    def test_create_callback_button(self, mocker):
        """Test creating a callback button with arguments"""
        parent = mocker.Mock()
        mock_callback = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_callback_button(
            parent, "Callback Test", mock_callback, "arg1", "arg2", width=120
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, FunctionMenuButtonImpl)
        assert button_widget.impl.text == "Callback Test"

        # Test that clicking calls the callback with arguments
        button_widget.impl.on_click()
        mock_callback.assert_called_once_with("arg1", "arg2")

    def test_create_callback_button_no_args(self, mocker):
        """Test creating callback button with no arguments"""
        parent = mocker.Mock()
        mock_callback = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = MenuButtonFactory.create_callback_button(
            parent, "Callback Test", mock_callback
        )

        # Test that clicking calls the callback with no arguments
        button_widget.impl.on_click()
        mock_callback.assert_called_once_with()

    def test_factory_methods_create_working_buttons(self, mocker):
        """Test that factory methods create functional MenuButtonWidget instances"""
        parent = mocker.Mock()
        mock_func = mocker.Mock()

        # We don't need to test tkinter kwargs - that's tkinter's job
        # We just need to test that our factory creates the right objects

        # Mock just the MenuButtonWidget creation
        mock_widget = mocker.Mock(spec=MenuButtonWidget)
        mock_widget_class = mocker.patch('view.menu_buttons.MenuButton.MenuButtonWidget', return_value=mock_widget)

        # Test function button
        result = MenuButtonFactory.create_function_button(
            parent, "Test Button", mock_func, width=200, height=50
        )

        # Should return the widget
        assert result == mock_widget

        # Should have created MenuButtonWidget with correct impl and passed kwargs
        mock_widget_class.assert_called_once()
        call_args, call_kwargs = mock_widget_class.call_args

        # Check the implementation is correct type
        impl = call_args[1]  # Second positional arg is the implementation
        assert isinstance(impl, FunctionMenuButtonImpl)
        assert impl.text == "Test Button"
        assert impl._on_click_func == mock_func

        # Check kwargs were passed
        assert call_kwargs['width'] == 200
        assert call_kwargs['height'] == 50

    def test_factory_button_implementations_work_correctly(self, mocker):
        """Test that factory-created button implementations function properly"""
        parent = mocker.Mock()

        # Test function execution
        call_tracker = {'count': 0}
        def test_function():
            call_tracker['count'] += 1

        # Create implementation directly (no tkinter involved)
        impl = FunctionMenuButtonImpl(parent, "Test", test_function, initial_clickable=True)

        # Test basic properties
        assert impl.text == "Test"
        assert impl.clickable is True
        assert impl.parent == parent

        # Test function execution
        impl.on_click()
        assert call_tracker['count'] == 1

        # Test state management
        impl.clickable = False
        assert impl.clickable is False

        # Test with None function (should not crash)
        none_impl = FunctionMenuButtonImpl(parent, "None", None)
        none_impl.on_click()  # Should not raise

    def test_different_factory_methods_create_correct_implementations(self, mocker):
        """Test that different factory methods create the expected button types"""
        parent = mocker.Mock()

        # Mock MenuButtonWidget to avoid tkinter
        mock_widget_class = mocker.patch('view.menu_buttons.MenuButton.MenuButtonWidget')

        # Test each factory method creates the right implementation type
        test_cases = [
            (MenuButtonFactory.create_function_button, "Function", lambda: None),
            (MenuButtonFactory.create_lambda_button, "Lambda", lambda: None),
        ]

        for factory_method, text, func in test_cases:
            mock_widget_class.reset_mock()

            factory_method(parent, text, func, width=100)

            # Should have called MenuButtonWidget
            mock_widget_class.assert_called_once()
            call_args, call_kwargs = mock_widget_class.call_args

            # Implementation should be FunctionMenuButtonImpl
            impl = call_args[1]
            assert isinstance(impl, FunctionMenuButtonImpl)
            assert impl.text == text

            # kwargs should be passed
            assert call_kwargs['width'] == 100

    def test_method_button_calls_correct_method(self, mocker):
        """Test that method button factory creates working method calls"""
        parent = mocker.Mock()

        # Create test object with method
        test_obj = mocker.Mock()
        test_obj.test_method = mocker.Mock()

        # Mock MenuButtonWidget
        mock_widget_class = mocker.patch('view.menu_buttons.MenuButton.MenuButtonWidget')

        MenuButtonFactory.create_method_button(
            parent, "Method Test", test_obj, "test_method"
        )

        # Get the implementation that was created
        impl = mock_widget_class.call_args[0][1]

        # Should be FunctionMenuButtonImpl with the method as the function
        assert isinstance(impl, FunctionMenuButtonImpl)

        # Calling on_click should call the method
        impl.on_click()
        test_obj.test_method.assert_called_once()

    def test_callback_button_passes_arguments_correctly(self, mocker):
        """Test that callback button factory handles arguments properly"""
        parent = mocker.Mock()
        mock_callback = mocker.Mock()

        # Mock MenuButtonWidget
        mock_widget_class = mocker.patch(
            "view.menu_buttons.MenuButton.MenuButtonWidget"
        )

        MenuButtonFactory.create_callback_button(
            parent, "Callback", mock_callback, "arg1", "arg2", key="value"
        )

        # Get the implementation
        impl = mock_widget_class.call_args[0][1]

        # Calling on_click should call callback with arguments
        impl.on_click()
        mock_callback.assert_called_once_with("arg1", "arg2")

        # Should have passed remaining kwargs to MenuButtonWidget
        call_kwargs = mock_widget_class.call_args[1]
        assert call_kwargs["key"] == "value"

    def test_factory_kwargs_dont_interfere_with_functionality(self, mocker):
        """Test that passing kwargs doesn't break the button functionality"""
        parent = mocker.Mock()
        call_tracker = {'called': False}

        def test_func():
            call_tracker['called'] = True

        # Mock ttk.Button
        mock_button_instance = mocker.Mock()
        mocker.patch('tkinter.ttk.Button', return_value=mock_button_instance)

        # Create button with kwargs
        button_widget = MenuButtonFactory.create_function_button(
            parent, "Test", test_func, width=100, style='Custom.TButton'
        )

        # Function should still work
        button_widget.impl.on_click()
        assert call_tracker['called'] is True

        # Button should still have correct properties
        assert button_widget.impl.text == "Test"
        assert button_widget.impl.clickable is True


class TestFactoryFunctions:
    """Test factory functions for creating buttons"""

    def test_create_configure_connection_button(self, mocker):
        """Test configure connection button factory"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = create_configure_connection_button(
            parent, connection_manager, width=200
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, ConfigureConnectionButtonImpl)
        assert button_widget.impl.text == "Configure Connection"

    def test_create_save_connection_button(self, mocker):
        """Test save connection button factory"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = create_save_connection_button(
            parent, connection_manager, state='disabled'
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, SaveConnectionButtonImpl)
        assert button_widget.impl.text == "Save Connection"

    def test_create_test_connection_button(self, mocker):
        """Test test connection button factory"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mocker.patch('tkinter.ttk.Button')

        button_widget = create_test_connection_button(
            parent, connection_manager
        )

        assert isinstance(button_widget, MenuButtonWidget)
        assert isinstance(button_widget.impl, TestConnectionButtonImpl)
        assert button_widget.impl.text == "Test Connection"


class TestUpdatedMenuFrame:
    """Test the updated MenuFrame class"""

    def test_menu_frame_creation(self, mocker):
        """Test MenuFrame creates all buttons correctly"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        # Mock the factory functions
        mock_configure_btn = mocker.Mock()
        mock_save_btn = mocker.Mock()
        mock_test_btn = mocker.Mock()

        mocker.patch(
            'view.menu_buttons.MenuButton.create_configure_connection_button',
            return_value=mock_configure_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_save_connection_button',
            return_value=mock_save_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_test_connection_button',
            return_value=mock_test_btn
        )

        # Mock ttk.Frame
        mocker.patch('tkinter.ttk.Frame.__init__')

        menu_frame = MenuFrame(parent, connection_manager)

        # Should create all buttons
        assert menu_frame.configure_btn == mock_configure_btn
        assert menu_frame.save_btn == mock_save_btn
        assert menu_frame.test_btn == mock_test_btn

        # Should call grid on all buttons
        mock_configure_btn.grid.assert_called_once()
        mock_save_btn.grid.assert_called_once()
        mock_test_btn.grid.assert_called_once()

    def test_refresh_button_states(self, mocker):
        """Test refreshing button states"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mock_configure_btn = mocker.Mock()
        mock_save_btn = mocker.Mock()
        mock_test_btn = mocker.Mock()

        mocker.patch(
            'view.menu_buttons.MenuButton.create_configure_connection_button',
            return_value=mock_configure_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_save_connection_button',
            return_value=mock_save_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_test_connection_button',
            return_value=mock_test_btn
        )
        mocker.patch('tkinter.ttk.Frame.__init__')

        menu_frame = UpdatedMenuFrame(parent, connection_manager)
        menu_frame.refresh_button_states()

        # Should refresh all buttons
        mock_configure_btn.refresh.assert_called_once()
        mock_save_btn.refresh.assert_called_once()
        mock_test_btn.refresh.assert_called_once()

    def test_menu_frame_layout(self, mocker):
        """Test that menu frame lays out buttons correctly"""
        parent = mocker.Mock()
        connection_manager = mocker.Mock()

        mock_configure_btn = mocker.Mock()
        mock_save_btn = mocker.Mock()
        mock_test_btn = mocker.Mock()

        mocker.patch(
            'view.menu_buttons.MenuButton.create_configure_connection_button',
            return_value=mock_configure_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_save_connection_button',
            return_value=mock_save_btn
        )
        mocker.patch(
            'view.menu_buttons.MenuButton.create_test_connection_button',
            return_value=mock_test_btn
        )

        mock_ttk_frame = mocker.patch('tkinter.ttk.Frame')
        mock_frame_instance = mocker.Mock()
        mock_ttk_frame.__init__ = mocker.Mock()

        menu_frame = MenuFrame(parent, connection_manager)

        # Should call grid with correct positions
        mock_configure_btn.grid.assert_called_with(
            column=0, row=0, sticky="EW", padx=2, pady=5
        )
        mock_save_btn.grid.assert_called_with(
            column=1, row=0, sticky="EW", padx=2, pady=5
        )
        mock_test_btn.grid.assert_called_with(
            column=2, row=0, sticky="EW", padx=2, pady=5
        )


class TestMenuButtonObserver:
    """Test the observer for menu button state updates"""

    def test_observer_updates_on_connection_change(self, mocker):
        """Test observer updates menu frame on connection change"""

        mock_menu_frame = mocker.Mock(spec=MenuFrame)

        observer = MenuButtonObserver(mock_menu_frame)

        # Simulate connection change event
        mock_event = mocker.Mock()
        mock_event.value = "connection_changed"

        observer.update(mock_event, {})

        # Should refresh button states
        mock_menu_frame.refresh_button_states.assert_called_once()

    def test_observer_ignores_other_events(self, mocker):
        """Test observer ignores non-connection events"""
        mock_menu_frame = mocker.Mock(spec=MenuFrame)

        observer = MenuButtonObserver(mock_menu_frame)

        # Simulate different event
        mock_event = mocker.Mock()
        mock_event.value = "repository_loaded"

        observer.update(mock_event, {})

        # Should not refresh button states
        mock_menu_frame.refresh_button_states.assert_not_called()
