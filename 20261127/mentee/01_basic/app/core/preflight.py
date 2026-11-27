"""B-02: /health는 설정 및 CUDA/DB 준비 확인이며 유료 모델 호출이 아니다."""
from app.services.errors import ServiceError

def require_cuda():
    import torch
    if not torch.cuda.is_available() or torch.cuda.device_count() < 1:
        raise ServiceError('GPU_UNAVAILABLE')
    return 'cuda:0'

def preflight(settings, repo):
    db_state = repo.preflight()
    # 검색 가능한 유효 벡터가 0건이면 서비스 불가 상태로 차단
    if db_state.get('eligible_vectors', 0) < 1:
        raise ServiceError('DB_UNAVAILABLE', 'no_eligible_vectors')
    gpu = require_cuda()
    if not settings.llm_configured:
        raise ServiceError('LLM_UNAVAILABLE', 'not_configured')
    return {
        **db_state,
        'gpu': gpu,
        'embedding_model': settings.embedding_model,
        'reranker_model': settings.reranker_model,
        'llm': 'configured',
        'llm_live_verified': False,
    }


"""
[코드 요약]
- require_cuda로 CUDA GPU(cuda:0) 가용성을 확인해 CPU fallback을 방지한다.
- preflight는 DB 상태(repo.preflight), 유효 벡터 수(1건 이상), GPU, LLM 설정 여부를 통합 점검한다.
- 점검 결과를 /health 응답용 상태 딕셔너리로 반환하며 실제 유료 LLM 호출은 수행하지 않는다.
"""
