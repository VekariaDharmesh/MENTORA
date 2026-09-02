-- ============================================================================
-- AI TEACHER — DATABASE SEED DATA
-- ============================================================================

-- Seed Concepts
INSERT INTO concepts (id, key, name, domain, difficulty_level, description) VALUES
('c0000001-0000-0000-0000-000000000001', 'electric_charge', 'Electric Charge', 'Physics', 'beginner', 'Coulomb''s Law, fundamental charge carriers, positive and negative charges.'),
('c0000001-0000-0000-0000-000000000002', 'electric_current', 'Electric Current', 'Physics', 'beginner', 'Rate of charge flow over time (I = Q / t). Measured in Amperes.'),
('c0000001-0000-0000-0000-000000000003', 'voltage', 'Voltage & Potential Difference', 'Physics', 'beginner', 'Work done per unit charge (ΔV = W / Q). Electric driving pressure.'),
('c0000001-0000-0000-0000-000000000004', 'resistance', 'Resistance & Impedance', 'Physics', 'intermediate', 'Opposition to current flow caused by atomic collisions. Measured in Ohms (Ω).'),
('c0000001-0000-0000-0000-000000000005', 'ohms_law', 'Ohm''s Law', 'Physics', 'intermediate', 'Fundamental relationship V = I * R linking voltage, current, and resistance.'),
('c0000001-0000-0000-0000-000000000006', 'circuit_analysis', 'Circuit Analysis & Kirchhoff''s Laws', 'Physics', 'advanced', 'Series and parallel topologies, current division, loop conservation.')
ON CONFLICT (key) DO NOTHING;

-- Seed Concept Prerequisites (Directed Edges)
INSERT INTO concept_prerequisites (concept_id, prerequisite_id) VALUES
('c0000001-0000-0000-0000-000000000002', 'c0000001-0000-0000-0000-000000000001'), -- Charge -> Current
('c0000001-0000-0000-0000-000000000003', 'c0000001-0000-0000-0000-000000000001'), -- Charge -> Voltage
('c0000001-0000-0000-0000-000000000004', 'c0000001-0000-0000-0000-000000000002'), -- Current -> Resistance
('c0000001-0000-0000-0000-000000000005', 'c0000001-0000-0000-0000-000000000003'), -- Voltage -> Ohm's Law
('c0000001-0000-0000-0000-000000000005', 'c0000001-0000-0000-0000-000000000002'), -- Current -> Ohm's Law
('c0000001-0000-0000-0000-000000000005', 'c0000001-0000-0000-0000-000000000004'), -- Resistance -> Ohm's Law
('c0000001-0000-0000-0000-000000000006', 'c0000001-0000-0000-0000-000000000005')  -- Ohm's Law -> Circuit Analysis
ON CONFLICT DO NOTHING;
