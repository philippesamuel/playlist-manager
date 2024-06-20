import datetime
from typing import Iterator
import cachier
import httpx

CHROME_FOR_TESTING_VERSIONS_URL = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
MY_CHROME_VERSION = "123.0.6312.105"
MY_CHROME_PLATFORM = "win64"


def main() -> None:
    my_driver_url = get_chrome_driver_url()
    print(my_driver_url)


def get_chrome_driver_url() -> str:
    (my_version, *_) = (v for v in get_versions() if v["version"] == MY_CHROME_VERSION)
    drivers = (d for d in my_version["downloads"]["chromedriver"])
    (my_driver, *_) = (d for d in drivers if d["platform"] == MY_CHROME_PLATFORM)
    return my_driver["url"]


def get_versions() -> Iterator[dict]:
    r_data = get_versions_json()
    for version_data in r_data["versions"]:
        yield version_data


@cachier.cachier(stale_after=datetime.timedelta(days=1))
def get_versions_json() -> dict:
    r = httpx.get(CHROME_FOR_TESTING_VERSIONS_URL)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    main()
