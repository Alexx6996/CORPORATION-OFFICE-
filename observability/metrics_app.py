from fastapi import FastAPI, Request, Response

from observability.metrics import render_metrics, track_request

app = FastAPI(title='AIOFFICE Observability Probe (aioffice)')

@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method
    done = track_request(endpoint, method)

    response = await call_next(request)

    done(response.status_code)
    return response

@app.get('/metrics')
async def metrics_endpoint():
    content_type, body = render_metrics()
    return Response(content=body, media_type=content_type)

@app.get('/healthz')
async def healthz():
    return {'status': 'ok', 'service': 'aioffice'}
