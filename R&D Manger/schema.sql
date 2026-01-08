DROP TABLE IF EXISTS journals;

CREATE TABLE journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Basic Details
    journal_status TEXT,
    department TEXT,
    author_position TEXT,
    author_name TEXT,
    collaborative_authors TEXT,
    
    -- Paper Details
    paper_title TEXT,
    publisher TEXT,
    journal_name TEXT,
    journal_scope TEXT, -- National / International
    vol_issue_page TEXT,
    month_year TEXT,
    issn_number TEXT,
    
    -- Indexing & Metrics
    is_scopus INTEGER DEFAULT 0,
    is_sci_scie_ssci INTEGER DEFAULT 0,
    is_wos INTEGER DEFAULT 0,
    impact_factor REAL,
    citation_score REAL,
    sjr_rating TEXT,      -- SJR with Q1 to Q4
    h_index REAL,
    anna_univ_list TEXT,  -- Yes/No or specific list name
    
    -- Links
    preview_link TEXT,    -- Scopus/WoS Preview Link
    home_page_link TEXT,
    doi_link TEXT,
    
    -- Collaboration Details
    collab_scope TEXT,    -- National / International
    collab_institution TEXT, -- Institution / Industry / Agencies
    
    proof_filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);