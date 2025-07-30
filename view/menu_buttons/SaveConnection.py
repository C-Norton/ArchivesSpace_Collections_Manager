from tkinter import ttk, Toplevel

from controller.connection import Connection
from controller.connection_exceptions import AuthenticationError, NetworkError, ServerError, ConfigurationError
from view.util.FrameUtils import FrameUtils
from model.credential_index_manager import credential_manager


def save_connection(connection: Connection):
    """
    This function checks the connection, and saves it to the system keyring if, and only if it is valid.
    Now uses the credential index manager for proper discovery.

    :param connection: see Connection.py
    :return: None
    """
    frame = Toplevel()
    frame.title("Credential Storage")

    FrameUtils.set_icon(frame)
    ttk.Button(
        frame, width=70, text="Close", command=lambda: ttk.Frame.destroy(frame)
    ).grid(column=1, row=2)
    text = "Your connection has been saved."

    try:
        # Test the connection first
        connection.test_connection()
    except ConfigurationError as e:
        text = f"Unable to store connection: Configuration error.\n{e}"
    except AuthenticationError as e:
        text = f"Unable to store connection: Bad username or password.\n{e}"
    except NetworkError as e:
        text = f"Unable to store connection: Network error.\n{e}"
    except ServerError as e:
        text = f"Unable to store connection: Server error.\n{e}"
    except Exception as e:
        text = f"Unable to store connection: Unexpected error.\n{e}"
    else:
        # Connection is valid, store it using the index manager
        try:
            success = credential_manager.store_credential(
                connection.server,
                connection.username,
                connection.password
            )

            if success:
                text = f"Successfully stored credentials for:\n{connection.username} @ {connection.server}"
            else:
                text = "Failed to store credentials. Check the application logs for details."

        except Exception as e:
            text = f"Unable to store connection: Storage error.\n{e}"

    ttk.Label(frame, text=text, wraplength=220).grid(column=1, row=1)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    frame.focus_set()
    frame.grab_set()