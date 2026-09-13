# download_dataset.py
import os
import requests
import zipfile
import shutil
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def download_and_extract(url, zip_path: Path, target_dir: Path):
    """지정된 URL에서 파일을 다운로드하고 압축을 해제합니다."""
    # 1. 다운로드
    if not zip_path.exists():
        print(f"\n[INFO] {zip_path.name} 다운로드 시작... (시간이 소요됩니다)")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[SUCCESS] {zip_path.name} 다운로드 완료!")
        except Exception as e:
            print(f"[ERROR] {zip_path.name} 다운로드 중 오류 발생: {e}")
            return
    else:
        print(f"\n[INFO] 이미 {zip_path.name} 파일이 존재합니다.")

    # 1-1. zip 무결성 체크 (다운로드 중단 등으로 손상된 파일 방지)
    if not zipfile.is_zipfile(zip_path):
        print(f"[ERROR] {zip_path.name}이 올바른 zip 파일이 아닙니다. 삭제 후 재다운로드가 필요합니다.")
        zip_path.unlink(missing_ok=True)
        return

    # 2. 압축 해제
    if not target_dir.exists():
        print(f"[INFO] {zip_path.name} 압축 해제 시작...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            print(f"[SUCCESS] {target_dir} 압축 해제 완료!")
        except Exception as e:
            print(f"[ERROR] {zip_path.name} 압축 해제 중 오류 발생: {e}")
    else:
        print(f"[INFO] 이미 압축 해제된 폴더가 존재합니다: {target_dir}")


def filter_dataset(target_dir: Path, dataset_prefix: str, targets: list):
    """지정된 데이터셋 폴더에서 타겟 시퀀스만 남기고 나머지는 삭제합니다."""
    full_path = target_dir / dataset_prefix
    if not full_path.exists():
        full_path = target_dir  # 폴더 구조에 따라 바로 타겟 디렉토리일 경우

    if not full_path.exists():
        print(f"[ERROR] 경로를 찾을 수 없습니다: {full_path}")
        return

    # train과 test 폴더 내부를 모두 정리
    for split in ['train', 'test']:
        split_path = full_path / split
        if not split_path.exists():
            continue

        print(f"\n--- {dataset_prefix} {split} 시퀀스 필터링 시작 ---")
        folders = os.listdir(split_path)

        for folder in folders:
            try:
                parts = folder.split('-')
                if len(parts) > 1:
                    seq_num = parts[1]
                    if seq_num not in targets:
                        dir_to_remove = split_path / folder
                        shutil.rmtree(dir_to_remove)
                        print(f"  [삭제] {folder}")
                    else:
                        print(f"  [유지] {folder}")
            except Exception:
                pass  # 폴더 형식이 맞지 않는 파일은 무시


def main():
    # (원본 버그 수정: 여기서 별도 하위 폴더를 또 만들면 config.py가 기대하는 경로
    #  MOT17_ROOT = PROJECT_DIR / 'MOT17_Full' / ... 와 어긋남.
    #  PROJECT_DIR을 그대로 다운로드 위치로 사용)
    project_path = PROJECT_DIR
    project_path.mkdir(parents=True, exist_ok=True)

    print("========== 데이터셋 준비 파이프라인 시작 ==========")
    print(f"[STATUS] 작업 폴더: {project_path}")

    # 2. MOT17 데이터셋 처리 (다운로드 -> 압축해제 -> 필터링)
    mot17_url = "https://motchallenge.net/data/MOT17.zip"
    mot17_zip = project_path / "MOT17.zip"
    mot17_target_dir = project_path / "MOT17_Full"
    mot17_targets = ['04', '05', '09', '11', '13']

    download_and_extract(mot17_url, mot17_zip, mot17_target_dir)
    filter_dataset(mot17_target_dir, "MOT17", mot17_targets)

    # 3. MOT20 데이터셋 처리 (다운로드 -> 압축해제 -> 필터링)
    mot20_url = "https://motchallenge.net/data/MOT20.zip"
    mot20_zip = project_path / "MOT20.zip"
    mot20_target_dir = project_path / "MOT20_Full"
    mot20_targets = ['02']

    download_and_extract(mot20_url, mot20_zip, mot20_target_dir)
    filter_dataset(mot20_target_dir, "MOT20", mot20_targets)

    print("\n========== 모든 데이터 준비가 완료되었습니다! ==========")
    print("사용할 6개의 핵심 시퀀스만 성공적으로 남았습니다.")


if __name__ == "__main__":
    main()
