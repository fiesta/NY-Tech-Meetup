import flask
import www
import base64, json, urllib2

api_client_id = "Send an email to Fiesta.cc for a API ID/Secret"
api_client_secret = ""
basic_auth = base64.b64encode("%s:%s" % (api_client_id, api_client_secret))

def _create_and_send_request(uri, api_inputs):
    """See http://docs.fiesta.cc/authentication.html#client-auth
    for more information about authenticating your client"""
    request = urllib2.Request(uri)
    request.add_header("Authorization", "Basic %s" % (basic_auth))
    request.add_header("Content-Type", "application/json")
    request.add_data(json.dumps(api_inputs))

    return urllib2.urlopen(request)

team_to_id = {}
id_to_team = {}
def create_group(team):
    """http://docs.fiesta.cc/list-management-api.html#creating-a-group"""
    create_group_uri = "https://api.fiesta.cc/group"

    #See https://fiesta.cc/custom for more information on using custom domains
    domain = "nytm.fiesta.cc"
    api_inputs = {'domain': domain}

    response = _create_and_send_request(create_group_uri, api_inputs)
    json_response = json.loads(response.read())

    group_id = json_response['data']['group_id']

    team_to_id[team] = group_id
    id_to_team[group_id] = [team, 0, []]

def add_member(member_email, team_name):
    """http://docs.fiesta.cc/list-management-api.html#adding-members"""
    add_member_uri = "https://api.fiesta.cc/membership/%s"

    welcome_message_subject = "%s thanks you for joining Fiesta's IDE Holy Wars" % team_name
    welcome_message_text = "%s needs your help. Respond to this email to do your part in vanquishing your enemies!" % team_name
    welcome_message = {'subject': welcome_message_subject,
                       'text': welcome_message_text}

    api_inputs = {'welcome_message': welcome_message,
                  'group_name': team_name.lower().replace(' ', '_'),
                  'address': member_email}

    _create_and_send_request(add_member_uri % team_to_id[team_name], api_inputs)

def message_middleware(request):
    """http://docs.fiesta.cc/message-middleware-api.html#incoming-messages"""
    email = json.loads(request.data)
    id_to_team[email['group_id']][1] += 1
    id_to_team[email['group_id']][2].append(email['text'])

    #http://docs.fiesta.cc/message-middleware-api.html#responses
    return flask.make_response({}, 202)
