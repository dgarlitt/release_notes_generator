MOCK_GOOD_COMMIT_1 = "\n".join([
    "557fec0b69228ae803c81e38f80c3b1fb993d9cb|||<<<(((ooo+++ooo)))>>>|||Bob Dole|||<<<(((ooo+++ooo)))>>>|||bob@dole.com|||<<<(((ooo+++ooo)))>>>|||2015-05-20|||<<<(((ooo+++ooo)))>>>|||TIK-1111 - Some important change|||<<<(((ooo+++ooo)))>>>|||This change affects something really important and the commit message",
    "body is formatted correctly"
])

MOCK_GOOD_COMMIT_2 = "ec213785cc02c8e7cdd4a8fbe3738e9847a916f8|||<<<(((ooo+++ooo)))>>>|||Bob Dole|||<<<(((ooo+++ooo)))>>>|||bob@dole.com|||<<<(((ooo+++ooo)))>>>|||2015-05-13|||<<<(((ooo+++ooo)))>>>|||TIK-1234 - This is a reasonable commit message|||<<<(((ooo+++ooo)))>>>|||It also has a body with more details"

MOCK_BAD_COMMIT_1 = "506adbe8292c255560c8983d46cf8d83a54aa04c|||<<<(((ooo+++ooo)))>>>|||John Rambo|||<<<(((ooo+++ooo)))>>>|||john@rambo.com|||<<<(((ooo+++ooo)))>>>|||2015-05-13|||<<<(((ooo+++ooo)))>>>|||This is a terrrible commit message! It's way too long and doesn't provide any value to the world as a whole. I feel terrible writing it.|||<<<(((ooo+++ooo)))>>>|||"

MOCK_BAD_COMMIT_2 = "9352d76d81e926e70a2857030702155f135d649a|||<<<(((ooo+++ooo)))>>>|||Sammy Davis Jr.|||<<<(((ooo+++ooo)))>>>|||sammy@davis.jr|||<<<(((ooo+++ooo)))>>>|||2015-05-12|||<<<(((ooo+++ooo)))>>>|||This is not a good commit message, it is way too long. But it does actually contain a ticket number TIK-1234 - so it isn't all bad!|||<<<(((ooo+++ooo)))>>>|||"

MOCK_GIT_LOG = [
    MOCK_GOOD_COMMIT_1,
    MOCK_BAD_COMMIT_1,
    MOCK_GOOD_COMMIT_2,
    MOCK_BAD_COMMIT_2
]

MOCK_RELEASE_NOTES_STR = "\n".join([
    "# PROJ [1.2.3.4](http://repo_web_url/commits/tag-1.2.3.4) Release Notes",
    "***",
    "  ",
    "## Tickets (2)",
    "***",
    "[__TIK-1111__](http://tickets/TIK-1111) (1 commits)",
    "   - Bob Dole <bob@dole.com>",
    "",
    "***",
    "[__TIK-1234__](http://tickets/TIK-1234) (2 commits)",
    "   - Bob Dole <bob@dole.com>",
    "   - Sammy Davis Jr. <sammy@davis.jr>",
    "",
    "***",
    "",
    "## Commits (4)",
    "***",
    "### [TIK-1111](http://tickets/TIK-1111) - Some important change",
    "",
    " - __commit:__ [557fec0b69228ae803c81e38f80c3b1fb993d9cb](http://repo_web_url/commit/557fec0b69228ae803c81e38f80c3b1fb993d9cb)",
    " - __author:__ Bob Dole <bob@dole.com>",
    " - __date:__ 2015-05-20",
    "",
    "> This change affects something really important and the commit message",
    "> body is formatted correctly",
    "",
    "***",
    "### This is a terrrible commit message! It's way too long and doesn't provide any value to the world as a whole. I feel terrible writing it.",
    "",
    " - __commit:__ [506adbe8292c255560c8983d46cf8d83a54aa04c](http://repo_web_url/commit/506adbe8292c255560c8983d46cf8d83a54aa04c)",
    " - __author:__ John Rambo <john@rambo.com>",
    " - __date:__ 2015-05-13",
    "",
    "",
    "",
    "***",
    "### [TIK-1234](http://tickets/TIK-1234) - This is a reasonable commit message",
    "",
    " - __commit:__ [ec213785cc02c8e7cdd4a8fbe3738e9847a916f8](http://repo_web_url/commit/ec213785cc02c8e7cdd4a8fbe3738e9847a916f8)",
    " - __author:__ Bob Dole <bob@dole.com>",
    " - __date:__ 2015-05-13",
    "",
    "> It also has a body with more details",
    "",
    "***",
    "### This is not a good commit message, it is way too long. But it does actually contain a ticket number [TIK-1234](http://tickets/TIK-1234) - so it isn't all bad!",
    "",
    " - __commit:__ [9352d76d81e926e70a2857030702155f135d649a](http://repo_web_url/commit/9352d76d81e926e70a2857030702155f135d649a)",
    " - __author:__ Sammy Davis Jr. <sammy@davis.jr>",
    " - __date:__ 2015-05-12",
    "",
    "",
    "",
    "***",
    "",
    "## Authors (3)",
    "***",
    "### Bob Dole <bob@dole.com>",
    "#### Commits",
    " - total: 2",
    " - with ticket number: 2",
    " - formatted correctly: 2",
    "",
    "***",
    "### John Rambo <john@rambo.com>",
    "#### Commits",
    " - total: 1",
    " - with ticket number: 0",
    " - formatted correctly: 0",
    "",
    "***",
    "### Sammy Davis Jr. <sammy@davis.jr>",
    "#### Commits",
    " - total: 1",
    " - with ticket number: 1",
    " - formatted correctly: 0",
    "",
    "***",
    ""
])