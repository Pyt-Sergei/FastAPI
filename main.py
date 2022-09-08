import logging

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


middleware = [    
    # max_age - Session expiry time in seconds. Defaults to 2 weeks.
    # If set to None then the cookie will last as long as the browser session.    
    Middleware(SessionMiddleware, secret_key='Juvenile', max_age=None)
]

app = FastAPI(middleware=middleware)
app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


logger = logging.getLogger()


@app.get('/chat', response_class=HTMLResponse)
async def index(request: Request):    
    return templates.TemplateResponse('index.html', {'request': request})


@app.websocket('/chat')
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    session = websocket.session
    session.setdefault('msg_number', 1)
    try:
        while True:
            data = await websocket.receive_json();
            message = data['message'];              
            msg_number = session['msg_number']      
            session['msg_number'] += 1
            await websocket.send_json({'msg_number': msg_number, 'message': message})                
    except WebSocketDisconnect:        
        logger.info(f'websocket {websocket.client} was disconnected')
