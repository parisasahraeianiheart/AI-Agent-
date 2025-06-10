from graph.orchestration import graph
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    inputs = {"query": "Investigate Ali Khaledi Nasab’s professional background and possible risk indicators"}
    print("🧠 Running OSINT pipeline...\n")
    final_state = graph.invoke(inputs)
    print("\n✅ Graph completed! Final state keys:\n")

    print("\n🧾 Final State:")
    for key, value in final_state.items():
        if key == "final_report":
            print(f"\n📄 Report:\n{value[:1000]}...\n")
        else:
            print(f"{key}: {type(value)}")