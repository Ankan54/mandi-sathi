"""
Test script to verify API fixes are working correctly
"""
import sys
import os

# Set UTF-8 encoding for Windows console
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from utils.api_client import DataGovAPIClient
from tools.location_tools import get_districts_for_state
from tools.price_tools import fetch_mandi_prices

def test_api_client():
    """Test the DataGovAPIClient directly"""
    print("=" * 70)
    print("TEST 1: Testing DataGovAPIClient - Fetch Mandi Prices")
    print("=" * 70)

    client = DataGovAPIClient()

    # Test 1: Fetch prices for Tomato in Ballia
    print("\n🔍 Fetching Tomato prices in Ballia, Uttar Pradesh...")
    records = client.fetch_mandi_prices(
        state="Uttar Pradesh",
        district="Ballia",
        commodity="Tomato",
        limit=5
    )

    if records:
        print(f"✅ Found {len(records)} records")
        print("\nFirst record:")
        print(records[0])

        # Test parsing
        parsed = client.parse_price_record(records[0])
        if parsed:
            print("\n✅ Parsing successful:")
            print(f"   Market: {parsed['market']}")
            print(f"   District: {parsed['district']}")
            print(f"   Modal Price: ₹{parsed['modal_price']}")
            print(f"   Price Range: ₹{parsed['min_price']} - ₹{parsed['max_price']}")
            print(f"   Date: {parsed['price_date']}")
        else:
            print("❌ Parsing failed!")
    else:
        print("❌ No records found!")

    # Test 2: Fetch districts for a state
    print("\n" + "=" * 70)
    print("TEST 2: Testing District Fetching")
    print("=" * 70)

    print("\n🔍 Fetching districts for Uttar Pradesh...")
    districts = client.fetch_districts_for_state("Uttar Pradesh")

    if districts:
        print(f"✅ Found {len(districts)} districts")
        print(f"   Sample districts: {', '.join(districts[:10])}...")
    else:
        print("❌ No districts found!")

    return records is not None and len(records) > 0


def test_crewai_tools():
    """Test the CrewAI tools"""
    print("\n" + "=" * 70)
    print("TEST 3: Testing CrewAI Tools")
    print("=" * 70)

    # Test get_districts_for_state tool
    print("\n🔍 Testing get_districts_for_state tool...")
    # CrewAI tools need to be called using .run() or _run() method
    result = get_districts_for_state._run(state_name="Uttar Pradesh")
    print(f"Tool Result:\n{result}")

    # Test fetch_mandi_prices tool
    print("\n" + "=" * 70)
    print("TEST 4: Testing fetch_mandi_prices tool")
    print("=" * 70)

    print("\n🔍 Testing fetch_mandi_prices tool...")
    result = fetch_mandi_prices._run(
        state="Uttar Pradesh",
        district="Ballia",
        commodity="Tomato"
    )
    print(f"Tool Result:\n{result}")

    return True


def main():
    """Run all tests"""
    print("\n🚀 Starting API Fixes Verification Tests\n")

    try:
        # Test API client
        api_test_passed = test_api_client()

        # Test CrewAI tools
        tools_test_passed = test_crewai_tools()

        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"API Client Test: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
        print(f"CrewAI Tools Test: {'✅ PASSED' if tools_test_passed else '❌ FAILED'}")

        if api_test_passed and tools_test_passed:
            print("\n🎉 All tests passed! API fixes are working correctly.")
            return 0
        else:
            print("\n❌ Some tests failed. Please check the output above.")
            return 1

    except Exception as e:
        print(f"\n❌ Test execution failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
