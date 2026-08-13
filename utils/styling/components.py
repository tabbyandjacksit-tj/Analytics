# =============================================================================
# IMPORTS
# =============================================================================
from __future__ import annotations

import streamlit as st

from utils.styling.base import apply_extra_css


# =============================================================================
# SHARED COMPONENT STYLES
# =============================================================================
def apply_component_styles() -> None:
    """Apply reusable component styles across the application."""

    apply_extra_css(
        """
/* ==========================================================================
   STANDARD HERO
   ========================================================================== */

.tj-hero {
    background-color: #1D5A3E;
    border-radius: 26px;
    box-shadow: 0 8px 22px rgba(29, 90, 62, 0.18);
    margin-bottom: 28px;
    padding: 28px;
}

.tj-hero h1 {
    color: #FFF9EF;
    font-size: 44px;
    font-weight: 800;
    margin: 0;
    text-align: center;
}

.tj-hero p {
    color: rgba(255, 249, 239, 0.88);
    font-size: 17px;
    margin: 12px 0 0;
    text-align: center;
}


/* ==========================================================================
   FILE UPLOADER
   ========================================================================== */

/* ==========================================================================
   FILE UPLOADER
   ========================================================================== */

[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFDF8 !important;
    border: 1px dashed #D7C8A4 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #1D5A3E !important;
    color: #FFFFFF !important;
    border: 1px solid #1D5A3E !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #174A33 !important;
    color: #FFFFFF !important;
    border-color: #174A33 !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #FFFFFF !important;
}


/* ==========================================================================
   SECTION HEADERS
   ========================================================================== */

.tj-section-header {
    margin-bottom: 20px;
}

.tj-section-label {
    color: #C97822;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 4px;
    text-transform: uppercase;
}

.tj-section-title {
    color: #1D5A3E;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.2;
    margin: 0;
}

.tj-section-subtitle {
    color: #5C7A58;
    font-size: 16px;
    line-height: 1.5;
    margin-top: 5px;
}


/* ==========================================================================
   SMALL SECTION HEADERS
   ========================================================================== */

.tj-subsection-title {
    color: #1D5A3E;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.3;
    margin: 0;
}

.tj-subsection-subtitle {
    color: #5C7A58;
    font-size: 15px;
    line-height: 1.5;
    margin-top: 5px;
}


/* ==========================================================================
   INFORMATION CARDS
   ========================================================================== */

.tj-info-card {
    background-color: #FFF9EF;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    box-shadow: 0 3px 10px rgba(47, 55, 45, 0.04);
    padding: 20px 22px;
}

.tj-card-label {
    color: #C97822;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.tj-card-title {
    color: #1D5A3E;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.3;
}

.tj-card-description {
    color: #5C7A58;
    font-size: 15px;
    line-height: 1.55;
    margin-top: 7px;
}


/* ==========================================================================
   METRIC CARDS
   ========================================================================== */

.tj-metric-card {
    background-color: #FFFDF8;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    box-shadow: 0 3px 10px rgba(47, 55, 45, 0.04);
    min-height: 130px;
    padding: 19px 20px;
}

.tj-metric-label {
    color: #5C7A58;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.tj-metric-value {
    color: #1D5A3E;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.15;
    margin: 10px 0 5px;
}

.tj-metric-description {
    color: #5C7A58;
    font-size: 13px;
    line-height: 1.45;
}


/* ==========================================================================
   EMPTY STATES
   ========================================================================== */

.tj-empty-card {
    background-color: #FFFDF8;
    border: 1px dashed #D7C8A4;
    border-radius: 22px;
    padding: 38px 24px;
    text-align: center;
}

.tj-empty-icon {
    font-size: 34px;
    margin-bottom: 9px;
}

.tj-empty-title {
    color: #1D5A3E;
    font-size: 19px;
    font-weight: 800;
}

.tj-empty-description {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.5;
    margin: 6px auto 0;
    max-width: 440px;
}


/* ==========================================================================
   NOTE CARDS
   ========================================================================== */

.tj-note-card {
    background-color: #FDF7EA;
    border: 1px solid #D7C8A4;
    border-radius: 18px;
    box-shadow: 0 3px 10px rgba(47, 55, 45, 0.04);
    padding: 18px 20px;
}

.tj-note-title {
    color: #1D5A3E;
    font-size: 17px;
    font-weight: 800;
}

.tj-note-text {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.55;
    margin-top: 5px;
}


/* ==========================================================================
   UPLOAD + DATE HELPER
   ========================================================================== */

.tj-helper-label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
}

.tj-date-result {
    margin-top: 2px;
    font-size: 13px;
    line-height: 1.2;
}

.tj-date-result-label {
    color: #C97822;
    font-weight: 600;
}

.tj-date-result-value {
    color: #1D5A3E;
    font-weight: 600;
}


/*  ==========================================================================
   REPORT DOWNLOAD HELPER
   ========================================================================== */

.upload-report-instructions {
    background-color: #FFFDF8;
    border: 1px solid #D7C8A4;
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 6px;
    margin-bottom: 10px;
}

.upload-report-row {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 22px;
}

.upload-report-section {
    min-width: 0;
}

.upload-report-label {
    color: #1D5A3E;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 5px;
}

.upload-report-description {
    color: #5C7A58;
    font-size: 14px;
    line-height: 1.45;
}

.upload-report-dates {
    color: #1D5A3E;
    font-size: 14px;
    margin-top: 8px;
}

.upload-report-arrow {
    color: #C97822;
    font-weight: 800;
    padding: 0 8px;
}

.upload-report-divider {
    width: 1px;
    height: 58px;
    background-color: #D7C8A4;
}


/* Report link button */

div[data-testid="stLinkButton"] a {
    background-color: #FFFDF8 !important;
    color: #1D5A3E !important;
    border: 1px solid #1D5A3E !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

div[data-testid="stLinkButton"] a:hover {
    background-color: #F6F1E5 !important;
    color: #174A33 !important;
    border-color: #174A33 !important;
}

div[data-testid="stLinkButton"] a * {
    color: inherit !important;
}


/* ==========================================================================
   RESPONSIVE STYLES
   ========================================================================== */

@media (max-width: 750px) {
    .upload-report-row {
        grid-template-columns: 1fr;
        gap: 14px;
    }

    .upload-report-divider {
        width: 100%;
        height: 1px;
    }

    .tj-hero h1 {
        font-size: 34px;
    }

    .tj-section-title {
        font-size: 26px;
    }

    .tj-metric-card {
        min-height: auto;
    }
}
"""
    )


# =============================================================================
# INSTRUCTION CARD STYLES
# =============================================================================
def apply_instruction_styles() -> None:
    """Apply styling for reusable instruction cards."""

    st.markdown(
        """
        <style>

        /* =========================================================
           INSTRUCTION CARD
           ========================================================= */

        .instruction-card {
            position: relative;

            background: #FFFCF7;
            border: 1px solid rgba(29, 90, 62, 0.10);
            border-radius: 18px;

            padding: 22px 22px 24px 22px;

            min-height: 220px;
            height: auto;

            display: flex;
            flex-direction: column;
            align-items: center;

            box-shadow:
                0 4px 12px rgba(29, 90, 62, 0.05),
                0 1px 3px rgba(29, 90, 62, 0.04);

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }


        /* =========================================================
           INSTRUCTION GRID
           ========================================================= */

        .instruction-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
            width: 100%;
        }


        /* Medium screens */
        @media (max-width: 900px) {
            .instruction-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }


        /* Small screens */
        @media (max-width: 600px) {
            .instruction-grid {
                grid-template-columns: 1fr;
            }
        }


        /* =========================================================
           HOVER
           ========================================================= */

        .instruction-card:hover {
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px rgba(29, 90, 62, 0.09),
                0 2px 5px rgba(29, 90, 62, 0.05);
        }


        /* =========================================================
           STEP NUMBER
           ========================================================= */

        .instruction-number {
            width: 34px;
            height: 34px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #E58C2F;
            color: white;

            border-radius: 50%;

            font-size: 13px;
            font-weight: 700;

            margin-bottom: 16px;

            flex-shrink: 0;
        }


        /* =========================================================
           IMAGE AREA
           ========================================================= */

        .instruction-image-wrapper {
            height: 82px;
            width: 100%;

            display: flex;
            align-items: center;
            justify-content: center;

            margin-bottom: 14px;
        }


        .instruction-image {
            max-width: 72px;
            max-height: 72px;

            width: auto;
            height: auto;

            object-fit: contain;
        }


        /* =========================================================
           TITLE
           ========================================================= */

        .instruction-title {
            color: #1D5A3E;

            font-size: 16px;
            font-weight: 750;
            line-height: 1.25;

            text-align: center;

            margin-bottom: 8px;
        }


        /* =========================================================
           DESCRIPTION
           ========================================================= */

        .instruction-description {
            color: #56645B;

            font-size: 13px;
            line-height: 1.45;

            text-align: center;

            max-width: 240px;

            margin: 0 auto;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )