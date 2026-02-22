"""
social_footprint.py — Passive social media and username OSINT.

Checks for username presence across major platforms using HTTP HEAD/GET
requests. Fully passive — only reads public profile pages.

Platforms checked:
  GitHub, GitLab, Twitter/X, Reddit, HackerNews, Instagram,
  LinkedIn (limited), YouTube, TikTok, Twitch, Medium, Dev.to,
  Stack Overflow, Keybase, Telegram (t.me), Signal (not applicable)

Usage:
    from scripts.osint.social_footprint import SocialFootprint

    sf = SocialFootprint()
    results = sf.check_username("targetuser")
    sf.check_github_profile("targetuser")
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Optional

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5   # seconds between requests — be a good netizen

PLATFORMS: dict[str, str] = {
    "GitHub":        "https://github.com/{username}",
    "GitLab":        "https://gitlab.com/{username}",
    "Twitter/X":     "https://twitter.com/{username}",
    "Reddit":        "https://www.reddit.com/user/{username}",
    "HackerNews":    "https://news.ycombinator.com/user?id={username}",
    "Instagram":     "https://www.instagram.com/{username}/",
    "YouTube":       "https://www.youtube.com/@{username}",
    "TikTok":        "https://www.tiktok.com/@{username}",
    "Twitch":        "https://www.twitch.tv/{username}",
    "Medium":        "https://medium.com/@{username}",
    "Dev.to":        "https://dev.to/{username}",
    "Stack Overflow": "https://stackoverflow.com/users/search?tab=Reputation&search={username}",
    "Keybase":       "https://keybase.io/{username}",
    "Telegram":      "https://t.me/{username}",
    "Mastodon":      "https://mastodon.social/@{username}",
    "Pinterest":     "https://www.pinterest.com/{username}/",
}

# Status codes that reliably mean "profile exists"
POSITIVE_CODES = {200, 301, 302}
# Pages with 200 that contain these strings are "not found" pages
NOT_FOUND_SIGNATURES = [
    "this account doesn't exist",
    "user not found",
    "no such user",                   # HackerNews: returns 200 + "No such user."
    "no such user.",
    "page not found",
    "sorry, this page isn't available",
    "isn't available",
    "404",
    "profile not found",
    "doesn't exist",
    "does not exist",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


@dataclass
class PlatformResult:
    platform: str
    username: str
    url: str
    found: bool
    status_code: int = 0
    error: str = ""


@dataclass
class GitHubProfile:
    username: str
    name: str = ""
    bio: str = ""
    location: str = ""
    company: str = ""
    email: str = ""
    blog: str = ""
    twitter: str = ""
    public_repos: int = 0
    followers: int = 0
    following: int = 0
    created_at: str = ""
    repos: list[dict] = field(default_factory=list)
    error: str = ""


@dataclass
class SocialResults:
    username: str
    platform_results: list[PlatformResult] = field(default_factory=list)
    github_profile: Optional[GitHubProfile] = None

    @property
    def found_on(self) -> list[str]:
        return [r.platform for r in self.platform_results if r.found]

    @property
    def not_found_on(self) -> list[str]:
        return [r.platform for r in self.platform_results if not r.found]

    def summary(self) -> str:
        lines = [
            f"# Social Footprint: {self.username}",
            "",
            f"**Found on {len(self.found_on)} platform(s):**",
        ]
        for r in self.platform_results:
            icon = "✅" if r.found else "❌"
            lines.append(f"  {icon} {r.platform}: {r.url if r.found else '—'}")

        if self.github_profile and not self.github_profile.error:
            g = self.github_profile
            lines += [
                "",
                "## GitHub Profile Details",
                f"  Name:     {g.name}",
                f"  Bio:      {g.bio}",
                f"  Location: {g.location}",
                f"  Company:  {g.company}",
                f"  Email:    {g.email}",
                f"  Repos:    {g.public_repos}",
                f"  Followers:{g.followers}",
                f"  Created:  {g.created_at}",
            ]
            if g.repos:
                lines.append("  Top repositories:")
                for repo in g.repos[:10]:
                    lines.append(f"    - {repo.get('name')} ⭐{repo.get('stargazers_count', 0)}"
                                 f" [{repo.get('language', '')}] — {repo.get('description', '')}")
        return "\n".join(lines)


class SocialFootprint:
    def __init__(self, delay: float = REQUEST_DELAY):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _check_platform(self, platform: str, url_template: str, username: str) -> PlatformResult:
        url = url_template.format(username=username)
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            body_lower = response.text.lower()
            found = (
                response.status_code in POSITIVE_CODES
                and not any(sig in body_lower for sig in NOT_FOUND_SIGNATURES)
            )
            return PlatformResult(platform, username, url, found, response.status_code)
        except requests.Timeout:
            return PlatformResult(platform, username, url, False, error="timeout")
        except Exception as e:
            return PlatformResult(platform, username, url, False, error=str(e))

    def check_username(
        self,
        username: str,
        platforms: list[str] | None = None,
    ) -> SocialResults:
        """
        Check username existence across social platforms.

        Args:
            username: The username/handle to check
            platforms: Optional subset of platforms to check (defaults to all)
        """
        results = SocialResults(username=username)
        target_platforms = {
            k: v for k, v in PLATFORMS.items()
            if platforms is None or k in platforms
        }

        logger.info("Checking %s across %d platforms", username, len(target_platforms))

        for platform, url_template in target_platforms.items():
            result = self._check_platform(platform, url_template, username)
            results.platform_results.append(result)
            if result.found:
                logger.info("  FOUND: %s — %s", platform, result.url)
            time.sleep(self.delay)

        # Always run GitHub profile enrichment if found
        github_result = next((r for r in results.platform_results if r.platform == "GitHub" and r.found), None)
        if github_result:
            results.github_profile = self.get_github_profile(username)

        return results

    def get_github_profile(self, username: str) -> GitHubProfile:
        """
        Fetch enriched GitHub profile data via the public GitHub API.
        No authentication needed for public profiles (60 req/hr unauthenticated).
        """
        profile = GitHubProfile(username=username)
        try:
            # User profile
            response = self.session.get(
                f"https://api.github.com/users/{username}",
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 404:
                profile.error = "GitHub user not found"
                return profile
            response.raise_for_status()
            data = response.json()

            profile.name = data.get("name", "")
            profile.bio = data.get("bio", "")
            profile.location = data.get("location", "")
            profile.company = data.get("company", "")
            profile.email = data.get("email", "")
            profile.blog = data.get("blog", "")
            profile.twitter = data.get("twitter_username", "")
            profile.public_repos = data.get("public_repos", 0)
            profile.followers = data.get("followers", 0)
            profile.following = data.get("following", 0)
            profile.created_at = data.get("created_at", "")

            # Public repos
            time.sleep(self.delay)
            repos_response = self.session.get(
                f"https://api.github.com/users/{username}/repos",
                params={"sort": "stars", "per_page": 20},
                timeout=REQUEST_TIMEOUT,
            )
            if repos_response.status_code == 200:
                profile.repos = repos_response.json()

            logger.info("GitHub profile enriched for %s: %d repos, %d followers",
                        username, profile.public_repos, profile.followers)

        except Exception as e:
            profile.error = str(e)
            logger.warning("GitHub profile error for %s: %s", username, e)

        return profile


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Passive social media OSINT")
    parser.add_argument("username", help="Username to investigate")
    parser.add_argument("--platforms", nargs="+", help="Specific platforms to check")
    parser.add_argument("--github", action="store_true", help="Deep GitHub profile only")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    sf = SocialFootprint()

    if args.github:
        profile = sf.get_github_profile(args.username)
        if profile.error:
            print(f"Error: {profile.error}")
        else:
            print(f"GitHub: {args.username}")
            print(f"  Name: {profile.name} | Location: {profile.location}")
            print(f"  Bio: {profile.bio}")
            print(f"  Repos: {profile.public_repos} | Followers: {profile.followers}")
    else:
        results = sf.check_username(args.username, platforms=args.platforms)
        print(results.summary())


if __name__ == "__main__":
    main()
