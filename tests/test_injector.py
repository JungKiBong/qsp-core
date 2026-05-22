# -*- coding: utf-8 -*-
import pytest
from qsp_core.injector import QspPromptInjector, FuzzyQspParser

def test_prompt_injector_structures():
    injector = QspPromptInjector()
    
    # 1. Claude 에이전트 시스템 프롬프트 생성 검증
    claude_prompt = injector.get_system_prompt(agent_type="claude", agent_name="ag-mac")
    assert "Quantum Semantic Protocol (QSP) 2.0" in claude_prompt
    assert "ACT(ag-mac)" in claude_prompt
    assert "XML 스타일 블록 없이" in claude_prompt

    # 2. GPT 에이전트 시스템 프롬프트 생성 검증
    gpt_prompt = injector.get_system_prompt(agent_type="gpt", agent_name="caeba")
    assert "ACT(caeba)" in gpt_prompt
    assert "QSP: " in gpt_prompt


def test_fuzzy_regex_parsing_and_repairs():
    # 3. 괄호가 중간에 유실되거나 공백이 뒤엉킨 망가진 DSL의 복원력 검증
    
    # 3-1. MUT 괄호 유실 복구
    broken_dsl_1 = "ACT(ag-mac)->MUT(gunicorn_worker:sync->gthread->OBJ(gunicorn_worker)->STATE(success)->SEV(critical)->TS(1779537280)"
    frame1 = FuzzyQspParser.parse_fuzzy_dsl(broken_dsl_1)
    assert frame1.actor == "ag-mac"
    assert frame1.target_object == "gunicorn_worker"
    assert frame1.mutation_from == "sync"
    assert frame1.mutation_to == "gthread"
    assert frame1.state == "success"
    assert frame1.severity == "critical"
    assert frame1.timestamp == 1779537280

    # 3-2. 무작위 대소문자 공백 및 지시부 화살표 이상 침입
    broken_dsl_2 = "act(caeba) -> mut( api_auth : free -> active ) -> obj(api_auth) -> state(success) -> sev(medium) -> ts(1779537280)"
    frame2 = FuzzyQspParser.parse_fuzzy_dsl(broken_dsl_2)
    assert frame2.actor == "caeba"
    assert frame2.target_object == "api_auth"
    assert frame2.mutation_from == "free"
    assert frame2.mutation_to == "active"
    assert frame2.severity == "medium"
    assert frame2.state == "success"
