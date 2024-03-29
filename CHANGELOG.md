# Changelog

<!--next-version-placeholder-->

## v2.1.0 (2021-04-14)
### Feature
* MVP for database upload ([`44ae871`](https://github.com/alekseik1/moodle-breaker/commit/44ae871b9ee70966ac03b289dcff2297cc950c85))
* **alembic:** Add column of HTML document type ([`800af5b`](https://github.com/alekseik1/moodle-breaker/commit/800af5b4c6d7fa12d4a73d34abe66d1c4eb9a0fb))
* **page-upload:** Safe method to upload page ([`96e387e`](https://github.com/alekseik1/moodle-breaker/commit/96e387e8cd6ede7c2e4ab6f3bbd9c70b5939f420))
* **logging:** Log errors in `safe_session` ([`5732b42`](https://github.com/alekseik1/moodle-breaker/commit/5732b421d0509edfe0482fa783f18bd76ac528a7))
* **sqlalchemy:** Add raw HTML table ([`97043e8`](https://github.com/alekseik1/moodle-breaker/commit/97043e8bc8300623c79c3f1ad71729373cba0dd8))

## v2.0.3 (2021-04-08)
### Fix
* **pageparser:** Failure in page parsing for summaries without score (mark-only) ([`8547045`](https://github.com/alekseik1/moodle-breaker/commit/85470456a1f63b93f234cf107195a3dc74d18089))

## v2.0.2 (2021-04-04)
### Fix
* **vk:** Broken `login declined` message ([`2f9369c`](https://github.com/alekseik1/moodle-breaker/commit/2f9369c7c89ed2136abc69289eb88dfe78f49643))

## v2.0.1 (2021-04-04)
### Fix
* **sqlalchemy:** Replace heroku url ([`14f625e`](https://github.com/alekseik1/moodle-breaker/commit/14f625ec72744a8d669439540cb05c2130a009bc))

## v2.0.0 (2021-04-04)
### Breaking
* need to bump new version since it wasn't done previously  ([`524cb21`](https://github.com/alekseik1/moodle-breaker/commit/524cb21a8e32fec3429a629d3e4e6981c7e01835))

## v1.5.0 (2021-04-04)
### Feature
* **crash:** Add simple crash dump email ([`b5f7c13`](https://github.com/alekseik1/moodle-breaker/commit/b5f7c132ac93dd6bf362afc26c2180bed1b6ac80))
* **logging:** Use Loguru for logging ([`882aa07`](https://github.com/alekseik1/moodle-breaker/commit/882aa077595070c78486fbe6c31282d988aa3bcc))
* **TaskSummaryPage:** Introduce summary page parser ([`2ad137f`](https://github.com/alekseik1/moodle-breaker/commit/2ad137fc7cfdeb9723743fd917c52df23484f294))
* **all-tasks-parser:** Initial support for parsing all tasks ([`4f5e313`](https://github.com/alekseik1/moodle-breaker/commit/4f5e313c54de2ca4e36e9d343bcd050da4e5d5a4))

### Fix
* **PageParser:** Incorrect type for `page_content` ([`072f4da`](https://github.com/alekseik1/moodle-breaker/commit/072f4daa63ed0393fe8f1dfeb141f7514b263c93))
* **None:** Support for None values in parsers ([`8dda000`](https://github.com/alekseik1/moodle-breaker/commit/8dda00090df35e22d76cef3ed1b0b58f6183c41f))

### Documentation
* Some docs ([`d6da6b4`](https://github.com/alekseik1/moodle-breaker/commit/d6da6b445440b771ecd7bc2e66f8a4e76b2b1a43))

## v1.4.0 (2021-04-02)
### Feature
* **moodle-api:** Parser for all courses page ([`f5c35c9`](https://github.com/alekseik1/moodle-breaker/commit/f5c35c9a4928b367ae6f43a9f59b110f20ce8343))
* **moodle-api:** Getter for page with all courses ([`8835eca`](https://github.com/alekseik1/moodle-breaker/commit/8835ecabdf5e007c35d338da07c8cc3252a1b7d6))

### Fix
* **radio-parser:** Fix new crashing tasks ([`6e12072`](https://github.com/alekseik1/moodle-breaker/commit/6e12072291d20aa5ce9ca1602f972842a9060ba7))

## v1.3.0 (2021-03-08)
### Feature
* Delete user command ([`2af2ce2`](https://github.com/alekseik1/moodle-breaker/commit/2af2ce2cd6937d83ea57dcdb48b52fadb84811ed))

## v1.2.2 (2021-02-25)
### Fix
* **moodle-api:** Reload summary page after an empty attempt ([`9a5e390`](https://github.com/alekseik1/moodle-breaker/commit/9a5e390f390c614312aeb2129cd08aba878335eb))

## v1.2.1 (2021-02-25)
### Fix
* **moodle-api:** Wait 2 seconds before starting anew ([`a06b5af`](https://github.com/alekseik1/moodle-breaker/commit/a06b5afe6b719ee8b806bc1285eac57e8a3b98d3))

## v1.2.0 (2021-02-12)
### Feature
* **messages:** Inform about multiple attempts ([`031c860`](https://github.com/alekseik1/moodle-breaker/commit/031c8604fa0284e5bb3eb9e0b06b9b87404d3b20))

### Fix
* **vk:** Send message on moodle auth error ([`50b69f3`](https://github.com/alekseik1/moodle-breaker/commit/50b69f3ad8a716cba1f9a317900184a51f3279d1))

## v1.1.7 (2021-02-12)
### Fix
* Deploy only after tests and on master ([`198c83f`](https://github.com/alekseik1/moodle-breaker/commit/198c83f814593276594ba904c2a1adb2654ccf87))

## v1.1.6 (2021-02-12)
### Fix
* Remove deploy stage ([`998de6c`](https://github.com/alekseik1/moodle-breaker/commit/998de6cb11677604fef38b9e0519048be04357fe))

## v1.1.5 (2021-02-12)
### Fix
* Better ci config ([`01f64a6`](https://github.com/alekseik1/moodle-breaker/commit/01f64a6bcc18d6c08474a4b22307eb204cf8eabd))

## v1.1.4 (2021-02-12)
### Fix
* **requirements:** Duplicate ([`49a6544`](https://github.com/alekseik1/moodle-breaker/commit/49a654473ed08e08ee77076c5d22be279777a727))
* Remove Sentry from requirements ([`d5b2ed5`](https://github.com/alekseik1/moodle-breaker/commit/d5b2ed570a0c19059abb20704c90d639cef8d4ac))

## v1.1.3 (2021-02-12)
### Fix
* Remove broken Sentry ([`e05c3c2`](https://github.com/alekseik1/moodle-breaker/commit/e05c3c21769d0b5a2049f2f6bd5c00ab0805db0e))

## v1.1.2 (2021-02-12)
### Fix
* Remove non-used VK keyboard ([`12882b7`](https://github.com/alekseik1/moodle-breaker/commit/12882b728e8fec52c3f6a915456c1db5b9ea667c))

## v1.1.1 (2021-02-12)
### Fix
* **vk:** Default button color ([`829d67f`](https://github.com/alekseik1/moodle-breaker/commit/829d67f686e82aec3fa9069b9790332f36a53100))
