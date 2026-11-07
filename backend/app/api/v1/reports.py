"""
PDF Audit Dossier Export and Human-in-the-Loop Audit Endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.models.audit import AuditLog
from app.models.review import Review
from app.models.analysis import ReviewAnalysis
from app.models.cluster import CollusionCluster
from app.schemas.report import AuditActionRequest
from app.api.v1.dashboard import get_dashboard_metrics
from app.services.report_service import report_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports & Auditing"])


@router.get("/pdf")
def download_pdf_report(db: Session = Depends(get_db)):
    """Generates and streams an enterprise-grade forensic PDF report."""
    metrics = get_dashboard_metrics(db)
    
    # Generate PDF in memory buffer
    pdf_buffer = report_service.generate_audit_dossier(metrics)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=Forensic_Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        }
    )


@router.post("/audit-action", status_code=status.HTTP_201_CREATED)
def record_audit_action(
    action: AuditActionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Records a human analyst's decision (e.g. dismissing a false positive
    or confirming a coordinated collusion ring).
    """
    log_entry = AuditLog(
        user_id=current_user.id,
        action_type=action.action_type,
        target_entity=action.target_entity,
        target_id=action.target_id,
        notes=action.notes,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(log_entry)

    # If action is against a review, we can update or record notes
    if action.target_entity.upper() == "REVIEW" and action.action_type.upper() == "DISMISSED_FLAG":
        analysis = db.query(ReviewAnalysis).filter(ReviewAnalysis.review_id == action.target_id).first()
        if analysis:
            analysis.risk_tier = "AUDITED_DISMISSED"
            analysis.composite_suspicion_score = 0.0

    # If action is against a cluster
    if action.target_entity.upper() == "CLUSTER":
        cluster = db.query(CollusionCluster).filter(CollusionCluster.id == action.target_id).first()
        if cluster:
            cluster.status = action.action_type.upper()

    db.commit()
    return {"message": "Audit action successfully recorded", "action_id": log_entry.id}


@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Lists audit action history for compliance tracking."""
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [
        {
            "id": l.id,
            "analyst": l.user.full_name if l.user else "System",
            "action_type": l.action_type,
            "target_entity": l.target_entity,
            "target_id": l.target_id,
            "notes": l.notes,
            "timestamp": l.timestamp
        }
        for l in logs
    ]
