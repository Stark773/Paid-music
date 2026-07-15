from Muskan.core.bot import Muskan
from Muskan.core.dir import dirr
from Muskan.core.git import git
from Muskan.core.userbot import Userbot
from Muskan.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Muskan()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
