from datetime import datetime

from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from dateutil import tz
from ghapi.core import GhApi

from bullets import create

aknow = datetime.now(tz.gettz('AKST'))
# TODO: as CLI option
search_start = aknow - relativedelta(days=21, hour=14, minute=0, second=0, microsecond=0)

gh = GhApi()

meta = {
    'title': 'Tools Team bullets',
    'description': f"Tools team bullets for {search_start.isoformat(timespec='seconds')}"
                   f" through {aknow.isoformat(timespec='seconds')}",
}

release_details = {}
dev_prs = {}
open_prs = {}
opened_issues = {}
for repo in gh.repos.list_for_org('ASFHyP3'):
    last_release = None
    for release in gh.repos.list_releases(repo.owner.login, repo.name):
        created_at = parse_date(release.created_at)
        if last_release is None:
            # FIXME: Hacky way to get last release time
            last_release = created_at
        if created_at >= search_start:
            release_details[release.target_commitish] = {
                'name': release.name,
                'title': '',
                'body': release.body,
                'html_url': release.html_url,
                'created_at': created_at,
            }
        else:
            break

    if last_release is None:
        last_release = search_start
    for pr in gh.pulls.list(repo.owner.login, repo.name,
                            state='closed', base='develop', sort='updated', direction='desc'):
        last_updated = parse_date(pr.updated_at)
        # FIXME: This probably should check if merged, and if the merge commit is *in* head.
        #        This assumes that everything merged into develop before the release was included
        #        in the release
        if last_updated >= last_release and pr.get('merged', False):
            dev_prs[pr.merge_commit_sha] = {
                'name': f'{repo.owner.login}/{repo.name} #{pr.number}',
                'number': pr.number,
                'title': pr.title,
                'body': pr.body,
                'html_url': pr.html_url,
                'last_updated': last_updated,
            }

    for pr in gh.pulls.list(repo.owner.login, repo.name,
                            state='open', sort='created', direction='desc'):
        created_at = parse_date(pr.created_at)
        open_prs[pr.head.sha] = {
            'name': f'{repo.owner.login}/{repo.name} #{pr.number}',
            'title': pr.title,
            'body': pr.body,
            'html_url': pr.html_url,
            'created_at': created_at,
        }

    # FIXME: Returns issues and PRs... simpler to filter this one list or make the three calls?
    for issue in gh.issues.list_for_repo(repo.owner.login, repo.name,
                                         state='open', sort='created', direction='desc',
                                         since=search_start.isoformat(timespec='seconds')):
        if issue.get('pull_request') is None:
            created_at = parse_date(issue.created_at)
            opened_issues[issue.id] = {
                'name': f'{repo.owner.login}/{repo.name} #{issue.number}',
                'title': issue.title,
                'body': issue.body,
                'html_url': issue.html_url,
                'created_at': created_at,
            }

# TODO: report format CLI option (email, md, ...)
# TODO: out file name CLI option
# TODO: detailed CLI option
report = create.render_template(
    'report.md.j2',
    releases=release_details,
    meta=meta,
    dev_prs=dev_prs,
    open_prs=open_prs,
    opened_issues=opened_issues,
)
with open('report.md', 'w') as f:
    f.write(report)

report_detailed = create.render_template(
    'report_detailed.md.j2',
    releases=release_details,
    meta=meta,
    dev_prs=dev_prs,
    open_prs=open_prs,
    opened_issues=opened_issues,
)
with open('report_detailed.md', 'w') as f:
    f.write(report_detailed)
