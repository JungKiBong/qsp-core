# -*- coding: utf-8 -*-
import pytest
from qsp_core.parser import QspFrame, QspParser
from qsp_core.interpreter import QspInterpreter

def test_qsp_frame_dsl_roundtrip():
    # 1. DSL 인코딩 & 디코딩 라운드트립 검증
    frame = QspParser.encode(
        actor="caeba",
        target_object="kernel_oom",
        mutation_from="stable",
        mutation_to="crash",
        resolves=["oom", "hang"],
        state="failure",
        severity="critical",
        emotions={"urgency": 0.95, "anxiety": 0.8},
        meta="Out of memory detected in master process. Triggering safety quarantine.",
        timestamp=1779537000
    )
    
    dsl_str = frame.to_hd_dsl()
    assert "ACT(caeba)" in dsl_str
    assert "MUT(kernel_oom:stable->crash)" in dsl_str
    assert "RESOLVE(oom,hang)" in dsl_str
    assert "AFF(urgency:0.95,anxiety:0.8)" in dsl_str
    
    # 디코딩 복원
    parsed = QspParser.parse_dsl(dsl_str)
    assert parsed.actor == "caeba"
    assert parsed.target_object == "kernel_oom"
    assert parsed.mutation_from == "stable"
    assert parsed.mutation_to == "crash"
    assert parsed.resolves == ["oom", "hang"]
    assert parsed.state == "failure"
    assert parsed.severity == "critical"
    assert parsed.emotions["urgency"] == 0.95
    assert parsed.meta == "Out of memory detected in master process. Triggering safety quarantine."
    assert parsed.timestamp == 1779537000

def test_qsp_bef_binary_roundtrip():
    # 2. BEF 바이너리 직렬화 라운드트립 검증
    frame = QspParser.encode(
        actor="ag-mac",
        target_object="db_cluster",
        mutation_from="sync",
        mutation_to="isolated",
        resolves=["db_recovery"],
        state="active",
        severity="medium",
        emotions={"caution": 0.9},
        meta="Local db replication latency warning",
        timestamp=1779537100
    )
    
    bef_bytes = frame.to_bef()
    assert isinstance(bef_bytes, bytes)
    
    parsed = QspParser.parse_bef(bef_bytes)
    assert parsed.actor == "ag-mac"
    assert parsed.target_object == "db_cluster"
    assert parsed.mutation_from == "sync"
    assert parsed.mutation_to == "isolated"
    assert parsed.resolves == ["db_recovery"]
    assert parsed.state == "active"
    assert parsed.severity == "medium"
    assert parsed.emotions["caution"] == 0.9
    assert parsed.meta == "Local db replication latency warning"

def test_qsp_multi_lingual_translation():
    # 3. 다국어 번역 출력 검증 (한국어, 영어, 일본어)
    frame = QspParser.encode(
        actor="caeba",
        target_object="kernel_oom",
        mutation_from="stable",
        mutation_to="crash",
        resolves=["oom"],
        state="failure",
        severity="critical",
        emotions={"urgency": 0.95},
        meta="Out of memory",
        timestamp=1779537000
    )
    
    # 3-1. 국문 검증
    kr_log = QspInterpreter.translate(frame, lang="ko")
    assert "🔴 [긴급]" in kr_log
    assert "메타 에이전트 카에바(CAEBA)" in kr_log
    assert "메모리 부족 현상(OOM) 오류" in kr_log
    assert "극도의 긴급함" in kr_log
    assert "Out of memory" in kr_log
    
    # 3-2. 영문 검증
    en_log = QspInterpreter.translate(frame, lang="en")
    assert "🔴 [URGENT]" in en_log
    assert "Meta Agent CAEBA" in en_log
    assert "Out of Memory (OOM) error" in en_log
    assert "Extreme Urgency" in en_log

    # 3-3. 일문 검증
    ja_log = QspInterpreter.translate(frame, lang="ja")
    assert "🔴 [緊急]" in ja_log
    assert "メタエージェント CAEBA" in ja_log
    assert "メモリ不足 (OOM) エラー" in ja_log
    assert "極度の緊急" in ja_log

    # 3-4. 중문 검증
    zh_log = QspInterpreter.translate(frame, lang="zh")
    assert "🔴 [紧急]" in zh_log
    assert "元代理 CAEBA" in zh_log
    assert "内存不足 (OOM) 错误" in zh_log
    assert "极度紧急" in zh_log

    # 3-5. 불문 검증
    fr_log = QspInterpreter.translate(frame, lang="fr")
    assert "🔴 [URGENT]" in fr_log
    assert "Méta-Agent CAEBA" in fr_log
    assert "erreur d'insuffisance de mémoire (OOM)" in fr_log
    assert "Urgence Extrême" in fr_log

    # 3-6. 서문 검증
    es_log = QspInterpreter.translate(frame, lang="es")
    assert "🔴 [URGENTE]" in es_log
    assert "Meta-Agente CAEBA" in es_log
    assert "error de falta de memoria (OOM)" in es_log
    assert "Urgencia Extrema" in es_log
