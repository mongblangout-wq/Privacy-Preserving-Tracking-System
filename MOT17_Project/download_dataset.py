# download_dataset.py
import os
import requests
import zipfile
import shutil


def download_and_extract(url, zip_filename, target_dir):
    """지정된 URL에서 파일을 다운로드하고 압축을 해제합니다."""
    # 1. 다운로드
    if not os.path.exists(zip_filename):
        print(f"\n[INFO] {zip_filename} 다운로드 시작... (시간이 소요됩니다)")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(zip_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[SUCCESS] {zip_filename} 다운로드 완료!")
        except Exception as e:
            print(f"[ERROR] {zip_filename} 다운로드 중 오류 발생: {e}")
            return
    else:
        print(f"\n[INFO] 이미 {zip_filename} 파일이 존재합니다.")

    # 2. 압축 해제
    if not os.path.exists(target_dir):
        print(f"[INFO] {zip_filename} 압축 해제 시작...")
        try:
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            print(f"[SUCCESS] {target_dir} 압축 해제 완료!")
        except Exception as e:
            print(f"[ERROR] {zip_filename} 압축 해제 중 오류 발생: {e}")
    else:
        print(f"[INFO] 이미 압축 해제된 폴더가 존재합니다: {target_dir}")


def filter_dataset(target_dir, dataset_prefix, targets):
    """지정된 데이터셋 폴더에서 타겟 시퀀스만 남기고 나머지는 삭제합니다."""
    # 데이터셋의 실제 하위 폴더 경로 (예: ./MOT17_Full/MOT17)
    full_path = os.path.join(target_dir, dataset_prefix)
    if not os.path.exists(full_path):
        full_path = target_dir  # 폴더 구조에 따라 바로 타겟 디렉토리일 경우

    if not os.path.exists(full_path):
        print(f"[ERROR] 경로를 찾을 수 없습니다: {full_path}")
        return

    # train과 test 폴더 내부를 모두 정리
    for split in ['train', 'test']:
        split_path = os.path.join(full_path, split)
        if not os.path.exists(split_path):
            continue

        print(f"\n--- {dataset_prefix} {split} 시퀀스 필터링 시작 ---")
        folders = os.listdir(split_path)

        for folder in folders:
            try:
                parts = folder.split('-')
                if len(parts) > 1:
                    seq_num = parts[1]
                    # 타겟 리스트에 없으면 폴더 전체 삭제
                    if seq_num not in targets:
                        dir_to_remove = os.path.join(split_path, folder)
                        shutil.rmtree(dir_to_remove)
                        print(f"  [삭제] {folder}")
                    else:
                        print(f"  [유지] {folder}")
            except Exception:
                pass  # 폴더 형식이 맞지 않는 파일은 무시


def main():
    # 1. 최상위 프로젝트 폴더 생성 및 이동
    project_folder = "MOT17_Project"
    current_path = os.getcwd()
    project_path = os.path.join(current_path, project_folder)

    if not os.path.exists(project_path):
        os.makedirs(project_path)
    os.chdir(project_path)
    print(f"========== 데이터셋 준비 파이프라인 시작 ==========")
    print(f"[STATUS] 작업 폴더: {os.getcwd()}")

    # 2. MOT17 데이터셋 처리 (다운로드 -> 압축해제 -> 필터링)
    mot17_url = "https://motchallenge.net/data/MOT17.zip"
    mot17_target_dir = "./MOT17_Full"
    mot17_targets = ['04', '05', '09', '11', '13']

    download_and_extract(mot17_url, "MOT17.zip", mot17_target_dir)
    filter_dataset(mot17_target_dir, "MOT17", mot17_targets)

    # 3. MOT20 데이터셋 처리 (다운로드 -> 압축해제 -> 필터링)
    mot20_url = "https://motchallenge.net/data/MOT20.zip"
    mot20_target_dir = "./MOT20_Full"
    mot20_targets = ['02']

    download_and_extract(mot20_url, "MOT20.zip", mot20_target_dir)
    filter_dataset(mot20_target_dir, "MOT20", mot20_targets)

    print("\n========== 모든 데이터 준비가 완료되었습니다! ==========")
    print("사용할 6개의 핵심 시퀀스만 성공적으로 남았습니다.")


if __name__ == "__main__":
    main()