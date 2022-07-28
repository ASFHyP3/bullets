# Tools Team Bullets

Generates a weekly bullet-point list of all the work done by ASF's Tools Team

![CI/CD All The Things!](docs/images/ci-cd-all-the-things.png)


```shell
$ bullets --help
usage: bullets [-h] [-d DAYS_BACK | -s START_SEARCH] [--detailed]

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS_BACK, --days-back DAYS_BACK
                        Start search at 2:00 PM this many days ago (default: 7)
  -s SEARCH_START, --search-start SEARCH_START
                        Start search at this time (must be parsable by dateutil) (default: None)
  --detailed            Produce a detailed report that includes the Release/PR/Issue body.
                        EXPERIMENTAL! Report formatting is likely not great. (default: False)
```

```shell
$ sendit --help
usage: sendit [-h] markdown_file sender subject to [to ...]

positional arguments:
  markdown_file  Markdown file with the email content
  sender         Send email from this address
  subject        Subject of the email
  to             Send email to these addresses

optional arguments:
  -h, --help     show this help message and exit
```

```shell
$ postit --help
usage: postit [-h] [--channel CHANNEL] markdown_file

positional arguments:
  markdown_file      Markdown file with the post content

optional arguments:
  -h, --help         show this help message and exit
  --channel CHANNEL  The MatterMost channel to post to (default: APD)
```

## Install

Tools Team Bullets is not currently distributed and as such expects users to be
developers on ASF's Tools Team.

To install a development version:
1. clone the repo
   ```shell
   git clone git@github.com:tools-bot/bullets.git
   cd bullets
   ```
2. create a development environment
   ```shell
   conda env create -f environment.yml
   ```
3. install an editable/develop version of `bullets`
   ```shell
    python -m pip install -e ".[develop]"
   ```
4. verify your install
   ```shell
   pytest
   ```

## Usage

### Initial setup

Bullets includes a `bullets` report generator, a `sendit` report emailer, and a
`postit` report MatterMost poster, all of which require some setup to authenticate to
[GitHub](https://github.com/), [Amazon Simple Email Service (SES)](https://aws.amazon.com/ses/)
and [ASF's MatterMost](https://chat.asf.alaska.edu), respectively.

#### Bullets report

`bullets` uses [`ghapi`](https://ghapi.fast.ai/) to interface to GitHub's API.
`ghapi` [requires](https://ghapi.fast.ai/#How-to-use---Python) a 
[GitHub Personal Access Token (PAT)](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
to connect to your github account. 

**For `bullets`, the PAT needs *no* scopes selected** since it's just reading information
about repositories you have access to. For best security, we recommend creating a
least-privileged PAT just for `bullets`.

Once you have your PAT, you need to set a `GITHUB_TOKEN` environment variable with
the PAT as its value:
```
export GITHUB_TOKEN=XXX
```

#### Send emails

To use `sendit`, you will need:
1. [AWS credentials set up for Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)
1. The AWS user/role needs to
   1. have a default region specified
   1. allow `ses:SendEmail`
1. Unless you've taken [Amazon SES out of the sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html),
   all "to" **and** "from" emails need to be verified

#### Post to MatterMost

`postit` uses [Mattermostdriver](https://vaelor.github.io/python-mattermost-driver/)
to post messages to [ASF's MatterMost](https://chat.asf.alaska.edu). You will need a
[A MatterMost Personal Access Token (PAT)](https://mattermost.com/blog/mattermost-integrations-mattermost-api/)
to connect to your MatterMost account.

*Note:* you may need to [open a Platform Ticket](https://asfdaac.atlassian.net/secure/CreateIssueDetails!init.jspa?pid=11808&issuetype=10002&priority=10000)
asking for permission to create a PAT.

Once you have your PAT, you need to set a `MATTERMOST_PAT` environment variable with
the PAT as its value:
```
export MATTERMOST_PAT=XXX
```

### Bullets Report

By default, running bullets with no options

```shell
$ bullets
100%|████████████████████████████████████████████████████████████████████| 17/17
```

will produce a file called `report.md` containing bullet report starting 7 days
previously at 5:00 AM. The report looks like:

```markdown
# Tools Team bullets

Tools team bullets for 2021-01-15T05:00:00-09:00 through 2021-01-22T14:50:26-09:00

## Released

We had 2 releases!
* [HyP3 autoRIFT v0.4.0](https://github.com/ASFHyP3/hyp3-autorift/releases/tag/v0.4.0)
* [HyP3-v0.8.10](https://github.com/ASFHyP3/hyp3/releases/tag/v0.8.10)

## In test

We've moved 1 (unreleased) features to test
* [ASFHyP3/hyp3 #335](https://github.com/ASFHyP3/hyp3/pull/335) fix changelog headers

## In flight

We're still working on 3 features
* [ASFHyP3/hyp3-lib #231](https://github.com/ASFHyP3/hyp3-lib/pull/231) Refactor DEM interface via global VRTs for Copernicus 30m and SRTMGL1 30m
* [ASFHyP3/hyp3-lib #223](https://github.com/ASFHyP3/hyp3-lib/pull/223) Changes needed to allow for use of IFSAR DEM
* [ASFHyP3/ASFHyP3 #11](https://github.com/ASFHyP3/ASFHyP3/pull/11) Convert RTC product guide to markdown

## Issues uncovered

4 outstanding issues were reported
* [ASFHyP3/hyp3-lib #232](https://github.com/ASFHyP3/hyp3-lib/issues/232) area2point.fix_geotiff_locations unexpectedly sets noDataValue=0
* [ASFHyP3/hyp3-autorift #52](https://github.com/ASFHyP3/hyp3-autorift/issues/52) autoRIFT assume 'glaciers' as the research application
* [ASFHyP3/hyp3-autorift #50](https://github.com/ASFHyP3/hyp3-autorift/issues/50) Remove dependence on mat file
* [ASFHyP3/hyp3 #336](https://github.com/ASFHyP3/hyp3/issues/336) autoRIFT Landsat validation too restrictive
```

You can either change the number of days to look back with `--days-back` or
specify a specific start time with the ` --start-search` option (must be parsable
by [dateutil](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse)).

There is also an **experimental** option to add each issues/pr/release body to
the report, which will modify the above bullets like:

```markdown
* [HyP3-v0.8.10](https://github.com/ASFHyP3/hyp3/releases/tag/v0.8.10)
  ### Added
  - AutoRIFT jobs now allow submission with Landsat 8 Collection 2 granules
  
  ### Changed
  - AutoRIFT jobs now only accept Sentinel-2 L1C granules, rather than any Sentinel-2 granules
  
  ### Removed
  - API responses are no longer validated against the OpenAPI schema.  `GET /jobs` requests for jobs
    with legacy parameter values (e.g. S2 L2A granules) will no longer return HTTP 500 errors.
```

but rendering will likely be #NotGreat.

### Send report email

Bullets includes a utility to send the bullets report by email using the
[Amazon Simple Email Service (SES)](https://aws.amazon.com/ses/). You can send a
previously generated report like:

```shell
export EMAIL_SUBJECT=$(sed -n 3p report.md)
sendit report.md sender@alaska.edu "${EMAIL_SUBJECT}" recepient@alaska.edu
```

### Post report to MatterMost

Bullets includes a utility to post messages to [ASF's MatterMost](https://chat.asf.alaska.edu).
You can send a previously generated report like:

```shell
postit report.md --channel APD
```
