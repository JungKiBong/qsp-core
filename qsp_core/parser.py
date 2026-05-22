# -*- coding: utf-8 -*-
"""
QSP Core Parser & Serialization Engine
High-Density DSL (HD-DSL) and Binary Episodic Frame (BEF) compiler.
"""

import time
import json
import zlib
import re
from typing import List, Dict, Any, Optional

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False


class QspFrame:
    """
    QspFrame represents a single compressed semantic state snapshot
    transmitted between heterogeneous AI agents or microservices.
    """
    def __init__(
        self,
        actor: str,
        target_object: str,
        mutation_from: str,
        mutation_to: str,
        resolves: Optional[List[str]] = None,
        state: str = "success",
        severity: str = "medium",
        emotions: Optional[Dict[str, float]] = None,
        meta: Optional[str] = None,
        timestamp: Optional[int] = None
    ):
        self.actor = actor
        self.target_object = target_object
        self.mutation_from = mutation_from
        self.mutation_to = mutation_to
        self.resolves = resolves if resolves else []
        self.state = state  # success, failure, active
        self.severity = severity  # low, medium, critical
        self.emotions = emotions if emotions else {}  # e.g., {"anxiety": 0.8, "urgency": 0.9}
        self.meta = meta  # Short nuance context sentence
        self.timestamp = timestamp if timestamp else int(time.time())

    def to_hd_dsl(self) -> str:
        """
        Converts the QspFrame into a High-Density Domain-Specific Language (HD-DSL) string
        for efficient token usage within LLM context windows.
        """
        resolves_str = ",".join(self.resolves)
        mutation_str = f"{self.target_object}:{self.mutation_from}->{self.mutation_to}"
        
        dsl_parts = [
            f"ACT({self.actor})",
            f"MUT({mutation_str})",
            f"OBJ({self.target_object})",
        ]
        if self.resolves:
            dsl_parts.append(f"RESOLVE({resolves_str})")
        
        dsl_parts.extend([
            f"STATE({self.state})",
            f"SEV({self.severity})"
        ])
        
        # Affective (Emotional) Channel
        if self.emotions:
            emo_str = ",".join([f"{k}:{v}" for k, v in self.emotions.items()])
            dsl_parts.append(f"AFF({emo_str})")
            
        # Detail Meta Context Channel
        if self.meta:
            safe_meta = self.meta.replace("(", "[").replace(")", "]")
            dsl_parts.append(f"META({safe_meta})")
            
        dsl_parts.append(f"TS({self.timestamp})")
        
        return "->".join(dsl_parts)

    @classmethod
    def from_hd_dsl(cls, dsl_str: str) -> "QspFrame":
        """
        Parses a High-Density DSL string back into a structured QspFrame object.
        """
        try:
            matches = re.findall(r"([A-Z]+)\((.*?)\)(?:->|$)", dsl_str)
            data = {key: val for key, val in matches}

            actor = data.get("ACT", "unknown")
            obj = data.get("OBJ", "unknown")
            
            # Parse Mutation (MUT)
            mut_val = data.get("MUT", "")
            mutation_from = "unknown"
            mutation_to = "unknown"
            if ":" in mut_val and "->" in mut_val:
                _, transition = mut_val.split(":", 1)
                mutation_from, mutation_to = transition.split("->", 1)
            
            resolves = data.get("RESOLVE", "").split(",") if "RESOLVE" in data else []
            state = data.get("STATE", "success")
            severity = data.get("SEV", "medium")
            
            # Parse emotions (AFF)
            emotions = {}
            if "AFF" in data:
                aff_val = data["AFF"]
                for item in aff_val.split(","):
                    if ":" in item:
                        k, v = item.split(":", 1)
                        try:
                            emotions[k] = float(v)
                        except ValueError:
                            pass
                        
            # Parse detail meta context (META)
            meta = data.get("META", None)
            if meta:
                meta = meta.replace("[", "(").replace("]", ")")
                
            timestamp = int(data.get("TS", int(time.time())))
            
            return cls(
                actor=actor,
                target_object=obj,
                mutation_from=mutation_from,
                mutation_to=mutation_to,
                resolves=resolves,
                state=state,
                severity=severity,
                emotions=emotions,
                meta=meta,
                timestamp=timestamp
            )
        except Exception as e:
            raise ValueError(f"Failed to parse HD-DSL: {e}")

    def to_bef(self) -> bytes:
        """
        Serializes the frame into Binary Episodic Frame (BEF) format using msgpack
        with strict single-character keys for microsecond processing and minimal bandwidth.
        """
        compact_dict = {
            'a': self.actor,
            'm': [self.target_object, self.mutation_from, self.mutation_to],
            'r': self.resolves,
            's': 1 if self.state == "success" else (0 if self.state == "failure" else 2),
            'v': 0 if self.severity == "low" else (1 if self.severity == "medium" else 2),
            'e': self.emotions,
            'd': self.meta,
            't': self.timestamp
        }
        
        if HAS_MSGPACK:
            return msgpack.packb(compact_dict, use_bin_type=True)
        else:
            compact_json = json.dumps(compact_dict, separators=(',', ':'))
            return zlib.compress(compact_json.encode('utf-8'))

    @classmethod
    def from_bef(cls, binary_data: bytes) -> "QspFrame":
        """
        Deserializes a Binary Episodic Frame (BEF) back into a QspFrame object.
        """
        if HAS_MSGPACK:
            compact_dict = msgpack.unpackb(binary_data, raw=False)
        else:
            decompressed = zlib.decompress(binary_data).decode('utf-8')
            compact_dict = json.loads(decompressed)

        actor = compact_dict['a']
        obj, m_from, m_to = compact_dict['m']
        resolves = compact_dict['r']
        
        state_val = compact_dict['s']
        state = "success" if state_val == 1 else ("failure" if state_val == 0 else "active")
        
        sev_val = compact_dict['v']
        severity = "low" if sev_val == 0 else ("medium" if sev_val == 1 else "critical")
        
        emotions = compact_dict.get('e', {})
        meta = compact_dict.get('d', None)
        timestamp = compact_dict['t']

        return cls(
            actor=actor,
            target_object=obj,
            mutation_from=m_from,
            mutation_to=m_to,
            resolves=resolves,
            state=state,
            severity=severity,
            emotions=emotions,
            meta=meta,
            timestamp=timestamp
        )


class QspParser:
    """
    QspParser is a standalone helper class providing stateless static interfaces
    for encoding and decoding QspFrame payloads.
    """
    @staticmethod
    def encode(
        actor: str,
        target_object: str,
        mutation_from: str,
        mutation_to: str,
        resolves: Optional[List[str]] = None,
        state: str = "success",
        severity: str = "medium",
        emotions: Optional[Dict[str, float]] = None,
        meta: Optional[str] = None,
        timestamp: Optional[int] = None
    ) -> QspFrame:
        return QspFrame(
            actor=actor,
            target_object=target_object,
            mutation_from=mutation_from,
            mutation_to=mutation_to,
            resolves=resolves,
            state=state,
            severity=severity,
            emotions=emotions,
            meta=meta,
            timestamp=timestamp
        )

    @staticmethod
    def parse_dsl(dsl_str: str) -> QspFrame:
        return QspFrame.from_hd_dsl(dsl_str)

    @staticmethod
    def parse_bef(binary_data: bytes) -> QspFrame:
        return QspFrame.from_bef(binary_data)
