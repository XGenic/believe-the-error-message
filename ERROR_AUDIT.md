# W4 audit: misleading error messages in production systems

**Status, 2026-10-20.** This audit is workstream W4 of [`PAPER_PLAN.md`](PAPER_PLAN.md).

**Purpose.** To show that the two C4 trap patterns, and cause-misstating errors in general, occur in real, widely used systems, and to see *why* they occur. It cannot say how *often* they occur.

**Method.**

- Web searches on 2026-10-20 for documented cases. Every source listed was retrieved in that search.
- **Source types:**
  - **O:** official documentation, or the vendor's own tracker or changelog;
  - **V:** a vendor knowledge base or support page;
  - **C:** community reports (forums, blogs, third-party bug reports).
- Each case is kept only if a source states *both* the message *and* the true cause.

**Not a sample.** Cases were found by targeted search, so their counts say nothing about base rates.

## How each case is coded

- **Stated cause:** what the message or status code implies, on C4's axes:
  - *client-fixable*, such as format or credentials;
  - *transient*, such as temporary, timeout or busy;
  - *permanent*, such as not found, unavailable or damaged.
- **C4 pattern:**
  - **give-up trap:** a permanent-sounding message hides something transient or fixable;
  - **retry trap:** a transient-sounding message hides something permanent or fixable;
  - **wrong target:** the message points to a fix for the wrong thing;
  - **honest:** the message names its uncertainty or the true cause.

## Cases

### Give-up pattern: the message says it doesn't exist, is forbidden or is broken, but it is transient or fixable

| # | System and message | True cause | Mechanism | Source |
|---|---|---|---|---|
| 1 | **GitHub REST API:** `404 Not Found` for a private resource | the request is not properly authenticated, or the token lacks scope (fixable) | security masking: GitHub won't confirm that private repositories exist | O: [GitHub docs, troubleshooting the REST API](https://docs.github.com/rest/using-the-rest-api/troubleshooting-the-rest-api) |
| 2 | **GitLab npm registry:** `404` for a private package | the request is unauthenticated (fixable) | security masking, to hide the package's existence | O: [GitLab issue 334897](https://gitlab.com/gitlab-org/gitlab/-/issues/334897) |
| 3 | **GitHub REST API:** `403 Forbidden` (or 429) on rate limits | the primary rate limit is exhausted; wait until reset (transient) | a status code shared by permission errors and rate limits | O: [GitHub docs, rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) |
| 4 | **Azure RBAC:** `PrincipalNotFound` when assigning a role to a newly created principal | replication delay: the principal exists but hasn't reached the region (transient) | eventual consistency | O: [Microsoft Learn, troubleshoot Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting) |
| 5 | **AWS Lambda:** "The role defined for the function cannot be assumed by Lambda", right after the role is created | IAM propagation delay; a retry succeeds (transient) | eventual consistency | C: [Ayende, AWS roles, Lambda and eventual consistency](https://ayende.com/blog/193665-a/aws-roles-aws-lambda-and-eventual-consistency); O for IAM's eventual consistency in general: [AWS IAM troubleshooting](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot.html) |
| 6 | **Amazon S3:** `NoSuchBucket` right after `CreateBucket` | the new bucket is not yet visible to the server reached (transient; reported to last about a minute) | eventual consistency or routing; no official statement found | C: [Magnolia EXTDAM-82](https://jira.magnolia-cms.com/browse/EXTDAM-82), [Lix commit](https://git.lix.systems/puck/lix/commit/a1355917ecf75e1f1f37101505a351743d590121) |
| 7 | **macOS:** "*App* is damaged and can't be opened" | Gatekeeper is blocking an unsigned or un-notarized app with a quarantine flag; the file is intact (fixable) | security policy reported as corruption | V: [Dynamsoft FAQ](https://dynamsoft.com/web-twain/docs/faq/file-damaged-on-macos.html), [Foundry Q100579](https://support.foundry.com/hc/en-us/articles/360013686379); O: [Apple Developer Forums (DTS)](https://developer.apple.com/forums/thread/799110) |

### Retry pattern: the message says "temporary", "timeout" or "too many requests", but retrying cannot help

| # | System and message | True cause | Mechanism | Source |
|---|---|---|---|---|
| 8 | **OpenAI API:** `429` "You exceeded your current quota" (`insufficient_quota`) | billing: no credits or a monthly cap reached. Fixable by the account owner; retrying won't help. | a rate-limit status code reused for a billing state; the message text is accurate | C: [OpenAI community, 429 insufficient_quota](https://community.openai.com/t/429-error-insufficient-quota/492350) |
| 9 | **MySQL:** "MySQL server has gone away" | the client sent a packet larger than `max_allowed_packet` (fixable client-side) | the server drops the connection; the client reports an outage | O: [MySQL 8.0 manual, "MySQL server has gone away"](https://dev.mysql.com/doc/refman/8.0/en/gone-away.html) |
| 10 | **Kubernetes ingress-nginx:** "503 Service Temporarily Unavailable" | the Service selector matches no Pods, so there are no endpoints (permanent until fixed) | a generic intermediary status: the proxy doesn't know why it has no backend | C: [resolve.ai glossary](https://resolve.ai/glossary/Kubernetes-Service-503-errors), [simplified.guide](https://www.simplified.guide/kubernetes/ingress-troubleshoot) |
| 11 | **AWS Application Load Balancer:** "503 Service Temporarily Unavailable" | the target group has no registered targets (permanent until fixed) | a generic intermediary status | O: [AWS Knowledge Center, ALB 503](https://repost.aws/knowledge-center/alb-troubleshoot-503-errors) |
| 12 | **AWS Lambda:** "Task timed out after N seconds" | a VPC-attached function has no route to the internet, such as a missing NAT gateway (permanent until fixed) | a timeout stands in for unreachable | O: [AWS Lambda, troubleshoot networking](https://docs.amazonaws.cn/en_us/lambda/latest/dg/troubleshooting-networking.html) |
| 13 | **AWS EC2 SSH:** "Connection timed out" | a security group, route table or network ACL blocks the traffic (permanent until fixed) | dropped packets look like slowness | O: [AWS EC2, troubleshoot connecting](https://docs.aws.eu/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html) |
| 14 | **GitLab Releases API:** `500` for an invalid tag name | invalid client input (fixable; a 400 was expected) | missing validation: bad input fails deep in the code | O: [GitLab issue 204718](https://gitlab.com/gitlab-org/gitlab/-/issues/204718) |
| 15 | **OpenStack Neutron API:** `500` for many invalid or missing parameters | invalid client input (fixable) | missing validation | O: [Launchpad bug 1062046](https://blueprints.launchpad.net/bugs/1062046) |
| 16 | **HashiCorp Vault:** `500` for requests failing field validation (since fixed to 400) | invalid client input (fixable) | missing validation | O: [Vault changelog 12042](https://third-party-mirror.googlesource.com/hashicorp/vault/+/refs/heads/main/v1.14.6/changelog/12042.txt) |

Cases 14–16 are coded under "retry" because a 5xx error tells a client that the fault is the server's and may pass, and standard retry policies retry 5xx errors.

### Wrong target: the stated cause points to the wrong fix

| # | System and message | True cause | Mechanism | Source |
|---|---|---|---|---|
| 17 | **Linux / Node.js:** `ENOSPC` "no space left on device" (in Node: "System limit for number of file watchers reached") | the inotify watch limit, not disk space | errno reuse | V: [Coder docs, inotify watch limits](https://coder.com/docs/guides/troubleshooting/inotify-watch-limits) |
| 18 | **Linux:** "No space left on device" while `df` shows free space | inodes exhausted | one errno for two resources | V: [Axway KB 177533](https://support.axway.com/kb/177533/language/en); C: [linuxize](https://linuxize.com/post/fix-no-space-left-on-device/) |
| 19 | **Java:** `OutOfMemoryError: unable to create new native thread` | the per-user process or thread limit (`nproc`), or systemd `TasksMax`, not heap memory | the same OS error code for both causes | O: [OpenJDK JDK-7182040](https://bugs.openjdk.org/browse/JDK-7182040); V: [Atlassian KB](https://support.atlassian.com/jira/kb/jira-data-center-throws-outofmemoryerror-unable-to-create-new-native-thread/) |
| 20 | **Browsers:** a CORS error ("No 'Access-Control-Allow-Origin' header") | the server returned a 500 or 503 without CORS headers; the real fault is server-side | the browser security model hides the real status | C: [dev.to, Misleading CORS errors](https://dev.to/davetrux/misleading-cors-errors-2apl); O: [WebKit bug 231928](https://bugs.webkit.org/show_bug.cgi?id=231928) |
| 21 | **TLS clients:** certificate "not yet valid" or "expired" | the local system clock is wrong, not the server's certificate | a local cause reported as remote | C: [flaviocopes, diagnose TLS validity time](https://flaviocopes.com/courses/tls-certificates/diagnose-validity-time/), [Arch forum](https://bbs.archlinux.org/viewtopic.php?id=266777) |
| 22 | **Python on macOS:** `CERTIFICATE_VERIFY_FAILED` "unable to get local issuer certificate" | the python.org build's local CA bundle is not installed; fix with "Install Certificates.command" | a local cause reported as a server certificate chain problem | V: [Chainstack docs](https://docs.chainstack.com/docs/common-ssl-issues-on-python-and-how-to-fix-it); C: [GitHub Unbabel/COMET 29](https://github.com/Unbabel/COMET/issues/29) |
| 23 | **Windows:** "The specified module could not be found" (error 126) for a DLL that exists | a *dependency* of that DLL is missing, or the architecture is mismatched | the error names the wrong module | V: [Broadcom KB 91733](https://knowledge.broadcom.com/external/article/91733/failed-to-load-dll-file-reason-code-126.html); C: [MBS blog](https://www.mbsplugins.de/archive/2019-08-21/Windows_DLL_Loading_errors) |
| 24 | **Amazon S3:** `403 AccessDenied` for an object that does not exist, when the caller lacks `s3:ListBucket` | the object does not exist (permanent); fixing credentials won't help | security masking: S3 won't reveal which keys exist | O: [AWS re:Post article](https://www.repost.aws/articles/ARe3OTZ3SCTWWqGtiJ6aHn8Q/why-does-s-3-return-403-instead-of-404-when-the-object-doesnt-exist) |
| 25 | **Google Cloud APIs:** `403 PERMISSION_DENIED` for a disabled API | the API is not enabled in the project (fixable). The status code says "permission", but the text says what is wrong (`SERVICE_DISABLED`, with an activation URL). | the status code and the message text disagree | O: [Google Cloud docs, Location Finder troubleshooting](https://docs.cloud.google.com/location-finder/docs/troubleshooting) |

### Honest messages: the text names the uncertainty or the real cause

| # | System and message | Why it matters for C4 | Source |
|---|---|---|---|
| 26 | **Docker:** "pull access denied for X, repository does not exist or may require 'docker login'" | names both possible causes, permanent (does not exist) and fixable (log in). This is the real-world counterpart of the E2 "honest" arm. | C: [Docker forums](https://forums.docker.com/t/error-response-from-daemon-pull-access-denied-repository-does-not-exist-or-may-require-docker-login/75795) |
| 27 | **Bitbucket package registry:** a message saying the package does not exist *or* that permission may be insufficient (paraphrased; the exact wording was not retrieved) | the same two-cause honesty | C: [Atlassian community](https://community.atlassian.com/forums/Bitbucket-questions/How-to-install-private-NPM-package-in-a-different-repository/qaa-p/3244077) |
| 28 | **OpenVPN-based clients:** "certificate is not yet valid or the system clock is incorrect" | names the local cause beside the remote one (compare case 21) | V: [ExpressVPN support](https://www.expressvpn.com/nl/support/troubleshooting/log-items/unable-to-connect-incorrect-system-date-and-time/) |
| 29 | **Google Cloud `SERVICE_DISABLED`:** message text with an activation URL | the text states the true cause precisely, even though the status code (403) does not (case 25) | O: see case 25 |

## What the audit shows

**Both C4 traps exist in the wild:**

- **Give-up pattern:** 7 cases (1–7). A permanent-sounding message ("not found", "forbidden", "damaged", "cannot be assumed") hides something transient or fixable.
- **Retry pattern:** 9 cases (8–16). A transient-sounding message (503, timeout, 429, 500, "server has gone away") hides something permanent or client-fixable.
- **Wrong target:** another 9 cases (17–25), where the stated cause points to the wrong fix.
- **Honest messages:** 4 cases (26–29).

**Misleading causes come from a few systematic mechanisms, not from carelessness:**

| Mechanism | Cases | What it produces |
|---|---|---|
| **Security masking:** deliberately hiding whether something exists | 1, 2, 24 | permanent-sounding or wrong-target messages |
| **Eventual consistency:** "does not exist" that is true only for a while | 4, 5, 6 | the give-up trap, exactly as in C4: the third try would work |
| **Generic intermediary status:** a proxy, load balancer or timeout that cannot know why | 10–13 | the retry trap |
| **Missing input validation:** a client error surfaces as a 5xx | 14–16 | the retry trap |
| **Shared status or errno codes:** one code for different causes | 3, 8, 17–19, 25 | trap or wrong target, depending on the code |
| **Local causes reported as remote** | 20–22 | wrong target |

**For the paper:**

- **Some mechanisms are deliberate and will not go away.** Security masking and eventual consistency guarantee that some stated causes are wrong, so agents need to handle wrong causes rather than wait for better messages.
- **Honest two-cause messages already exist** (cases 26–28). E2's "honest" arm is a realistic design option, not an artificial one.
- **The status code and the text can disagree** (cases 8 and 25). Which one an agent attends to is a measurable question; C4 used text only.

## How the wrong cause is carried

*Added 2026-10-28, after an external review.* The cases differ in where the wrong cause sits, and C4 manipulates only the first kind: a cause stated in words. The coding is the author's judgment.

| Carrier | Cases | Count |
|---|---|---|
| **Stated in text:** the message text itself names a wrong cause | 4, 5, 6, 7, 17, 18, 19, 23 | 8 |
| **Implied by true text:** the text is literally true but points to the wrong cause | 9, 12, 13, 20, 21, 22 | 6 |
| **Status code:** a status code and its standard phrase carry the wrong cause; any text is generic, or even accurate | 1, 2, 3, 8, 10, 11, 14, 15, 16, 24, 25 | 11 |

## Limits

- **Targeted search, not a sample.** The audit shows that these patterns exist, not how often they occur. A frequency estimate would need a corpus of real tool-call logs.
- **Several cases rest on community sources (C).** The strongest cases have official documentation: 1, 3, 4, 9, 11, 12, 13, 19 and 24. Cases 6 (S3 after creation) and 8 (OpenAI 429) rely on community reports only.
- **The C4 categories are coarse.** Some cases fit more than one; each was coded under the pattern an agent acting on the message would most likely follow.
- **Sources were retrieved on 2026-10-20.** Vendor behavior can change; Vault, for example, has fixed case 16.
