from microdot import Microdot, send_file

app = Microdot()


@app.route('/')
async def hello(request):
    return send_file("static/index.html")


@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

