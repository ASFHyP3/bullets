import logging
from datetime import datetime

from dateutil import tz
from dateutil.parser import parse as parse_date
from fastcore.net import HTTP404NotFoundError
from ghapi.core import GhApi
from tqdm import tqdm

from bullets import util

log = logging.getLogger(__name__)


def generate_bullets(search_start: datetime, detailed: bool = False):
    aknow = datetime.now(tz.gettz('AKST'))
    search_start = util.ensure_tzinfo(search_start)

    meta = {
        'title': 'Tools Team bullets',
        'description': f"Tools team bullets for {search_start.isoformat(timespec='seconds')}"
                       f" through {aknow.isoformat(timespec='seconds')}",
    }
    log.info(f'Generating {meta["description"]}')

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
                print('-'*80)
                print(created_at)
                print(search_start)
                print('-'*80)
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
