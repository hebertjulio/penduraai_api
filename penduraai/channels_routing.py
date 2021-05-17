from channels.routing import ProtocolTypeRouter, URLRouter

import bridges.routing


routing = [
    *bridges.routing.urlpatterns
]

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(routing)
})
