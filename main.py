from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,HTMLResponse
from pydantic import EmailStr
from deta import Deta
from typing import Optional
from mailjet_rest import Client



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

deta = Deta()
sub_db = deta.Base('genesen_subscribers')


@app.get('/', response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/about', response_class=HTMLResponse)
def about(request:Request):
    return templates.TemplateResponse('about.html', {'request': request})

@app.get('/contact', response_class=HTMLResponse)
def contact(request:Request):
    return templates.TemplateResponse('contact.html', {'request': request})

@app.get('/complaint', response_class=HTMLResponse)
def contact(request:Request):
    return templates.TemplateResponse('complaint.html', {'request': request})

@app.get('/services', response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse('services.html', {'request': request})

#@app.get('/blacklisted', response_class=HTMLResponse)
#def blacklisted(request:Request):


    import requests
    import json
    from itertools import islice
    import collections

    url = "https://api.cryptoscamdb.org/v1/scams"

    payload={}
    headers = {}

    r = requests.request("GET", url, headers=headers, data=payload)

    parsed = r.json()
    for key, value in islice(parsed.items(), 1, None):
        blu = value[:5]            
    return templates.TemplateResponse('blacklisted.html', {'request': request, 'blu':blu})

@app.post('/subscribe')
def Courses(request:Request, email: Optional[EmailStr] = Form(...)):
    user = ({
            'email':email,
            })
    sub_db.put(user)
    resp = RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    return resp

@app.post('/email')
def Contact_form(request:Request, email: EmailStr = Form(...),  name: str = Form(...),  message: str = Form(...)):
    mailjet = Client(auth=('5e59570aaae2e4a7c5e2a57f24f3253b', '664b1383b87203510e004ce67e971ed1'), version='v3.1')
    data = {
    'Messages': [
            {
                "From": {
                    "Email": "complaint@genesenpilot.org",
                    "Name": "complaint@genesenpilot.org"
                },
                "To": [
                    {
                        "Email": "complaint@genesenpilot.org",
                        "Name":"complaint@genesenpilot.org"
                    }
                ],
                "TemplateID": 3221882,
                "TemplateLanguage": True,
                "Subject": "New submission from contact form",
                "Variables": {
        "name": name,
        "email":email,
        "message": message
    }
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    resp = RedirectResponse(url="/contact",status_code=status.HTTP_302_FOUND)
    return resp

@app.post('/complaint_form')
def Contact_form(request:Request, email: EmailStr = Form(...),  name: str = Form(...),  message: Optional[str] = Form('no message'), phone: str = Form(...), country: str = Form(...), name2: str = Form(...), amount: str = Form(...), payment: str = Form(...), ):
    mailjet = Client(auth=('5e59570aaae2e4a7c5e2a57f24f3253b', '664b1383b87203510e004ce67e971ed1'), version='v3.1')
    data = {
  'Messages': [
		{
			"From": {
				"Email": "complaint@genesenpilot.org",
				"Name": "complaint@genesenpilot.org"
			},
			"To": [
				{
					"Email": "complaint@genesenpilot.org",
					"Name": "complaint@genesenpilot.org"
				}
			],
			"TemplateID": 3221923,
			"TemplateLanguage": True,
			"Subject": "New submission From Complaint Form",
			"Variables": {
            "name": name,
            "email": email,
            "phone": phone,
            "country": country,
            "name2": name2,
            "amount": amount,
            "payment": payment,
            "message": message
        }
                }
            ]
        }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    resp = RedirectResponse(url="/complaint",status_code=status.HTTP_302_FOUND)
    return resp