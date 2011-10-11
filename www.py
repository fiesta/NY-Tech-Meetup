import flask
import fiesta
import os, urllib

web_server = flask.Flask('IDE Holy Wars')
team_to_id = {}

@web_server.route('/~hook', methods=['POST'])
def message_middleware():
    return fiesta.message_middleware(flask.request)

@web_server.route('/')
def homepage():
    return flask.render_template('homepage.html')

@web_server.route('/join', methods=['POST'])
def join():
    email = flask.request.form['email']
    team = flask.request.form['team']

    fiesta.add_member(email, team)

    return flask.redirect('/hero?%s' % (urllib.urlencode({"team": team})))

@web_server.route('/hero')
def hero():
    team = flask.request.values['team']
    return flask.render_template('hero.html', team=team)

@web_server.route('/vote_view')
def view():
    return flask.render_template('vote_view.html',
                                 info=fiesta.id_to_team.values())

if __name__ == '__main__':
    fiesta.create_group('Team Emacs')
    fiesta.create_group('Team VI')
    port = int(os.environ.get("PORT", 5000))
    web_server.run(debug=True, host='0.0.0.0', port=port)
