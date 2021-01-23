# Tools Team Bullets

Generates a weekly bullet-point list of all the work done by ASF's Tools Team

![CI/CD All The Things!](docs/images/ci-cd-all-the-things.png)


```shell
$ python -m bullets --help
usage: bullets [-h] [-d DAYS_BACK | -s START_SEARCH] [--detailed]

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS_BACK, --days-back DAYS_BACK
                        Start search at 2:00 PM this many days ago (default: 7)
  -s START_SEARCH, --start-search START_SEARCH
                        Start search at this time (must be parsable by dateutil) (default: None)
  --detailed            Produce a detailed report that includes the Release/PR/Issue body.
                        EXPERIMENTAL! Report formatting is likely not great. (default: False)
```

## Install

Tools Team Bullets is not currently distributed and as such expects users to be
developers on the Tools Team.

To install a development version:
1. clone the repo
   ```shell
   git clone git@github.com:tools-bot/bullets.git
   cd bullets
   ```
2. create a development environment
   ```shell
   conda env create -f conda-env.yml
   ```
3. install an editable/develop version of `bullets`
   ```shell
    python -m pip install -e ".[develop]"
   ```

## Usage

By default, running bullets with no options

```shell
$ bullets
100%|████████████████████████████████████████████████████████████████████| 17/17
```

will produce a file called `report.md` containing bullet report starting days
previously at 2:00 PM 7. The report looks like:

```md
# Tools Team bullets

Tools team bullets for 2021-01-15T14:00:00-09:00 through 2021-01-22T14:50:26-09:00

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

```md
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