"""Shared probe helper: reuse one login across probe runs.

Eufy rate-limits the login endpoint (HTTP 429 after a handful of logins), and every login
with a fresh openudid looks like a new phone. The probes therefore keep the HTTP session
(tokens + openudid, never the password or the MQTT key material) in a cache file outside
the repo, in the directory named by EUFY_SESSION_CACHE, falling back to the user's temp dir.
Delete the file to force a fresh login.
"""

from __future__ import annotations

import json
import os
import pathlib
import tempfile
import time

import aiohttp

from eufy_omni_cloud.exceptions import EufyAuthError
from eufy_omni_cloud.http import EufyCloudHttp, Session, new_openudid


def cache_path() -> pathlib.Path:
    base = os.environ.get("EUFY_SESSION_CACHE") or tempfile.gettempdir()
    return pathlib.Path(base) / "eufy-omni-probe-session.json"


def _load() -> dict | None:
    p = cache_path()
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _save(sess: Session, openudid: str) -> None:
    p = cache_path()
    p.write_text(
        json.dumps(
            {
                "saved": time.time(),
                "openudid": openudid,
                "access_token": sess.access_token,
                "user_id": sess.user_id,
                "login_client": sess.login_client,
                "user_center_id": sess.user_center_id,
                "user_center_token": sess.user_center_token,
            }
        ),
        encoding="utf-8",
    )
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


async def get_cloud(http: aiohttp.ClientSession) -> EufyCloudHttp:
    """Return a logged-in client, reusing the cached session when it still works."""
    user, pw = os.environ.get("EUFY_USERNAME"), os.environ.get("EUFY_PASSWORD")
    cached = _load()
    openudid = (cached or {}).get("openudid") or new_openudid()
    cloud = EufyCloudHttp(user or "", pw or "", openudid, http)
    if cached and cached.get("access_token"):
        cloud.session = Session(
            access_token=cached["access_token"],
            user_id=cached.get("user_id", ""),
            login_client=cached.get("login_client", "cached"),
            user_center_id=cached.get("user_center_id"),
            user_center_token=cached.get("user_center_token"),
        )
        try:
            await cloud.async_aiot_devices()  # cheap validity check
            return cloud
        except EufyAuthError:
            print("cached session expired; logging in again")
    if not user or not pw:
        raise SystemExit("set EUFY_USERNAME and EUFY_PASSWORD (no valid cached session)")
    sess = await cloud.async_login()
    _save(sess, openudid)
    print(f"logged in via {sess.login_client}; session cached at {cache_path()}")
    return cloud
