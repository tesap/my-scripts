# main.py
from graph import graph
import json

def run_agent_system(query: str):
    initial_state = {
        "query": query,
        "balancer_choice": -1,
        "search_values": [],
        "thought_text": "",
    }
    
    print(f"🧠 Запрос: {query}")
    print("=" * 50)
    
    # Запуск графа
    final_state = None
    for step, state in enumerate(graph.stream(initial_state)):
        node_name = list(state.keys())[0]
        print(f"🔹 Шаг {step+1}: {node_name}")
        
        # if node_name == "verification":
        #     verification = state[node_name]["verification"]
        #     print(f"   Результат верификации: {verification['verdict'].upper()}")
        #     print(f"   Оценки: Точность={verification['accuracy']}, Полнота={verification['completeness']}")
        #     print(f"   Фидбэк: {verification['feedback']}")
        # 
        # final_state = state
    
    # print("=" * 50)
    # print("📋 ФИНАЛЬНЫЙ ОТВЕТ:")
    # if final_state and "verification" in final_state:
    #     print(final_state["verification"].get("answer", "Нет ответа"))
    # 
    # return final_state

if __name__ == "__main__":
    # query = "Сколько будет 2 + 2"
    query = input()
    run_agent_system(query)
    # print("\n" + "="*60 + "\n")
