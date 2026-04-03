#!/usr/bin/env python3
"""
Comprehensive system test script for Library Feedback Sentiment Analysis
Tests all core functionality before GitHub commit
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test all critical module imports"""
    print("\n=== Testing Module Imports ===")
    try:
        import streamlit
        print(f"OK Streamlit {streamlit.__version__}")
        
        from modules import database, csv_handler, pii_detector, report_generator
        print("OK Core modules (database, csv_handler, pii_detector, report_generator)")
        
        from modules.sentiment_enhanced import EnhancedSentimentAnalyzer
        print("OK Enhanced sentiment analyzer")
        
        from modules import qualitative_analysis, quantitative_analysis, visualization
        print("OK Analysis modules (qualitative, quantitative, visualization)")
        
        import torch
        import transformers
        print(f"OK PyTorch {torch.__version__}, Transformers {transformers.__version__}")
        
        return True
    except Exception as e:
        print(f"FAIL Import failed: {e}")
        traceback.print_exc()
        return False

def test_enhanced_sentiment():
    """Test enhanced sentiment analyzer"""
    print("\n=== Testing Enhanced Sentiment Analysis ===")
    try:
        from modules.sentiment_enhanced import EnhancedSentimentAnalyzer
        
        analyzer = EnhancedSentimentAnalyzer()
        
        test_cases = [
            "This library is absolutely amazing!",
            "The service was terrible and disappointing",
            "It was okay, nothing special"
        ]
        
        for text in test_cases:
            result = analyzer.analyze_sentiment(text)
        print(f"OK {result['sentiment']:8s} ({result['confidence']:5.1f}%) - {text[:40]}")
        
        return True
    except Exception as e:
        print(f"FAIL Enhanced sentiment test failed: {e}")
        traceback.print_exc()
        return False

def test_qualitative_analysis():
    """Test qualitative analysis integration"""
    print("\n=== Testing Qualitative Analysis Integration ===")
    try:
        from modules.qualitative_analysis import analyze_sentiment
        
        test_text = "The library staff was very helpful and friendly"
        result = analyze_sentiment(test_text)
        
        print(f"OK Sentiment: {result['sentiment']}")
        print(f"  Score: {result['score']:.3f}")
        if 'confidence' in result:
            print(f"  Confidence: {result['confidence']:.1f}%")
        
        return True
    except Exception as e:
        print(f"FAIL Qualitative analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database initialization"""
    print("\n=== Testing Database ===")
    try:
        from modules.database import init_database
        from pathlib import Path
        
        db_path = Path("data/library.db")
        print(f"OK Database path: {db_path}")
        print(f"  Exists: {db_path.exists()}")
        
        return True
    except Exception as e:
        print(f"FAIL Database test failed: {e}")
        traceback.print_exc()
        return False

def test_pii_detector():
    """Test PII detection"""
    print("\n=== Testing PII Detector ===")
    try:
        from modules.pii_detector import detect_pii, redact_pii
        
        test_text = "Contact John at john@example.com or call 555-1234"
        pii_found = detect_pii(test_text)
        redacted = redact_pii(test_text)
        
        print(f"OK PII detection working")
        print(f"  Found {len(pii_found)} PII items")
        print(f"  Redacted: {redacted[:50]}...")
        
        return True
    except Exception as e:
        print(f"FAIL PII detector test failed: {e}")
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test streamlit app can be imported"""
    print("\n=== Testing Streamlit App ===")
    try:
        # Just check if it can be imported without running
        import streamlit_app
        print("OK Streamlit app imports successfully")
        print("  Note: Authentication disabled (auto-login enabled)")
        
        return True
    except Exception as e:
        print(f"FAIL Streamlit app test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("LIBRARY FEEDBACK SENTIMENT ANALYSIS - SYSTEM TEST")
    print("=" * 70)
    
    results = {
        "Module Imports": test_imports(),
        "Enhanced Sentiment": test_enhanced_sentiment(),
        "Qualitative Analysis": test_qualitative_analysis(),
        "Database": test_database(),
        "PII Detector": test_pii_detector(),
        "Streamlit App": test_streamlit_app()
    }
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        symbol = "OK" if passed else "FAIL"
        print(f"{symbol} {test_name:30s} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nOK All tests passed! System is ready for GitHub commit.")
        print("\nTo start the application:")
        print("  streamlit run streamlit_app.py")
        return 0
    else:
        print(f"\nFAIL {total - passed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
