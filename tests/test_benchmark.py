# -*- coding: utf-8 -*-
import pytest
import json
from qsp_core.parser import QspParser

def test_qsp_standalone_performance_benchmark():
    # 1. 테스트용 정밀 상태 데이터 프레임 준비
    frame = QspParser.encode(
        actor="caeba",
        target_object="database_cluster_primary",
        mutation_from="healthy",
        mutation_to="degraded",
        resolves=["read_timeout", "write_latency"],
        state="active",
        severity="critical",
        emotions={"urgency": 0.9, "anxiety": 0.85},
        meta="Primary Postgres replication lag exceeded 15 seconds. Triggering adaptive failover.",
        timestamp=1779537500
    )
    
    # 2. 전통적인 JSON 직렬화 용량
    raw_dict = {
        "actor": frame.actor,
        "target_object": frame.target_object,
        "mutation_from": frame.mutation_from,
        "mutation_to": frame.mutation_to,
        "resolves": frame.resolves,
        "state": frame.state,
        "severity": frame.severity,
        "emotions": frame.emotions,
        "meta": frame.meta,
        "timestamp": frame.timestamp
    }
    json_bytes = json.dumps(raw_dict).encode("utf-8")
    json_len = len(json_bytes)
    
    # 3. QSP 2.0 HD-DSL 문자열 토큰 바이트 용량
    hd_dsl_str = frame.to_hd_dsl()
    hd_dsl_bytes = hd_dsl_str.encode("utf-8")
    hd_dsl_len = len(hd_dsl_bytes)
    
    # 4. QSP 2.0 BEF 바이너리 직렬화 용량
    bef_bytes = frame.to_bef()
    bef_len = len(bef_bytes)
    
    # 5. 절감율 측정 계산
    token_saving_ratio = (1.0 - (hd_dsl_len / json_len)) * 100
    network_saving_ratio = (1.0 - (bef_len / json_len)) * 100
    
    print("\n")
    print("=" * 60)
    print("      QSP-CORE STANDALONE PERFORMANCE REPORT      ")
    print("=" * 60)
    print(f"[-] Original JSON Size       : {json_len} Bytes")
    print(f"[-] QSP HD-DSL Size (LLM)    : {hd_dsl_len} Bytes")
    print(f"[-] QSP BEF Size (Network)   : {bef_len} Bytes")
    print("-" * 60)
    print(f"[★] LLM Context Token Saving : {token_saving_ratio:.2f}% (Target > 15.0%)")
    print(f"[★] Network Bandwidth Saving : {network_saving_ratio:.2f}% (Target > 40.0%)")
    print("=" * 60)
    
    # 6. 정량적 성공 기준 어설션 검증
    assert token_saving_ratio > 15.0
    assert network_saving_ratio > 40.0
