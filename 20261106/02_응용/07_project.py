"""
실습 07~08: 객체 추적기(ByteTrack vs BoT-SORT) 벤치마크
동일한 데모 영상(demo.avi)에 대해 두 가지 추적 알고리즘을 독립 실행합니다.
처리 프레임 수, 추적된 행 수, 소요 시간 및 처리량(FPS)을 비교 분석합니다.
"""
from pathlib import Path
from time import perf_counter
import os, cv2, torch
import pandas as pd
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
os.chdir(BASE)
out = BASE / "outputs"; out.mkdir(exist_ok=True); torch.set_num_threads(1)
summaries = []

for name in ["bytetrack.yaml", "botsort.yaml"]:
    model = YOLO(str(BASE / "data/demo.pt"))  # 비교마다 상태가 새로 시작됩니다.
    rows = []; frame_counts = []; start = perf_counter()
    writer = cv2.VideoWriter(f"outputs/{Path(name).stem}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, (160, 128))
    # >>> A07
    # 지정된 추적기(bytetrack / botsort)와 stream=True 옵션으로 영상 추적을 수행합니다.
    results = model.track(source="data/demo.avi", tracker=name, stream=True, persist=False, verbose=False)
    # <<< A07
    for frame, r in enumerate(results):
        writer.write(r.plot()); frame_counts.append([frame, len(r.boxes)])
        if r.boxes.id is not None:
            for box, cls, score, tid in zip(r.boxes.xyxy.cpu().tolist(), r.boxes.cls.cpu().tolist(), r.boxes.conf.cpu().tolist(), r.boxes.id.cpu().tolist()):
                rows.append([frame, int(tid), int(cls), score, *box])
    writer.release(); seconds = perf_counter() - start
    # >>> A08
    # 프레임, 트랙ID, 클래스, 확신도, 좌표를 CSV 파일로 저장합니다.
    pd.DataFrame(rows, columns=["frame", "track_id", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv(f"outputs/{Path(name).stem}_tracks.csv", index=False)
    # <<< A08
    pd.DataFrame(frame_counts, columns=["frame", "detections"]).to_csv(f"outputs/{Path(name).stem}_frames.csv", index=False)
    summaries.append(dict(tracker=name, frames=len(frame_counts), track_rows=len(rows), seconds=seconds, throughput=len(frame_counts) / seconds, scope="decode+infer+track+plot+encode; first-run cost included", id_switch="별도 GT 매칭 필요"))

r = pd.DataFrame(summaries); r.to_csv("outputs/tracker_comparison.csv", index=False); print(r.to_string(index=False))
