# Happy birthday message only the user can see
USER_BIRTHDAY_MESSAGE = True
# Show a list of users with birthdays today
GLOBAL_BIRTHDAYS = True # TODO: create component for this
# Display user signatures and allow users to set them in profile settings
SIGNATURES_ENABLED = True

# Theme (punkweb)
BOARD_THEME = 'punkweb'

# Shoutbox settings
SHOUTBOX_ENABLED = True
SHOUTBOX_MINIMUM_POSTS = False
SHOUTBOX_MINIMUM_POSTS_REQ = 25
SHOUTBOX_DISABLED_TAGS = [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube', 'code',
]

CAPTCHAS_ENABLED = True

USERNAME_MODIFIERS_ENABLED = True
# TODO: Make disabled tags work
USERNAME_MODIFIERS_DISABLED_TAGS = [
    'img', 'hr', 'ol', 'ul', 'li', 'youtube'
]

# TODO: make this work
PRIVATE_MESSAGING_ENABLED = True

# TODO: make this work
GRAVATAR_SUPPORT_ENABLED = True

# Number of seconds of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 300

# Number of seconds that we will keep track of inactive users for before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7
