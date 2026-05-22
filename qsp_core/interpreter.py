# -*- coding: utf-8 -*-
"""
QSP Core Multi-lingual Interpreter
Translates compact symbolic QSP frames into rich human-friendly statements (Korean, English, Japanese).
"""

import time
from qsp_core.parser import QspFrame

class QspInterpreter:
    """
    QspInterpreter translates cryptic HD-DSL or BEF bytes 
    into business-friendly, human-readable monitoring alerts in multiple languages.
    """
    @staticmethod
    def translate(frame: QspFrame, lang: str = "ko") -> str:
        """
        Translates a QspFrame to the specified language (ko, en, ja, zh, fr, es).
        """
        lang = lang.lower()
        if lang == "en":
            return QspInterpreter._translate_en(frame)
        elif lang == "ja":
            return QspInterpreter._translate_ja(frame)
        elif lang == "zh":
            return QspInterpreter._translate_zh(frame)
        elif lang == "fr":
            return QspInterpreter._translate_fr(frame)
        elif lang == "es":
            return QspInterpreter._translate_es(frame)
        else:
            return QspInterpreter._translate_ko(frame)

    @staticmethod
    def translate_to_korean(frame: QspFrame) -> str:
        """Backward compatibility helper for Korean translation."""
        return QspInterpreter.translate(frame, lang="ko")

    @staticmethod
    def _translate_ko(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "로컬 안티그래비티(Mac)",
            "ag-pc": "하청 안티그래비티(PC)",
            "caeba": "메타 에이전트 카에바(CAEBA)",
            "zenith": "상위 인지 체계 제니스(Zenith)",
            "bat-sim": "배터리 수명 시뮬레이터 API",
            "traffic-sim": "네트워크 트래픽 시뮬레이터"
        }
        resolves_kr = {
            "oom": "메모리 부족 현상(OOM) 오류",
            "hang": "서버 무반응 교착 상태",
            "overheating_prot": "과열 보호 조치 트리거",
            "vuln_patch": "2026년 2분기 보안 취약점 조치",
            "db_recovery": "Neo4j 데이터베이스 복구",
            "latency": "지연 시간 병목 현상"
        }

        actor_kr = agent_names.get(frame.actor, f"에이전트 [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_kr.get(r, r) for r in frame.resolves]
        resolves_str = " 및 ".join(resolves_list) if resolves_list else "내부 비정상 상태"
        
        sev_decor = "🔴 [긴급] " if frame.severity == "critical" else ("🟡 [경고] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_kr}가 {target_name} 모듈을 '{mut_from}' 방식에서 '{mut_to}' 방식으로 성공적으로 전환하여, 발생 중이던 {resolves_str}를 완전하게 해결하였습니다."
        elif frame.state == "active":
            sentence = f"{actor_kr}의 {target_name} 모듈 상태가 '{mut_from}'에서 '{mut_to}'으로 자동 변환되었으며, {resolves_str}을 위해 즉각적인 실시간 관제를 가동 중입니다."
        else:
            sentence = f"{actor_kr}가 {target_name} 모듈을 '{mut_from}'에서 '{mut_to}'으로 패치하려 했으나, {resolves_str} 조치 과정에서 장애가 발생하여 실패했습니다."
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("극도의 긴급함")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("사용자 불안 해소 필요")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("높은 경계 상태")
            if emotions_list:
                sentence += f" (당시 시스템 정서 상태: {', '.join(emotions_list)} 반영됨)"

        if frame.meta:
            sentence += f" *세부 관찰 피드백: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"

    @staticmethod
    def _translate_en(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "Local Antigravity (Mac)",
            "ag-pc": "Subordinate Antigravity (PC)",
            "caeba": "Meta Agent CAEBA",
            "zenith": "Zenith Cognitive System",
            "bat-sim": "Battery Simulator API",
            "traffic-sim": "Traffic Simulator"
        }
        resolves_en = {
            "oom": "Out of Memory (OOM) error",
            "hang": "Server Hang/Deadlock state",
            "overheating_prot": "Overheating protection trigger",
            "vuln_patch": "Q2 2026 security vulnerability fix",
            "db_recovery": "Neo4j database recovery",
            "latency": "latency bottleneck"
        }

        actor_en = agent_names.get(frame.actor, f"Agent [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_en.get(r, r) for r in frame.resolves]
        resolves_str = " and ".join(resolves_list) if resolves_list else "internal anomalies"
        
        sev_decor = "🔴 [URGENT] " if frame.severity == "critical" else ("🟡 [WARNING] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_en} successfully switched {target_name} module from '{mut_from}' to '{mut_to}', completely resolving the ongoing {resolves_str}."
        elif frame.state == "active":
            sentence = f"{target_name} module of {actor_en} transitioned from '{mut_from}' to '{mut_to}'. Active monitoring has been initiated to address {resolves_str}."
        else:
            sentence = f"{actor_en} failed to patch {target_name} module from '{mut_from}' to '{mut_to}' due to unhandled exceptions in resolving {resolves_str}."
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("Extreme Urgency")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("High Anxiety")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("High Caution")
            if emotions_list:
                sentence += f" (System affect states: {', '.join(emotions_list)})"

        if frame.meta:
            sentence += f" *Details: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"

    @staticmethod
    def _translate_ja(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "ローカル・アンチグラビティ (Mac)",
            "ag-pc": "下請アンチグラビティ (PC)",
            "caeba": "メタエージェント CAEBA",
            "zenith": "ゼニス認知システム",
            "bat-sim": "バッテリーシミュレータ API",
            "traffic-sim": "トラフィックシミュレータ"
        }
        resolves_ja = {
            "oom": "メモリ不足 (OOM) エラー",
            "hang": "サーバー無反応のデッドロック状態",
            "overheating_prot": "過熱防止措置トリガー",
            "vuln_patch": "2026年第2四半期セキュリティ脆弱性パッチ",
            "db_recovery": "Neo4j データベース修復",
            "latency": "レイテンシのボトルネック"
        }

        actor_ja = agent_names.get(frame.actor, f"エージェント [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_ja.get(r, r) for r in frame.resolves]
        resolves_str = "および".join(resolves_list) if resolves_list else "内部異常状態"
        
        sev_decor = "🔴 [緊急] " if frame.severity == "critical" else ("🟡 [警告] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_ja}が{target_name}モジュールを'{mut_from}'から'{mut_to}'へ正常に切り替え、発生中だった{resolves_str}を完全に解決しました。"
        elif frame.state == "active":
            sentence = f"{actor_ja}の{target_name}モジュールの状態が'{mut_from}'から'{mut_to}'へ自動遷移しました。{resolves_str}に対応するため、リアルタイム監視を実行中です。"
        else:
            sentence = f"{actor_ja}が{target_name}モジュールを'{mut_from}'から'{mut_to}'へ更新しようとしましたが、{resolves_str}の対処中にエラーが発生し失敗しました。"
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("極度の緊急")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("ユーザー不安解消プロセス")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("高い警戒")
            if emotions_list:
                sentence += f" (システム情動感情: {', '.join(emotions_list)})"

        if frame.meta:
            sentence += f" *観測詳細: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"

    @staticmethod
    def _translate_zh(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "本地 Antigravity (Mac)",
            "ag-pc": "下属 Antigravity (PC)",
            "caeba": "元代理 CAEBA",
            "zenith": "Zenith 认知系统",
            "bat-sim": "电池寿命模拟器 API",
            "traffic-sim": "网络流量模拟器"
        }
        resolves_zh = {
            "oom": "内存不足 (OOM) 错误",
            "hang": "服务器无响应死锁状态",
            "overheating_prot": "过热保护措施触发",
            "vuln_patch": "2026年第二季度安全漏洞修复",
            "db_recovery": "Neo4j 数据库修复",
            "latency": "延迟时间瓶颈现象"
        }

        actor_zh = agent_names.get(frame.actor, f"代理 [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_zh.get(r, r) for r in frame.resolves]
        resolves_str = " 及 ".join(resolves_list) if resolves_list else "内部异常状态"
        
        sev_decor = "🔴 [紧急] " if frame.severity == "critical" else ("🟡 [警告] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_zh}成功将 {target_name} 模块从 '{mut_from}' 切换为 '{mut_to}'，完全解决了正在发生的 {resolves_str}。"
        elif frame.state == "active":
            sentence = f"{actor_zh}的 {target_name} 模块状态已从 '{mut_from}' 转换为 '{mut_to}'。已启动实时监控以应对 {resolves_str}。"
        else:
            sentence = f"{actor_zh}尝试将 {target_name} 模块从 '{mut_from}' 修补为 '{mut_to}' 时失败，原因是在处理 {resolves_str} 时发生未处理的异常。"
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("极度紧急")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("需要消除用户焦虑")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("高度警惕状态")
            if emotions_list:
                sentence += f" (当时系统情绪状态: {', '.join(emotions_list)} 已反映)"

        if frame.meta:
            sentence += f" *详细观察反馈: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"

    @staticmethod
    def _translate_fr(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "Antigravity Local (Mac)",
            "ag-pc": "Antigravity Subordonné (PC)",
            "caeba": "Méta-Agent CAEBA",
            "zenith": "Système Cognitif Zenith",
            "bat-sim": "API de Simulateur de Batterie",
            "traffic-sim": "Simulateur de Trafic Réseau"
        }
        resolves_fr = {
            "oom": "erreur d'insuffisance de mémoire (OOM)",
            "hang": "état de blocage/deadlock du serveur",
            "overheating_prot": "déclenchement de la protection contre la surchauffe",
            "vuln_patch": "correctif de vulnérabilité de sécurité du Q2 2026",
            "db_recovery": "restauration de la base de données Neo4j",
            "latency": "goulot d'étranglement de latence"
        }

        actor_fr = agent_names.get(frame.actor, f"Agent [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_fr.get(r, r) for r in frame.resolves]
        resolves_str = " et ".join(resolves_list) if resolves_list else "anomalies internes"
        
        sev_decor = "🔴 [URGENT] " if frame.severity == "critical" else ("🟡 [AVERTISSEMENT] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_fr} a basculé avec succès le module {target_name} de '{mut_from}' à '{mut_to}', résolvant complètement {resolves_str}."
        elif frame.state == "active":
            sentence = f"Le module {target_name} de {actor_fr} a transité de '{mut_from}' à '{mut_to}'. Une surveillance active a été initiée pour traiter {resolves_str}."
        else:
            sentence = f"{actor_fr} a échoué à patcher le module {target_name} de '{mut_from}' à '{mut_to}' en raison d'exceptions non gérées lors de la résolution de {resolves_str}."
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("Urgence Extrême")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("Anxiété Élevée")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("Grande Prudence")
            if emotions_list:
                sentence += f" (États affectifs du système: {', '.join(emotions_list)})"

        if frame.meta:
            sentence += f" *Détails: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"

    @staticmethod
    def _translate_es(frame: QspFrame) -> str:
        agent_names = {
            "ag-mac": "Antigravity Local (Mac)",
            "ag-pc": "Antigravity Subordinado (PC)",
            "caeba": "Meta-Agente CAEBA",
            "zenith": "Sistema Cognitivo Zenith",
            "bat-sim": "API de Simulador de Batería",
            "traffic-sim": "Simulador de Tráfico"
        }
        resolves_es = {
            "oom": "error de falta de memoria (OOM)",
            "hang": "estado de bloqueo/deadlock del servidor",
            "overheating_prot": "disparador de protección contra sobrecalentamiento",
            "vuln_patch": "corrección de vulnerabilidad de seguridad del Q2 2026",
            "db_recovery": "recuperación de la base de datos Neo4j",
            "latency": "cuello de botella de latencia"
        }

        actor_es = agent_names.get(frame.actor, f"Agente [{frame.actor}]")
        target_name = frame.target_object.upper()
        mut_from = frame.mutation_from.upper()
        mut_to = frame.mutation_to.upper()
        
        resolves_list = [resolves_es.get(r, r) for r in frame.resolves]
        resolves_str = " y ".join(resolves_list) if resolves_list else "anomalías internas"
        
        sev_decor = "🔴 [URGENTE] " if frame.severity == "critical" else ("🟡 [ADVERTENCIA] " if frame.severity == "medium" else "🟢 ")
        
        if frame.state == "success":
            sentence = f"{actor_es} cambió con éxito el módulo {target_name} de '{mut_from}' a '{mut_to}', resolviendo por completo {resolves_str}."
        elif frame.state == "active":
            sentence = f"El módulo {target_name} de {actor_es} pasó de '{mut_from}' a '{mut_to}'. Se ha iniciado un monitoreo activo para abordar {resolves_str}."
        else:
            sentence = f"{actor_es} falló al parchear el módulo {target_name} de '{mut_from}' a '{mut_to}' debido a excepciones no manejadas al resolver {resolves_str}."
            
        if frame.emotions:
            emotions_list = []
            if frame.emotions.get("urgency", 0) > 0.7:
                emotions_list.append("Urgencia Extrema")
            if frame.emotions.get("anxiety", 0) > 0.7:
                emotions_list.append("Ansiedad Alta")
            if frame.emotions.get("caution", 0) > 0.7:
                emotions_list.append("Gran Precaución")
            if emotions_list:
                sentence += f" (Estados afectivos del sistema: {', '.join(emotions_list)})"

        if frame.meta:
            sentence += f" *Detalles: \"{frame.meta}\""

        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame.timestamp))
        return f"{sev_decor}({time_str}) {sentence}"
