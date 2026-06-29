from fastapi.templating import Jinja2Templates # For HTML responses, not needed for API only


templates = Jinja2Templates(directory="templates") # Template directory for HTML uses
