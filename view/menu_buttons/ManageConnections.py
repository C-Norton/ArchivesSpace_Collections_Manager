

import logging
import tkinter
from tkinter import ttk, Toplevel

from controller.connection_manager import ConnectionManager
from view.util.FrameUtils import FrameUtils
from model.credential_index_manager import credential_manager
from view.menu_buttons.MenuButton import MenuButtonWidget, BaseMenuButtonImpl

logger = logging.getLogger(__name__)


class ManageConnections:
    """
    Button implementation for managing saved connections using the credential index.
    """

    def __init__(self, master_frame, connection_manager: ConnectionManager):
        self.master_frame = master_frame
        self.connection_manager = connection_manager
        self.dialog = None

    def on_click(self) -> None:
        """Handle button click - show the manage connections dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.lift()
            self.dialog.focus_force()
        else:
            self._create_dialog()

    def clickable(self) -> bool:
        """Return whether the button should be clickable."""
        return True

    def on_close(self) -> None:
        """Handle dialog close."""
        if self.dialog:
            try:
                self.dialog.destroy()
            except tkinter.TclError:
                pass
            finally:
                self.dialog = None

    def _create_dialog(self):
        """Create and display the manage connections dialog."""
        self.dialog = Toplevel(self.master_frame)
        self.dialog.title("Manage Connections")
        self.dialog.geometry("600x400")
        FrameUtils.set_icon(self.dialog)

        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create main frame
        self.main_frame = ttk.Frame(self.dialog, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        # Load credentials and create UI
        self._create_ui()

        # Center and focus the dialog
        self.dialog.transient(self.master_frame.root)
        self.dialog.grab_set()
        self.dialog.focus_set()

    def _create_ui(self):
        """Create the dialog UI."""
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="Manage Saved Connections",
            font=("TkDefaultFont", 12, "bold"),
        )
        title_label.pack(pady=(0, 15))

        # Get credentials from index
        credentials = credential_manager.get_all_credentials()

        if not credentials:
            self._create_no_credentials_ui()
        else:
            self._create_credentials_list_ui(credentials)

        # Buttons frame
        self._create_buttons(bool(credentials))

    def _create_no_credentials_ui(self):
        """Create UI when no credentials are found."""
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(expand=True, fill="both", padx=20)

        ttk.Label(
            info_frame,
            text="No saved connections found.",
            font=("TkDefaultFont", 10, "bold"),
            justify="center",
        ).pack(pady=(20, 10))

        ttk.Label(
            info_frame,
            text="To save a connection:\n1. Configure a connection\n2. Test the connection\n3. Click 'Save Connection'",
            justify="center",
        ).pack(pady=10)

    def _create_credentials_list_ui(self, credentials):
        """Create UI for displaying the list of credentials."""
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(expand=True, fill="both", padx=20)

        ttk.Label(
            info_frame,
            text=f"Found {len(credentials)} saved connection(s):",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(pady=(10, 5))

        # Create treeview for better display
        tree_frame = ttk.Frame(info_frame)
        tree_frame.pack(pady=10, fill="both", expand=True)

        # Treeview with columns
        columns = ("username", "server")
        self.credentials_tree = ttk.Treeview(
            tree_frame, columns=columns, show="tree headings", height=8
        )

        # Configure columns
        self.credentials_tree.heading("#0", text="Display Name")
        self.credentials_tree.heading("username", text="Username")
        self.credentials_tree.heading("server", text="Server")

        self.credentials_tree.column("#0", width=200)
        self.credentials_tree.column("username", width=100)
        self.credentials_tree.column("server", width=250)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.credentials_tree.yview
        )
        self.credentials_tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.credentials_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate treeview
        for i, cred in enumerate(credentials):
            self.credentials_tree.insert(
                "",
                "end",
                iid=str(i),
                text=cred.display_name,
                values=(cred.username, cred.server),
            )

        # Select first item
        if credentials:
            self.credentials_tree.selection_set("0")

        # Store credentials for reference
        self.current_credentials = credentials

    def _create_buttons(self, has_credentials):
        """Create the button frame."""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=15, side="bottom")

        if has_credentials:
            ttk.Button(
                button_frame,
                text="Load Connection",
                command=self._load_selected_credential,
            ).pack(side="left", padx=5)

            ttk.Button(
                button_frame,
                text="Delete Connection",
                command=self._delete_selected_credential,
            ).pack(side="left", padx=5)

            ttk.Button(
                button_frame,
                text="Test Connection",
                command=self._test_selected_credential,
            ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Refresh", command=self._refresh_credentials
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Cleanup", command=self._cleanup_invalid_credentials
        ).pack(side="left", padx=5)

        ttk.Button(button_frame, text="Close", command=self.on_close).pack(
            side="left", padx=5
        )

    def _get_selected_credential(self):
        """Get the currently selected credential."""
        if not hasattr(self, "credentials_tree") or not hasattr(
            self, "current_credentials"
        ):
            return None

        selection = self.credentials_tree.selection()
        if selection:
            try:
                index = int(selection[0])
                return self.current_credentials[index]
            except (ValueError, IndexError):
                pass
        return None

    def _load_selected_credential(self):
        """Load the selected credential into the connection manager."""
        selected = self._get_selected_credential()
        if not selected:
            FrameUtils.modal_message_popup(
                self.dialog, "No connection selected", "Selection Error"
            )
            return

        try:
            connection = credential_manager.load_credential(selected)
            if connection:
                self.connection_manager.set_connection(
                    connection.server, connection.username, connection.password
                )
                logger.info(f"Loaded connection: {selected.display_name}")
                FrameUtils.modal_message_popup(
                    self.dialog,
                    f"Connection loaded successfully:\n{selected.display_name}",
                    "Connection Loaded",
                )
                self.on_close()
            else:
                FrameUtils.modal_message_popup(
                    self.dialog,
                    f"Failed to load connection: {selected.display_name}",
                    "Load Error",
                )
        except Exception as e:
            logger.error(f"Error loading credential: {e}")
            FrameUtils.modal_message_popup(
                self.dialog, f"Error loading connection: {e}", "Error"
            )

    def _test_selected_credential(self):
        """Test the selected credential."""
        selected = self._get_selected_credential()
        if not selected:
            FrameUtils.modal_message_popup(
                self.dialog, "No connection selected", "Selection Error"
            )
            return

        try:
            connection = credential_manager.load_credential(selected)
            if connection:
                connection.test_connection()
                FrameUtils.modal_message_popup(
                    self.dialog,
                    f"Connection test successful:\n{selected.display_name}",
                    "Test Successful",
                )
            else:
                FrameUtils.modal_message_popup(
                    self.dialog,
                    f"Failed to load connection for testing: {selected.display_name}",
                    "Test Error",
                )
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            FrameUtils.modal_message_popup(
                self.dialog,
                f"Connection test failed:\n{selected.display_name}\n\nError: {e}",
                "Test Failed",
            )

    def _delete_selected_credential(self):
        """Delete the selected credential."""
        selected = self._get_selected_credential()
        if not selected:
            FrameUtils.modal_message_popup(
                self.dialog, "No connection selected", "Selection Error"
            )
            return

        try:
            from tkinter import messagebox

            if messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the saved connection:\n{selected.display_name}?",
            ):
                success = credential_manager.delete_credential(selected)
                if success:
                    FrameUtils.modal_message_popup(
                        self.dialog,
                        "Connection deleted successfully",
                        "Connection Deleted",
                    )
                    self._refresh_credentials()
                else:
                    FrameUtils.modal_message_popup(
                        self.dialog, "Failed to delete connection", "Deletion Error"
                    )
        except Exception as e:
            logger.error(f"Error deleting credential: {e}")
            FrameUtils.modal_message_popup(
                self.dialog, f"Error deleting connection: {e}", "Deletion Error"
            )

    def _refresh_credentials(self):
        """Refresh the credential list."""
        self._create_ui()

    def _cleanup_invalid_credentials(self):
        """Clean up invalid credentials from the index."""
        try:
            removed_count = credential_manager.cleanup_invalid_credentials()
            if removed_count > 0:
                FrameUtils.modal_message_popup(
                    self.dialog,
                    f"Cleaned up {removed_count} invalid credential(s)",
                    "Cleanup Complete",
                )
                self._refresh_credentials()
            else:
                FrameUtils.modal_message_popup(
                    self.dialog, "No invalid credentials found", "Cleanup Complete"
                )
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            FrameUtils.modal_message_popup(
                self.dialog, f"Cleanup failed: {e}", "Cleanup Error"
            )


class ManageConnectionsButtonImpl(BaseMenuButtonImpl):
    """Implementation for Manage Connections button"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent, "Manage Saved Connections")
        self.parent = parent
        self.connection_manager = connection_manager
        self._manage_connections = None
    
    def on_click(self) -> None:
        """Show manage connections dialog"""
        if not self._manage_connections:
            self._manage_connections = ManageConnections(self.parent, self.connection_manager)
        self._manage_connections.on_click()


# Factory function for easier integration
def create_manage_connections_button(
    parent, connection_manager: ConnectionManager, **kwargs
) -> MenuButtonWidget:
    """Factory function to create a Manage Connections button."""
    impl = ManageConnectionsButtonImpl(parent, connection_manager)
    return MenuButtonWidget(parent, impl, **kwargs)
