from IQ_Paid.core.bot import Istu
from IQ_Paid.core.dir import dirr
from IQ_Paid.core.git import git
from IQ_Paid.core.userbot import Userbot
from IQ_Paid.misc import dbb, heroku
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Istu()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

