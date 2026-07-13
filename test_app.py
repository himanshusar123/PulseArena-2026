import pytest
from app import get_mock_fan_response, calculate_eco_points, parse_incident_report

def test_get_mock_fan_response():
    # Test Accessibility keywords
    res_en = get_mock_fan_response("where is the wheelchair ramp?", "English")
    assert "Accessibility Support" in res_en
    assert "105" in res_en
    
    res_es = get_mock_fan_response("silla de ruedas ramp", "Spanish")
    assert "Soporte de Accesibilidad" in res_es
    
    res_fr = get_mock_fan_response("fauteuil roulant ramp", "French")
    assert "Assistance Accessibilité" in res_fr

    # Test Transit keywords
    res_transit = get_mock_fan_response("is there a shuttle bus or metro?", "English")
    assert "Transportation Guide" in res_transit
    assert "CO2" in res_transit

    # Test Eco keywords
    res_eco = get_mock_fan_response("how to earn eco points?", "English")
    assert "Sustainability Center" in res_eco
    
    # Test Gate navigation
    res_gate = get_mock_fan_response("which gate to section 110?", "English")
    assert "Navigation Assist" in res_gate

    # Test Default fallback
    res_default = get_mock_fan_response("hello there", "English")
    assert "Welcome to the" in res_default

def test_calculate_eco_points():
    # Test Active/Green journey modes
    pts, co2 = calculate_eco_points("Walking / Running", 10.0)
    assert pts == 25
    assert pytest.approx(co2) == 2.5
    
    pts, co2 = calculate_eco_points("Cycling", 5.0)
    assert pts == 11
    assert pytest.approx(co2) == 1.1

    pts, co2 = calculate_eco_points("Metro Train", 20.0)
    assert pts == 30
    assert pytest.approx(co2) == 3.0

    pts, co2 = calculate_eco_points("Shuttle Bus", 8.0)
    assert pts == 8
    assert pytest.approx(co2) == 0.8

    # Test carbon-neutral/negative modes
    pts, co2 = calculate_eco_points("Rideshare / Car", 15.0)
    assert pts == 0
    assert pytest.approx(co2) == 0.0

    # Test invalid transport mode fallback
    pts, co2 = calculate_eco_points("Helicopter", 10.0)
    assert pts == 0
    assert pytest.approx(co2) == 0.0

def test_parse_incident_report():
    # Test standard output parsing
    summary, severity = parse_incident_report("Summary: Leak in restroom | Severity: Low | Response: Dispatch plumber")
    assert summary == "Leak in restroom"
    assert severity == "Low"

    # Test with different casing and spacing
    summary, severity = parse_incident_report("  Summary: Fight at gate A   |   Severity: High   |   Response: Dispatch security ")
    assert summary == "Fight at gate A"
    assert severity == "High"

    # Test invalid severity fallback
    summary, severity = parse_incident_report("Summary: Lost ticket | Severity: None | Response: Help desk")
    assert summary == "Lost ticket"
    assert severity == "Medium"

    # Test malformed input fallback
    summary, severity = parse_incident_report("This is a random response without separator")
    assert summary == "This is a random response without separator"
    assert severity == "Medium"

    # Test empty input fallback
    summary, severity = parse_incident_report("")
    assert summary == ""
    assert severity == "Medium"
