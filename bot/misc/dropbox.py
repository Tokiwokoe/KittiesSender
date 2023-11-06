import random
import dropbox
from bot.misc import EnvironmentVariables


def find_random_picture():
    dbx = dropbox.Dropbox(app_key=EnvironmentVariables.APP_KEY,
                          app_secret=EnvironmentVariables.APP_SECRET,
                          oauth2_refresh_token=EnvironmentVariables.REFRESH_TOKEN)

    folder_path = '/KittiesSender'
    files = dbx.files_list_folder(folder_path).entries
    if files:
        random_image = random.choice(files)
        image_link = dbx.sharing_create_shared_link(random_image.path_display).url
        return image_link
    else:
        return None
