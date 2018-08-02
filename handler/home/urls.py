#!/usr/bin/env python
# -*- coding: utf-8 -*-



from .index import IndexHandler
from .login import (RegisterHandler, LoginHandler,
                    LogoutHandler, )


urls_pattern_home = [
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/reg', RegisterHandler),
    ('/logout', LogoutHandler),
    # ('/bye', ByeHandler),
    #('/upload', UploadHandler)
    # ('/settings/profile', ProfileHandler),
    # ('/settings/notifications', NotificationsHandler),
    # ('/settings/password', PasswordHandler),
    # ('/help/about_us', AboutUsHandler),
    # ('/help/contact_us', ContactUsHandler),
    # ('/help/join_us', JoinUsHandler),
    # ('/help/official_news', OfficialNewsHandler)
]