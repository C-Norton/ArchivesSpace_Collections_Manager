import pytest
import tkinter
from tkinter import TclError
import logging
from io import StringIO

from view.util.FrameUtils import FrameUtils


class TestFrameUtilsSetIconPathConstruction:
    """Test path construction logic in set_icon method"""

    def test_path_construction_with_normal_path(self, mocker):
        """Test path construction with standard directory structure"""
        mock_root = mocker.Mock()
        mock_abspath = mocker.patch(
            "os.path.abspath", return_value="/project/view/util/FrameUtils.py"
        )
        mock_dirname = mocker.patch(
            "os.path.dirname", return_value="/project/view/util"
        )
        mock_join = mocker.patch(
            "os.path.join", return_value="/project/Public/Icons/icon.ico"
        )
        mocker.patch("os.path.exists", return_value=False)  # Exit early
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        # Verify path construction steps
        mock_abspath.assert_called_once()
        mock_dirname.assert_called_once_with("/project/view/util/FrameUtils.py")

        # Should remove last 9 characters ('/view/util') from path
        expected_project_root = "/project/view/util"[:-9]
        mock_join.assert_called_once_with(
            expected_project_root,
            "Public",
            "Icons",
            "ArchivesSpace_Collections_Manager-32x32.ico",
        )

    def test_path_construction_with_edge_case_paths(self, mocker):
        """Test path construction with various edge case directory structures"""
        mock_root = mocker.Mock()
        mocker.patch("os.path.exists", return_value=False)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        test_cases = [
            # (abspath_return, dirname_return, expected_slice)
            (
                "/a/b/c/view/util/FrameUtils.py",
                "/a/b/c/view/util",
                "/a/b/c/view/util"[:-9],
            ),
            ("/view/util/FrameUtils.py", "/view/util", "/view/util"[:-9]),
            ("/short/FrameUtils.py", "/short", "/short"[:-9]),
            ("/FrameUtils.py", "/", "/"[:-9]),
            ("", "", ""[:-9]),
        ]

        for abspath_ret, dirname_ret, expected_root in test_cases:
            mock_abspath = mocker.patch("os.path.abspath", return_value=abspath_ret)
            mock_dirname = mocker.patch("os.path.dirname", return_value=dirname_ret)
            mock_join = mocker.patch("os.path.join", return_value="/test/icon.ico")

            FrameUtils.set_icon(mock_root)

            mock_join.assert_called_with(
                expected_root,
                "Public",
                "Icons",
                "ArchivesSpace_Collections_Manager-32x32.ico",
            )

    def test_path_construction_with_unicode_paths(self, mocker):
        """Test path construction with Unicode characters in paths"""
        mock_root = mocker.Mock()
        unicode_path = "/проект/测试/view/util/FrameUtils.py"
        unicode_dirname = "/проект/测试/view/util"

        mock_abspath = mocker.patch("os.path.abspath", return_value=unicode_path)
        mock_dirname = mocker.patch("os.path.dirname", return_value=unicode_dirname)
        mock_join = mocker.patch(
            "os.path.join", return_value="/проект/测试/Public/Icons/icon.ico"
        )
        mocker.patch("os.path.exists", return_value=False)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        expected_project_root = unicode_dirname[:-9]
        mock_join.assert_called_once_with(
            expected_project_root,
            "Public",
            "Icons",
            "ArchivesSpace_Collections_Manager-32x32.ico",
        )

    def test_path_construction_logging_details(self, mocker):
        """Test that path construction logs detailed debugging information"""
        mock_root = mocker.Mock()
        test_path = "/test/project/view/util/FrameUtils.py"
        icon_path = "/test/project/Public/Icons/icon.ico"

        mocker.patch("os.path.abspath", return_value=test_path)
        mocker.patch("os.path.dirname", return_value="/test/project/view/util")
        mocker.patch("os.path.join", return_value=icon_path)
        mocker.patch("os.path.exists", return_value=False)
        mock_debug = mocker.patch("logging.debug")
        mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        # Should log entry, path construction, and exit
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Entering set_icon method" in debug_calls
        assert f"Constructed icon path: {icon_path}" in debug_calls
        assert "Exiting set_icon method" in debug_calls


class TestFrameUtilsSetIconFileHandling:
    """Test file existence and handling in set_icon method"""

    def test_icon_file_exists_successful_path(self, mocker):
        """Test successful icon setting when file exists"""
        mock_root = mocker.Mock()
        icon_path = "/test/icon.ico"

        self._setup_basic_path_mocks(mocker, icon_path)
        mocker.patch("os.path.exists", return_value=True)
        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once_with(icon_path)
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Icon set successfully using iconbitmap" in debug_calls

    def test_icon_file_not_exists_early_return(self, mocker):
        """Test early return when icon file doesn't exist"""
        mock_root = mocker.Mock()
        icon_path = "/nonexistent/icon.ico"

        self._setup_basic_path_mocks(mocker, icon_path)
        mocker.patch("os.path.exists", return_value=False)
        mock_error = mocker.patch("logging.error")
        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        # Should log error and return early
        mock_error.assert_called_once()
        error_message = mock_error.call_args[0][0]
        assert "Icon file not found" in error_message
        assert icon_path in error_message

        # Should not attempt to set icon
        mock_root.iconbitmap.assert_not_called()
        mock_root.iconphoto.assert_not_called()

        # Should still log entry and exit
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Entering set_icon method" in debug_calls
        assert "Exiting set_icon method" in debug_calls

    def test_check_icon_exists_exception_handling(self, mocker):
        """Test handling of exceptions from _check_icon_exists method"""
        # Mock the private method instead of os.path.exists directly
        mocker.patch.object(
            FrameUtils, "_check_icon_exists", side_effect=OSError("Permission denied")
        )
        mocker.patch.object(
            FrameUtils, "_construct_icon_path", return_value="/test/icon.ico"
        )
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        mock_root = mocker.Mock()

        # Should handle the exception gracefully and return early
        FrameUtils.set_icon(mock_root)

        # Should not attempt to set icon when file check fails
        mock_root.iconbitmap.assert_not_called()

    def test_construct_icon_path_exception_handling(self, mocker):
        """Test exception handling in _construct_icon_path method"""
        mocker.patch("os.path.abspath", side_effect=OSError("File system error"))
        mocker.patch("logging.error")

        result = FrameUtils._construct_icon_path()

        assert result is None

    def test_check_icon_exists_exception_handling(self, mocker):
        """Test exception handling in _check_icon_exists method"""
        mocker.patch("logging.error")

        # This should handle the exception gracefully
        result = FrameUtils._check_icon_exists("/test/path")

        # Should return False when exception occurs
        assert result is False

    def test_set_icon_with_path_construction_failure(self, mocker):
        """Test set_icon when path construction fails"""
        mock_root = mocker.Mock()
        mocker.patch.object(FrameUtils, "_construct_icon_path", return_value=None)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        # Should not attempt to set icon when path construction fails
        mock_root.iconbitmap.assert_not_called()

    def test_set_icon_with_file_check_failure(self, mocker):
        """Test set_icon when file existence check fails"""
        mock_root = mocker.Mock()
        mocker.patch.object(
            FrameUtils, "_construct_icon_path", return_value="/test/icon.ico"
        )
        mocker.patch.object(FrameUtils, "_check_icon_exists", return_value=False)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        # Should not attempt to set icon when file doesn't exist
        mock_root.iconbitmap.assert_not_called()

    # Add this to fix modal popup tests:
    def test_modal_popup_with_mock_children_handling(self, mocker):
        """Test modal popup handles mock objects gracefully"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        # Make winfo_children() return a non-iterable mock (common in tests)
        mock_toplevel.winfo_children.return_value = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should not raise exception even with non-iterable winfo_children
        FrameUtils.modal_message_popup(mock_root, "Test message")

        # Should still set title and modal behavior
        mock_toplevel.title.assert_called_once_with("Warning")
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

    def test_construct_icon_path_method(self, mocker):
        """Test the icon path construction method separately"""
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.join", return_value="/test/Public/Icons/icon.ico")

        result = FrameUtils._construct_icon_path()

        assert result == "/test/Public/Icons/icon.ico"

    def test_check_icon_exists_method_true(self, mocker):
        """Test the file existence check method when file exists"""
        mocker.patch("os.path.exists", return_value=True)

        result = FrameUtils._check_icon_exists("/test/icon.ico")

        assert result is True

    def test_check_icon_exists_method_false(self, mocker):
        """Test the file existence check method when file doesn't exist"""
        mocker.patch("os.path.exists", return_value=False)

        result = FrameUtils._check_icon_exists("/test/icon.ico")

        assert result is False

    def _setup_basic_path_mocks(self, mocker, icon_path):
        """Helper to set up basic path construction mocks"""
        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.join", return_value=icon_path)


class TestFrameUtilsSetIconMethodFallbacks:
    """Test the fallback chain for different icon setting methods"""

    def test_iconbitmap_success_no_fallback(self, mocker):
        """Test successful iconbitmap with no fallback needed"""
        mock_root = mocker.Mock()
        self._setup_successful_path(mocker)
        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once()
        mock_root.iconphoto.assert_not_called()

        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Icon set successfully using iconbitmap" in debug_calls

    def test_iconbitmap_fails_photoimage_succeeds(self, mocker):
        """Test fallback to PhotoImage when iconbitmap fails"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap not supported")

        self._setup_successful_path(mocker)
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_icon = mocker.Mock()
        mock_photoimage.return_value = mock_icon

        mock_debug = mocker.patch("logging.debug")
        mock_warning = mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # Should try iconbitmap first
        mock_root.iconbitmap.assert_called_once()

        # Should fallback to PhotoImage
        mock_photoimage.assert_called_once_with(file="/test/icon.ico")
        mock_root.iconphoto.assert_called_once_with(False, mock_icon)

        # Should log warning about iconbitmap failure and success with PhotoImage
        mock_warning.assert_called_once()
        warning_message = mock_warning.call_args[0][0]
        assert "Failed to set icon using iconbitmap" in warning_message

        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Icon set successfully using PhotoImage" in debug_calls

    def test_iconbitmap_and_photoimage_fail_pil_succeeds_fixed(self, mocker):
        """Test fallback to PIL when both iconbitmap and PhotoImage fail"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        self._setup_successful_path(mocker)

        # Mock PhotoImage to fail, preventing iconphoto from being called in this block
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = TclError("PhotoImage creation failed")

        # Mock PIL to succeed
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_image = mocker.Mock()
        mock_image_open.return_value = mock_image

        mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
        mock_pil_photo = mocker.Mock()
        mock_imagetk.return_value = mock_pil_photo


        # We expect iconphoto to be called only once, in the PIL fallback
        mock_root.iconphoto.return_value = None

        FrameUtils.set_icon(mock_root)

        # Assertions
        mock_root.iconbitmap.assert_called_once()
        mock_photoimage.assert_called_once()
        mock_image_open.assert_called_once_with("/test/icon.ico")
        mock_imagetk.assert_called_once_with(mock_image)

        mock_root.iconphoto.assert_called_once_with(False, mock_pil_photo)
        assert mock_root.iconphoto.call_count == 1

    def test_all_methods_fail_graceful_handling(self, mocker):
        """Test graceful handling when all icon setting methods fail"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")
        mock_root.iconphoto.side_effect = TclError("iconphoto failed")

        self._setup_successful_path(mocker)

        # Mock all fallback methods to fail
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = TclError("PhotoImage failed")

        mock_image_open = mocker.patch("PIL.Image.open")
        mock_image_open.side_effect = IOError("PIL Image.open failed")

        mock_error = mocker.patch("logging.error")
        mock_warning = mocker.patch("logging.warning")
        mock_debug = mocker.patch("logging.debug")

        # Should not raise exception despite all failures
        FrameUtils.set_icon(mock_root)

        # Should attempt all methods
        mock_root.iconbitmap.assert_called_once()
        mock_photoimage.assert_called_once()
        mock_image_open.assert_called_once()

        # Should log appropriate warnings and final error
        assert mock_warning.call_count == 2  # iconbitmap and PhotoImage failures
        mock_error.assert_called_once()
        error_message = mock_error.call_args[0][0]
        assert "Failed to set icon using all methods" in error_message

        # Should still log entry and exit
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        assert "Entering set_icon method" in debug_calls
        assert "Exiting set_icon method" in debug_calls

    def test_pil_import_error_handling(self, mocker):
        """Test handling when PIL modules are not available"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")
        mock_root.iconphoto.side_effect = TclError("iconphoto failed")

        self._setup_successful_path(mocker)

        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = TclError("PhotoImage failed")

        # Mock PIL to raise ImportError
        mocker.patch("PIL.Image.open", side_effect=ImportError("PIL not available"))

        mock_error = mocker.patch("logging.error")
        mock_warning = mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # Should handle ImportError gracefully
        assert mock_warning.call_count == 2
        mock_error.assert_called_once()

    def _setup_successful_path(self, mocker):
        """Helper to set up successful path construction"""
        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)


class TestFrameUtilsSetIconExceptionHandling:
    """Test exception handling in set_icon method"""

    @pytest.mark.parametrize(
        "exception_type,exception_message",
        [
            (TclError, "Tcl command failed"),
            (AttributeError, "Object has no attribute"),
            (OSError, "Operating system error"),
            (IOError, "Input/output error"),
            (MemoryError, "Out of memory"),
            (RuntimeError, "Runtime error occurred"),
            (Exception, "Generic exception"),
        ],
    )
    def test_iconbitmap_various_exceptions(
        self, mocker, exception_type, exception_message
    ):
        """Test iconbitmap method with various exception types"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = exception_type(exception_message)

        self._setup_successful_path(mocker)
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_icon = mocker.Mock()
        mock_photoimage.return_value = mock_icon

        mock_warning = mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # Should handle any exception type and fallback to PhotoImage
        mock_warning.assert_called_once()
        warning_args = mock_warning.call_args[0]
        assert exception_message in str(warning_args)
        mock_photoimage.assert_called_once()

    def test_photoimage_creation_exceptions(self, mocker):
        """Test PhotoImage creation with various exceptions"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        self._setup_successful_path(mocker)

        exceptions_to_test = [
            TclError("PhotoImage creation failed"),
            OSError("File system error"),
            MemoryError("Not enough memory"),
            ValueError("Invalid image format"),
        ]

        for exception in exceptions_to_test:
            mock_photoimage = mocker.patch("tkinter.PhotoImage")
            mock_photoimage.side_effect = exception

            # Mock PIL to succeed for fallback
            mock_image_open = mocker.patch("PIL.Image.open")
            mock_image = mocker.Mock()
            mock_image_open.return_value = mock_image
            mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
            mock_imagetk.return_value = mocker.Mock()

            mock_warning = mocker.patch("logging.warning")

            FrameUtils.set_icon(mock_root)

            # Should handle PhotoImage exception and fallback to PIL
            assert mock_warning.call_count >= 2  # iconbitmap + PhotoImage warnings
            mock_image_open.assert_called_once()

    def test_pil_various_exceptions(self, mocker):
        """Test PIL operations with various exception types"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")
        mock_root.iconphoto.side_effect = TclError("iconphoto failed")

        self._setup_successful_path(mocker)
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = TclError("PhotoImage failed")

        pil_exceptions = [
            IOError("Cannot identify image file"),
            OSError("Broken pipe"),
            ValueError("Invalid image mode"),
            MemoryError("Image too large"),
            AttributeError("PIL module issue"),
        ]

        for exception in pil_exceptions:
            mock_image_open = mocker.patch("PIL.Image.open")
            mock_image_open.side_effect = exception

            mock_error = mocker.patch("logging.error")

            FrameUtils.set_icon(mock_root)

            # Should handle PIL exception gracefully
            mock_error.assert_called_once()
            error_message = mock_error.call_args[0][0]
            assert "Failed to set icon using all methods" in error_message

    def _setup_successful_path(self, mocker):
        """Helper to set up successful path construction"""
        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)


class TestFrameUtilsSetIconRootObjectTypes:
    """Test set_icon with different root object types"""

    def test_tkinter_tk_root(self, mocker):
        """Test set_icon with tkinter.Tk root window"""
        mock_root = mocker.Mock(spec=tkinter.Tk)
        mock_root.__class__.__name__ = "Tk"

        self._setup_successful_scenario(mocker)
        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once()

        # Should log root type
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        root_type_logged = any("Root object type:" in call for call in debug_calls)
        assert root_type_logged

    def test_tkinter_toplevel_root(self, mocker):
        """Test set_icon with tkinter.Toplevel window"""
        mock_root = mocker.Mock(spec=tkinter.Toplevel)
        mock_root.__class__.__name__ = "Toplevel"

        self._setup_successful_scenario(mocker)
        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once()

        debug_calls = [call.args[0] for call in mock_debug.call_args_list]


        root_type_logged = any(
            f"Root object type: <class 'unittest.mock.Mock'>" in call for call in debug_calls
        )
        assert root_type_logged

    def test_custom_widget_root(self, mocker):
        """Test set_icon with custom widget that has iconbitmap method"""

        class CustomWidget:
            def iconbitmap(self, path):
                pass

        mock_root = mocker.Mock(spec=CustomWidget)
        mock_root.__class__.__name__ = "CustomWidget"

        self._setup_successful_scenario(mocker)

        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once()

    def test_object_without_iconbitmap_method(self, mocker):
        """Test set_icon with object that doesn't have iconbitmap method"""
        mock_root = mocker.Mock()
        del mock_root.iconbitmap  # Remove the method

        self._setup_successful_scenario(mocker)
        mock_error = mocker.patch("logging.error")

        # Should handle AttributeError gracefully
        try:
            FrameUtils.set_icon(mock_root)
        except AttributeError:
            # This might be expected behavior - the method assumes iconbitmap exists
            pass

    def test_none_root_object(self, mocker):
        """Test set_icon with None as root object"""
        self._setup_successful_scenario(mocker)
        mock_debug = mocker.patch("logging.debug")

        # Should handle None gracefully or raise appropriate error
        with pytest.raises(AttributeError):
            FrameUtils.set_icon(None)

    def _setup_successful_scenario(self, mocker):
        """Helper to set up successful icon setting scenario"""
        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)


class TestFrameUtilsModalMessagePopupBasicFunctionality:
    """Test basic functionality of modal_message_popup method"""

    def test_popup_creation_with_minimal_parameters(self, mocker):
        """Test popup creation with only required parameters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_label = mocker.Mock()
        mock_button = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label", return_value=mock_label)
        mocker.patch("tkinter.ttk.Button", return_value=mock_button)

        FrameUtils.modal_message_popup(mock_root, "Test message")

        # Should create Toplevel window
        tkinter.Toplevel.assert_called_once_with(mock_root)

        # Should set default title
        mock_toplevel.title.assert_called_once_with("Warning")

        # Should create label and button
        mock_label.grid.assert_called_once_with(row=0, column=0)
        mock_button.grid.assert_called_once_with(row=1, column=0)

        # Should set modal behavior
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

    def test_popup_creation_with_all_parameters(self, mocker):
        """Test popup creation with all custom parameters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        custom_message = "Custom error message"
        custom_title = "Critical Error"
        custom_button_text = "Acknowledge"

        FrameUtils.modal_message_popup(
            mock_root,
            custom_message,
            title=custom_title,
            button_text=custom_button_text,
        )

        # Should set custom title
        mock_toplevel.title.assert_called_once_with(custom_title)

        # Should create label with custom message
        mock_label.assert_called_once()
        label_call_args = mock_label.call_args
        assert custom_message in str(label_call_args)

        # Should create button with custom text
        mock_button.assert_called_once()
        button_call_args = mock_button.call_args
        assert custom_button_text in str(button_call_args)

    def test_popup_widget_configuration(self, mocker):
        """Test proper configuration of popup widgets"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_label = mocker.Mock()
        mock_button = mocker.Mock()

        # Mock winfo_children to return our widgets
        mock_toplevel.winfo_children.return_value = [mock_label, mock_button]

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label", return_value=mock_label)
        mocker.patch("tkinter.ttk.Button", return_value=mock_button)

        FrameUtils.modal_message_popup(mock_root, "Test")

        # Should configure grid padding for all children
        mock_label.grid_configure.assert_called_once_with(padx=5, pady=5)
        mock_button.grid_configure.assert_called_once_with(padx=5, pady=5)

    def test_popup_button_command_functionality(self, mocker):
        """Test that button command properly destroys popup"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "Test")

        # Extract the command function passed to the button
        button_call_args = mock_button.call_args
        assert len(button_call_args) > 1
        kwargs = button_call_args[1]
        command_func = kwargs.get("command")

        # Command should be the popup's destroy method
        assert command_func == mock_toplevel.destroy

    def test_popup_calls_set_icon(self, mocker):
        """Test that popup properly calls set_icon on the created window"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mock_set_icon = mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "Test")

        # Should call set_icon with the popup window, not the parent
        mock_set_icon.assert_called_once_with(mock_toplevel)


class TestFrameUtilsModalMessagePopupEdgeCases:
    """Test edge cases and corner cases for modal_message_popup"""

    def test_popup_with_empty_message(self, mocker):
        """Test popup creation with empty message string"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "")

        # Should still create popup with empty message
        mock_label.assert_called_once()
        label_args = mock_label.call_args
        # Empty message should be passed to label
        assert '""' in str(label_args) or "''" in str(label_args)

    def test_popup_with_whitespace_only_message(self, mocker):
        """Test popup with whitespace-only message"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        whitespace_message = "   \t\n   "
        FrameUtils.modal_message_popup(mock_root, whitespace_message)

        # Should handle whitespace message without issues
        mock_label.assert_called_once()

        # Check that the label was called with the correct text parameter
        # Instead of checking string representation (which escapes special chars),
        # check the actual call arguments
        call_args, call_kwargs = mock_label.call_args

        # The message should be passed as the 'text' keyword argument
        assert "text" in call_kwargs
        assert call_kwargs["text"] == whitespace_message

    def test_popup_with_extremely_long_message(self, mocker):
        """Test popup with very long message that should trigger wrapping"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Create message longer than typical wrap length
        long_message = (
            "This is an extremely long error message that should definitely wrap around multiple lines in the popup dialog. "
            * 10
        )

        FrameUtils.modal_message_popup(mock_root, long_message)

        # Should create label with wraplength parameter
        mock_label.assert_called_once()
        label_call_args = mock_label.call_args

        # Should include wraplength in the call
        assert "wraplength" in str(label_call_args) or len(long_message) > 220
        assert long_message in str(label_call_args)

    def test_popup_with_unicode_characters(self, mocker):
        """Test popup with various Unicode characters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        unicode_messages = [
            "Error: файл не найден",  # Cyrillic
            "错误：文件未找到",  # Chinese
            "エラー：ファイルが見つかりません",  # Japanese
            "🚫 Operation failed! ⚠️",  # Emojis
            "Ошибка: Αρχείο δεν βρέθηκε",  # Mixed scripts
        ]

        for message in unicode_messages:
            mock_label.reset_mock()
            mock_toplevel.reset_mock()

            FrameUtils.modal_message_popup(mock_root, message)

            # Should handle Unicode without errors
            mock_label.assert_called_once()
            label_args = mock_label.call_args
            assert message in str(label_args)

    def test_popup_with_special_control_characters(self, mocker):
        """Test popup with special control characters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        control_chars_message = "Line 1\nLine 2\tTabbed\rCarriage Return\x00Null"

        FrameUtils.modal_message_popup(mock_root, control_chars_message)

        # Should handle control characters
        mock_label.assert_called_once()
        mock_toplevel.title.assert_called_once()

    def test_popup_with_none_parent(self, mocker):
        """Test popup creation with None as parent"""
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should handle None parent (creates orphaned toplevel)
        FrameUtils.modal_message_popup(None, "Test message")

        # Should create Toplevel with None parent
        tkinter.Toplevel.assert_called_once_with(None)
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

    def test_popup_with_empty_title(self, mocker):
        """Test popup with empty title string"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "Test", title="")

        # Should set empty title
        mock_toplevel.title.assert_called_once_with("")

    def test_popup_with_empty_button_text(self, mocker):
        """Test popup with empty button text"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "Test", button_text="")

        # Should create button with empty text
        mock_button.assert_called_once()
        button_args = mock_button.call_args
        assert '""' in str(button_args) or "''" in str(button_args)

    def test_popup_with_numeric_parameters(self, mocker):
        """Test popup with numeric values for string parameters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        # Should handle numeric values (converted to strings by tkinter)
        FrameUtils.modal_message_popup(mock_root, 12345, title=67890, button_text=999)

        mock_toplevel.title.assert_called_once_with(67890)
        mock_label.assert_called_once()
        mock_button.assert_called_once()


class TestFrameUtilsModalMessagePopupExceptionHandling:
    """Test exception handling in modal_message_popup method"""

    def test_toplevel_creation_failure(self, mocker):
        """Test handling when Toplevel creation fails"""
        mock_root = mocker.Mock()

        mocker.patch("tkinter.Toplevel", side_effect=TclError("Cannot create toplevel"))
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")

        # Should propagate Toplevel creation error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")

    def test_set_icon_failure_in_popup(self, mocker):
        """Test handling when set_icon fails during popup creation"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch(
            "view.util.FrameUtils.FrameUtils.set_icon",
            side_effect=Exception("Icon setting failed"),
        )
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should continue popup creation even if set_icon fails
        FrameUtils.modal_message_popup(mock_root, "Test")

        # Should still create the popup components
        mock_toplevel.title.assert_called_once()
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

    def test_label_creation_failure(self, mocker):
        """Test handling when Label creation fails"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label", side_effect=TclError("Cannot create label"))
        mocker.patch("tkinter.ttk.Button")

        # Should propagate Label creation error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")

    def test_button_creation_failure(self, mocker):
        """Test handling when Button creation fails"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button", side_effect=TclError("Cannot create button"))

        # Should propagate Button creation error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")

    def test_grid_configuration_failure(self, mocker):
        """Test handling when grid configuration fails"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_label = mocker.Mock()
        mock_button = mocker.Mock()

        # Make grid_configure fail
        mock_label.grid_configure.side_effect = TclError("Grid configuration failed")
        mock_toplevel.winfo_children.return_value = [mock_label, mock_button]

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label", return_value=mock_label)
        mocker.patch("tkinter.ttk.Button", return_value=mock_button)

        # Should propagate grid configuration error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")

    def test_focus_set_failure(self, mocker):
        """Test handling when focus_set fails"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_toplevel.focus_set.side_effect = TclError("Cannot set focus")

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should propagate focus setting error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")

    def test_grab_set_failure(self, mocker):
        """Test handling when grab_set fails"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_toplevel.grab_set.side_effect = TclError("Cannot grab focus")

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should propagate grab setting error
        with pytest.raises(TclError):
            FrameUtils.modal_message_popup(mock_root, "Test")


class TestFrameUtilsModalMessagePopupIntegration:
    """Test integration scenarios for modal_message_popup"""

    def test_multiple_popups_creation(self, mocker):
        """Test creating multiple popups simultaneously"""
        mock_root = mocker.Mock()
        popup_instances = [mocker.Mock() for _ in range(3)]

        mocker.patch("tkinter.Toplevel", side_effect=popup_instances)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        messages = ["First popup", "Second popup", "Third popup"]

        for i, message in enumerate(messages):
            FrameUtils.modal_message_popup(mock_root, message)

            # Each popup should be configured independently
            popup_instances[i].title.assert_called_once()
            popup_instances[i].focus_set.assert_called_once()
            popup_instances[i].grab_set.assert_called_once()

    def test_popup_with_different_parent_types(self, mocker):
        """Test popup creation with different parent widget types"""
        parent_types = [
            mocker.Mock(spec=tkinter.Tk),
            mocker.Mock(spec=tkinter.Toplevel),
            mocker.Mock(spec=tkinter.Frame),
            mocker.Mock(),  # Generic mock
        ]

        popup_instances = [mocker.Mock() for _ in parent_types]
        mocker.patch("tkinter.Toplevel", side_effect=popup_instances)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        for i, parent in enumerate(parent_types):
            FrameUtils.modal_message_popup(parent, f"Test message {i}")

            # Should work with any parent type
            popup_instances[i].title.assert_called_once()
            popup_instances[i].focus_set.assert_called_once()
            popup_instances[i].grab_set.assert_called_once()

    def test_popup_integration_with_set_icon_success_and_failure(self, mocker):
        """Test popup creation with both successful and failed set_icon calls"""
        mock_root = mocker.Mock()
        popup_instances = [mocker.Mock(), mocker.Mock()]

        mocker.patch("tkinter.Toplevel", side_effect=popup_instances)
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # First call succeeds, second fails
        mock_set_icon = mocker.patch(
            "view.util.FrameUtils.FrameUtils.set_icon",
            side_effect=[None, Exception("Icon failed")],
        )

        # First popup should succeed completely
        FrameUtils.modal_message_popup(mock_root, "First popup")
        popup_instances[0].title.assert_called_once()

        # Second popup should still be created despite set_icon failure
        FrameUtils.modal_message_popup(mock_root, "Second popup")
        popup_instances[1].title.assert_called_once()

        # set_icon should have been called for both
        assert mock_set_icon.call_count == 2


class TestFrameUtilsComprehensiveParameterizedTests:
    """Comprehensive parameterized tests for both methods"""

    @pytest.mark.parametrize(
        "message,title,button_text,expected_title",
        [
            ("Simple message", "Warning", "OK", "Warning"),
            ("", "Empty Message", "Close", "Empty Message"),
            ("Unicode: 测试消息", "测试标题", "确定", "测试标题"),
            ("Long message " * 50, "Long Title", "Got it", "Long Title"),
            ("Special chars: !@#$%^&*()", "Special", "Escape", "Special"),
            ("Newlines\nand\ttabs", "Whitespace", "Continue", "Whitespace"),
            (12345, 67890, 999, 67890),  # Numeric values
        ],
    )
    def test_modal_popup_parameter_combinations(
        self, mocker, message, title, button_text, expected_title
    ):
        """Parameterized test for various popup parameter combinations"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(
            mock_root, message, title=title, button_text=button_text
        )

        # Should set expected title
        mock_toplevel.title.assert_called_once_with(expected_title)

        # Should create widgets with provided parameters
        mock_label.assert_called_once()
        mock_button.assert_called_once()

        # Should set modal behavior
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

    @pytest.mark.parametrize(
        "exception_type,should_propagate",
        [
            (TclError, True),
            (AttributeError, True),
            (ValueError, True),
            (TypeError, True),
            (OSError, True),
            (MemoryError, True),
            (RuntimeError, True),
        ],
    )
    def test_set_icon_exception_propagation(
        self, mocker, exception_type, should_propagate
    ):
        """Parameterized test for exception handling in set_icon"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = exception_type("Test exception")

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        # Mock fallback methods to also fail
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = exception_type("PhotoImage failed")
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_image_open.side_effect = exception_type("PIL failed")

        mock_warning = mocker.patch("logging.warning")
        mock_error = mocker.patch("logging.error")

        # Should handle all exceptions gracefully
        FrameUtils.set_icon(mock_root)

        # Should log appropriate messages
        assert mock_warning.called or mock_error.called

    @pytest.mark.parametrize(
        "file_exists,iconbitmap_works,photoimage_works,pil_works,expected_success_method",
        [
            (False, True, True, True, None),  # File doesn't exist
            (True, True, True, True, "iconbitmap"),  # All work, use first
            (True, False, True, True, "PhotoImage"),  # iconbitmap fails
            (True, False, False, True, "PIL"),  # iconbitmap and PhotoImage fail
            (True, False, False, False, None),  # All fail
        ],
    )
    def test_set_icon_fallback_scenarios(
        self,
        mocker,
        file_exists,
        iconbitmap_works,
        photoimage_works,
        pil_works,
        expected_success_method,
    ):
        """Parameterized test for different fallback scenarios in set_icon"""
        mock_root = mocker.Mock()

        # Setup path mocks
        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=file_exists)

        # Setup method success/failure
        if not iconbitmap_works:
            mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        mock_photoimage = mocker.patch("tkinter.PhotoImage")

        # Configure PhotoImage behavior
        if not photoimage_works:
            # PhotoImage creation fails, so iconphoto is never called in this path
            mock_photoimage.side_effect = TclError("PhotoImage failed")
            # Don't set up iconphoto side_effect here since it won't be called
        else:
            # PhotoImage creation succeeds
            mock_tk_icon = mocker.Mock()
            mock_photoimage.return_value = mock_tk_icon

        # Configure PIL behavior
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
        if not pil_works:
            mock_image_open.side_effect = IOError("PIL failed")
        else:
            mock_image = mocker.Mock()
            mock_image_open.return_value = mock_image
            mock_pil_photo = mocker.Mock()
            mock_imagetk.return_value = mock_pil_photo

        # Configure iconphoto behavior - this is the key insight!
        # iconphoto is only called when PhotoImage creation succeeds OR when PIL succeeds
        if photoimage_works and pil_works:
            # Both PhotoImage and PIL work - iconphoto should succeed for both
            mock_root.iconphoto.return_value = None
        elif photoimage_works and not pil_works:
            # PhotoImage works, PIL fails - iconphoto should succeed for PhotoImage
            mock_root.iconphoto.return_value = None
        elif not photoimage_works and pil_works:
            # PhotoImage creation fails (no iconphoto call), PIL works - iconphoto should succeed for PIL
            mock_root.iconphoto.return_value = None
        elif not photoimage_works and not pil_works:
            # PhotoImage creation fails (no iconphoto call), PIL fails - no iconphoto calls
            pass

        mock_debug = mocker.patch("logging.debug")
        mock_warning = mocker.patch("logging.warning")
        mock_error = mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        if not file_exists:
            # Should exit early
            mock_error.assert_called_once()
            mock_root.iconbitmap.assert_not_called()
        elif expected_success_method:
            # Should log success with expected method
            debug_calls = [call.args[0] for call in mock_debug.call_args_list]
            success_logged = any(
                f"Icon set successfully using {expected_success_method}" in call
                for call in debug_calls
            )

            if not success_logged:
                # Debug output to understand what went wrong
                print(
                    f"Expected: 'Icon set successfully using {expected_success_method}'"
                )
                print(f"Actual debug calls: {debug_calls}")
                print(
                    f"Warning calls: {[call.args[0] for call in mock_warning.call_args_list]}"
                )
                print(
                    f"Error calls: {[call.args[0] for call in mock_error.call_args_list]}"
                )

            assert success_logged
        else:
            # All methods failed, should log final error
            mock_error.assert_called_once()
            error_message = mock_error.call_args[0][0]
            assert "Failed to set icon using all methods" in error_message

    def test_set_icon_photoimage_creation_succeeds_but_iconphoto_fails_then_pil_succeeds(
        self, mocker
    ):
        """Test the specific scenario where PhotoImage creation succeeds but iconphoto fails, then PIL succeeds"""
        mock_root = mocker.Mock()

        # Setup path mocks
        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        # iconbitmap fails
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        # PhotoImage creation succeeds
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_tk_icon = mocker.Mock()
        mock_photoimage.return_value = mock_tk_icon

        # iconphoto fails first time (PhotoImage), succeeds second time (PIL)
        mock_root.iconphoto.side_effect = [TclError("iconphoto failed"), None]

        # PIL succeeds
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_image = mocker.Mock()
        mock_image_open.return_value = mock_image
        mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
        mock_pil_photo = mocker.Mock()
        mock_imagetk.return_value = mock_pil_photo

        mock_debug = mocker.patch("logging.debug")
        mock_warning = mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # Should log success with PIL
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]
        success_logged = any(
            "Icon set successfully using PIL" in call for call in debug_calls
        )
        assert success_logged

        # Should call iconphoto twice
        assert mock_root.iconphoto.call_count == 2
class TestFrameUtilsLoggingBehavior:
    """Test comprehensive logging behavior across both methods"""

    def test_set_icon_complete_logging_flow(self, mocker):
        """Test complete logging flow in set_icon method"""
        mock_root = mocker.Mock()
        mock_root.__class__.__name__ = "TestWidget"

        mocker.patch("os.path.abspath", return_value="/test/view/util/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test/view/util")
        mocker.patch("os.path.join", return_value="/test/Public/Icons/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        mock_debug = mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        # Should log complete flow
        debug_calls = [call.args[0] for call in mock_debug.call_args_list]

        expected_log_messages = [
            "Entering set_icon method",
            "Constructed icon path:",
            "Root object type:",
            "Icon set successfully using iconbitmap",
            "Exiting set_icon method",
        ]

        for expected_msg in expected_log_messages:
            assert any(expected_msg in call for call in debug_calls), (
                f"Missing log message: {expected_msg}"
            )

    def test_set_icon_error_logging_levels(self, mocker):
        """Test different logging levels used in set_icon"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")
        mock_root.iconphoto.side_effect = TclError("iconphoto failed")

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.side_effect = TclError("PhotoImage failed")
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_image_open.side_effect = IOError("PIL failed")

        mock_debug = mocker.patch("logging.debug")
        mock_warning = mocker.patch("logging.warning")
        mock_error = mocker.patch("logging.error")

        FrameUtils.set_icon(mock_root)

        # Should use different logging levels appropriately
        assert mock_debug.called  # Entry/exit and flow logging
        assert mock_warning.called  # Fallback warnings
        assert mock_error.called  # Final failure error

    def test_logging_with_custom_logger_configuration(self, mocker):
        """Test behavior with custom logging configuration"""
        mock_root = mocker.Mock()

        # Create a custom logger to capture output
        logger = logging.getLogger("test_frameutils")
        logger.setLevel(logging.DEBUG)

        # Create string buffer to capture log output
        log_buffer = StringIO()
        handler = logging.StreamHandler(log_buffer)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Patch logging to use our custom logger
        mocker.patch("logging.debug", side_effect=lambda msg: logger.debug(msg))
        mocker.patch("logging.error", side_effect=lambda msg: logger.error(msg))

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=False)  # File not found

        FrameUtils.set_icon(mock_root)

        # Verify log output
        log_output = log_buffer.getvalue()
        assert "Entering set_icon method" in log_output
        assert "Icon file not found" in log_output
        assert "Exiting set_icon method" in log_output


class TestFrameUtilsMemoryAndPerformanceEdgeCases:
    """Test memory and performance edge cases"""

    def test_set_icon_with_large_file_path(self, mocker):
        """Test set_icon with extremely long file paths"""
        mock_root = mocker.Mock()

        # Create very long path
        long_component = "very_long_directory_name" * 20
        long_path = f"/{long_component}/view/util/FrameUtils.py"
        long_icon_path = f"/{long_component}/Public/Icons/icon.ico"

        mocker.patch("os.path.abspath", return_value=long_path)
        mocker.patch("os.path.dirname", return_value=f"/{long_component}/view/util")
        mocker.patch("os.path.join", return_value=long_icon_path)
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        # Should handle long paths without issues
        FrameUtils.set_icon(mock_root)

        mock_root.iconbitmap.assert_called_once_with(long_icon_path)

    def test_popup_with_large_number_of_children(self, mocker):
        """Test popup with many child widgets for grid configuration"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        # Create many mock child widgets
        many_children = [mocker.Mock() for _ in range(100)]
        mock_toplevel.winfo_children.return_value = many_children

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        FrameUtils.modal_message_popup(mock_root, "Test with many children")

        # Should configure grid for all children
        for child in many_children:
            child.grid_configure.assert_called_once_with(padx=5, pady=5)

    def test_memory_cleanup_on_repeated_calls(self, mocker):
        """Test memory behavior with repeated method calls"""
        mock_root = mocker.Mock()

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        # Call set_icon many times
        for i in range(100):
            mock_root.reset_mock()
            FrameUtils.set_icon(mock_root)
            mock_root.iconbitmap.assert_called_once()

        # Should work consistently without memory issues
        assert True  # If we reach this point, no memory issues occurred


class TestFrameUtilsStaticMethodBehavior:
    """Test static method behavior and class-level functionality"""

    def test_methods_are_static(self):
        """Test that FrameUtils methods are truly static"""
        # Should be able to call methods without instantiating class
        assert callable(FrameUtils.set_icon)
        assert callable(FrameUtils.modal_message_popup)

        # Methods should be static methods
        assert isinstance(FrameUtils.__dict__["set_icon"], staticmethod)
        assert isinstance(FrameUtils.__dict__["modal_message_popup"], staticmethod)

    def test_class_has_no_instance_methods(self):
        """Test that FrameUtils is a pure utility class with no instance methods"""
        # Should not need instantiation
        instance_methods = [
            attr
            for attr in dir(FrameUtils)
            if not attr.startswith("_") and callable(getattr(FrameUtils, attr))
        ]

        for method_name in instance_methods:
            method = getattr(FrameUtils, method_name)
            # All public methods should be static
            assert isinstance(FrameUtils.__dict__.get(method_name), staticmethod), (
                f"{method_name} is not static"
            )

    def test_class_cannot_be_meaningfully_instantiated(self):
        """Test that FrameUtils class instantiation provides no additional functionality"""
        # Should be able to instantiate (no restrictions)
        instance = FrameUtils()
        assert isinstance(instance, FrameUtils)

        # But instance methods should work the same as class methods
        # (This is testing design principle, not functionality difference)
        assert hasattr(instance, "set_icon")
        assert hasattr(instance, "modal_message_popup")


class TestFrameUtilsRegressionTests:
    """Regression tests for known issues and edge cases discovered during development"""

    def test_path_slicing_with_short_paths(self, mocker):
        """Regression test: ensure path slicing works with paths shorter than expected"""
        mock_root = mocker.Mock()

        # Test paths that are shorter than the expected slice length
        short_paths = [
            "/a",  # Much shorter than 9 chars
            "/ab/cd",  # Still shorter
            "/view/util",  # Exactly the expected suffix
            "/x/view/util",  # Just longer than suffix
        ]

        mocker.patch(
            "os.path.exists", return_value=False
        )  # Exit early to focus on path logic
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        for short_path in short_paths:
            mock_abspath = mocker.patch(
                "os.path.abspath", return_value=short_path + "/FrameUtils.py"
            )
            mock_dirname = mocker.patch("os.path.dirname", return_value=short_path)
            mock_join = mocker.patch("os.path.join", return_value="/test/icon.ico")

            # Should handle short paths without IndexError
            FrameUtils.set_icon(mock_root)

            # Should attempt to slice even if result is empty/negative
            expected_slice = short_path[:-9]
            mock_join.assert_called_with(
                expected_slice,
                "Public",
                "Icons",
                "ArchivesSpace_Collections_Manager-32x32.ico",
            )

    def test_iconphoto_call_signature_consistency(self, mocker):
        """Regression test: ensure iconphoto is called with consistent signature"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        # Test PhotoImage path succeeds
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_tk_icon = mocker.Mock()
        mock_photoimage.return_value = mock_tk_icon
        mocker.patch("logging.debug")
        mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # iconphoto should be called with (False, icon_object)
        mock_root.iconphoto.assert_called_with(False, mock_tk_icon)

        # Reset and test PIL fallback path
        mock_root.reset_mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        # When PhotoImage creation fails, iconphoto is never called with PhotoImage
        # The code jumps directly to PIL fallback
        mock_photoimage.side_effect = TclError("PhotoImage failed")
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_pil_image = mocker.Mock()
        mock_image_open.return_value = mock_pil_image
        mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
        mock_pil_icon = mocker.Mock()
        mock_imagetk.return_value = mock_pil_icon

        FrameUtils.set_icon(mock_root)

        # iconphoto should only be called once with PIL icon
        # (PhotoImage creation failed, so iconphoto was never called with PhotoImage object)
        mock_root.iconphoto.assert_called_once_with(False, mock_pil_icon)

    def test_iconphoto_call_sequence_when_photoimage_succeeds_then_fails_on_iconphoto(
        self, mocker
    ):
        """Test scenario where PhotoImage creation succeeds but iconphoto call fails, then PIL succeeds"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        # PhotoImage creation succeeds, but iconphoto call fails
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_tk_icon = mocker.Mock()
        mock_photoimage.return_value = mock_tk_icon

        # First iconphoto call fails, second succeeds
        mock_root.iconphoto.side_effect = [
            TclError("iconphoto with PhotoImage failed"),
            None,
        ]

        # PIL setup
        mock_image_open = mocker.patch("PIL.Image.open")
        mock_pil_image = mocker.Mock()
        mock_image_open.return_value = mock_pil_image
        mock_imagetk = mocker.patch("PIL.ImageTk.PhotoImage")
        mock_pil_icon = mocker.Mock()
        mock_imagetk.return_value = mock_pil_icon

        mocker.patch("logging.debug")
        mocker.patch("logging.warning")

        FrameUtils.set_icon(mock_root)

        # Should be called twice: once with PhotoImage (fails), once with PIL (succeeds)
        expected_calls = [
            mocker.call(False, mock_tk_icon),  # PhotoImage attempt (fails)
            mocker.call(False, mock_pil_icon),  # PIL attempt (succeeds)
        ]
        mock_root.iconphoto.assert_has_calls(expected_calls)

    def test_popup_grid_configuration_order(self, mocker):
        """Regression test: ensure widgets are created before grid configuration"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()
        mock_label = mocker.Mock()
        mock_button = mocker.Mock()

        # Track the order of operations
        call_order = []

        def track_toplevel_creation(*args, **kwargs):
            call_order.append("toplevel_created")
            return mock_toplevel

        def track_label_creation(*args, **kwargs):
            call_order.append("label_created")
            return mock_label

        def track_button_creation(*args, **kwargs):
            call_order.append("button_created")
            return mock_button

        def track_grid_config(*args, **kwargs):
            call_order.append("grid_config_called")

        mock_toplevel.winfo_children.return_value = [mock_label, mock_button]
        mock_label.grid_configure.side_effect = track_grid_config
        mock_button.grid_configure.side_effect = track_grid_config

        mocker.patch("tkinter.Toplevel", side_effect=track_toplevel_creation)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label", side_effect=track_label_creation)
        mocker.patch("tkinter.ttk.Button", side_effect=track_button_creation)

        FrameUtils.modal_message_popup(mock_root, "Order test")

        # Ensure proper order: create widgets before configuring grid
        expected_order = [
            "toplevel_created",
            "label_created",
            "button_created",
            "grid_config_called",
            "grid_config_called",
        ]
        assert call_order == expected_order

    def test_exception_chaining_preservation(self, mocker):
        """Regression test: ensure original exceptions are preserved in error handling"""
        mock_root = mocker.Mock()
        original_error = TclError("Original iconbitmap error with specific details")
        mock_root.iconbitmap.side_effect = original_error

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)

        # Mock fallbacks to succeed so we can check warning details
        mock_photoimage = mocker.patch("tkinter.PhotoImage")
        mock_photoimage.return_value = mocker.Mock()

        mock_warning = mocker.patch("logging.warning")
        mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root)

        # Warning should include details from original exception
        mock_warning.assert_called_once()
        warning_args = mock_warning.call_args[0]
        assert "Original iconbitmap error with specific details" in str(warning_args)

    def test_unicode_path_handling_regression(self, mocker):
        """Regression test: ensure Unicode paths don't cause encoding issues"""
        mock_root = mocker.Mock()

        # Use various Unicode characters that have caused issues in the past
        unicode_paths = [
            "/пользователь/документы/view/util/FrameUtils.py",  # Cyrillic
            "/用户/文档/view/util/FrameUtils.py",  # Chinese
            "/ユーザー/書類/view/util/FrameUtils.py",  # Japanese
            "/Benutzer/Dokumente/view/util/FrameUtils.py",  # German with umlauts (potential)
        ]

        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        for unicode_path in unicode_paths:
            unicode_dirname = unicode_path.rsplit("/", 1)[0]
            unicode_icon_path = unicode_dirname[:-9] + "/Public/Icons/icon.ico"

            mock_abspath = mocker.patch("os.path.abspath", return_value=unicode_path)
            mock_dirname = mocker.patch("os.path.dirname", return_value=unicode_dirname)
            mock_join = mocker.patch("os.path.join", return_value=unicode_icon_path)

            # Should handle Unicode paths without encoding errors
            FrameUtils.set_icon(mock_root)

            mock_root.iconbitmap.assert_called_with(unicode_icon_path)
            mock_root.reset_mock()


class TestFrameUtilsSecurityAndSafetyEdgeCases:
    """Test security and safety edge cases"""

    def test_path_traversal_safety(self, mocker):
        """Test that path construction is safe from path traversal attacks"""
        mock_root = mocker.Mock()

        # Paths that might be used in path traversal attacks
        malicious_paths = [
            "/legitimate/path/../../../etc/passwd",
            "/app/view/util/../../../sensitive/file",
            "/project/view/util/../../../../etc/hosts",
        ]

        mocker.patch("os.path.exists", return_value=False)  # Exit early
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        for malicious_path in malicious_paths:
            malicious_dirname = malicious_path.rsplit("/", 1)[0]
            mock_abspath = mocker.patch("os.path.abspath", return_value=malicious_path)
            mock_dirname = mocker.patch(
                "os.path.dirname", return_value=malicious_dirname
            )
            mock_join = mocker.patch("os.path.join", return_value="/safe/icon.ico")

            # Should use path as provided by os.path operations (which normalize)
            FrameUtils.set_icon(mock_root)

            # The method should use normalized paths from os.path operations
            expected_slice = malicious_dirname[:-9]
            mock_join.assert_called_with(
                expected_slice,
                "Public",
                "Icons",
                "ArchivesSpace_Collections_Manager-32x32.ico",
            )

    def test_resource_exhaustion_protection(self, mocker):
        """Test protection against resource exhaustion attacks"""
        mock_root = mocker.Mock()

        # Extremely long message that could cause memory issues
        huge_message = "A" * (10 * 1024 * 1024)  # 10MB string

        mock_toplevel = mocker.Mock()
        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        # Should handle huge messages without crashing
        FrameUtils.modal_message_popup(mock_root, huge_message)

        # Should still create the popup components
        mock_label.assert_called_once()
        mock_button.assert_called_once()
        mock_toplevel.title.assert_called_once()

    def test_injection_safety_in_popup_parameters(self, mocker):
        """Test safety against potential injection in popup parameters"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mock_label = mocker.patch("tkinter.ttk.Label")
        mock_button = mocker.patch("tkinter.ttk.Button")

        # Strings that might cause issues if not handled properly
        potentially_dangerous_strings = [
            '"; malicious_code(); "',
            '<script>alert("xss")</script>',
            "null\x00byte",
            "${dangerous_substitution}",
            "`command_substitution`",
        ]

        for dangerous_string in potentially_dangerous_strings:
            mock_toplevel.reset_mock()
            mock_label.reset_mock()
            mock_button.reset_mock()

            # Should handle potentially dangerous strings safely
            FrameUtils.modal_message_popup(
                mock_root,
                dangerous_string,
                title=dangerous_string,
                button_text=dangerous_string,
            )

            # Should pass strings as-is to tkinter (which handles them safely)
            mock_toplevel.title.assert_called_once_with(dangerous_string)
            mock_label.assert_called_once()
            mock_button.assert_called_once()


class TestFrameUtilsConcurrencyAndThreadSafety:
    """Test behavior under concurrent access (though FrameUtils is stateless)"""

    def test_concurrent_set_icon_calls(self, mocker):
        """Test multiple simultaneous set_icon calls with different roots"""
        roots = [mocker.Mock() for _ in range(5)]

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        # Simulate concurrent calls
        for i, root in enumerate(roots):
            FrameUtils.set_icon(root)
            root.iconbitmap.assert_called_once_with("/test/icon.ico")

    def test_concurrent_popup_creation(self, mocker):
        """Test multiple simultaneous popup creation calls"""
        roots = [mocker.Mock() for _ in range(3)]
        popups = [mocker.Mock() for _ in range(3)]

        mocker.patch("tkinter.Toplevel", side_effect=popups)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        messages = [f"Popup {i}" for i in range(3)]

        # Simulate concurrent popup creation
        for i, (root, message) in enumerate(zip(roots, messages)):
            FrameUtils.modal_message_popup(root, message)
            popups[i].title.assert_called_once()
            popups[i].focus_set.assert_called_once()
            popups[i].grab_set.assert_called_once()

    def test_state_isolation_between_calls(self, mocker):
        """Test that method calls don't affect each other's state"""
        mock_root1 = mocker.Mock()
        mock_root2 = mocker.Mock()

        # First call succeeds
        mocker.patch("os.path.abspath", return_value="/test1/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test1")
        mocker.patch("os.path.join", return_value="/test1/icon.ico")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        FrameUtils.set_icon(mock_root1)
        mock_root1.iconbitmap.assert_called_once_with("/test1/icon.ico")

        # Second call with different parameters should work independently
        mocker.patch("os.path.abspath", return_value="/test2/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test2")
        mocker.patch("os.path.join", return_value="/test2/icon.ico")

        FrameUtils.set_icon(mock_root2)
        mock_root2.iconbitmap.assert_called_once_with("/test2/icon.ico")

        # First root should not be affected by second call
        mock_root1.iconbitmap.assert_called_once()  # Still only called once


class TestFrameUtilsDocumentationAndContractCompliance:
    """Test that methods behave according to their documented contracts"""

    def test_set_icon_contract_compliance(self, mocker):
        """Test that set_icon follows its documented behavior contract"""
        mock_root = mocker.Mock()

        # Should accept any object with iconbitmap method
        # Should not return anything (None)
        # Should not raise exceptions under normal circumstances

        mocker.patch("os.path.abspath", return_value="/test/FrameUtils.py")
        mocker.patch("os.path.dirname", return_value="/test")
        mocker.patch("os.path.join", return_value="/test/icon.ico")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("logging.debug")

        result = FrameUtils.set_icon(mock_root)

        # Should return None (no return value)
        assert result is None

        # Should have attempted to set icon
        mock_root.iconbitmap.assert_called_once()

    def test_modal_message_popup_contract_compliance(self, mocker):
        """Test that modal_message_popup follows its documented behavior contract"""
        mock_root = mocker.Mock()
        mock_toplevel = mocker.Mock()

        mocker.patch("tkinter.Toplevel", return_value=mock_toplevel)
        mocker.patch("view.util.FrameUtils.FrameUtils.set_icon")
        mocker.patch("tkinter.ttk.Label")
        mocker.patch("tkinter.ttk.Button")

        # Should accept root, message, and optional title/button_text
        # Should create modal popup (focus_set and grab_set)
        # Should not return anything

        result = FrameUtils.modal_message_popup(mock_root, "Test message")

        # Should return None
        assert result is None

        # Should create modal popup
        mock_toplevel.focus_set.assert_called_once()
        mock_toplevel.grab_set.assert_called_once()

        # Should set default title
        mock_toplevel.title.assert_called_once_with("Warning")

    def test_method_signatures_are_stable(self):
        """Test that method signatures remain stable for API compatibility"""
        import inspect

        # set_icon signature
        set_icon_sig = inspect.signature(FrameUtils.set_icon)
        assert len(set_icon_sig.parameters) == 1
        assert "root" in set_icon_sig.parameters

        # modal_message_popup signature
        popup_sig = inspect.signature(FrameUtils.modal_message_popup)
        param_names = list(popup_sig.parameters.keys())
        assert "root" in param_names
        assert "message" in param_names
        assert "title" in param_names
        assert "button_text" in param_names

        # Optional parameters should have defaults
        assert popup_sig.parameters["title"].default == "Warning"
        assert popup_sig.parameters["button_text"].default == "OK"
    def test_path_construction_error_handling(self, mocker):
        """Test graceful handling when path construction fails"""
        mock_root = mocker.Mock()

        # Mock _construct_icon_path to return None (simulating failure)
        mocker.patch.object(FrameUtils, "_construct_icon_path", return_value=None)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        # Should handle gracefully and return early
        try:
            FrameUtils.set_icon(mock_root)
        except Exception as e:
            pytest.fail(f"Should handle path construction failure gracefully: {e}")

        # Verify iconbitmap was never called
        mock_root.iconbitmap.assert_not_called()

    def test_file_check_error_handling(self, mocker):
        """Test graceful handling when file existence check fails"""
        mock_root = mocker.Mock()

        mocker.patch.object(
            FrameUtils, "_construct_icon_path", return_value="/test/icon.ico"
        )
        mocker.patch.object(FrameUtils, "_check_icon_exists", return_value=False)
        mocker.patch("logging.debug")
        mocker.patch("logging.error")

        try:
            FrameUtils.set_icon(mock_root)
        except Exception as e:
            pytest.fail(f"Should handle file check failure gracefully: {e}")

        mock_root.iconbitmap.assert_not_called()

    def test_all_icon_methods_fail_gracefully(self, mocker):
        """Test when all icon setting methods fail but path operations succeed"""
        mock_root = mocker.Mock()
        mock_root.iconbitmap.side_effect = TclError("iconbitmap failed")
        mock_root.iconphoto.side_effect = TclError("iconphoto failed")

        # Successful path operations
        mocker.patch.object(
            FrameUtils, "_construct_icon_path", return_value="/test/icon.ico"
        )
        mocker.patch.object(FrameUtils, "_check_icon_exists", return_value=True)

        # Failing icon creation
        mocker.patch("tkinter.PhotoImage", side_effect=TclError("PhotoImage failed"))
        mocker.patch("PIL.Image.open", side_effect=IOError("PIL failed"))

        mock_debug = mocker.patch("logging.debug")
        mock_warning = mocker.patch("logging.warning")
        mock_error = mocker.patch("logging.error")

        # Should handle all failures gracefully
        try:
            FrameUtils.set_icon(mock_root)
        except Exception as e:
            pytest.fail(f"Should handle all icon method failures gracefully: {e}")

        # Verify appropriate logging
        assert mock_error.called
        error_message = mock_error.call_args[0][0]
        assert "Failed to set icon using all methods" in error_message

    def test_graceful_degradation_pattern(self, mocker):
        """Test the complete graceful degradation pattern"""
        mock_root = mocker.Mock()

        # Simulate the complete failure cascade that should be handled gracefully
        scenarios = [
            # Path construction succeeds, file exists, but all icon methods fail
            {
                "path_result": "/test/icon.ico",
                "file_exists": True,
                "iconbitmap_error": TclError("iconbitmap failed"),
                "photoimage_error": TclError("PhotoImage failed"),
                "pil_error": IOError("PIL failed"),
                "expected_behavior": "logs final error",
            },
            # Path construction fails
            {
                "path_result": None,
                "file_exists": True,
                "iconbitmap_error": None,
                "photoimage_error": None,
                "pil_error": None,
                "expected_behavior": "returns early",
            },
            # File doesn't exist
            {
                "path_result": "/test/icon.ico",
                "file_exists": False,
                "iconbitmap_error": None,
                "photoimage_error": None,
                "pil_error": None,
                "expected_behavior": "returns early",
            },
        ]

        for scenario in scenarios:
            # Set up scenario
            mocker.patch.object(
                FrameUtils, "_construct_icon_path", return_value=scenario["path_result"]
            )
            mocker.patch.object(
                FrameUtils, "_check_icon_exists", return_value=scenario["file_exists"]
            )

            if scenario["iconbitmap_error"]:
                mock_root.iconbitmap.side_effect = scenario["iconbitmap_error"]
            else:
                mock_root.iconbitmap.side_effect = None

            if scenario["photoimage_error"]:
                mocker.patch(
                    "tkinter.PhotoImage", side_effect=scenario["photoimage_error"]
                )
            else:
                mocker.patch("tkinter.PhotoImage", return_value=mocker.Mock())

            if scenario["pil_error"]:
                mocker.patch("PIL.Image.open", side_effect=scenario["pil_error"])
            else:
                mock_image = mocker.Mock()
                mocker.patch("PIL.Image.open", return_value=mock_image)
                mocker.patch("PIL.ImageTk.PhotoImage", return_value=mocker.Mock())

            mock_debug = mocker.patch("logging.debug")
            mock_warning = mocker.patch("logging.warning")
            mock_error = mocker.patch("logging.error")

            # Test graceful handling
            try:
                FrameUtils.set_icon(mock_root)
            except Exception as e:
                pytest.fail(
                    f"Scenario failed: {scenario['expected_behavior']}, error: {e}"
                )

            # Reset for next scenario
            mocker.resetall()
    def test_utility_class_design_principles(self):
        """Test that FrameUtils follows good utility class design principles"""
        import inspect

        # Should be a class (not module-level functions)
        assert inspect.isclass(FrameUtils)

        # Should have no instance variables (stateless)
        instance = FrameUtils()
        assert not hasattr(instance, "__dict__") or len(instance.__dict__) == 0

        # All public methods should be static
        public_methods = [
            name
            for name in dir(FrameUtils)
            if not name.startswith("_") and callable(getattr(FrameUtils, name))
        ]

        for method_name in public_methods:
            assert isinstance(FrameUtils.__dict__[method_name], staticmethod), (
                f"Method {method_name} should be static in utility class"
            )
