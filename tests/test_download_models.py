from pathlib import Path

from download_models import download_file


LFS_POINTER = b"version https://git-lfs.github.com/spec/v1\noid sha256:123\nsize 123\n"


def test_download_file_replaces_lfs_pointer(tmp_path, monkeypatch):
    model = tmp_path / "model.onnx"
    model.write_bytes(LFS_POINTER)

    def download(url, dest):
        Path(dest).write_bytes(b"model contents")

    monkeypatch.setattr("download_models.urllib.request.urlretrieve", download)
    assert download_file("https://example.com/model.onnx", model)
    assert model.read_bytes() == b"model contents"
    assert list(tmp_path.iterdir()) == [model]


def test_failed_download_preserves_existing_file(tmp_path, monkeypatch):
    model = tmp_path / "model.onnx"
    model.write_bytes(LFS_POINTER)

    def download(url, dest):
        Path(dest).write_bytes(b"partial")
        raise OSError("connection lost")

    monkeypatch.setattr("download_models.urllib.request.urlretrieve", download)
    assert not download_file("https://example.com/model.onnx", model)
    assert model.read_bytes() == LFS_POINTER
    assert list(tmp_path.iterdir()) == [model]
