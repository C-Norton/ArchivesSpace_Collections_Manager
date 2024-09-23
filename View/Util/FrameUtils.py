import os
import tkinter
import logging
from tkinter import ttk

from PIL import Image, ImageTk


class FrameUtils:
    @staticmethod
    def set_icon(root):
        logging.debug("Entering set_icon method")
        project_root = os.path.dirname(os.path.abspath(__file__))[:-9]
        icon_path = os.path.join(
            project_root,
            "Public",
            "Icons",
            "ArchivesSpace_Collections_Manager-32x32.ico",
        )
        logging.debug(f"Constructed icon path: {icon_path}")

        if not os.path.exists(icon_path):
            logging.error(f"Icon file not found: {icon_path}")
            return

        logging.debug(f"Root object type: {type(root)}")

        try:
            # Try using iconbitmap first
            root.iconbitmap(icon_path)
            logging.debug("Icon set successfully using iconbitmap")
        except Exception as e:
            logging.warning(f"Failed to set icon using iconbitmap: {e}")

            try:
                # If iconbitmap fails, try using PhotoImage
                icon = tkinter.PhotoImage(file=icon_path)
                root.iconphoto(False, icon)
                logging.debug("Icon set successfully using PhotoImage")
            except Exception as e:
                logging.warning(f"Failed to set icon using PhotoImage: {e}")

                try:
                    # If both methods fail, try using PIL
                    icon = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(icon)
                    root.iconphoto(False, photo)
                    logging.debug("Icon set successfully using PIL")
                except Exception as e:
                    logging.error(f"Failed to set icon using all methods: {e}")

        logging.debug("Exiting set_icon method")

    @staticmethod
    def modal_message_popup(root, message, title="Warning", button_text="OK"):
        popup = tkinter.Toplevel(root)
        FrameUtils.set_icon(popup)
        popup.title(title)
        ttk.Label(popup, text=message).grid(row=0, column=0)
        ttk.Button(popup, text=button_text, command=popup.destroy).grid(row=1, column=0)
        popup.focus_set()
        popup.grab_set()
