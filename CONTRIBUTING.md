# Contributing to QSP Core

We welcome contributions from the community! QSP Core is an open-source project designed to enable high-efficiency, zero-ambiguity semantic communication for heterogeneous AI agents.

---

## How to Contribute

### 1. Bug Reports & Feature Requests
* Search the existing Issues before opening a new one.
* Use a clear and descriptive title.
* Provide a minimal reproducible example if reporting a bug.

### 2. Adding New Languages to Interpreter
If you want to add support for a new language (e.g., German, Italian, Vietnamese):
1. **Python**: Update `qsp_core/interpreter.py` by adding the translation templates in `QspInterpreter.translate()`.
2. **JavaScript/TypeScript**: Update `javascript/src/interpreter.ts` with matching translation dictionary mappings.
3. **Tests**: Add unit test assertions in `tests/test_parser.py` (Python) and verify the outputs.

### 3. Pull Request Process
1. Fork the repository and create your branch from `main`.
2. Ensure all tests pass:
   * **Python**: `pytest tests/`
   * **JavaScript**: `cd javascript && npm run build`
3. Update the `README.md` if your change introduces new features or APIs.
4. Open a Pull Request with a clear description of the problem and your solution.

---

## 贡献指南 (Contributing in Chinese)

我们非常欢迎社区的贡献！QSP Core 是一个旨在为异构 AI 代理提供高效、零歧义语义通信的开源项目。

### 如何贡献

1. **报告 Bug 与新功能建议**：在提交 Issue 之前，请先搜索已有的 Issue，并提供可复现的最小示例。
2. **添加新语言支持**：
   * **Python**: 修改 `qsp_core/interpreter.py` 并增加相应的翻译模版。
   * **JavaScript**: 修改 `javascript/src/interpreter.ts`。
   * **测试**: 在 `tests/test_parser.py` 中添加对应的断言测试。
3. **Pull Request 流程**：
   * 从 `main` 分支拉出开发分支。
   * 确保通过所有测试（`pytest` 及 `npm run build`）。
   * 提交 PR 并附带清晰的修改说明。

---

## 기여 가이드라인 (Contributing in Korean)

커뮤니티의 모든 기여를 환영합니다! QSP Core는 이기종 AI 에이전트 간의 초고효율, 무손실 의미론적 기호 통신을 구현하기 위한 오픈소스 프로젝트입니다.

### 기여 방법

1. **버그 보고 및 기능 제안**: 새로운 이슈를 열기 전에 기존 Issue를 검색해 주시고, 버그 보고 시 최소 재현 코드(reproducible example)를 동봉해 주세요.
2. **신규 다국어 통역 레이어 추가**:
   * **Python**: `qsp_core/interpreter.py`에 새로운 언어 코드 템플릿을 반영합니다.
   * **JavaScript/TypeScript**: `javascript/src/interpreter.ts`에 번역 어휘를 연동합니다.
   * **테스트**: `tests/test_parser.py`에 다국어 복원 검증 단언문(assert)을 추가하고 테스트합니다.
3. **Pull Request 프로세스**:
   * `main` 브랜치로부터 새로운 작업 브랜치를 생성합니다.
   * 단위 테스트 및 빌드가 모두 통과하는지 확인합니다 (`pytest` 및 `npm run build` 검증).
   * 변경 사항에 대한 명확한 요약과 함께 PR을 제출합니다.

---

## License
By contributing to QSP Core, you agree that your contributions will be licensed under the **Apache License 2.0**.
