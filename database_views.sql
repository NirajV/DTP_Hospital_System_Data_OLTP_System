-- View: Active Doctors with Department Info
CREATE OR REPLACE VIEW vw_active_doctors AS
SELECT 
    d.doctor_id,
    d.employee_id,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    d.specialization,
    d.sub_specialization,
    d.phone,
    d.email,
    d.license_number,
    d.npi_number,
    dept.department_name,
    dept.location AS department_location,
    d.consultation_fee
FROM doctors d
LEFT JOIN departments dept ON d.department_id = dept.department_id
WHERE d.status = 'active';

-- View: Patient Summary with Latest Visit
CREATE OR REPLACE VIEW vw_patient_summary AS
SELECT 
    p.patient_id,
    p.mrn,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.date_of_birth,
    YEAR(CURDATE()) - YEAR(p.date_of_birth) AS age,
    p.gender,
    p.phone,
    p.email,
    p.blood_group,
    p.status,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    MAX(e.encounter_date) AS last_visit_date,
    COUNT(DISTINCT a.appointment_id) AS total_appointments
FROM patients p
LEFT JOIN encounters e ON p.patient_id = e.patient_id
LEFT JOIN appointments a ON p.patient_id = a.patient_id
WHERE p.status = 'active'
GROUP BY p.patient_id, p.mrn, p.first_name, p.last_name, p.date_of_birth, 
         p.gender, p.phone, p.email, p.blood_group, p.status;

-- View: Upcoming Appointments
CREATE OR REPLACE VIEW vw_upcoming_appointments AS
SELECT 
    a.appointment_id,
    a.appointment_number,
    a.appointment_date,
    a.appointment_time,
    a.duration_minutes,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    p.phone AS patient_phone,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    d.specialization,
    dept.department_name,
    r.room_number,
    at.type_name AS appointment_type,
    a.status,
    a.priority,
    a.reason
FROM appointments a
INNER JOIN patients p ON a.patient_id = p.patient_id
INNER JOIN doctors d ON a.doctor_id = d.doctor_id
LEFT JOIN departments dept ON d.department_id = dept.department_id
LEFT JOIN rooms r ON a.room_id = r.room_id
LEFT JOIN appointment_types at ON a.appointment_type_id = at.type_id
WHERE a.appointment_date >= CURDATE() 
  AND a.status IN ('scheduled', 'confirmed')
ORDER BY a.appointment_date, a.appointment_time;

-- View: Today's Appointments
CREATE OR REPLACE VIEW vw_todays_appointments AS
SELECT 
    a.appointment_id,
    a.appointment_time,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    p.phone AS patient_phone,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    dept.department_name,
    r.room_number,
    a.status,
    a.chief_complaint
FROM appointments a
INNER JOIN patients p ON a.patient_id = p.patient_id
INNER JOIN doctors d ON a.doctor_id = d.doctor_id
LEFT JOIN departments dept ON d.department_id = dept.department_id
LEFT JOIN rooms r ON a.room_id = r.room_id
WHERE a.appointment_date = CURDATE()
ORDER BY a.appointment_time;

-- View: Active Encounters
CREATE OR REPLACE VIEW vw_active_encounters AS
SELECT 
    e.encounter_id,
    e.encounter_number,
    e.encounter_date,
    e.encounter_type,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    dept.department_name,
    r.room_number,
    b.bed_number,
    e.chief_complaint,
    e.status,
    DATEDIFF(CURDATE(), DATE(e.encounter_date)) AS days_in_facility
FROM encounters e
INNER JOIN patients p ON e.patient_id = p.patient_id
INNER JOIN doctors d ON e.doctor_id = d.doctor_id
LEFT JOIN departments dept ON e.department_id = dept.department_id
LEFT JOIN rooms r ON e.room_id = r.room_id
LEFT JOIN beds b ON e.bed_id = b.bed_id
WHERE e.status IN ('scheduled', 'in_progress')
ORDER BY e.encounter_date DESC;

-- View: Outstanding Invoices
CREATE OR REPLACE VIEW vw_outstanding_invoices AS
SELECT 
    i.invoice_id,
    i.invoice_number,
    i.invoice_date,
    i.due_date,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    p.phone AS patient_phone,
    p.email AS patient_email,
    i.total_amount,
    i.amount_paid,
    i.amount_due,
    i.insurance_paid,
    i.patient_responsibility,
    i.payment_status,
    DATEDIFF(CURDATE(), i.due_date) AS days_overdue,
    CASE 
        WHEN DATEDIFF(CURDATE(), i.due_date) > 90 THEN 'Critical'
        WHEN DATEDIFF(CURDATE(), i.due_date) > 60 THEN 'Severe'
        WHEN DATEDIFF(CURDATE(), i.due_date) > 30 THEN 'Warning'
        ELSE 'Current'
    END AS aging_status
FROM invoices i
INNER JOIN patients p ON i.patient_id = p.patient_id
WHERE i.payment_status IN ('pending', 'partial', 'overdue')
  AND i.amount_due > 0
ORDER BY i.due_date;

-- View: Pending Lab Orders
CREATE OR REPLACE VIEW vw_pending_lab_orders AS
SELECT 
    lo.order_id,
    lo.order_number,
    lo.order_datetime,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    CONCAT(d.first_name, ' ', d.last_name) AS ordering_doctor,
    lo.priority,
    lo.status,
    COUNT(lt.test_id) AS total_tests,
    e.encounter_number
FROM lab_orders lo
INNER JOIN patients p ON lo.patient_id = p.patient_id
INNER JOIN doctors d ON lo.ordering_doctor_id = d.doctor_id
INNER JOIN encounters e ON lo.encounter_id = e.encounter_id
LEFT JOIN lab_tests lt ON lo.order_id = lt.order_id
WHERE lo.status IN ('ordered', 'collected', 'in_progress')
GROUP BY lo.order_id, lo.order_number, lo.order_datetime, p.first_name, p.last_name,
         p.mrn, d.first_name, d.last_name, lo.priority, lo.status, e.encounter_number
ORDER BY lo.priority DESC, lo.order_datetime;

-- View: Pending Radiology Orders
CREATE OR REPLACE VIEW vw_pending_radiology_orders AS
SELECT 
    ro.order_id,
    ro.order_number,
    ro.order_datetime,
    ro.scheduled_datetime,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    CONCAT(d.first_name, ' ', d.last_name) AS ordering_doctor,
    ro.exam_type,
    ro.body_part,
    ro.modality,
    ro.priority,
    ro.status,
    e.encounter_number
FROM radiology_orders ro
INNER JOIN patients p ON ro.patient_id = p.patient_id
INNER JOIN doctors d ON ro.ordering_doctor_id = d.doctor_id
INNER JOIN encounters e ON ro.encounter_id = e.encounter_id
WHERE ro.status IN ('ordered', 'scheduled', 'in_progress')
ORDER BY ro.priority DESC, ro.scheduled_datetime;

-- View: Active Prescriptions by Patient
CREATE OR REPLACE VIEW vw_active_prescriptions AS
SELECT 
    pr.prescription_id,
    pr.prescription_number,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    m.medication_name,
    m.generic_name,
    pr.dosage,
    pr.frequency,
    pr.route,
    pr.start_date,
    pr.end_date,
    pr.refills_remaining,
    pr.status
FROM prescriptions pr
INNER JOIN patients p ON pr.patient_id = p.patient_id
INNER JOIN doctors d ON pr.doctor_id = d.doctor_id
INNER JOIN medications m ON pr.medication_id = m.medication_id
WHERE pr.status = 'active'
  AND (pr.end_date IS NULL OR pr.end_date >= CURDATE())
ORDER BY p.last_name, p.first_name, pr.start_date DESC;

-- View: Available Beds
CREATE OR REPLACE VIEW vw_available_beds AS
SELECT 
    b.bed_id,
    b.bed_number,
    b.bed_type,
    r.room_number,
    r.room_type,
    r.floor_number,
    f.facility_name,
    dept.department_name,
    b.status,
    b.is_occupied
FROM beds b
INNER JOIN rooms r ON b.room_id = r.room_id
INNER JOIN facilities f ON r.facility_id = f.facility_id
LEFT JOIN departments dept ON r.department_id = dept.department_id
WHERE b.status = 'available' 
  AND b.is_occupied = FALSE
  AND r.status = 'available'
ORDER BY f.facility_name, r.floor_number, r.room_number, b.bed_number;

-- View: Current Bed Occupancy
CREATE OR REPLACE VIEW vw_bed_occupancy AS
SELECT 
    ba.assignment_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    r.room_number,
    b.bed_number,
    b.bed_type,
    dept.department_name,
    ba.assignment_datetime,
    DATEDIFF(CURDATE(), DATE(ba.assignment_datetime)) AS days_occupied,
    CONCAT(n.first_name, ' ', n.last_name) AS assigned_nurse,
    CONCAT(d.first_name, ' ', d.last_name) AS attending_doctor
FROM bed_assignments ba
INNER JOIN patients p ON ba.patient_id = p.patient_id
INNER JOIN beds b ON ba.bed_id = b.bed_id
INNER JOIN rooms r ON b.room_id = r.room_id
LEFT JOIN departments dept ON r.department_id = dept.department_id
LEFT JOIN encounters e ON ba.encounter_id = e.encounter_id
LEFT JOIN doctors d ON e.doctor_id = d.doctor_id
LEFT JOIN nurse_assignments na ON p.patient_id = na.patient_id AND na.end_date IS NULL
LEFT JOIN nurses n ON na.nurse_id = n.nurse_id
WHERE ba.status = 'active'
ORDER BY dept.department_name, r.room_number, b.bed_number;

-- View: Medication Inventory Low Stock Alert
CREATE OR REPLACE VIEW vw_low_stock_medications AS
SELECT 
    m.medication_id,
    m.medication_name,
    m.generic_name,
    m.drug_class,
    mi.quantity_on_hand,
    mi.reorder_level,
    mi.location,
    mi.expiration_date,
    DATEDIFF(mi.expiration_date, CURDATE()) AS days_to_expiry,
    mi.status
FROM medication_inventory mi
INNER JOIN medications m ON mi.medication_id = m.medication_id
WHERE mi.quantity_on_hand <= mi.reorder_level
   OR DATEDIFF(mi.expiration_date, CURDATE()) <= 90
ORDER BY mi.quantity_on_hand, mi.expiration_date;

-- View: Insurance Claims Summary
CREATE OR REPLACE VIEW vw_insurance_claims_summary AS
SELECT 
    ic.claim_id,
    ic.claim_number,
    ic.claim_date,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    p.mrn,
    ins_comp.company_name AS insurance_company,
    ins_plan.plan_name AS insurance_plan,
    ic.total_charge,
    ic.allowed_amount,
    ic.paid_amount,
    ic.patient_responsibility,
    ic.status,
    ic.submission_date,
    ic.adjudication_date,
    DATEDIFF(CURDATE(), ic.submission_date) AS days_pending
FROM insurance_claims ic
INNER JOIN patients p ON ic.patient_id = p.patient_id
INNER JOIN patient_insurance_policies pip ON ic.policy_id = pip.policy_id
INNER JOIN insurance_plans ins_plan ON pip.insurance_plan_id = ins_plan.plan_id
INNER JOIN insurance_companies ins_comp ON ins_plan.insurance_company_id = ins_comp.insurance_company_id
ORDER BY ic.claim_date DESC;

-- View: Doctor Performance Metrics
CREATE OR REPLACE VIEW vw_doctor_performance AS
SELECT 
    d.doctor_id,
    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
    d.specialization,
    dept.department_name,
    COUNT(DISTINCT a.appointment_id) AS total_appointments,
    COUNT(DISTINCT CASE WHEN a.status = 'completed' THEN a.appointment_id END) AS completed_appointments,
    COUNT(DISTINCT CASE WHEN a.status = 'no_show' THEN a.appointment_id END) AS no_show_count,
    COUNT(DISTINCT e.encounter_id) AS total_encounters,
    AVG(a.duration_minutes) AS avg_appointment_duration,
    COUNT(DISTINCT pr.prescription_id) AS total_prescriptions
FROM doctors d
LEFT JOIN departments dept ON d.department_id = dept.department_id
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id 
    AND a.appointment_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
LEFT JOIN encounters e ON d.doctor_id = e.doctor_id 
    AND e.encounter_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
LEFT JOIN prescriptions pr ON d.doctor_id = pr.doctor_id 
    AND pr.prescription_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
WHERE d.status = 'active'
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization, dept.department_name;

-- View: Department Statistics
CREATE OR REPLACE VIEW vw_department_statistics AS
SELECT 
    dept.department_id,
    dept.department_name,
    dept.location,
    COUNT(DISTINCT d.doctor_id) AS total_doctors,
    COUNT(DISTINCT n.nurse_id) AS total_nurses,
    COUNT(DISTINCT s.staff_id) AS total_staff,
    COUNT(DISTINCT r.room_id) AS total_rooms,
    COUNT(DISTINCT b.bed_id) AS total_beds,
    COUNT(DISTINCT CASE WHEN b.is_occupied = TRUE THEN b.bed_id END) AS occupied_beds,
    COUNT(DISTINCT e.equipment_id) AS total_equipment
FROM departments dept
LEFT JOIN doctors d ON dept.department_id = d.department_id AND d.status = 'active'
LEFT JOIN nurses n ON dept.department_id = n.department_id AND n.status = 'active'
LEFT JOIN staff s ON dept.department_id = s.department_id AND s.status = 'active'
LEFT JOIN rooms r ON dept.department_id = r.department_id
LEFT JOIN beds b ON r.room_id = b.room_id
LEFT JOIN department_equipment de ON dept.department_id = de.department_id AND de.return_date IS NULL
LEFT JOIN equipment e ON de.equipment_id = e.equipment_id
WHERE dept.status = 'active'
GROUP BY dept.department_id, dept.department_name, dept.location;

-- =====================================================
-- NOTE: SAMPLE DATA (DML) MOVED TO SEPARATE FILE
-- =====================================================
--
-- All INSERT statements for sample data have been moved to:
--   hospital_sample_data.sql
--
-- This keeps the schema (DDL) separate from data (DML) for better
-- organization and maintenance.
--
-- To load sample data, run:
--   mysql -u root -p hospital_OLTP_system < hospital_sample_data.sql
--
-- =====================================================
