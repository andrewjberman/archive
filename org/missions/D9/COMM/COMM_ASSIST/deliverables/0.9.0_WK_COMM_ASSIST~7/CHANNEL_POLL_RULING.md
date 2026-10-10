# CHANNEL_POLL_RULING -- COMM_ASSIST.TO-CA-e-3 (worker 0.9.0_WK_COMM_ASSIST~7)

## Live counts (read-only logs filter-log-events, us-east-1, last hour, filter-pattern channel_poll)
- Log group /aws/lambda/teams-global-chat-assist-ingress-lambda, window = the 3600 s before the read on 2026-10-10.
- 59 channel_poll lines; 59 of 59 carry "failed": 1 (0 of 59 carry failed 0). Every line also reads calls=1, channels=0, read=0, mentions=0.
- The window held at most 200 lines (--max-items 200); 59 < 200, so the read was not cut short.

## The failing call, and how sure
- calls=1 and channels=0 on every line: the poll spent ONE gateway call and failed on it. The first call a poll makes with an empty
  team list is `gw.teams()` (GET /teams, route label `teams`). So the failing call is most plausibly `teams`. Confidence: moderate
  (inferred from calls=1, not read from an error). It could also be the single `channel_messages` or `channels` call only if the
  team list were already cached; channels=0 says the list is empty, so `teams` is the one.
- The deployed code logs no error text. After the next deploy of this change the `channel_poll` line carries
  `error` = "route=<label> status=<http status> error=<code>" (at most 200 characters, never message content) and the step
  raises, so `ingress_step_failed` with step `channels` appears every minute. That line will name the call and the status.
- Gateway source (infra/aws/ec2/opal-gateway/app/teams_route.py, server.py lines 1118-1121): the routes TEAMS_ROUTE, CHANNELS_ROUTE
  and CHANNEL_MESSAGES_ROUTE exist in the repo source under the /hx/teams prefix. Not established: whether the DEPLOYED gateway
  serves them, whether the load balancer routes /hx/teams/teams to the gateway (a non-routed path answers a 302 that assist.py
  treats as an error), and whether the delegated Graph token holds the Team/Channel read scopes.

## Whose fix
- The code fix in this cell (name the error, raise) is inside COMM's own code. The cure of the failure itself is UNKNOWN until the
  `error` field is read after deploy; if it is a 404/302 (route or listener) or a 401/403 (token scope) it depends on the gateway,
  which is another project, and COMM can only report it.

## Dependent outcome
- FWD-3's "every Teams message reaches his phone", for channel @mentions of Andrew: while this step fails, 0 channel mentions are
  read and none reaches his phone, and nothing said so. After deploy the failure is loud every minute.
