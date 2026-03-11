from django.http import HttpRequest, HttpResponse


def metrics_view(request: HttpRequest) -> HttpResponse:
    """Expose Prometheus metrics at /metrics/."""
    try:
        from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

        data = generate_latest()
        return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
    except ImportError:
        return HttpResponse(
            "prometheus_client not installed",
            content_type="text/plain",
            status=503,
        )
