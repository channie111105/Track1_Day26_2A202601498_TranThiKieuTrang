#!/usr/bin/env python3
"""Build the two-page Day 26 dashboard PDF from the validated worksheet values."""

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "TranThiKieuTrang_Day26_dashboard.pdf"

NAVY = colors.HexColor("#16243B")
BLUE = colors.HexColor("#2457FF")
PALE_BLUE = colors.HexColor("#EAF0FF")
LIGHT = colors.HexColor("#F4F6F9")
MID = colors.HexColor("#D8DEE9")
TEXT = colors.HexColor("#172033")
MUTED = colors.HexColor("#566176")
GREEN = colors.HexColor("#DFF3E5")
YELLOW = colors.HexColor("#FFF1C7")
RED = colors.HexColor("#FADDDD")
UNMEASURED = colors.HexColor("#ECEFF4")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))


register_fonts()
styles = getSampleStyleSheet()

BODY = ParagraphStyle(
    "BodyVN",
    parent=styles["BodyText"],
    fontName="Arial",
    fontSize=8.1,
    leading=10.0,
    textColor=TEXT,
    spaceAfter=0,
)
SMALL = ParagraphStyle(
    "SmallVN",
    parent=BODY,
    fontSize=7.1,
    leading=8.5,
)
TINY = ParagraphStyle(
    "TinyVN",
    parent=BODY,
    fontSize=6.4,
    leading=7.5,
)
SECTION = ParagraphStyle(
    "SectionVN",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=10.0,
    leading=11.5,
    textColor=BLUE,
    spaceBefore=3,
    spaceAfter=3,
)
TITLE = ParagraphStyle(
    "TitleVN",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=17,
    leading=19,
    textColor=colors.white,
)
WHITE_SMALL = ParagraphStyle(
    "WhiteSmall",
    parent=SMALL,
    fontName="Arial-Bold",
    textColor=colors.white,
    alignment=TA_CENTER,
)
CARD_LABEL = ParagraphStyle(
    "CardLabel",
    parent=SMALL,
    fontName="Arial-Bold",
    textColor=MUTED,
    alignment=TA_CENTER,
)
CARD_VALUE = ParagraphStyle(
    "CardValue",
    parent=BODY,
    fontName="Arial-Bold",
    fontSize=9.5,
    leading=11,
    alignment=TA_CENTER,
)


def p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def header_row(labels: list[str]) -> list[Paragraph]:
    return [p(label, WHITE_SMALL) for label in labels]


def base_table_style(header=True, font_size=6.3) -> TableStyle:
    rules = [
        ("FONTNAME", (0, 0), (-1, -1), "Arial"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, MID),
    ]
    if header:
        rules.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, 0), 4),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
            ]
        )
    return TableStyle(rules)


def page_decor(canvas, doc) -> None:
    canvas.saveState()
    width, _ = landscape(A4)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, 7 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Arial", 6.5)
    canvas.drawString(12 * mm, 2.5 * mm, "Day 26 - AI Product Handbook | Trần Thị Kiều Trang - 2A202601498")
    canvas.drawRightString(width - 12 * mm, 2.5 * mm, f"Trang {doc.page}")
    canvas.restoreState()


def title_band(title: str, subtitle: str) -> Table:
    data = [[p(title, TITLE), p(subtitle, WHITE_SMALL)]]
    table = Table(data, colWidths=[180 * mm, 89 * mm], rowHeights=[16 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 5 * mm),
                ("RIGHTPADDING", (1, 0), (1, 0), 4 * mm),
            ]
        )
    )
    return table


def build_story() -> list:
    story = []
    story.append(
        title_band(
            "OPERATING DASHBOARD | AI TRAVEL PLANNER",
            "B2C | Cập nhật 2026-08-28<br/>Owner phiên họp: Founder/Product",
        )
    )
    story.append(Spacer(1, 2 * mm))

    diagnosis = (
        "<b>Chẩn đoán:</b> Cá nhân lập kế hoạch mua gói Pro và trực tiếp tạo, chốt, "
        "chia sẻ lịch trình trên web app/Zalo. Affiliate chỉ bổ trợ, không phải partner phân phối."
    )
    north_star = (
        "<b>NORTH STAR:</b> Mức giảm cohort retention D30-D60 | "
        "<b>Mục tiêu <= 5 điểm %</b> | Hiện tại: chưa có cohort | Trạng thái: CHƯA ĐO"
    )
    overview = Table(
        [[p(diagnosis, BODY)], [p(north_star, BODY)]],
        colWidths=[269 * mm],
    )
    overview.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("BACKGROUND", (0, 1), (-1, 1), PALE_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.5, MID),
                ("LINEBELOW", (0, 0), (-1, 0), 0.4, MID),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(overview)
    story.append(Spacer(1, 1.5 * mm))

    story.append(p("CÂY ĐÈN 3 TẦNG", SECTION))
    metric_data = [
        header_row(["Tầng/ID", "Metric - cách đo", "Hiện tại", "Xanh | Vàng | Đỏ", "Nguồn", "Downstream - Rule"]),
        [p("L | L-01", SMALL), p("Giảm retention D30-D60; retained khi làm/chỉnh itinerary đạt chuẩn", SMALL), p("CHƯA ĐO — chưa có cohort", SMALL), p("<=5 | >5-10 | >10 điểm %", SMALL), p("[TB] 2 cohort", SMALL), p("Paid retention 1-3 tháng, LTV 2-6 tháng - R-01", SMALL)],
        [p("L | L-02", SMALL), p("Activated 24h = itinerary đạt chuẩn + share / user mới hợp lệ", SMALL), p("CHƯA ĐO — chưa có event log", SMALL), p(">=66,7% | >=40% và <66,7% | <40%", SMALL), p("[TB] 4 cohort", SMALL), p("Retention D30 ~30 ngày, trial-to-paid ~30 ngày - R-02", SMALL)],
        [p("O | O-01", SMALL), p("Containment = completed không cần operator / job thử hợp lệ", SMALL), p("CHƯA ĐO (mô hình 70%, không tính màu)", SMALL), p(">=70% | >=33% và <70% | <33%", SMALL), p("[MH] MH-02", SMALL), p("AI cost/job, GM (1-4 tuần) - R-03", SMALL)],
        [p("O | O-02", SMALL), p("AI cost/job = LLM + data + infra + retry + QA / completed job", SMALL), p("CHƯA ĐO (mô hình 7.938đ, không tính màu)", SMALL), p("<=7.938 | 7.939-16.857 | >16.857đ", SMALL), p("[MH] MH-01", SMALL), p("Gross margin (2-8 tuần) - R-04", SMALL)],
        [p("O | O-03", SMALL), p("Trial-to-paid 30d = paid / free users đủ điều kiện thấy paywall", SMALL), p("CHƯA ĐO — chưa có paid cohort", SMALL), p(">=10% | >=5% và <10% | <5%", SMALL), p("[MH] MH-04", SMALL), p("Paid retention, payback (1-4 tháng) - R-02", SMALL)],
        [p("G | G-01", SMALL), p("GM gồm variable cost của cả free và paid jobs / Pro revenue", SMALL), p("CHƯA ĐO (mô hình 81,2%, chưa free mix)", SMALL), p(">=60% | >=50% và <60% | <50%", SMALL), p("[MH] MH-01", SMALL), p("Khả năng tiếp tục - R-05", SMALL)],
    ]
    metrics = Table(metric_data, colWidths=[15 * mm, 62 * mm, 48 * mm, 54 * mm, 24 * mm, 66 * mm], repeatRows=1)
    ts = base_table_style()
    ts.add("BACKGROUND", (0, 1), (-1, 2), colors.white)
    ts.add("BACKGROUND", (0, 3), (-1, 5), LIGHT)
    ts.add("BACKGROUND", (0, 6), (-1, 6), colors.HexColor("#EEF2F7"))
    ts.add("BACKGROUND", (2, 1), (2, 6), UNMEASURED)
    ts.add("TEXTCOLOR", (2, 1), (2, 6), MUTED)
    metrics.setStyle(ts)
    story.append(metrics)

    story.append(p("5 LUẬT QUYẾT ĐỊNH", SECTION))
    rule_data = [
        header_row(["ID", "Trigger - window - sample", "THÌ", "KHÔNG THÌ", "Dừng"]),
        [p("R-01", SMALL), p("D30-D60 giảm >10 điểm % | 2 cohort | >=30 activated/cohort", SMALL), p("Đóng băng acquisition 21 ngày; chạy 2 activation experiments", SMALL), p("Không tăng ads/referral để bù churn", SMALL), p("CÓ", SMALL)],
        [p("R-02", SMALL), p("Activation <40% hoặc conversion <5% | 2 cohort | >=20 user/cohort", SMALL), p("Dừng traffic 14 ngày; 1 template; test 8 user", SMALL), p("Không giảm giá trước aha moment", SMALL), p("CÓ", SMALL)],
        [p("R-03", SMALL), p("Containment <33% | 2 tuần | >=60 job thử", SMALL), p("Dừng mở segment 14 ngày; constrained template", SMALL), p("Không tăng retry/prompt/HITL để che failure", SMALL), p("CÓ", SMALL)],
        [p("R-04", SMALL), p("AI cost/job >16.857đ | 2 tuần | >=100 completed jobs", SMALL), p("Giới hạn context, model-route, khóa free usage vượt cap", SMALL), p("Không bỏ data/retry/QA khỏi cost", SMALL), p("KHÔNG", SMALL)],
        [p("R-05", SMALL), p("GM <50% | 2 tháng | >=100 jobs/tháng + 2 cost sprints", SMALL), p("Dừng mở ngách; đóng băng acquisition; thu hẹp cap", SMALL), p("Không tính affiliate chưa realized vào GM", SMALL), p("CÓ", SMALL)],
    ]
    rules = Table(rule_data, colWidths=[13 * mm, 75 * mm, 78 * mm, 83 * mm, 20 * mm], repeatRows=1)
    rs = base_table_style()
    rs.add("BACKGROUND", (0, 1), (-1, 1), colors.white)
    rs.add("BACKGROUND", (0, 2), (-1, 2), LIGHT)
    rs.add("BACKGROUND", (0, 3), (-1, 3), colors.white)
    rs.add("BACKGROUND", (0, 4), (-1, 4), LIGHT)
    rs.add("BACKGROUND", (0, 5), (-1, 5), colors.white)
    rs.add("BACKGROUND", (4, 1), (4, 3), RED)
    rs.add("BACKGROUND", (4, 5), (4, 5), RED)
    rules.setStyle(rs)
    story.append(rules)

    story.append(p("CỔNG 90 NGÀY", SECTION))
    gate_data = [
        header_row(["Ngày", "Một metric - ngưỡng", "Evidence vật lý", "Đạt", "Trượt"]),
        [p("30", SMALL), p("Pain-validation >=16/20 interview", SMALL), p("Interview notes redacted + consent + coding sheet", SMALL), p("GO", SMALL), p("FIX", SMALL)],
        [p("60", SMALL), p("Containment >=70% trên >=60 job thử", SMALL), p("Eval report + event/retry/QA log", SMALL), p("GO", SMALL), p("PIVOT", SMALL)],
        [p("90", SMALL), p("GM sau AI cost >=60% trên >=100 completed jobs", SMALL), p("Usage ledger + invoices + QA + billing allocation", SMALL), p("GO", SMALL), p("KILL", SMALL)],
    ]
    gates = Table(gate_data, colWidths=[17 * mm, 80 * mm, 116 * mm, 25 * mm, 31 * mm], repeatRows=1)
    gs = base_table_style()
    gs.add("BACKGROUND", (3, 1), (3, -1), GREEN)
    gs.add("BACKGROUND", (4, 1), (4, 1), YELLOW)
    gs.add("BACKGROUND", (4, 2), (4, 2), colors.HexColor("#FFE3C2"))
    gs.add("BACKGROUND", (4, 3), (4, 3), RED)
    gates.setStyle(gs)
    story.append(gates)
    story.append(Spacer(1, 1.5 * mm))
    note = Table(
        [
            [p("<b>KILL:</b> Ngày 2026-11-26 nếu GM sau AI cost vẫn &lt;60% trên >=100 completed jobs sau 2 cost-optimization sprints — cùng ngưỡng cổng ngày 90. R-05 vẫn cắt expansion sớm nếu GM &lt;50% trước ngày 90.", SMALL)],
            [p("<b>CHƯA ĐO:</b> Containment · Eval 100 case + job log · AI/Backend · 2026-09-15 | Token/Maps cost · usage ledger + invoice · FinOps · 2026-10-20<br/>Trial-to-paid/CAC · paywall/payment log · Growth Ops · 2026-11-26 | Retention plateau · event schema + cohort report · Product Analytics · 2026-12-15.", SMALL)],
        ],
        colWidths=[269 * mm],
    )
    note.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), RED),
                ("BACKGROUND", (0, 1), (0, 1), YELLOW),
                ("BOX", (0, 0), (-1, -1), 0.4, MID),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(note)

    story.append(PageBreak())
    story.append(title_band("PHỤ LỤC - NGƯỠNG VÀ EVIDENCE", "Worksheet đã PASS validator v2.0.0<br/>Không dùng benchmark [BM] bên ngoài"))
    story.append(Spacer(1, 2 * mm))

    story.append(p("PHÉP TÍNH SUY TỪ DAY 24-25", SECTION))
    mh_data = [
        header_row(["ID", "Metric", "Input", "Phép tính", "Áp dụng"]),
        [p("MH-01", SMALL), p("Trần AI cost/job cho GM 60%", SMALL), p("P=42.143đ/job; GM=60%; Base cost=7.938đ", SMALL), p("42.143 x (1-60%) = 16.857,2đ<br/>Buffer = 16.857,2 - 7.938 = 8.919,2đ", SMALL), p("O-02 đỏ >16.857đ; G-01 xanh >=60%", SMALL)],
        [p("MH-02", SMALL), p("Containment tối thiểu", SMALL), p("v=$0,179604; q=$0,031686; e=$0; P=$1,60239; GM=60%", SMALL), p("R=(0,179604+0,031686)/(1,60239 x 40%) = 0,32964 = 33,0%", SMALL), p("O-01 đỏ <33%; green target 70%", SMALL)],
        [p("MH-03", SMALL), p("Activation beta", SMALL), p("30 beta users; cần 20 activated interviews", SMALL), p("20 / 30 = 66,67%", SMALL), p("Giả thuyết mốc xanh tạm L-02; thẻ L-02 dùng [TB]", SMALL)],
        [p("MH-04", SMALL), p("Trial-to-paid ngày 90", SMALL), p("6.000 free; 600 paid theo Day 25", SMALL), p("600 / 6.000 = 10,0%", SMALL), p("O-03 xanh >=10%; đỏ <5% (<300 paid)", SMALL)],
    ]
    mh = Table(mh_data, colWidths=[17 * mm, 48 * mm, 69 * mm, 77 * mm, 58 * mm], repeatRows=1)
    ms = base_table_style()
    ms.add("BACKGROUND", (0, 1), (-1, 1), PALE_BLUE)
    ms.add("BACKGROUND", (0, 2), (-1, 2), LIGHT)
    ms.add("BACKGROUND", (0, 3), (-1, 3), PALE_BLUE)
    ms.add("BACKGROUND", (0, 4), (-1, 4), LIGHT)
    mh.setStyle(ms)
    story.append(mh)

    story.append(p("KHOẢNG TRỐNG DỮ LIỆU - KHÔNG TỰ NHẬN LÀ ACTUAL", SECTION))
    unknown_data = [
        header_row(["Khoảng trống", "Evidence cần có", "Owner", "Ngày có số"]),
        [p("Containment 70% chỉ là ước tính", SMALL), p("Eval 100 case + complete/escalate/fail log + QA 5%", SMALL), p("AI/Backend", SMALL), p("2026-09-15", SMALL)],
        [p("Activation và retention", SMALL), p("Signup/finalize/share/second-trip event + cohort report", SMALL), p("Product Analytics", SMALL), p("2026-12-15", SMALL)],
        [p("Token, retry, Maps/data, p95 cost", SMALL), p("Pseudonymous usage ledger + prompt version + invoices", SMALL), p("FinOps", SMALL), p("2026-10-20", SMALL)],
        [p("Conversion, refund, CAC PLG", SMALL), p("Paywall/checkout/payment/refund + acquisition attribution", SMALL), p("Growth Ops", SMALL), p("2026-11-26", SMALL)],
    ]
    unknowns = Table(unknown_data, colWidths=[60 * mm, 116 * mm, 50 * mm, 43 * mm], repeatRows=1)
    unknowns.setStyle(base_table_style())
    story.append(unknowns)

    story.append(p("NGUỒN NỘI BỘ VÀ TRACEABILITY", SECTION))
    source_data = [
        header_row(["Nguồn", "Evidence được dùng", "As-of"]),
        [p("2A202601498_TranThiKieuTrang_Day24.xlsx", SMALL), p("Assumptions D7/D12:D15/D18/D22; Unit Economics D11/D21/D22: ARPU 59.000đ, GM 71,19%, CAC 180.000đ, LTV/CAC 3,89x, payback 4,29 tháng", SMALL), p("2026-08-26", SMALL)],
        [p("TranThiKieuTrang_Day25_model.xlsx", SMALL), p("1_Cost_Job B5/B10/B66:B69; 2_Pricing B19/B21/B33; 3_Value_Metric B30:B34; 5_90Day_Plan B13:B25", SMALL), p("2026-08-27", SMALL)],
        [p("TranThiKieuTrang_Day25_onepager.pdf", SMALL), p("Đối chiếu product, job definition, Hybrid 708.000đ/năm, PLG, Cost/Job 7.938đ, GM 81,2%, evidence deadlines", SMALL), p("2026-08-27", SMALL)],
    ]
    sources = Table(source_data, colWidths=[75 * mm, 159 * mm, 35 * mm], repeatRows=1)
    sources.setStyle(base_table_style())
    story.append(sources)

    story.append(p("AI CRITIQUE ĐÃ ÁP DỤNG", SECTION))
    critique_data = [
        header_row(["Phản biện", "Quyết định và thay đổi", "Lý do"]),
        [p("Retention 'phẳng' chưa có định nghĩa số", SMALL), p("ACCEPT - dùng giảm D30-D60; current chưa có cohort; [TB] hai cohort", SMALL), p("Không biến khái niệm định tính thành actual giả", SMALL)],
        [p("Containment 70% và GM 81,2% là mô hình", SMALL), p("ACCEPT - CHƯA ĐO, không tính màu; gate 60 yêu cầu >=60 jobs", SMALL), p("Tách model output khỏi market evidence", SMALL)],
        [p("Luật dễ phản ứng với mẫu nhỏ và chỉ làm thêm", SMALL), p("ACCEPT - thêm numeric window/sample; 4 luật dừng", SMALL), p("Chống nhiễu và wrong reflex B2C", SMALL)],
    ]
    critique = Table(critique_data, colWidths=[80 * mm, 117 * mm, 72 * mm], repeatRows=1)
    critique.setStyle(base_table_style())
    story.append(critique)

    story.append(Spacer(1, 1.5 * mm))
    score = Table(
        [[p("<b>TỰ CHẤM THẬN TRỌNG: 94/100</b> - Tier 20 | Threshold 26 | Rules 28 | Gates 15 | Honesty 5", BODY),
          p("Điểm yếu lớn nhất: retention, conversion và free-tier cost chưa có actual cohort. PASS validator chỉ là minimum bar cấu trúc.", SMALL)]],
        colWidths=[116 * mm, 153 * mm],
    )
    score.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), PALE_BLUE), ("BACKGROUND", (1, 0), (1, 0), YELLOW), ("BOX", (0, 0), (-1, -1), 0.5, MID), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(score)
    return story


def build_pdf() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    submission_copy = ROOT / "submissions" / "2A202601498" / OUTPUT.name
    page_width, page_height = landscape(A4)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=9 * mm,
        bottomMargin=11 * mm,
        title="AI Travel Planner - Day 26 Operating Dashboard",
        author="Trần Thị Kiều Trang",
        subject="Day 26 Track 1 - AI Product Handbook",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        page_width - doc.leftMargin - doc.rightMargin,
        page_height - doc.topMargin - doc.bottomMargin,
        id="normal",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="dashboard", frames=[frame], onPage=page_decor)])
    doc.build(build_story())
    submission_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT, submission_copy)
    return OUTPUT


if __name__ == "__main__":
    result = build_pdf()
    print(result)
