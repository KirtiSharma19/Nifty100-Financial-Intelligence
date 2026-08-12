from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# --------------------------------------------------
# PROJECT DIRECTORIES
# --------------------------------------------------

REPORTS_DIR = Path("reports")
OUTPUT_DIR = Path("output")


# --------------------------------------------------
# DOCUMENT CATALOG
# --------------------------------------------------

DOCUMENTS = {
    "elbow_plot": REPORTS_DIR / "elbow_plot.png",
    "correlation_heatmap": REPORTS_DIR / "correlation_heatmap.png",
    "cluster_profiles": OUTPUT_DIR / "cluster_profiles.csv",
    "cluster_labels": OUTPUT_DIR / "cluster_labels.csv",
    "cluster_analysis": OUTPUT_DIR / "cluster_analysis.csv",
    "outlier_report": OUTPUT_DIR / "outlier_report.csv",
    "portfolio_stats": OUTPUT_DIR / "portfolio_stats.csv",
    "cagr_report": Path("exports/cagr_report.csv"),
    "sector_report": Path("exports/sector_report.csv"),
}


# --------------------------------------------------
# LIST AVAILABLE DOCUMENTS
# --------------------------------------------------


@router.get("")
def list_documents():
    """
    Return all generated project documents/reports
    and their availability status.
    """

    documents = []

    for document_name, path in DOCUMENTS.items():

        documents.append(
            {
                "name": document_name,
                "filename": path.name,
                "path": str(path),
                "available": path.exists(),
                "size_bytes": (path.stat().st_size if path.exists() else None),
            }
        )

    return {
        "count": len(documents),
        "documents": documents,
    }


# --------------------------------------------------
# GET ONE DOCUMENT
# --------------------------------------------------


@router.get("/{document_name}")
def get_document(document_name: str):
    """
    Download one generated document/report.
    """

    document_name = document_name.lower().strip()

    if document_name not in DOCUMENTS:
        raise HTTPException(
            status_code=404, detail=f"Document '{document_name}' not found"
        )

    path = DOCUMENTS[document_name]

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=(f"Document '{document_name}' " "has not been generated yet"),
        )

    return FileResponse(
        path=str(path),
        filename=path.name,
    )
