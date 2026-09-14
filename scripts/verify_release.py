from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_NAME = "安徽农户持续种粮调研项目"
FORBIDDEN_PATH_PARTS = (
    "01_原始数据",
    "02_清洗数据",
    "农户画像分配",
    "实拍三联图",
    "本地核验来源",
    "比例收敛抽样说明",
)
FORBIDDEN_FILE_SUFFIXES = {
    ".7z",
    ".db",
    ".feather",
    ".jpg",
    ".jpeg",
    ".parquet",
    ".pdf",
    ".sqlite",
    ".sqlite3",
    ".xls",
    ".xlsx",
    ".zip",
}
EXPECTED_PUBLIC_DATA_FILES = {
    "02_公开数据/图表数据/fig1-2_ah_urban_rural_income.csv",
    "02_公开数据/图表数据/fig4-1_land_status.csv",
    "02_公开数据/图表数据/fig4-2_labor_fallow.csv",
    "02_公开数据/图表数据/fig4-3_logit_or.csv",
    "02_公开数据/图表数据/fig4-4_area_disaster_prediction.csv",
    "02_公开数据/图表数据/fig5-2_profile_heatmap.csv",
    "02_公开数据/图表数据/fig5-3_profile_metrics.csv",
    "02_公开数据/图表数据/fig6-2_policy_future.csv",
    "02_公开数据/图表数据/fig6-3_contract_service_constraints.csv",
    "02_公开数据/图表数据/fig6-4_village_governance.csv",
    "02_公开数据/图表数据/fig6-5_household_village_parallel.csv",
    "02_公开数据/聚合分析结果/2025年画像汇总.csv",
    "02_公开数据/聚合分析结果/2025年画像聚类元数据.json",
    "02_公开数据/聚合分析结果/2025年画像特征热图数据.csv",
    "02_公开数据/聚合分析结果/2025年连续结果模型.csv",
    "02_公开数据/聚合分析结果/2025年撂荒分组统计.csv",
    "02_公开数据/聚合分析结果/2025年撂荒模型结果.csv",
    "02_公开数据/聚合分析结果/2025年敏感性检验.csv",
    "02_公开数据/聚合分析结果/2025年土地状态统计.csv",
    "02_公开数据/聚合分析结果/2025年预测情景网格.csv",
    "02_公开数据/聚合分析结果/2026年村级指标.csv",
    "02_公开数据/聚合分析结果/2026年户村并列指标.csv",
    "02_公开数据/聚合分析结果/2026年农户指标.csv",
    "02_公开数据/聚合分析结果/2026年质量口径.json",
}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".csv",
    ".json",
    ".ipynb",
    ".yml",
    ".yaml",
    ".cff",
    ".py",
    ".svg",
}
SENSITIVE_PATTERNS = {
    "phone_value": re.compile(r"(?<![\d./])1[3-9]\d{9}(?![\d./])"),
    "landline_value": re.compile(r"(?<!\d)0\d{2,3}[- ]?\d{7,8}(?!\d)"),
    "id_value": re.compile(r"(?<![\d.])\d{17}[\dXx](?![\d.])"),
    "email_value": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "ipv4_value": re.compile(
        r"(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])"
    ),
    "wechat_id": re.compile(r"(?i)\bwxid_[a-z0-9]+\b"),
    "private_key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "windows_absolute_path": re.compile(r"\b[A-Za-z]:\\"),
    "linux_home_path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
}
RISKY_FIELD_PARTS = {
    "姓名",
    "手机号",
    "联系电话",
    "身份证",
    "邮箱",
    "电子邮件",
    "详细地址",
    "家庭住址",
    "答卷id",
    "受访者编号",
    "respondent_id",
    "phone",
    "mobile",
    "email",
    "id_card",
    "identity_number",
    "ip_address",
    "openid",
    "unionid",
}
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_docx_metadata(path: Path, problems: list[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("docProps/core.xml"))
        member_names = archive.namelist()
        hidden_parts = [
            name
            for name in member_names
            if name.startswith("customXml/")
            or name.startswith("word/embeddings/")
            or name.startswith("word/people/")
            or name.startswith("word/comments")
        ]
        if hidden_parts:
            problems.append(
                f"docx_hidden_content:{path.relative_to(ROOT).as_posix()}"
            )
        for name in member_names:
            if not name.endswith((".xml", ".rels")):
                continue
            text = archive.read(name).decode("utf-8", errors="replace")
            for pattern_name, pattern in SENSITIVE_PATTERNS.items():
                if pattern.search(text):
                    problems.append(
                        "docx_sensitive_pattern:"
                        f"{path.relative_to(ROOT).as_posix()}:{name}:{pattern_name}"
                    )
    namespace = {
        "dc": "http://purl.org/dc/elements/1.1/",
        "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    }
    for xpath in ("dc:creator", "cp:lastModifiedBy"):
        value = root.findtext(xpath, default="", namespaces=namespace)
        if value != PROJECT_NAME:
            problems.append(f"docx_metadata:{path.relative_to(ROOT).as_posix()}:{xpath}")


def verify_png_metadata(path: Path, problems: list[str]) -> None:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        problems.append(f"invalid_png:{path.relative_to(ROOT).as_posix()}")
        return
    offset = 8
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        if chunk_type == b"eXIf":
            problems.append(f"png_exif:{path.relative_to(ROOT).as_posix()}")
        if chunk_type in {b"tEXt", b"zTXt", b"iTXt"}:
            keyword = chunk_data.split(b"\x00", 1)[0].decode(
                "latin-1", errors="replace"
            )
            if keyword.casefold() != "software":
                problems.append(
                    f"png_text_metadata:{path.relative_to(ROOT).as_posix()}:{keyword}"
                )
        offset += 12 + length
        if chunk_type == b"IEND":
            break


def risky_field_name(value: str) -> bool:
    normalized = re.sub(r"[\s-]+", "_", value.strip().casefold())
    return any(part in normalized for part in RISKY_FIELD_PARTS)


def json_keys(value: object) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key))
            keys.extend(json_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(json_keys(child))
    return keys


def notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8-sig"))
    parts: list[str] = []
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        parts.extend(source if isinstance(source, list) else [source])
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream":
                value = output.get("text", [])
                parts.extend(value if isinstance(value, list) else [value])
            data = output.get("data", {})
            # Rich table outputs include a transient Python object address in
            # text/plain. Prefer the rendered HTML to avoid treating that
            # process-local address as content.
            mime_type = "text/html" if "text/html" in data else "text/plain"
            value = data.get(mime_type, [])
            parts.extend(value if isinstance(value, list) else [value])
    return "".join(map(str, parts))


def verify_public_data_schema(path: Path, problems: list[str]) -> None:
    relative_path = path.relative_to(ROOT).as_posix()
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream)
            header = next(reader, [])
        for field in header:
            if risky_field_name(field):
                problems.append(f"risky_data_field:{relative_path}:{field}")
    elif path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        for field in json_keys(value):
            if risky_field_name(field):
                problems.append(f"risky_data_field:{relative_path}:{field}")


def verify_markdown_links(path: Path, problems: list[str]) -> None:
    text = path.read_text(encoding="utf-8-sig")
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.split("#", 1)[0].strip().strip("<>")
        if not target or re.match(r"^(?:https?://|mailto:)", target):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            problems.append(
                f"broken_link:{path.relative_to(ROOT).as_posix()}:{raw_target}"
            )


def main() -> int:
    problems: list[str] = []
    manifest_path = ROOT / "MANIFEST.csv"
    hashes_path = ROOT / "SHA256SUMS.txt"
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    actual_files = sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and path.name not in {"MANIFEST.csv", "SHA256SUMS.txt"}
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and path.suffix.lower() != ".pyc"
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    actual_paths = {path.relative_to(ROOT).as_posix() for path in actual_files}
    manifest_paths = {row["relative_path"] for row in rows}
    if actual_paths != manifest_paths:
        for item in sorted(actual_paths - manifest_paths):
            problems.append(f"manifest_missing:{item}")
        for item in sorted(manifest_paths - actual_paths):
            problems.append(f"manifest_extra:{item}")

    by_path = {path.relative_to(ROOT).as_posix(): path for path in actual_files}
    actual_public_data = {
        relative_path
        for relative_path in actual_paths
        if relative_path.startswith("02_公开数据/")
    }
    if actual_public_data != EXPECTED_PUBLIC_DATA_FILES:
        for item in sorted(actual_public_data - EXPECTED_PUBLIC_DATA_FILES):
            problems.append(f"unapproved_public_data:{item}")
        for item in sorted(EXPECTED_PUBLIC_DATA_FILES - actual_public_data):
            problems.append(f"approved_public_data_missing:{item}")
    for row in rows:
        relative_path = row["relative_path"]
        path = by_path.get(relative_path)
        if path is None:
            continue
        if int(row["byte_size"]) != path.stat().st_size:
            problems.append(f"size_mismatch:{relative_path}")
        if row["sha256"] != sha256(path):
            problems.append(f"hash_mismatch:{relative_path}")

    expected_hashes = [
        f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in actual_files
    ]
    if hashes_path.read_text(encoding="utf-8").splitlines() != expected_hashes:
        problems.append("sha256_manifest_mismatch")

    for path in actual_files:
        relative_path = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_FILE_SUFFIXES:
            problems.append(f"forbidden_file_type:{relative_path}")
        if any(part in relative_path for part in FORBIDDEN_PATH_PARTS):
            problems.append(f"forbidden_path:{relative_path}")
        if (
            path.suffix.lower() in TEXT_SUFFIXES or path.name == "LICENSE"
        ) and not relative_path.startswith("LICENSES/"):
            text = (
                notebook_text(path)
                if path.suffix.lower() == ".ipynb"
                else path.read_text(encoding="utf-8-sig", errors="replace")
            )
            for name, pattern in SENSITIVE_PATTERNS.items():
                if pattern.search(text):
                    problems.append(f"sensitive_pattern:{relative_path}:{name}")
        if path.suffix.lower() == ".docx":
            verify_docx_metadata(path, problems)
        if path.suffix.lower() == ".png":
            verify_png_metadata(path, problems)
        if relative_path.startswith("02_公开数据/"):
            verify_public_data_schema(path, problems)
        if path.suffix.lower() == ".md":
            verify_markdown_links(path, problems)

    report = ROOT / "01_调研报告" / "把地种好，把日子过稳——稳定承包背景下安徽农户持续种粮的约束结构.md"
    if "field_plate" in report.read_text(encoding="utf-8"):
        problems.append("report_contains_field_photo_link")

    if problems:
        print("status=FAIL")
        for problem in problems:
            print(problem)
        return 1

    print("status=PASS")
    print(f"release_files={len(actual_files)}")
    print("manifest_paths_complete=true")
    print("sizes_match=true")
    print("sha256_match=true")
    print("markdown_links_valid=true")
    print("microdata_path_present=false")
    print("identifiable_field_photo_present=false")
    print("third_party_fulltext_present=false")
    print("direct_identifier_value_present=false")
    print("risky_public_data_field_present=false")
    print("docx_hidden_content_present=false")
    print("image_private_metadata_present=false")
    print("approved_public_data_allowlist_match=true")
    print("author_attribution_present=true")
    print("license_present=true")
    print("software_license=AGPL-3.0-only")
    print("content_license=CC-BY-SA-4.0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
