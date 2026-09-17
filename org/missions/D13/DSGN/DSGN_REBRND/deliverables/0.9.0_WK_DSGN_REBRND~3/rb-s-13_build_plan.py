"""RB-s-13 plan builder (0.9.0_WK_DSGN_REBRND~3). Reads the inventory's render-obligation rows and emits one capture job
per row for rb-s-13_capture.mjs, split into N part files. The denominator is the inventory's own: every row with a
non-empty render_obligation becomes exactly one job, keyed '<route>|<state>' exactly as rb13-coverage-check.py keys it.

Usage (workspace root): python <this> <parts>
Writes: deliverables/0.9.0_WK_DSGN_REBRND~3/rb-s-13_plan.json (all jobs) and .scratch/rb13_plan_part<k>.json
"""
import io
import json
import pathlib
import sys

OWN = pathlib.Path('org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~3')
FX = 'C:/tmp/wk-dsgn-3b/portal/.frontend-dev/testing/'
# The ONLY ui-smoke-shaped ({url-substring: body}) fixtures that exist for inventory routes. Every other file the
# inventory's `fixture` field names is a page description / constitution / markdown matrix, not a fixture body.
UISMOKE_FIXTURE = {
    '/market': FX + 'rb-s-9-market.json',
    '/positioning': FX + 'rb-s-9-attribution.json',
    '/attribution': FX + 'rb-s-9-attribution.json',
}
# toggled-panel: the control each route exposes at load (read from the probe pass, rb-s-13_capture.mjs probe).
TOGGLE = {
    '/market': [{'kind': 'click', 'arg': 'Equities'}],
    '/portfolios': [{'kind': 'click', 'arg': 'Peers'}],
    '/investor-reporting': [{'kind': 'click', 'arg': 'Analysis'}],
    '/philosophy': [{'kind': 'click', 'arg': 'Views'}],
    '/positioning': [{'kind': 'click', 'arg': 'ETFs'}],
    '/attribution': [{'kind': 'click', 'arg': 'YTD'}],
    '/factor-tilts': [{'kind': 'click', 'arg': 'Factor Spreads'}],
    '/valuations': [],  # no control is rendered while the route's data is refused -- recorded, not faked
    '/macro': [{'kind': 'click', 'arg': 'Volatility'}],
    '/advisor-intelligence': [{'kind': 'click', 'arg': 'Distribution'}],
    '/security-scanner': [{'kind': 'click', 'arg': 'Universe Data'}],
    '/portfolio-management': [{'kind': 'click', 'arg': 'Trade'}],
    '/trade-submission': [{'kind': 'click', 'arg': 'History'}],
    '/ticket-center': [{'kind': 'click', 'arg': 'In Progress'}],
    '/data-refresh': [{'kind': 'click', 'arg': 'History'}],
    '/dev/page-surface-control': [{'kind': 'click', 'arg': '3Y'}, {'kind': 'click', 'arg': 'NNA'}],
}
PW = 'rb13-Passw0rd!'
AUTH = {  # the public / auth routes: each state is driven through its own form and its own /auth/* endpoint
    ('/login', 'default'): {'auth': 'none'},
    ('/login', 'loading'): {'auth': 'hold'},
    ('/login', 'error'): {'auth': 'none', 'respond': {'/auth/login': {'status': 401, 'body': {'error': 'Invalid email or password'}}},
                          'steps': [{'kind': 'fill', 'arg': '#email=advisor@example.com'}, {'kind': 'fill', 'arg': '#password=' + PW},
                                    {'kind': 'click', 'arg': 'Sign in'}]},
    ('/login', 'toggled-panel'): {'auth': 'none', 'respond': {'/auth/login': {'status': 200, 'body': {'mfaRequired': True, 'challengeId': 'rb13-challenge', 'channel': 'email', 'ttlSec': 300}}},
                                  'steps': [{'kind': 'fill', 'arg': '#email=advisor@example.com'}, {'kind': 'fill', 'arg': '#password=' + PW},
                                            {'kind': 'click', 'arg': 'Sign in'}]},
    ('/forgot-password', 'default'): {'auth': 'none'},
    ('/forgot-password', 'loading'): {'auth': 'none', 'respond': {'/auth/forgot-password': {'hold': True}},
                                      'steps': [{'kind': 'fill', 'arg': '#email=advisor@example.com'}, {'kind': 'click', 'arg': 'Send reset link', 'wait': 800}]},
    ('/forgot-password', 'error'): {'auth': 'none', 'respond': {'/auth/forgot-password': {'status': 500, 'body': {'error': 'The reset email could not be sent. Try again in a few minutes.'}}},
                                    'steps': [{'kind': 'fill', 'arg': '#email=advisor@example.com'}, {'kind': 'click', 'arg': 'Send reset link'}]},
    ('/reset-password', 'default'): {'auth': 'none', 'route': '/reset-password?token=rb13-token'},
    ('/reset-password', 'loading'): {'auth': 'none', 'route': '/reset-password?token=rb13-token', 'respond': {'/auth/reset-password': {'hold': True}},
                                     'steps': [{'kind': 'fill', 'arg': '#password=' + PW}, {'kind': 'fill', 'arg': '#confirmPassword=' + PW},
                                               {'kind': 'click', 'arg': 'Reset password', 'wait': 800}]},
    ('/reset-password', 'error'): {'auth': 'none', 'route': '/reset-password?token=rb13-token', 'respond': {'/auth/reset-password': {'status': 400, 'body': {'error': 'This reset link has expired. Request a new link.'}}},
                                   'steps': [{'kind': 'fill', 'arg': '#password=' + PW}, {'kind': 'fill', 'arg': '#confirmPassword=' + PW},
                                             {'kind': 'click', 'arg': 'Reset password'}]},
    ('/change-password', 'default'): {},
    ('/change-password', 'loading'): {'respond': {'/auth/change-password': {'hold': True}},
                                      'steps': [{'kind': 'fill', 'arg': '#currentPassword=old-Passw0rd!'}, {'kind': 'fill', 'arg': '#newPassword=' + PW},
                                                {'kind': 'fill', 'arg': '#confirmPassword=' + PW}, {'kind': 'click', 'arg': 'Update password', 'wait': 800}]},
    ('/change-password', 'error'): {'respond': {'/auth/change-password': {'status': 400, 'body': {'error': 'Current password is incorrect.'}}},
                                    'steps': [{'kind': 'fill', 'arg': '#currentPassword=old-Passw0rd!'}, {'kind': 'fill', 'arg': '#newPassword=' + PW},
                                              {'kind': 'fill', 'arg': '#confirmPassword=' + PW}, {'kind': 'click', 'arg': 'Update password'}]},
}
NOPERM = {  # the denying claim for each no-permission row (ProtectedRoute's own gate for that route)
    '/ticket-center': {'firmId': '49financial', 'userType': 'Advisor', 'role': 'user'},  # requireInternal
    '/data-refresh': {'role': 'user'},  # requireAdmin
}


def slug(route, state):
    return 'rb-s-13_%s_%s_1440.png' % (route.strip('/').replace('/', '_') or 'root', state)


def main():
    parts = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    inv = json.load(io.open('design/brand/portal-surface-inventory.json', encoding='utf-8'))
    rows = [r for r in inv['rows'] if r.get('render_obligation')]
    jobs = []
    for r in rows:
        route, state = r['route'], r['state']
        job = {'key': '%s|%s' % (route, state), 'route': route, 'state': state, 'png': slug(route, state),
               'kb': bool(r.get('keyboard_obligation')), 'inventory_fixture': r.get('fixture')}
        if (route, state) in AUTH:
            job['mode'] = 'default'
            job.update(AUTH[(route, state)])
        elif state == 'no-permission':
            job['mode'] = 'default'
            job['claims'] = NOPERM[route]
        else:
            job['mode'] = {'default': 'default', 'toggled-panel': 'default'}.get(state, state)
            if route in UISMOKE_FIXTURE and state in ('default', 'toggled-panel', 'empty'):
                job['fixtures'] = UISMOKE_FIXTURE[route]
            if state == 'toggled-panel':
                job['steps'] = TOGGLE[route]
        jobs.append(job)
    keys = [j['key'] for j in jobs]
    assert len(keys) == len(set(keys)), 'duplicate keys'
    (OWN / 'rb-s-13_plan.json').write_text(json.dumps(jobs, indent=1), encoding='utf-8', newline='\n')
    for k in range(parts):
        pathlib.Path('.scratch/rb13_plan_part%d.json' % (k + 1)).write_text(json.dumps(jobs[k::parts], indent=1), encoding='utf-8', newline='\n')
    print('INVENTORY rows', len(inv['rows']), '| render obligations', len(rows), '| jobs', len(jobs), '| distinct keys', len(set(keys)),
          '| keyboard walks', sum(1 for j in jobs if j['kb']), '| parts', parts)


if __name__ == '__main__':
    main()
