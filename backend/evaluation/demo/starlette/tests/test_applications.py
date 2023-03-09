import os
from contextlib import asynccontextmanager

import anyio
import pytest

from starlette import status
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException, WebSocketException
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Host, Mount, Route, Router, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket


async def error_500(request, exc):
    return JSONResponse({"detail": "Server Error"}, status_code=500)


async def method_not_allowed(request, exc):
    return JSONResponse({"detail": "Custom message"}, status_code=405)


async def http_exception(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


def func_homepage(request):
    return PlainTextResponse("Hello, world!")


async def async_homepage(request):
    return PlainTextResponse("Hello, world!")


class Homepage(HTTPEndpoint):
    def get(self, request):
        return PlainTextResponse("Hello, world!")


def all_users_page(request):
    return PlainTextResponse("Hello, everyone!")


def user_page(request):
    username = request.path_params["username"]
    return PlainTextResponse(f"Hello, {username}!")


def custom_subdomain(request):
    return PlainTextResponse("Subdomain: " + request.path_params["subdomain"])


def runtime_error(request):
    raise RuntimeError()


async def websocket_endpoint(session):
    await session.accept()
    await session.send_text("Hello, world!")
    await session.close()


async def websocket_raise_websocket(websocket: WebSocket):
    await websocket.accept()
    raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)


class CustomWSException(Exception):
    pass


async def websocket_raise_custom(websocket: WebSocket):
    await websocket.accept()
    raise CustomWSException()


def custom_ws_exception_handler(websocket: WebSocket, exc: CustomWSException):
    anyio.from_thread.run(websocket.close, status.WS_1013_TRY_AGAIN_LATER)


users = Router(
    routes=[
        Route("/", endpoint=all_users_page),
        Route("/{username}", endpoint=user_page),
    ]
)

subdomain = Router(
    routes=[
        Route("/", custom_subdomain),
    ]
)

exception_handlers = {
    500: error_500,
    405: method_not_allowed,
    HTTPException: http_exception,
    CustomWSException: custom_ws_exception_handler,
}

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=["testserver", "*.example.org"])
]

app = Starlette(
    routes=[
        Route("/func", endpoint=func_homepage),
        Route("/async", endpoint=async_homepage),
        Route("/class", endpoint=Homepage),
        Route("/500", endpoint=runtime_error),
        WebSocketRoute("/ws", endpoint=websocket_endpoint),
        WebSocketRoute("/ws-raise-websocket", endpoint=websocket_raise_websocket),
        WebSocketRoute("/ws-raise-custom", endpoint=websocket_raise_custom),
        Mount("/users", app=users),
        Host("{subdomain}.example.org", app=subdomain),
    ],
    exception_handlers=exception_handlers,
    middleware=middleware,
)


@pytest.fixture
def client(test_client_factory):
    with test_client_factory(app) as client:
        yield client


def test_url_path_for():
    assert app.url_path_for("func_homepage") == "/func"


def test_func_route(client):
    response = client.get("/func")
    assert response.status_code == 200
    assert response.text == "Hello, world!"

    response = client.head("/func")
    assert response.status_code == 200
    assert response.text == ""


def test_async_route(client):
    response = client.get("/async")
    assert response.status_code == 200
    assert response.text == "Hello, world!"


def test_class_route(client):
    response = client.get("/class")
    assert response.status_code == 200
    assert response.text == "Hello, world!"


def test_mounted_route(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.text == "Hello, everyone!"


def test_mounted_route_path_params(client):
    response = client.get("/users/tomchristie")
    assert response.status_code == 200
    assert response.text == "Hello, tomchristie!"


def test_subdomain_route(test_client_factory):
    client = test_client_factory(app, base_url="https://foo.example.org/")

    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Subdomain: foo"


def test_websocket_route(client):
    with client.websocket_connect("/ws") as session:
        text = session.receive_text()
        assert text == "Hello, world!"


def test_400(client):
    response = client.get("/404")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_405(client):
    response = client.post("/func")
    assert response.status_code == 405
    assert response.json() == {"detail": "Custom message"}

    response = client.post("/class")
    assert response.status_code == 405
    assert response.json() == {"detail": "Custom message"}


def test_500(test_client_factory):
    client = test_client_factory(app, raise_server_exceptions=False)
    response = client.get("/500")
    assert response.status_code == 500
    assert response.json() == {"detail": "Server Error"}


def test_websocket_raise_websocket_exception(client):
    with client.websocket_connect("/ws-raise-websocket") as session:
        response = session.receive()
        assert response == {
            "type": "websocket.close",
            "code": status.WS_1003_UNSUPPORTED_DATA,
            "reason": "",
        }


def test_websocket_raise_custom_exception(client):
    with client.websocket_connect("/ws-raise-custom") as session:
        response = session.receive()
        assert response == {
            "type": "websocket.close",
            "code": status.WS_1013_TRY_AGAIN_LATER,
            "reason": "",
        }


def test_middleware(test_client_factory):
    client = test_client_factory(app, base_url="http://incorrecthost")
    response = client.get("/func")
    assert response.status_code == 400
    assert response.text == "Invalid host header"


def test_routes():
    assert app.routes == [
        Route("/func", endpoint=func_homepage, methods=["GET"]),
        Route("/async", endpoint=async_homepage, methods=["GET"]),
        Route("/class", endpoint=Homepage),
        Route("/500", endpoint=runtime_error, methods=["GET"]),
        WebSocketRoute("/ws", endpoint=websocket_endpoint),
        WebSocketRoute("/ws-raise-websocket", endpoint=websocket_raise_websocket),
        WebSocketRoute("/ws-raise-custom", endpoint=websocket_raise_custom),
        Mount(
            "/users",
            app=Router(
                routes=[
                    Route("/", endpoint=all_users_page),
                    Route("/{username}", endpoint=user_page),
                ]
            ),
        ),
        Host(
            "{subdomain}.example.org",
            app=Router(routes=[Route("/", endpoint=custom_subdomain)]),
        ),
    ]


def test_app_mount(tmpdir, test_client_factory):
    path = os.path.join(tmpdir, "example.txt")
    with open(path, "w") as file:
        file.write("<file content>")

    app = Starlette(
        routes=[
            Mount("/static", StaticFiles(directory=tmpdir)),
        ]
    )

    client = test_client_factory(app)

    response = client.get("/static/example.txt")
    assert response.status_code == 200
    assert response.text == "<file content>"

    response = client.post("/static/example.txt")
    assert response.status_code == 405
    assert response.text == "Method Not Allowed"


def test_app_debug(test_client_factory):
    async def homepage(request):
        raise RuntimeError()

    app = Starlette(
        routes=[
            Route("/", homepage),
        ],
    )
    app.debug = True

    client = test_client_factory(app, raise_server_exceptions=False)
    response = client.get("/")
    assert response.status_code == 500
    assert "RuntimeError" in response.text
    assert app.debug


def test_app_add_route(test_client_factory):
    async def homepage(request):
        return PlainTextResponse("Hello, World!")

    app = Starlette(
        routes=[
            Route("/", endpoint=homepage),
        ]
    )

    client = test_client_factory(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, World!"


def test_app_add_websocket_route(test_client_factory):
    async def websocket_endpoint(session):
        await session.accept()
        await session.send_text("Hello, world!")
        await session.close()

    app = Starlette(
        routes=[
            WebSocketRoute("/ws", endpoint=websocket_endpoint),
        ]
    )
    client = test_client_factory(app)

    with client.websocket_connect("/ws") as session:
        text = session.receive_text()
        assert text == "Hello, world!"


def test_app_add_event_handler(test_client_factory):
    startup_complete = False
    cleanup_complete = False

    def run_startup():
        nonlocal startup_complete
        startup_complete = True

    def run_cleanup():
        nonlocal cleanup_complete
        cleanup_complete = True

    app = Starlette(
        on_startup=[run_startup],
        on_shutdown=[run_cleanup],
    )

    assert not startup_complete
    assert not cleanup_complete
    with test_client_factory(app):
        assert startup_complete
        assert not cleanup_complete
    assert startup_complete
    assert cleanup_complete


def test_app_async_cm_lifespan(test_client_factory):
    startup_complete = False
    cleanup_complete = False

    @asynccontextmanager
    async def lifespan(app):
        nonlocal startup_complete, cleanup_complete
        startup_complete = True
        yield
        cleanup_complete = True

    app = Starlette(lifespan=lifespan)

    assert not startup_complete
    assert not cleanup_complete
    with test_client_factory(app):
        assert startup_complete
        assert not cleanup_complete
    assert startup_complete
    assert cleanup_complete


deprecated_lifespan = pytest.mark.filterwarnings(
    r"ignore"
    r":(async )?generator function lifespans are deprecated, use an "
    r"@contextlib\.asynccontextmanager function instead"
    r":DeprecationWarning"
    r":starlette.routing"
)


@deprecated_lifespan
def test_app_async_gen_lifespan(test_client_factory):
    startup_complete = False
    cleanup_complete = False

    async def lifespan(app):
        nonlocal startup_complete, cleanup_complete
        startup_complete = True
        yield
        cleanup_complete = True

    app = Starlette(lifespan=lifespan)

    assert not startup_complete
    assert not cleanup_complete
    with test_client_factory(app):
        assert startup_complete
        assert not cleanup_complete
    assert startup_complete
    assert cleanup_complete


@deprecated_lifespan
def test_app_sync_gen_lifespan(test_client_factory):
    startup_complete = False
    cleanup_complete = False

    def lifespan(app):
        nonlocal startup_complete, cleanup_complete
        startup_complete = True
        yield
        cleanup_complete = True

    app = Starlette(lifespan=lifespan)

    assert not startup_complete
    assert not cleanup_complete
    with test_client_factory(app):
        assert startup_complete
        assert not cleanup_complete
    assert startup_complete
    assert cleanup_complete


def test_decorator_deprecations() -> None:
    app = Starlette()

    with pytest.deprecated_call(
        match=(
            "The `exception_handler` decorator is deprecated, "
            "and will be removed in version 1.0.0."
        )
    ) as record:
        app.exception_handler(500)(http_exception)
        assert len(record) == 1

    with pytest.deprecated_call(
        match=(
            "The `middleware` decorator is deprecated, "
            "and will be removed in version 1.0.0."
        )
    ) as record:

        async def middleware(request, call_next):
            ...  # pragma: no cover

        app.middleware("http")(middleware)
        assert len(record) == 1

    with pytest.deprecated_call(
        match=(
            "The `route` decorator is deprecated, "
            "and will be removed in version 1.0.0."
        )
    ) as record:
        app.route("/")(async_homepage)
        assert len(record) == 1

    with pytest.deprecated_call(
        match=(
            "The `websocket_route` decorator is deprecated, "
            "and will be removed in version 1.0.0."
        )
    ) as record:
        app.websocket_route("/ws")(websocket_endpoint)
        assert len(record) == 1

    with pytest.deprecated_call(
        match=(
            "The `on_event` decorator is deprecated, "
            "and will be removed in version 1.0.0."
        )
    ) as record:

        async def startup():
            ...  # pragma: no cover

        app.on_event("startup")(startup)
        assert len(record) == 1
