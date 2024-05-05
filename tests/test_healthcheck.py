from tests.utils.requisition import ClientRequisition


class TestHealthCheck:
    def test_home(self):
        response = ClientRequisition.send("GET", "/")
        assert response.response_status == 200

    def test_health_check(self):
        response = ClientRequisition.send("GET", "/health_check")
        assert response.response_status == 204

    def test_sink(self):
        response = ClientRequisition.send("PUT", "/samplee")
        assert response.response_status == 404
        assert response.response_json["code"] == "UCS000404"

    def test_method_not_allowed(self):
        response = ClientRequisition.send("PUT", "/health_check")
        assert response.response_status == 405
        assert response.response_json["code"] == "UCS000405"

    def test_secure_headers_middleware(self):
        response = ClientRequisition.send("GET", "/health_check")
        headers_response = response.response.headers
        assert response.response_status == 204
        assert headers_response["Server"] == "undisclosed"
        assert headers_response["x-frame-options"] == "SAMEORIGIN"
        assert headers_response["x-xss-protection"] == "1; mode=block"
        assert headers_response["x-content-type-options"] == "nosniff"
        assert headers_response["strict-transport-security"] == "max-age=63072000; includeSubdomains"
        assert headers_response["content-security-policy"] == "default-src 'self'"
