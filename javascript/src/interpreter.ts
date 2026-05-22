import { QspFrame } from './parser';

export class QspInterpreter {
  /**
   * Translates a QspFrame to the specified language (ko, en, ja, zh, fr, es).
   */
  public static translate(frame: QspFrame, lang = 'ko'): string {
    const targetLang = lang.toLowerCase();
    switch (targetLang) {
      case 'en':
        return QspInterpreter.translateEn(frame);
      case 'ja':
        return QspInterpreter.translateJa(frame);
      case 'zh':
        return QspInterpreter.translateZh(frame);
      case 'fr':
        return QspInterpreter.translateFr(frame);
      case 'es':
        return QspInterpreter.translateEs(frame);
      default:
        return QspInterpreter.translateKo(frame);
    }
  }

  public static translateToKorean(frame: QspFrame): string {
    return QspInterpreter.translate(frame, 'ko');
  }

  private static formatDate(timestamp: number): string {
    const date = new Date(timestamp * 1000);
    const pad = (n: number) => n.toString().padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  }

  private static translateKo(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': '로컬 안티그래비티(Mac)',
      'ag-pc': '하청 안티그래비티(PC)',
      'caeba': '메타 에이전트 카에바(CAEBA)',
      'zenith': '상위 인지 체계 제니스(Zenith)',
      'bat-sim': '배터리 수명 시뮬레이터 API',
      'traffic-sim': '네트워크 트래픽 시뮬레이터',
    };

    const resolvesKr: Record<string, string> = {
      oom: '메모리 부족 현상(OOM) 오류',
      hang: '서버 무반응 교착 상태',
      overheating_prot: '과열 보호 조치 트리거',
      vuln_patch: '2026년 2분기 보안 취약점 조치',
      db_recovery: 'Neo4j 데이터베이스 복구',
      latency: '지연 시간 병목 현상',
    };

    const actorKr = agentNames[frame.actor] || `에이전트 [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesKr[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join(' 및 ') : '내부 비정상 상태';

    const sevDecor = frame.severity === 'critical' ? '🔴 [긴급] ' : frame.severity === 'medium' ? '🟡 [경고] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorKr}가 ${targetName} 모듈을 '${mutFrom}' 방식에서 '${mutTo}' 방식으로 성공적으로 전환하여, 발생 중이던 ${resolvesStr}를 완전하게 해결하였습니다.`;
    } else if (frame.state === 'active') {
      sentence = `${actorKr}의 ${targetName} 모듈 상태가 '${mutFrom}'에서 '${mutTo}'으로 자동 변환되었으며, ${resolvesStr}을 위해 즉각적인 실시간 관제를 가동 중입니다.`;
    } else {
      sentence = `${actorKr}가 ${targetName} 모듈을 '${mutFrom}'에서 '${mutTo}'으로 패치하려 했으나, ${resolvesStr} 조치 과정에서 장애가 발생하여 실패했습니다.`;
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('극도의 긴급함');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('사용자 불안 해소 필요');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('높은 경계 상태');
      if (emotionsList.length > 0) {
        sentence += ` (당시 시스템 정서 상태: ${emotionsList.join(', ')} 반영됨)`;
      }
    }

    if (frame.meta) {
      sentence += ` *세부 관찰 피드백: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }

  private static translateEn(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': 'Local Antigravity (Mac)',
      'ag-pc': 'Subordinate Antigravity (PC)',
      'caeba': 'Meta Agent CAEBA',
      'zenith': 'Zenith Cognitive System',
      'bat-sim': 'Battery Simulator API',
      'traffic-sim': 'Traffic Simulator',
    };

    const resolvesEn: Record<string, string> = {
      oom: 'Out of Memory (OOM) error',
      hang: 'Server Hang/Deadlock state',
      overheating_prot: 'Overheating protection trigger',
      vuln_patch: 'Q2 2026 security vulnerability fix',
      db_recovery: 'Neo4j database recovery',
      latency: 'latency bottleneck',
    };

    const actorEn = agentNames[frame.actor] || `Agent [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesEn[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join(' and ') : 'internal anomalies';

    const sevDecor = frame.severity === 'critical' ? '🔴 [URGENT] ' : frame.severity === 'medium' ? '🟡 [WARNING] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorEn} successfully switched ${targetName} module from '${mutFrom}' to '${mutTo}', completely resolving the ongoing ${resolvesStr}.`;
    } else if (frame.state === 'active') {
      sentence = `${targetName} module of ${actorEn} transitioned from '${mutFrom}' to '${mutTo}'. Active monitoring has been initiated to address ${resolvesStr}.`;
    } else {
      sentence = `${actorEn} failed to patch ${targetName} module from '${mutFrom}' to '${mutTo}' due to unhandled exceptions in resolving ${resolvesStr}.`;
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('Extreme Urgency');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('High Anxiety');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('High Caution');
      if (emotionsList.length > 0) {
        sentence += ` (System affect states: ${emotionsList.join(', ')})`;
      }
    }

    if (frame.meta) {
      sentence += ` *Details: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }

  private static translateJa(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': 'ローカル・アン치グラビティ (Mac)',
      'ag-pc': '下請アン치グラビティ (PC)',
      'caeba': 'メタエージェント CAEBA',
      'zenith': 'ゼニス認知システム',
      'bat-sim': 'バッテリーシミュレータ API',
      'traffic-sim': 'トラフィックシミュレータ',
    };

    const resolvesJa: Record<string, string> = {
      oom: 'メモリ不足 (OOM) エラー',
      hang: 'サーバー無反応のデッドロック状態',
      overheating_prot: '過熱防止措置トリガー',
      vuln_patch: '2026年第2四半期セキュリティ脆弱性パッチ',
      db_recovery: 'Neo4j データベース修復',
      latency: 'レイテンシのボトルネック',
    };

    const actorJa = agentNames[frame.actor] || `エージェント [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesJa[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join('および') : '内部異常状態';

    const sevDecor = frame.severity === 'critical' ? '🔴 [緊急] ' : frame.severity === 'medium' ? '🟡 [警告] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorJa}が${targetName}モジュールを'${mutFrom}'から'${mutTo}'へ正常に切り替え、発生中だった${resolvesStr}を完全に解決しました。`;
    } else if (frame.state === 'active') {
      sentence = `${actorJa}の${targetName}モジュールの状態が'${mutFrom}'から'${mutTo}'へ自動遷移しました。${resolvesStr}に対応するため、リアルタイム監視を実行中です。`;
    } else {
      sentence = `${actorJa}가${targetName}モジュールを'${mutFrom}'から'${mutTo}'へ更新しようとしましたが、${resolvesStr}の対処中にエラーが発生し失敗しました。`;
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('極度の緊急');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('ユーザー不安解消プロセス');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('高い警戒');
      if (emotionsList.length > 0) {
        sentence += ` (システム情動感情: ${emotionsList.join(', ')})`;
      }
    }

    if (frame.meta) {
      sentence += ` *観測詳細: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }

  private static translateZh(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': '本地 Antigravity (Mac)',
      'ag-pc': '下属 Antigravity (PC)',
      'caeba': '元代理 CAEBA',
      'zenith': 'Zenith 认知系统',
      'bat-sim': '电池寿命模拟器 API',
      'traffic-sim': '网络流量模拟器',
    };

    const resolvesZh: Record<string, string> = {
      oom: '内存不足 (OOM) 错误',
      hang: '服务器无响应死锁状态',
      overheating_prot: '过热保护措施触发',
      vuln_patch: '2026年第二季度安全漏洞修复',
      db_recovery: 'Neo4j 数据库修复',
      latency: '延迟时间瓶颈现象',
    };

    const actorZh = agentNames[frame.actor] || `代理 [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesZh[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join(' 及 ') : '内部异常状态';

    const sevDecor = frame.severity === 'critical' ? '🔴 [紧急] ' : frame.severity === 'medium' ? '🟡 [警告] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorZh}成功将 ${targetName} 模块从 '${mutFrom}' 切换为 '${mutTo}'，完全解决了正在发生的 {resolvesStr}。`.replace('{resolvesStr}', resolvesStr);
    } else if (frame.state === 'active') {
      sentence = `${actorZh}的 ${targetName} 模块状态已从 '${mutFrom}' 转换为 '${mutTo}'。已启动实时监控以应对 ${resolvesStr}。`;
    } else {
      sentence = `${actorZh}尝试将 {targetName} 模块从 '{mutFrom}' 修补为 '{mutTo}' 时失败，原因是在处理 {resolvesStr} 时发生未处理的异常。`
        .replace('{targetName}', targetName)
        .replace('{mutFrom}', mutFrom)
        .replace('{mutTo}', mutTo)
        .replace('{resolvesStr}', resolvesStr);
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('极度紧急');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('需要消除用户焦虑');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('高度警惕状态');
      if (emotionsList.length > 0) {
        sentence += ` (当时系统情绪状态: ${emotionsList.join(', ')} 已反映)`;
      }
    }

    if (frame.meta) {
      sentence += ` *详细观察反馈: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }

  private static translateFr(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': 'Antigravity Local (Mac)',
      'ag-pc': 'Antigravity Subordonné (PC)',
      'caeba': 'Méta-Agent CAEBA',
      'zenith': 'Système Cognitif Zenith',
      'bat-sim': 'API de Simulateur de Batterie',
      'traffic-sim': 'Simulateur de Trafic Réseau',
    };

    const resolvesFr: Record<string, string> = {
      oom: "erreur d'insuffisance de mémoire (OOM)",
      hang: 'état de blocage/deadlock du serveur',
      overheating_prot: 'déclenchement de la protection contre la surchauffe',
      vuln_patch: 'correctif de vulnérabilité de sécurité du Q2 2026',
      db_recovery: 'restauration de la base de données Neo4j',
      latency: 'goulot d\'étranglement de latence',
    };

    const actorFr = agentNames[frame.actor] || `Agent [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesFr[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join(' et ') : 'anomalies internes';

    const sevDecor = frame.severity === 'critical' ? '🔴 [URGENT] ' : frame.severity === 'medium' ? '🟡 [AVERTISSEMENT] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorFr} a basculé avec succès le module ${targetName} de '${mutFrom}' à '${mutTo}', résolvant complètement ${resolvesStr}.`;
    } else if (frame.state === 'active') {
      sentence = `Le module ${targetName} de ${actorFr} a transité de '${mutFrom}' à '${mutTo}'. Une surveillance active a été initiée pour traiter ${resolvesStr}.`;
    } else {
      sentence = `${actorFr} a échoué à patcher le module ${targetName} de '${mutFrom}' à '${mutTo}' en raison d'exceptions non gérées lors de la résolution de ${resolvesStr}.`;
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('Urgence Extrême');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('Anxiété Élevée');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('Grande Prudence');
      if (emotionsList.length > 0) {
        sentence += ` (États affectifs du système: ${emotionsList.join(', ')})`;
      }
    }

    if (frame.meta) {
      sentence += ` *Détails: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }

  private static translateEs(frame: QspFrame): string {
    const agentNames: Record<string, string> = {
      'ag-mac': 'Antigravity Local (Mac)',
      'ag-pc': 'Antigravity Subordinado (PC)',
      'caeba': 'Meta-Agente CAEBA',
      'zenith': 'Sistema Cognitivo Zenith',
      'bat-sim': 'API de Simulador de Batería',
      'traffic-sim': 'Simulador de Tráfico',
    };

    const resolvesEs: Record<string, string> = {
      oom: 'error de falta de memoria (OOM)',
      hang: 'estado de bloqueo/deadlock del servidor',
      overheating_prot: 'disparador de protección contra sobrecalentamiento',
      vuln_patch: 'corrección de vulnerabilidad de seguridad del Q2 2026',
      db_recovery: 'recuperación de la base de datos Neo4j',
      latency: 'cuello de botella de latencia',
    };

    const actorEs = agentNames[frame.actor] || `Agente [${frame.actor}]`;
    const targetName = frame.targetObject.toUpperCase();
    const mutFrom = frame.mutationFrom.toUpperCase();
    const mutTo = frame.mutationTo.toUpperCase();

    const resolvesList = frame.resolves.map((r) => resolvesEs[r] || r);
    const resolvesStr = resolvesList.length > 0 ? resolvesList.join(' y ') : 'anomalías internas';

    const sevDecor = frame.severity === 'critical' ? '🔴 [URGENT] ' : frame.severity === 'medium' ? '🟡 [ADVERTENCIA] ' : '🟢 ';

    let sentence = '';
    if (frame.state === 'success') {
      sentence = `${actorEs} cambió con éxito el módulo ${targetName} de '${mutFrom}' a '${mutTo}', resolviendo por completo ${resolvesStr}.`;
    } else if (frame.state === 'active') {
      sentence = `El módulo ${targetName} de ${actorEs} pasó de '${mutFrom}' a '${mutTo}'. Se ha iniciado un monitoreo activo para abordar ${resolvesStr}.`;
    } else {
      sentence = `${actorEs} falló al parchear el módulo ${targetName} de '${mutFrom}' a '${mutTo}' debido a excepciones no manejadas al resolver ${resolvesStr}.`;
    }

    if (frame.emotions) {
      const emotionsList: string[] = [];
      if ((frame.emotions['urgency'] || 0) > 0.7) emotionsList.push('Urgencia Extrema');
      if ((frame.emotions['anxiety'] || 0) > 0.7) emotionsList.push('Ansiedad Alta');
      if ((frame.emotions['caution'] || 0) > 0.7) emotionsList.push('Gran Precaución');
      if (emotionsList.length > 0) {
        sentence += ` (Estados afectivos del sistema: ${emotionsList.join(', ')})`;
      }
    }

    if (frame.meta) {
      sentence += ` *Detalles: "${frame.meta}"`;
    }

    const timeStr = QspInterpreter.formatDate(frame.timestamp);
    return `${sevDecor}(${timeStr}) ${sentence}`;
  }
}
