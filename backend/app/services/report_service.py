"""
Automated Forensic PDF Audit Dossier Generator.
Uses ReportLab to generate enterprise-grade compliance and safety reports.
"""
import io
from datetime import datetime, timezone
from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFReportService:
    def generate_audit_dossier(self, report_data: Dict[str, Any]) -> io.BytesIO:
        """
        Builds a multi-page PDF audit dossier in memory and returns BytesIO buffer.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=12
        )
        section_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=14,
            spaceAfter=8
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )
        callout_style = ParagraphStyle(
            "Callout",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#991b1b")
        )

        elements = []

        # Header Title
        elements.append(Paragraph("FORENSIC AUDIT DOSSIER", title_style))
        elements.append(Paragraph(
            f"AI-Powered Fake Review & Coordinated Network Detection Engine | "
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            subtitle_style
        ))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=15))

        # Confidentiality Alert Notice
        notice_data = [
            [Paragraph("<b>CONFIDENTIAL & ETHICAL SAFEGUARD NOTICE:</b> Indicators presented herein represent algorithmic anomaly signals for human trust & safety review. They do not constitute legal determinations of intentional fraud.", callout_style)]
        ]
        notice_table = Table(notice_data, colWidths=[540])
        notice_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef2f2")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#fca5a5")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(notice_table)
        elements.append(Spacer(1, 15))

        # 1. Executive Summary KPIs Table
        elements.append(Paragraph("1. Executive Threat Landscape & KPIs", section_style))
        
        kpis = [
            ["Metric", "Value", "Status / Interpretation"],
            ["Total Analyzed Reviews", str(report_data.get("total_reviews", 0)), "Full Platform Ingestion"],
            ["Suspicious Reviews Flagged", str(report_data.get("suspicious_reviews_count", 0)), f"{report_data.get('suspicious_reviews_percentage', 0)}% of total corpus"],
            ["Identified Collusion Clusters", str(report_data.get("detected_clusters_count", 0)), "Coordinated Ring Subgraphs"],
            ["Monitored Products", str(report_data.get("total_products", 0)), "Active Catalog SKUs"],
            ["Monitored Reviewer Accounts", str(report_data.get("total_reviewers", 0)), "Pseudonymized Reviewer Nodes"],
            ["Overall Catalog Trust Index", f"{report_data.get('average_trust_score', 100):.1f} / 100", "Composite Trust Health Score"]
        ]
        
        kpi_table = Table(kpis, colWidths=[180, 120, 240])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 15))

        # 2. Top Suspicious Reviews Table
        elements.append(Paragraph("2. High-Priority Flagged Reviews", section_style))
        suspicious_list = report_data.get("recent_suspicious_reviews", [])
        
        if suspicious_list:
            review_rows = [["ID", "Product SKU", "Rating", "Score", "Risk Tier", "Key Explainability Trigger"]]
            for r in suspicious_list[:10]:
                review_rows.append([
                    str(r.get("review_id", "N/A")),
                    str(r.get("product_sku", "N/A"))[:15],
                    f"{r.get('rating', 0.0):.1f} ★",
                    f"{r.get('composite_suspicion_score', 0):.1f}",
                    str(r.get("risk_tier", "HIGH")),
                    str(r.get("top_reason", "Anomalous Pattern Detected"))[:45]
                ])
            
            review_table = Table(review_rows, colWidths=[35, 95, 55, 50, 65, 240])
            review_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            elements.append(review_table)
        else:
            elements.append(Paragraph("No critical reviews currently exceeding the suspicion threshold.", body_style))
            
        elements.append(Spacer(1, 15))

        # 3. Actionable Recommendations for Human-in-the-Loop Team
        elements.append(Paragraph("3. Trust & Safety Analyst Recommendations", section_style))
        recs = [
            "1. <b>Manual Audit Verification</b>: Inspect all reviews tagged with 'High Duplicate Similarity' for template copy-paste rings.",
            "2. <b>Network Quarantine</b>: Temporarily dampen the rating weights of reviewers identified within high-density collusion clusters.",
            "3. <b>Buyer Verification Friction</b>: Enforce SMS or purchase verification steps before allowing reviews on high-risk product SKUs.",
            "4. <b>Preserve Anonymity</b>: Adhere to data privacy policies and do not publicize raw reviewer credentials during investigation."
        ]
        for rec in recs:
            elements.append(Paragraph(rec, body_style))
            elements.append(Spacer(1, 4))

        # Build document
        doc.build(elements)
        buffer.seek(0)
        return buffer


report_service = PDFReportService()
