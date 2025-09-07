"""
Enhanced AnimalShelter CRUD Module (drop-in)
Origin: CS-340 artifact by Milfred (enhanced for CS-499)

Key improvements (Design/Security/Quality):
- No hard-coded secrets: uses MONGO_URI env var or __init__(uri=...)
- Layer-ready structure: clear repository-style class with typed, consistent returns
- Validation & errors: input checks, descriptive exceptions
- Observability: structured logging (no prints), UTC timestamps, optional audits
- Reliability: server ping on connect, safe delete guard, optional indexes

Environment:
    MONGO_URI = "mongodb://<user>:<pass>@<host>:<port>/"

Usage:
    from AnimalShelter import AnimalShelter
    shelter = AnimalShelter(database="AAC", collection="animals")
    shelter.create({...})
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


# -----------------------------
# Logging (JSON-ish single-line)
# -----------------------------
_logger = logging.getLogger("animalshelter")
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)sZ level=%(levelname)s message="%(message)s" module=%(name)s'
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


class AnimalShelter:
    """
    Repository-style wrapper around a MongoDB collection for AAC animals.

    Methods return consistent dictionaries (create/update/delete)
    and a list of documents for read().
    """

    def __init__(
        self,
        uri: Optional[str] = None,
        database: str = "AAC",
        collection: str = "animals",
        audits_collection: str = "audits",
        ensure_indexes: bool = True,
        connect_timeout_ms: int = 5000,
    ) -> None:
        mongo_uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=connect_timeout_ms)
            # Connectivity check (throws on failure)
            self.client.admin.command("ping")
            self.database = self.client[database]
            self.collection: Collection = self.database[collection]
            self.audits: Collection = self.database[audits_collection]
            if ensure_indexes:
                self._ensure_indexes()
            _logger.info("connected to mongodb database=%s collection=%s", database, collection)
        except Exception as exc:
            _logger.error("mongo_connect_error: %s", exc)
            raise

    # ------------- Utilities -------------

    @staticmethod
    def _utcnow() -> datetime:
        return datetime.now(timezone.utc)

    def _audit(self, action: str, details: Dict[str, Any]) -> None:
        """Store a minimal audit record (best-effort; does not block core ops)."""
        doc = {
            "action": action,
            "details": details,
            "ts": self._utcnow(),
        }
        try:
            self.audits.insert_one(doc)
        except Exception as exc:
            _logger.warning("audit_failed action=%s error=%s", action, exc)

    def _ensure_indexes(self) -> None:
        """Create helpful indexes without assuming uniqueness in noisy datasets."""
        try:
            self.collection.create_index([("animal_id", ASCENDING)])
            self.collection.create_index([("created_timestamp", ASCENDING)])
            self.collection.create_index([("last_modified_timestamp", ASCENDING)])
        except Exception as exc:
            _logger.warning("index_creation_failed: %s", exc)

    # ------------- Validation -------------

    @staticmethod
    def _require_dict(value: Any, name: str, allow_empty: bool = False) -> Dict[str, Any]:
        if not isinstance(value, dict):
            raise ValueError(f"{name} must be a dict")
        if not allow_empty and not value:
            raise ValueError(f"{name} must be a non-empty dict")
        return value  # type: ignore[return-value]

    @staticmethod
    def _validate_required_fields(data: Dict[str, Any], required: List[str]) -> None:
        missing = [f for f in required if f not in data]
        if missing:
            raise ValueError(f"missing required field(s): {', '.join(missing)}")

    # ------------- CRUD API -------------

    def create(self, data: Dict[str, Any], actor: Optional[str] = None) -> Dict[str, Any]:
        """
        Insert a single animal record.
        Returns: {"ok": bool, "inserted_id": str}
        """
        try:
            doc = self._require_dict(data, "data")
            # Required fields may vary by dataset; choose robust minimal set
            self._validate_required_fields(doc, ["animal_id", "animal_type", "breed"])
            doc["created_timestamp"] = self._utcnow()
            res = self.collection.insert_one(doc)
            out = {"ok": bool(res.acknowledged), "inserted_id": str(res.inserted_id)}
            self._audit("CREATE", {"actor": actor, "inserted_id": out["inserted_id"]})
            return out
        except (ValueError, PyMongoError) as exc:
            _logger.error("create_failed error=%s", exc)
            raise

    def read(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: int = 0,
        sort_field: Optional[str] = None,
        sort_order: int = ASCENDING,
    ) -> List[Dict[str, Any]]:
        """
        Find documents. Returns a list of dicts.
        """
        try:
            q = {} if query is None else self._require_dict(query, "query", allow_empty=True)
            cur = self.collection.find(q, projection) if isinstance(projection, dict) else self.collection.find(q)
            if sort_field:
                cur = cur.sort(sort_field, sort_order)
            if limit and limit > 0:
                cur = cur.limit(limit)
            results = list(cur)
            _logger.info("read count=%d", len(results))
            return results
        except (ValueError, PyMongoError) as exc:
            _logger.error("read_failed error=%s", exc)
            raise

    def update(
        self,
        query: Dict[str, Any],
        new_values: Dict[str, Any],
        *,
        upsert: bool = False,
        actor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update documents matching query.
        Returns: {"ok": bool, "matched": int, "modified": int, "upserted_id": str|None}
        """
        try:
            q = self._require_dict(query, "query")
            nv = self._require_dict(new_values, "new_values")
            nv["last_modified_timestamp"] = self._utcnow()
            res = self.collection.update_many(q, {"$set": nv}, upsert=upsert)
            out = {
                "ok": bool(res.acknowledged),
                "matched": int(res.matched_count),
                "modified": int(res.modified_count),
                "upserted_id": str(res.upserted_id) if res.upserted_id else None,
            }
            self._audit("UPDATE", {"actor": actor, "matched": out["matched"], "modified": out["modified"]})
            return out
        except (ValueError, PyMongoError) as exc:
            _logger.error("update_failed error=%s", exc)
            raise

    def delete(
        self,
        query: Dict[str, Any],
        *,
        actor: Optional[str] = None,
        confirm_delete: bool = True,
    ) -> Dict[str, Any]:
        """
        Delete documents matching query.
        Returns: {"ok": bool, "deleted": int}
        Safe-guard: refuses to delete all documents unless confirm_delete=False is passed.
        """
        try:
            q = self._require_dict(query, "query")
            if not q and confirm_delete:
                raise ValueError("refusing to delete all documents; pass confirm_delete=False to override")
            res = self.collection.delete_many(q)
            out = {"ok": bool(res.acknowledged), "deleted": int(res.deleted_count)}
            self._audit("DELETE", {"actor": actor, "deleted": out["deleted"]})
            return out
        except (ValueError, PyMongoError) as exc:
            _logger.error("delete_failed error=%s", exc)
            raise

    # ------------- Extras (nice-to-have) -------------

    def stats(self) -> Dict[str, Any]:
        """Lightweight stats for dashboards/ePortfolio evidence."""
        try:
            count = self.collection.estimated_document_count()
            latest = self.collection.find({}, {"created_timestamp": 1}).sort("created_timestamp", -1).limit(1)
            latest_ts = next(iter(latest), {}).get("created_timestamp")
            return {"count": count, "latest_created_timestamp": latest_ts}
        except PyMongoError as exc:
            _logger.error("stats_failed error=%s", exc)
            raise

    def close(self) -> None:
        try:
            self.client.close()
        except Exception:
            pass


# ----------------- Smoke test -----------------
if __name__ == "__main__":
    """
    Quick connectivity check (does not modify data).
    Set MONGO_URI first or pass uri=... to AnimalShelter().
    """
    try:
        s = AnimalShelter()
        print("OK: connected. Stats:", s.stats())
        s.close()
    except Exception as e:
        print("Connection failed:", e)
