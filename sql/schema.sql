
CREATE TABLE IF NOT EXISTS fund_master (
    amfi_code INTEGER,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE IF NOT EXISTS nav_history (
    amfi_code INTEGER,
    date TEXT,
    nav REAL
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    amfi_code INTEGER,
    scheme_name TEXT,
    cagr_pct REAL,
    sharpe_ratio REAL,
    beta REAL,
    var_95_pct REAL
);
