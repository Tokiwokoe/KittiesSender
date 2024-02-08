import random
import dropbox
from bot.misc import EnvironmentVariables


def connect_to_dropbox():
    dbx = dropbox.Dropbox(app_key=EnvironmentVariables.APP_KEY,
                          app_secret=EnvironmentVariables.APP_SECRET,
                          oauth2_refresh_token=EnvironmentVariables.REFRESH_TOKEN)
    return dbx


def show_all_pictures(dbx):
    folder_path = '/KittiesSender'
    files = dbx.files_list_folder(folder_path).entries
    return files


def find_random_picture(files, dbx):
    if files:
        random_image = random.choice(files)
        image_link = dbx.sharing_create_shared_link(random_image.path_display).url
        return image_link
