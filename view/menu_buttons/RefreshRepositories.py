from controller.connection import Connection
from view.menu_buttons import TestConnection
from controller.HttpRequestType import HttpRequestType
from view.menu_buttons.MenuButton import MenuButtonWidget, BaseMenuButtonImpl


def refresh_repositories(connection):
    """
    This method is used with an initally valid connection to get a set of repositories to return to the UI
    Notice this is just a method, and not a full class.
    :param connection: connection object (see Connection.py)
    :return:
    TODO: What if a user tries with no saved connection. Add logging and error handling
    """
    if connection.test_connection():
        repositories = Connection.query(
            http_request_type=HttpRequestType.GET, endpoint="repositories"
        )

    else:
        TestConnection.TestConnection(connection)
        return False

class RefreshRepositoriesButtonImpl(BaseMenuButtonImpl):
    """Implementation for Refresh Repositories button"""
    
    def __init__(self, parent, repo_frame):
        super().__init__(parent, "Refresh Repositories")
        self.parent = parent
        self.repo_frame = repo_frame
    
    @property
    def clickable(self) -> bool:
        """Only clickable when repo_frame exists"""
        return self._clickable and hasattr(self, 'repo_frame') and self.repo_frame is not None
    
    def on_click(self) -> None:
        """Refresh the repositories"""
        if self.clickable and hasattr(self.repo_frame, 'refresh'):
            self.repo_frame.refresh()


def create_refresh_repositories_button(parent, repo_frame, **kwargs) -> MenuButtonWidget:
    """Factory function to create Refresh Repositories button"""
    impl = RefreshRepositoriesButtonImpl(parent, repo_frame)
    return MenuButtonWidget(parent, impl, **kwargs)