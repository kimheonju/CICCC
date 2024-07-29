import random
import math

class DeliveryCompany:
    def __init__(self, cities, distances, temperature=10000, cooling_rate=0.003):
        self.cities = cities
        self.distances = distances
        self.temperature = temperature
        self.cooling_rate = cooling_rate

    def calculate_total_distance(self, route):
        # 총 거리를 계산합니다.
        route = route + [route[0]]  # 경로를 원형으로 만들어 총 거리를 계산합니다.
        return sum(self.distances[route[i]][route[i+1]] for i in range(len(route)-1))

    def generate_random_solution(self):
        # 도시 리스트를 무작위로 섞어 새로운 경로를 생성합니다.
        random.shuffle(self.cities)
        return self.cities[:]

    def acceptance_probability(self, current_distance, new_distance, temperature):
        # 새로운 경로의 거리가 더 짧으면 무조건 수용합니다.
        if new_distance < current_distance:
            return 1.0
        # 새로운 경로의 거리가 더 길면 확률적으로 수용합니다.
        else:
            return math.exp((current_distance - new_distance) / temperature)

    def simulated_annealing(self):
        # 초기 경로와 거리를 설정합니다.
        current_route = self.generate_random_solution()
        current_distance = self.calculate_total_distance(current_route)
        best_route = current_route
        best_distance = current_distance

        while self.temperature > 0.0001:
            # 새로운 경로를 생성합니다.
            new_route = self.generate_random_solution()
            new_distance = self.calculate_total_distance(new_route)

            # 새로운 경로를 수용할지 결정합니다.
            if self.acceptance_probability(current_distance, new_distance, self.temperature) > random.uniform(0, 1):
                current_route = new_route
                current_distance = new_distance

            # 최적 경로와 거리를 업데이트합니다.
            if new_distance < best_distance:
                best_route = new_route
                best_distance = new_distance

            # 온도를 감소시킵니다.
            self.temperature *= 1 - self.cooling_rate

        return best_route, best_distance

if __name__ == "__main__":
    cities = ["A", "B", "C", "D", "E"]
    distances = {
        "A": {"B": 10, "C": 15, "D": 20, "E": 25},
        "B": {"A": 10, "C": 12, "D": 18, "E": 22},
        "C": {"A": 15, "B": 12, "D": 14, "E": 16},
        "D": {"A": 20, "B": 18, "C": 14, "E": 10},
        "E": {"A": 25, "B": 22, "C": 16, "D": 10},
    }

    delivery_company = DeliveryCompany(cities, distances)
    optimal_route, total_distance = delivery_company.simulated_annealing()

    print("Optimal Route:", optimal_route)
    print("Total Distance:", total_distance)
