
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
import string
import re
import openpyxl
from flask import jsonify
from flask import request
from collections import Counter
from flask import redirect, session, make_response
from urllib.parse import urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import datetime
import re
import uuid
import random
import os
import ssl
from data import Statistic


# the dictionary that will be sent to the webpage
data = dict()

categories = [
    "New",
    "Expansion",
    "Churn",
    "Net New"
]

prevValuesByMonth = [
    "Current",
    "1 Month Ago",
    "3 Months Ago",
    "6 Months Ago",
    "1 Year Ago"
]

prevValuesByQuarter = [
    "Current",
    "1 Quarter Ago",
    "2 Quarters Ago",
    "3 Quarters Ago",
    "1 Fiscal Year Ago"
]

# open the excel file
wb = openpyxl.load_workbook("TensorDashboardData.xlsx")

"""THIS LIST CONTROLS THE TILES DISPLAYED ON THE WEBSITE. THE NAMES HERE
SHOULD MATCH THE DICTIONARY KEYS AND RESPECTIVE SHEET NAMES EXACTLY. IN ORDER
TO ADD A NEW METRIC TO THE SITE, ADD THE NAME TO THE STATS LIST AND INITIALIZE
A NEW STATISTIC OBJECT AS DEMONSTRATED BELOW."""
stats = [
    "ARR",
    "ARRDetailed",
    "Seats",
    "Customers",
    "ARRChurnPct",
    "SeatChurnPct",
    "SAOs",
    "SRLs",
    "MQLs",
    "NoOfTrialsRequested",
]


data["ARR"] = Statistic(
    workbook = wb,
    sheetName = "ARR",
    title = "ARR",
    associatedStat = "ARRTotal",
    associatedStatSheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    ),
    prefix = "$",
    suffix = "M",
    timescale = "months",
    dps = 2,
    posColor = "green",
    negColor = "red",
    categories = categories,
    categoryToGraph = None,
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        category = "B",
        value = "C"
    )
).info

data["Customers"] = Statistic(
    workbook = wb,
    sheetName = "Customers",
    title = "Customers",
    associatedStat = "CustomerTotal",
    associatedStatSheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    ),
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = categories,
    categoryToGraph = None,
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        category = "B",
        value = "C"
    )
).info

data["Seats"] = Statistic(
    workbook = wb,
    sheetName = "Seats",
    title = "Seats",
    associatedStat = "SeatsTotal",
    associatedStatSheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    ),
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = categories,
    categoryToGraph = None,
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        category = "B",
        value = "C"
    )
).info

data["ARRChurnPct"] = Statistic(
    workbook = wb,
    sheetName = "ARRChurnPct",
    title = "ARR Churn Rate",
    associatedStat = None,
    prefix = "",
    suffix = "%",
    timescale = "months",
    dps = 1,
    posColor = "red",
    negColor = "green",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = True,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["SeatChurnPct"] = Statistic(
    workbook = wb,
    sheetName = "SeatChurnPct",
    title = "Seat Churn Rate",
    associatedStat = None,
    prefix = "",
    suffix = "%",
    timescale = "months",
    dps = 1,
    posColor = "red",
    negColor = "green",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = True,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["SAOs"] = Statistic(
    workbook = wb,
    sheetName = "SAOs",
    title = "SAOs",
    associatedStat = None,
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["SRLs"] = Statistic(
    workbook = wb,
    sheetName = "SRLs",
    title = "SRLs",
    associatedStat = None,
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["MQLs"] = Statistic(
    workbook = wb,
    sheetName = "MQLs",
    title = "MQLs",
    associatedStat = None,
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["NoOfTrialsRequested"] = Statistic(
    workbook = wb,
    sheetName = "NoOfTrialsRequested",
    title = "Number Of Trials Requested",
    associatedStat = None,
    prefix = "",
    suffix = "",
    timescale = "months",
    dps = 0,
    posColor = "green",
    negColor = "red",
    categories = [],
    prevValueHeaders = prevValuesByMonth,
    isPercentage = False,
    sheetColumns = dict(
        date = "A",
        value = "B",
        category = None
    )
).info

data["ARRDetailed"] = dict(
    title = "ARR (Detailed)",
    timescale = "months",
    prefix = "$",
    suffix = "M",
    dps = 2,
    categories = [],
    prevValuesHeaders = [],
    categoryValues = data["ARR"]["categoryValues"],
    values = dict(
        dates = [],
        values = []
    ),
    graphType = "bar"   
)

# configure application
app = Flask(__name__)

#SAML2 based SSO - SP and IDP code -----------------------------------------------------------------------
app.config['SAML_PATH'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saml')
def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config['SAML_PATH'])
    return auth


def prepare_flask_request(request):
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }
#---------------------------------------------------------------------------------------------------------
@app.route("/", methods=['GET', 'POST'])
def home():
    sid = uuid.uuid1()  # or uuid.uuid4()
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if 'sso' in request.args:
        return redirect(auth.login())
    elif 'sso2' in request.args:
        return_to = '%sattrs/' % request.host_url
        return redirect(auth.login(return_to))
    elif 'slo' in request.args:
        name_id = None
        session_index = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        return redirect(auth.logout(name_id=name_id, session_index=session_index))
    elif 'acs' in request.args:
        auth.process_response()
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if 'RelayState' in request.form and self_url != request.form['RelayState']:
                return redirect(auth.redirect_to(request.form['RelayState']))
    elif 'sls' in request.args:
        dscb = lambda: session.clear()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                success_slo = True
    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    idpresponse = auth.get_last_response_xml()

    xmlstart = '<ns2:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">'
    xmlend = '</ns2:NameID>'
    nameid = re.search('%s(.*)%s' % (xmlstart, xmlend), idpresponse)
    timestart = 'IssueInstant='
    timeend = 'Version="2.0"'
    accesstime = re.search('%s(.*)%s' % (timestart, timeend), idpresponse)

    if nameid is not None:
#        md = mongo.db['sessions']
#        md.insert_one({'user': nameid.group(1), 'ts': datetime.datetime.utcnow(), 'destination': 'landing'})
#        print(nameid.group(1), ' -- ', accesstime.group(1))
#        session['uid'] = nameid.group(1)

        return redirect(url_for('homepage'))

    else:
        return render_template('error.html')

@app.route('/attrs/')
def attrs():
    paint_logout = False
    attributes = False

    if 'samlUserdata' in session:
        paint_logout = True
        if len(session['samlUserdata']) > 0:
            attributes = session['samlUserdata'].items()

    return render_template('attrs.html', paint_logout=paint_logout,
                           attributes=attributes)


@app.route('/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp

@app.route('/homepage')
def homepage():
    return render_template("dashboard.html", stats=stats)

@app.route("/stat/<stat>")
def displayStat(stat):
    return render_template("drilldown.html", title = data[stat]["title"], stat = stat)

@app.route("/data")
def get_data():
    return jsonify(data)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('ssl.pem', 'ssl.key')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=context, threaded=True, debug=True)




