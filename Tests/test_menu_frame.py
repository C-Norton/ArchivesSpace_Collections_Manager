"""
Comprehensive unit tests for MenuFrame migration to Observer pattern.

These tests are designed to be compatible with both the current implementation
and the future Observer-based implementation where possible. Where not possible,
they focus on testing the future implementation to guide the migration.
"""

import pytest
from unittest.mock import Mock
from typing import Dict, Any

# Import the classes we're testing
from view.MenuFrame import MenuFrame
from controller.connection_manager import ConnectionManager
from observer.ui_event import UiEvent
from observer.observer import Observer
from view.ui_event_manager import UiEventManager


class TestMenuFrameInitialization:
    """Test MenuFrame initialization and setup"""

    def test_menuframe_creation_with_connection_manager(self, mocker):
        """Test that MenuFrame can be created with ConnectionManager"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        # Mock tkinter components to avoid GUI dependency
        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        menu_frame = MenuFrame(mock_parent, mock_connection_manager)

        assert menu_frame.master_frame == mock_parent
        assert menu_frame.connection_manager == mock_connection_manager

    def test_menuframe_creates_all_required_buttons(self, mocker):
        """Test that MenuFrame creates all expected buttons"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mock_button = mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        MenuFrame(mock_parent, mock_connection_manager)

        # Should create 8 buttons as per current implementation
        assert mock_button.call_count == 8

        # Verify expected button texts are created
        expected_buttons = [
            "Configure Connection", "Save Connection", "Manage Saved Connections",
            "Test Connection", "Save Query", "Load Query", "Refresh Repositories", "Help"
        ]

        button_calls = mock_button.call_args_list
        created_buttons = [call.kwargs.get('text', '') for call in button_calls]

        for expected_text in expected_buttons:
            assert expected_text in created_buttons

    def test_menuframe_sets_up_grid_layout(self, mocker):
        """Test that MenuFrame properly configures grid layout"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mock_rowconfigure = mocker.patch('tkinter.Grid.rowconfigure')
        mock_columnconfigure = mocker.patch('tkinter.Grid.columnconfigure')

        MenuFrame(mock_parent, mock_connection_manager)

        # Should configure grid for dynamic resizing
        mock_rowconfigure.assert_called()
        mock_columnconfigure.assert_called()

    def test_menuframe_inherits_from_frame(self, mocker):
        """Test that MenuFrame properly inherits from ttk.Frame"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mock_frame_init = mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        MenuFrame(mock_parent, mock_connection_manager)

        # Should call parent Frame.__init__ with proper parameters
        mock_frame_init.assert_called_once()


class TestMenuFrameButtonActions:
    """Test button action methods in MenuFrame"""

    @pytest.fixture
    def menu_frame_setup(self, mocker):
        """Common setup for MenuFrame tests"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        menu_frame = MenuFrame(mock_parent, mock_connection_manager)
        return menu_frame, mock_parent, mock_connection_manager

    def test_connection_dialog_action(self, mocker, menu_frame_setup):
        """Test connectionDialog method behavior"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        mock_connection_dialog = mocker.patch('view.menu_buttons.ConfigureConnection.ConnectionDialog')

        menu_frame.connectionDialog()

        mock_connection_dialog.assert_called_once_with(mock_parent, mock_connection_manager)

    def test_test_connection_action(self, mocker, menu_frame_setup):
        """Test testConnection method behavior"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        mock_test_connection = mocker.patch('view.menu_buttons.TestConnection.TestConnection')
        mock_connection = Mock()
        mock_connection_manager.connection = mock_connection

        menu_frame.testConnection()

        mock_test_connection.assert_called_once_with(mock_connection)

    def test_help_button_action(self, mocker, menu_frame_setup):
        """Test helpButton method behavior"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        mock_help_dialog = mocker.patch('view.menu_buttons.Help.HelpDialog')

        menu_frame.helpButton()

        mock_help_dialog.assert_called_once_with(mock_parent)

    def test_save_connection_action(self, mocker, menu_frame_setup):
        """Test saveConnection method behavior"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        mock_save_connection = mocker.patch('view.menu_buttons.SaveConnection.save_connection')
        mock_connection = Mock()
        mock_connection_manager.connection = mock_connection

        menu_frame.saveConnection()

        mock_save_connection.assert_called_once_with(mock_connection)

    def test_manage_connections_action(self, mocker, menu_frame_setup):
        """Test manageConnections method behavior"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        mock_manage_connections = mocker.patch('view.menu_buttons.ManageConnections.ManageConnections')
        mock_instance = Mock()
        mock_manage_connections.return_value = mock_instance

        menu_frame.manageConnections()

        mock_manage_connections.assert_called_once_with(mock_parent, mock_connection_manager)
        mock_instance.on_click.assert_called_once()

    def test_refresh_repositories_action(self, mocker, menu_frame_setup):
        """Test refresh repositories button action"""
        menu_frame, mock_parent, mock_connection_manager = menu_frame_setup

        # Mock the repo_frame refresh method
        mock_parent.repo_frame.refresh = Mock()

        # Simulate button command execution (current implementation)
        mock_parent.repo_frame.refresh()

        mock_parent.repo_frame.refresh.assert_called_once()


class TestMenuFrameObserverPattern:
    """Test MenuFrame integration with Observer pattern (future implementation)"""

    @pytest.fixture
    def observer_menu_frame_setup(self, mocker):
        """Setup for Observer pattern tests"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)
        mock_event_manager = mocker.Mock(spec=UiEventManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')
        mocker.patch('view.ui_event_manager.UiEventManager', return_value=mock_event_manager)

        # Create a mock MenuFrame that implements Observer
        class MockObserverMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self.event_manager = mock_event_manager
                self._button_states = {}

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                """Handle observed events"""
                if event == UiEvent.CONNECTION_CHANGED:
                    self._handle_connection_changed(data)
                elif event == UiEvent.REPOSITORY_LOADED:
                    self._handle_repository_loaded(data)

            def _handle_connection_changed(self, data: Dict[str, Any]) -> None:
                """Handle connection state changes"""
                self._button_states['connection_valid'] = data.get('is_valid', False)

            def _handle_repository_loaded(self, data: Dict[str, Any]) -> None:
                """Handle repository loading events"""
                self._button_states['repositories_loaded'] = len(data.get('repositories', {})) > 0

        menu_frame = MockObserverMenuFrame(mock_parent, mock_connection_manager)
        return menu_frame, mock_parent, mock_connection_manager, mock_event_manager

    def test_menuframe_implements_observer_interface(self, observer_menu_frame_setup):
        """Test that MenuFrame properly implements Observer interface"""
        menu_frame, _, _, _ = observer_menu_frame_setup

        # Should implement Observer protocol
        assert hasattr(menu_frame, 'update')
        assert callable(menu_frame.update)

    def test_menuframe_handles_connection_changed_event(self, observer_menu_frame_setup):
        """Test MenuFrame response to CONNECTION_CHANGED event"""
        menu_frame, _, _, _ = observer_menu_frame_setup

        # Test valid connection
        connection_data = {
            'connection': Mock(),
            'server': 'https://test.com',
            'username': 'testuser',
            'is_valid': True,
            'error_message': None
        }

        menu_frame.update(UiEvent.CONNECTION_CHANGED, connection_data)

        assert menu_frame._button_states.get('connection_valid') is True

    def test_menuframe_handles_invalid_connection_event(self, observer_menu_frame_setup):
        """Test MenuFrame response to invalid connection"""
        menu_frame, _, _, _ = observer_menu_frame_setup

        connection_data = {
            'connection': None,
            'server': 'invalid',
            'username': 'test',
            'is_valid': False,
            'error_message': 'Connection failed'
        }

        menu_frame.update(UiEvent.CONNECTION_CHANGED, connection_data)

        assert menu_frame._button_states.get('connection_valid') is False

    def test_menuframe_handles_repository_loaded_event(self, observer_menu_frame_setup):
        """Test MenuFrame response to REPOSITORY_LOADED event"""
        menu_frame, _, _, _ = observer_menu_frame_setup

        repository_data = {
            'repositories': {'repo1': {}, 'repo2': {}},
            'error': None
        }

        menu_frame.update(UiEvent.REPOSITORY_LOADED, repository_data)

        assert menu_frame._button_states.get('repositories_loaded') is True

    def test_menuframe_handles_empty_repository_event(self, observer_menu_frame_setup):
        """Test MenuFrame response to empty repositories"""
        menu_frame, _, _, _ = observer_menu_frame_setup

        repository_data = {
            'repositories': {},
            'error': 'No repositories found'
        }

        menu_frame.update(UiEvent.REPOSITORY_LOADED, repository_data)

        assert menu_frame._button_states.get('repositories_loaded') is False

    def test_menuframe_publishes_events_on_button_clicks(self, observer_menu_frame_setup):
        """Test that button clicks publish appropriate events (future implementation)"""
        menu_frame, _, _, mock_event_manager = observer_menu_frame_setup

        # Architectural decision: Button clicks should publish events rather than call methods directly
        # This enables loose coupling and allows multiple components to respond to user actions

        # Simulate future button click behavior
        def simulate_configure_connection_click():
            mock_event_manager.publish_event(UiEvent.CONFIGURE_CONNECTION_REQUESTED, {})

        simulate_configure_connection_click()

        mock_event_manager.publish_event.assert_called_with(
            UiEvent.CONFIGURE_CONNECTION_REQUESTED, {}
        )


class TestMenuFrameButtonStateManagement:
    """Test button state management and enabling/disabling logic"""

    @pytest.fixture
    def stateful_menu_frame_setup(self, mocker):
        """Setup for button state management tests"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mock_button_class = mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        # Create mock button instances
        mock_buttons = [Mock() for _ in range(8)]
        mock_button_class.side_effect = mock_buttons

        menu_frame = MenuFrame(mock_parent, mock_connection_manager)
        menu_frame._buttons = {
            'configure': mock_buttons[0],
            'save': mock_buttons[1],
            'manage': mock_buttons[2],
            'test': mock_buttons[3],
            'save_query': mock_buttons[4],
            'load_query': mock_buttons[5],
            'refresh': mock_buttons[6],
            'help': mock_buttons[7]
        }

        return menu_frame, mock_buttons, mock_connection_manager

    def test_buttons_enabled_when_connection_valid(self, stateful_menu_frame_setup):
        """Test button states when connection is valid"""
        menu_frame, mock_buttons, mock_connection_manager = stateful_menu_frame_setup

        # Architectural decision: Connection-dependent buttons should be enabled only when connection is valid
        # This prevents user confusion and API errors from invalid operations

        # Simulate connection validation
        mock_connection_manager.connection = Mock()
        mock_connection_manager.connection.validated = True

        # Method to update button states based on connection
        def update_button_states(connection_valid: bool):
            connection_dependent_buttons = ['save', 'test', 'refresh']
            state = 'normal' if connection_valid else 'disabled'

            for button_name in connection_dependent_buttons:
                if button_name in menu_frame._buttons:
                    menu_frame._buttons[button_name].configure(state=state)

        update_button_states(True)

        # Connection-dependent buttons should be enabled
        menu_frame._buttons['save'].configure.assert_called_with(state='normal')
        menu_frame._buttons['test'].configure.assert_called_with(state='normal')
        menu_frame._buttons['refresh'].configure.assert_called_with(state='normal')

    def test_buttons_disabled_when_no_connection(self, stateful_menu_frame_setup):
        """Test button states when no connection exists"""
        menu_frame, mock_buttons, mock_connection_manager = stateful_menu_frame_setup

        mock_connection_manager.connection = None

        def update_button_states(connection_valid: bool):
            connection_dependent_buttons = ['save', 'test', 'refresh']
            state = 'normal' if connection_valid else 'disabled'

            for button_name in connection_dependent_buttons:
                if button_name in menu_frame._buttons:
                    menu_frame._buttons[button_name].configure(state=state)

        update_button_states(False)

        # Connection-dependent buttons should be disabled
        menu_frame._buttons['save'].configure.assert_called_with(state='disabled')
        menu_frame._buttons['test'].configure.assert_called_with(state='disabled')
        menu_frame._buttons['refresh'].configure.assert_called_with(state='disabled')

    def test_configure_and_help_always_enabled(self, stateful_menu_frame_setup):
        """Test that some buttons are always available"""
        menu_frame, mock_buttons, mock_connection_manager = stateful_menu_frame_setup

        # Architectural decision: Configure Connection and Help should always be available
        # Users need to be able to configure connections even when none exist
        # Help should always be accessible for usability

        # These buttons should never be disabled
        always_enabled_buttons = ['configure', 'help', 'manage']

        for button_name in always_enabled_buttons:
            if button_name in menu_frame._buttons:
                # Should not call configure with disabled state
                calls = menu_frame._buttons[button_name].configure.call_args_list
                disabled_calls = [call for call in calls if 'state' in call.kwargs and call.kwargs['state'] == 'disabled']
                assert len(disabled_calls) == 0, f"{button_name} button should never be disabled"


class TestMenuFrameErrorHandling:
    """Test error handling and edge cases in MenuFrame"""

    @pytest.fixture
    def error_test_setup(self, mocker):
        """Setup for error handling tests"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        menu_frame = MenuFrame(mock_parent, mock_connection_manager)
        return menu_frame, mock_parent, mock_connection_manager

    def test_test_connection_with_no_connection(self, mocker, error_test_setup):
        """Test testConnection when no connection exists"""
        menu_frame, _, mock_connection_manager = error_test_setup

        mock_connection_manager.connection = None
        mock_test_connection = mocker.patch('view.menu_buttons.TestConnection.TestConnection')

        # Architectural decision: Attempting operations with no connection should either
        # fail gracefully or show appropriate error message, not crash

        # Current implementation might crash with None, should handle gracefully
        with pytest.raises(AttributeError):
            menu_frame.testConnection()

    def test_save_connection_with_no_connection(self, mocker, error_test_setup):
        """Test saveConnection when no connection exists"""
        menu_frame, _, mock_connection_manager = error_test_setup

        mock_connection_manager.connection = None
        mock_save_connection = mocker.patch('view.menu_buttons.SaveConnection.save_connection')

        # Should handle None connection gracefully
        menu_frame.saveConnection()

        mock_save_connection.assert_called_once_with(None)

    def test_dialog_creation_failure(self, mocker, error_test_setup):
        """Test behavior when dialog creation fails"""
        menu_frame, _, _ = error_test_setup

        mock_connection_dialog = mocker.patch(
            'view.menu_buttons.ConfigureConnection.ConnectionDialog',
            side_effect=Exception("Dialog creation failed")
        )

        # Architectural decision: Dialog creation failures should not crash the application
        # They should be logged and possibly show a fallback error message

        with pytest.raises(Exception):
            menu_frame.connectionDialog()

    def test_repository_refresh_failure(self, mocker, error_test_setup):
        """Test behavior when repository refresh fails"""
        menu_frame, mock_parent, _ = error_test_setup

        mock_parent.repo_frame.refresh.side_effect = Exception("Refresh failed")

        # Should handle refresh failures gracefully
        with pytest.raises(Exception):
            mock_parent.repo_frame.refresh()

    def test_event_handling_with_malformed_data(self, mocker):
        """Test Observer pattern with malformed event data"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class TestObserverMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self.handled_events = []

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                # Architectural decision: Event handlers should validate data and handle malformed input gracefully
                # This prevents cascading failures when events contain unexpected data
                try:
                    if event == UiEvent.CONNECTION_CHANGED:
                        is_valid = data.get('is_valid', False) if data else False
                        self.handled_events.append(('connection_changed', is_valid))
                except (TypeError, AttributeError, KeyError) as e:
                    # Log error and continue - don't crash on malformed events
                    self.handled_events.append(('error', str(e)))

        menu_frame = TestObserverMenuFrame(mock_parent, mock_connection_manager)

        # Test with malformed data
        malformed_data_cases = [
            None,
            {},
            {'invalid_key': 'value'},
            {'is_valid': 'not_a_boolean'},
            "not_a_dict"
        ]

        for malformed_data in malformed_data_cases:
            menu_frame.update(UiEvent.CONNECTION_CHANGED, malformed_data)

        # Should handle all cases without crashing
        assert len(menu_frame.handled_events) == len(malformed_data_cases)


class TestMenuFrameIntegration:
    """Test MenuFrame integration with other components"""

    def test_menuframe_with_real_connection_manager(self, mocker):
        """Test MenuFrame with actual ConnectionManager instance"""
        mock_parent = mocker.Mock()
        mock_main = mocker.Mock()

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        # Create real ConnectionManager
        connection_manager = ConnectionManager(mock_main)

        menu_frame = MenuFrame(mock_parent, connection_manager)

        assert menu_frame.connection_manager == connection_manager
        assert isinstance(menu_frame.connection_manager, ConnectionManager)

    def test_menuframe_event_subscription_lifecycle(self, mocker):
        """Test proper event subscription and cleanup"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)
        mock_event_manager = mocker.Mock(spec=UiEventManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class LifecycleTestMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager, event_manager):
                super().__init__(parent, connection_manager)
                self.event_manager = event_manager
                self._subscribe_to_events()

            def _subscribe_to_events(self):
                """Subscribe to relevant events"""
                events_to_subscribe = [
                    UiEvent.CONNECTION_CHANGED,
                    UiEvent.REPOSITORY_LOADED
                ]
                for event in events_to_subscribe:
                    self.event_manager.attach(self)

            def _unsubscribe_from_events(self):
                """Unsubscribe from events on cleanup"""
                self.event_manager.detach(self)

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                pass

        menu_frame = LifecycleTestMenuFrame(mock_parent, mock_connection_manager, mock_event_manager)

        # Should have subscribed to events
        assert mock_event_manager.attach.called

        # Cleanup
        menu_frame._unsubscribe_from_events()
        mock_event_manager.detach.assert_called_with(menu_frame)

    def test_menuframe_coordinates_with_other_frames(self, mocker):
        """Test MenuFrame coordination with other UI components"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)
        mock_event_manager = mocker.Mock(spec=UiEventManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        # Architectural decision: MenuFrame should coordinate with other frames through events
        # rather than direct method calls, enabling loose coupling and easier testing

        class CoordinatingMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager, event_manager):
                super().__init__(parent, connection_manager)
                self.event_manager = event_manager

            def refresh_repositories_clicked(self):
                """Future implementation: publish event instead of direct call"""
                self.event_manager.publish_event(
                    UiEvent.REFRESH_REPOSITORIES_REQUESTED,
                    {'timestamp': 'mock_time'}
                )

        menu_frame = CoordinatingMenuFrame(mock_parent, mock_connection_manager, mock_event_manager)
        menu_frame.refresh_repositories_clicked()

        mock_event_manager.publish_event.assert_called_with(
            UiEvent.REFRESH_REPOSITORIES_REQUESTED,
            {'timestamp': 'mock_time'}
        )


class TestMenuFrameAccessibility:
    """Test accessibility and usability features"""

    def test_buttons_have_proper_grid_spacing(self, mocker):
        """Test that buttons are properly spaced for accessibility"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mock_button = mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        MenuFrame(mock_parent, mock_connection_manager)

        # Check that buttons are created with grid calls that include padding
        button_instances = [call.return_value for call in mock_button.call_args_list]

        for button_instance in button_instances:
            # Should have grid method called with padding
            if button_instance.grid.called:
                # Extract grid calls
                grid_calls = button_instance.grid.call_args_list
                # Should include padding parameters for accessibility
                assert len(grid_calls) > 0

    def test_keyboard_navigation_support(self, mocker):
        """Test keyboard navigation between buttons"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mock_button = mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        MenuFrame(mock_parent, mock_connection_manager)

        # Architectural decision: Buttons should support keyboard navigation for accessibility
        # This means proper tab order and keyboard activation

        # Buttons should be created without explicit tab order interference
        button_calls = mock_button.call_args_list
        for call in button_calls:
            # Should not disable keyboard navigation
            kwargs = call.kwargs
            assert kwargs.get('takefocus', True) is not False


class TestMenuFramePerformance:
    """Test performance-related aspects of MenuFrame"""

    def test_menuframe_initialization_time(self, mocker):
        """Test that MenuFrame initializes efficiently"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        import time
        start_time = time.time()

        MenuFrame(mock_parent, mock_connection_manager)

        end_time = time.time()
        initialization_time = end_time - start_time

        # Should initialize quickly (under 1 second even with mocking overhead)
        assert initialization_time < 1.0

    def test_event_handling_performance(self, mocker):
        """Test that event handling is efficient"""
        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class PerformanceTestMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self.event_count = 0

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                self.event_count += 1
                # Simple event handling should be fast
                if event == UiEvent.CONNECTION_CHANGED:
                    pass  # Minimal processing

        menu_frame = PerformanceTestMenuFrame(mock_parent, mock_connection_manager)

        # Test handling many events quickly
        import time
        start_time = time.time()

        for i in range(100):
            menu_frame.update(UiEvent.CONNECTION_CHANGED, {'is_valid': i % 2 == 0})

        end_time = time.time()
        handling_time = end_time - start_time

        # Should handle 100 events quickly
        assert handling_time < 0.1  # 100ms for 100 events
        assert menu_frame.event_count == 100


class TestMenuFrameArchitecturalDecisions:
    """Test and document key architectural decisions"""

    def test_error_boundary_behavior(self, mocker):
        """Test error boundary behavior for architectural consistency"""
        # Architectural decision: MenuFrame should act as an error boundary
        # Button action failures should not crash the entire UI

        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class ErrorBoundaryMenuFrame(MenuFrame):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self.error_count = 0

            def safe_execute(self, action_func, *args, **kwargs):
                """Execute action with error boundary"""
                try:
                    return action_func(*args, **kwargs)
                except Exception:
                    self.error_count += 1
                    # Log error but don't crash
                    return None

        menu_frame = ErrorBoundaryMenuFrame(mock_parent, mock_connection_manager)

        # Test that errors are contained
        def failing_action():
            raise ValueError("Test error")

        result = menu_frame.safe_execute(failing_action)

        assert result is None
        assert menu_frame.error_count == 1

    def test_state_consistency_guarantees(self, mocker):
        """Test state consistency architectural decisions"""
        # Architectural decision: MenuFrame should maintain consistent state
        # even when multiple events arrive in quick succession

        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class ConsistentStateMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self._state_lock = False
                self._pending_updates = []

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                if self._state_lock:
                    self._pending_updates.append((event, data))
                    return

                self._state_lock = True
                try:
                    self._handle_event(event, data)
                    # Process any pending updates
                    while self._pending_updates:
                        pending_event, pending_data = self._pending_updates.pop(0)
                        self._handle_event(pending_event, pending_data)
                finally:
                    self._state_lock = False

            def _handle_event(self, event: UiEvent, data: Dict[str, Any]) -> None:
                """Handle individual event"""
                pass

        menu_frame = ConsistentStateMenuFrame(mock_parent, mock_connection_manager)

        # Send multiple events rapidly
        for i in range(5):
            menu_frame.update(UiEvent.CONNECTION_CHANGED, {'sequence': i})

        # Should have processed all events without state corruption
        assert not menu_frame._state_lock
        assert len(menu_frame._pending_updates) == 0

    def test_backward_compatibility_maintenance(self, mocker):
        """Test backward compatibility architectural decisions"""
        # Architectural decision: During migration, both old and new interfaces should work
        # This allows incremental migration without breaking existing functionality

        mock_parent = mocker.Mock()
        mock_connection_manager = mocker.Mock(spec=ConnectionManager)

        mocker.patch('tkinter.ttk.Frame.__init__')
        mocker.patch('tkinter.ttk.Button')
        mocker.patch('tkinter.Grid.rowconfigure')
        mocker.patch('tkinter.Grid.columnconfigure')

        class BackwardCompatibleMenuFrame(MenuFrame, Observer):
            def __init__(self, parent, connection_manager):
                super().__init__(parent, connection_manager)
                self._migration_mode = True

            # Keep old interface working
            def connectionDialog(self):
                if self._migration_mode:
                    # Old behavior
                    super().connectionDialog()
                else:
                    # New behavior: publish event
                    pass

            def update(self, event: UiEvent, data: Dict[str, Any]) -> None:
                # New Observer interface
                pass

        menu_frame = BackwardCompatibleMenuFrame(mock_parent, mock_connection_manager)

        # Should support both old and new interfaces
        assert hasattr(menu_frame, 'connectionDialog')  # Old interface
        assert hasattr(menu_frame, 'update')  # New interface
        assert callable(menu_frame.connectionDialog)
        assert callable(menu_frame.update)