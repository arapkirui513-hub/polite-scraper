from app.robots import RobotsChecker

checker = RobotsChecker("KevinKiruiPoliteScraper/1.0")

url = "https://en.wikipedia.org/wiki/Ministry_of_Health_(Kenya)"

parser = checker._get_parser(url)

print("Parser:", parser)
print("disallow_all:", parser.disallow_all)
print("allow_all:", parser.allow_all)
print("mtime:", parser.mtime())
print("Allowed:", checker.can_fetch(url))
print("Crawl delay:", checker.crawl_delay(url))