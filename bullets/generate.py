from datetime import datetime
from typing import Optional

from dateutil import tz
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from fastcore.net import HTTP404NotFoundError
from ghapi.core import GhApi
from tqdm import tqdm

from bullets import util

_DAYS_BACK = 7
_RD_ARGS = {'hour': 5, 'minute': 0, 'second': 0, 'microsecond': 0}


def generate_bullets(search_start: Optional[datetime] = None, detailed: bool = False):
    aknow = datetime.now(tz.gettz('AKST'))
    if search_start is None:
        search_start = aknow - relativedelta(days=_DAYS_BACK, **_RD_ARGS)

    meta = {
        'title': 'Tools Team bullets',
        'description': f"Tools team bullets for {search_start.isoformat(timespec='seconds')}"
                       f" through {aknow.isoformat(timespec='seconds')}",
    }

    gh = GhApi()
    release_details = {}
    dev_prs = {}
    open_prs = {}
    opened_issues = {}
    for repo in tqdm(gh.repos.list_for_org('ASFHyP3')):
        # FIXME: Returns issues and PRs... simpler to filter this one list or make the three calls?
        for issue in gh.issues.list_for_repo(repo.owner.login, repo.name,
                                             state='open', sort='created', direction='desc',
                                             since=search_start.isoformat(timespec='seconds')):
            if issue.get('pull_request') is None:
                opened_issues[issue.id] = util.get_details(issue)

        try:
            last_release = parse_date(gh.repos.get_latest_release(repo.owner.login, repo.name).created_at)
            for release in gh.repos.list_releases(repo.owner.login, repo.name):
                created_at = parse_date(release.created_at)
                if created_at >= search_start:
                    release_details[release.target_commitish] = util.get_details(release)
                else:
                    break
        except HTTP404NotFoundError:
            last_release = search_start

        # FIXME: might be able to use issues.list_for_repo with since=... to simplify logic
        for pull in gh.pulls.list(repo.owner.login, repo.name,
                                  state='closed', base='develop', sort='updated', direction='desc'):
            merged_at = pull.get('merged_at')
            if merged_at and parse_date(merged_at) > max(search_start, last_release):
                dev_prs[pull.merge_commit_sha] = util.get_details(pull)

        for pull in gh.pulls.list(repo.owner.login, repo.name,
                                  state='open', sort='created', direction='desc'):
            open_prs[pull.head.sha] = util.get_details(pull)

    template = 'report_detailed.md.j2' if detailed else 'report.md.j2'
    report_name = 'report_detailed.md' if detailed else 'report.md'
    report = util.render_template(
        template,
        releases=release_details,
        meta=meta,
        dev_prs=dev_prs,
        open_prs=open_prs,
        opened_issues=opened_issues,
    )
    with open(report_name, 'w') as f:
        f.write(report)
