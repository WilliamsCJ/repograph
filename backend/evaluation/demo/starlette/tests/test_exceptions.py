import warnings

import pytest

from starlette.exceptions import HTTPException, WebSocketException
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Router, WebSocketRoute


def raise_runtime_error(request):
    raise RuntimeError("Yikes")


def not_acceptable(request):
    raise HTTPException(status_code=406)


def no_content(request):
    raise HTTPException(status_code=204)


def not_modified(request):
    raise HTTPException(status_code=304)


def with_headers(request):
    raise HTTPException(status_code=200, headers={"x-potato": "always"})


class HandledExcAfterResponse:
    async def __call__(self, scope, receive, send):
        response = PlainTextResponse("OK", status_code=200)
        await response(scope, receive, send)
        raise HTTPException(status_code=406)


router = Router(
    routes=[
        Route("/runtime_error", endpoint=raise_runtime_error),
        Route("/not_acceptable", endpoint=not_acceptable),
        Route("/no_content", endpoint=no_content),
        Route("/not_modified", endpoint=not_modified),
        Route("/with_headers", endpoint=with_headers),
        Route("/handled_exc_after_response", endpoint=HandledExcAfterResponse()),
        WebSocketRoute("/runtime_error", endpoint=raise_runtime_error),
    ]
)


app = ExceptionMiddleware(router)


@pytest.fixture
def client(test_client_factory):
    with test_client_factory(app) as client:
        yield client


def test_not_acceptable(client):
    response = client.get("/not_acceptable")
    assert response.status_code == 406
    assert response.text == "Not Acceptable"


def test_no_content(client):
    response = client.get("/no_content")
    assert response.status_code == 204
    assert "content-length" not in response.headers


def test_not_modified(client):
    response = client.get("/not_modified")
    assert response.status_code == 304
    assert response.text == ""


def test_with_headers(client):
    response = client.get("/with_headers")
    assert response.status_code == 200
    assert response.headers["x-potato"] == "always"


def test_websockets_should_raise(client):
    with pytest.raises(RuntimeError):
        with client.websocket_connect("/runtime_error"):
            pass  # pragma: nocover


def test_handled_exc_after_response(test_client_factory, client):
    # A 406 HttpException is raised *after* the response has already been sent.
    # The exception middleware should raise a RuntimeError.
    with pytest.raises(RuntimeError):
        client.get("/handled_exc_after_response")

    # If `raise_server_exceptions=False` then the test client will still allow
    # us to see the response as it will have been seen by the client.
    allow_200_client = test_client_factory(app, raise_server_exceptions=False)
    response = allow_200_client.get("/handled_exc_after_response")
    assert response.status_code == 200
    assert response.text == "OK"


def test_force_500_response(test_client_factory):
    # use a sentinal variable to make sure we actually
    # make it into the endpoint and don't get a 500
    # from an incorrect ASGI app signature or something
    called = False

    async def app(scope, receive, send):
        nonlocal called
        called = True
        raise RuntimeError()

    force_500_client = test_client_factory(app, raise_server_exceptions=False)
    response = force_500_client.get("/")
    assert called
    assert response.status_code == 500
    assert response.text == ""


def test_http_repr():
    assert repr(HTTPException(404)) == (
        "HTTPException(status_code=404, detail='Not Found')"
    )
    assert repr(HTTPException(404, detail="Not Found: foo")) == (
        "HTTPException(status_code=404, detail='Not Found: foo')"
    )

    class CustomHTTPException(HTTPException):
        pass

    assert repr(CustomHTTPException(500, detail="Something custom")) == (
        "CustomHTTPException(status_code=500, detail='Something custom')"
    )


def test_websocket_repr():
    assert repr(WebSocketException(1008, reason="Policy Violation")) == (
        "WebSocketException(code=1008, reason='Policy Violation')"
    )

    class CustomWebSocketException(WebSocketException):
        pass

    assert (
        repr(CustomWebSocketException(1013, reason="Something custom"))
        == "CustomWebSocketException(code=1013, reason='Something custom')"
    )


def test_exception_middleware_deprecation() -> None:
    # this test should be removed once the deprecation shim is removed
    with pytest.warns(DeprecationWarning):
        from starlette.exceptions import ExceptionMiddleware  # noqa: F401

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        import starlette.exceptions

    with pytest.warns(DeprecationWarning):
        starlette.exceptions.ExceptionMiddleware
