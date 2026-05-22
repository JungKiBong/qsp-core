# -*- coding: utf-8 -*-
import pytest
from qsp_core.parser import QspFrame, QspParser

def test_qsp_lite_standalone_roundtrip():
    # 1. Create a frame representing a realistic scenario
    frame = QspParser.encode(
        actor="caeba",
        target_object="kernel_oom",
        mutation_from="stable",
        mutation_to="crash",
        resolves=["oom", "hang"],
        state="failure",
        severity="critical",
        emotions={"urgency": 0.9},
        meta="Out of memory detected in worker process",
        timestamp=1716382025
    )
    
    # 2. Encode to QSP-Lite
    lite_str = frame.to_lite_dsl()
    
    # Ensure syntax mappings match perfectly
    assert lite_str.startswith("QL[")
    assert lite_str.endswith("]")
    assert "a:caeba" in lite_str
    assert "m:kernel_oom:stable->crash" in lite_str
    assert "r:oom,hang" in lite_str
    assert "s:0" in lite_str
    assert "v:2" in lite_str
    assert "t:1716382025" in lite_str
    
    # Emotions and meta details must be stripped
    assert "urgency" not in lite_str
    assert "detected" not in lite_str

    # 3. Decode back to QspFrame via static Parser API
    decoded = QspParser.parse_lite_dsl(lite_str)
    
    # Verify exact restore parameters
    assert decoded.actor == "caeba"
    assert decoded.target_object == "kernel_oom"
    assert decoded.mutation_from == "stable"
    assert decoded.mutation_to == "crash"
    assert decoded.resolves == ["oom", "hang"]
    assert decoded.state == "failure"
    assert decoded.severity == "critical"
    assert decoded.timestamp == 1716382025
    assert decoded.emotions == {}
    assert decoded.meta is None
