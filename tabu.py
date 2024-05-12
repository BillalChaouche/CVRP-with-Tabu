import numpy as np
import random
import copy

class CVRP:
    def __init__(self, num_customers, num_vehicles, capacity, demands, distance_matrix):
        self.num_customers = num_customers
        self.num_vehicles = num_vehicles
        self.capacity = capacity
        self.demands = demands
        self.distance_matrix = distance_matrix
        self.tabu_list = []

    def initialize_solution(self):
        solution = []
        customers = list(range(1, self.num_customers))
        depot_node = self.num_customers  + 1
        random.shuffle(customers)
        chunks = [customers[i:i + self.num_customers//self.num_vehicles] for i in range(0, len(customers), self.num_customers//self.num_vehicles)]
    
        for i in range(self.num_vehicles):
            
            route = [0] + chunks[i] + [depot_node]  # Add depot at the beginning and additional depot at the end of each route
            solution.append(route)
        
        # Ensure each customer is visited exactly once
        remaining_customers = set(range(1, self.num_customers + 1))
        for route in solution:
            for customer in route[1:-1]:
                remaining_customers.remove(customer)
        for remaining_customer in remaining_customers:
            vehicle_idx = random.randint(0, self.num_vehicles - 1)
            solution[vehicle_idx].insert(-1, remaining_customer)

        return solution

    def calculate_cost(self, solution):
        total_cost = 0
        for route in solution:
            route_cost = 0
            if len(route) >= 2:
                for i in range(len(route) - 2):
                    route_cost += self.distance_matrix[route[i]][route[i+1]]
                total_cost += route_cost
        return total_cost

    def check_capacity_constraint(self, route):
        total_demand = sum(self.demands[node] for node in route[1:-1])
        return total_demand <= self.capacity

    def swap_customer(self, solution):
        print(solution)
        best_solution = copy.deepcopy(solution)
        best_delta = float('inf')
        for vehicle_idx1, route1 in enumerate(solution):
            for vehicle_idx2, route2 in enumerate(solution):
                if vehicle_idx1 != vehicle_idx2:  # Only swap between different vehicles
                    for i in range(1, len(route1) - 1):
                        for j in range(1, len(route2) - 1):
                            new_solution = copy.deepcopy(solution)
                            new_solution[vehicle_idx1][i], new_solution[vehicle_idx2][j] = new_solution[vehicle_idx2][j], new_solution[vehicle_idx1][i]
                            if self.check_capacity_constraint(new_solution[vehicle_idx1]) and self.check_capacity_constraint(new_solution[vehicle_idx2]):
                                cost_delta = self.calculate_cost(new_solution) - self.calculate_cost(solution)
                                if cost_delta < best_delta and new_solution not in self.tabu_list:
                                    best_delta = cost_delta
                                    best_solution = new_solution
        return best_solution

    def tabu_search(self, max_iter):
        #do while
        current_solution = self.initialize_solution()
        best_solution = current_solution
        for i in range(max_iter):
            current_solution = self.swap_customer(current_solution)
            current_cost = self.calculate_cost(current_solution)
            best_cost = self.calculate_cost(best_solution)
            if current_cost < best_cost:
                best_solution = current_solution
            if current_solution not in self.tabu_list or current_cost < best_cost:
                self.tabu_list.append(current_solution)
                if len(self.tabu_list) > 10:
                    self.tabu_list.pop(0)
        return best_solution


# Example usage
num_customers = 10
num_vehicles = 6
capacity = 100
demands =  [0, 5, 20, 10, 20, 85,65, 30, 20, 70, 30]
distance_matrix = np.array([
    [0,    13,  6,   55,  93, 164, 166, 168, 169, 241, 212],
    [13,    0,  11,  66, 261, 175, 177, 179, 180, 239, 208],
    [6,    11,   0,  60,  97, 168, 171, 173, 174, 239 ,209],
    [55,   66,  60,   0,  82, 113, 115, 117, 177, 295, 265],
    [93,  261,  97,  82,   0, 113, 115, 117, 118, 333, 302],
    [164, 175, 168, 113, 113,   0,   6,   7,   2, 403, 374],
    [166, 177, 171, 115, 115,   6,   0,   8,   7, 406, 376],
    [168, 179, 173, 117, 117,   4,   8,   0,   3, 408, 378],
    [169, 180, 174, 117, 118,   3,   7,   3,   0, 409, 379],
    [241, 239, 239, 295, 333, 403, 406, 408, 409,   0,  46],
    [212, 208, 209, 265, 302, 374, 376, 378, 379,  46,   0]
]) 

cvrp = CVRP(num_customers, num_vehicles, capacity, demands, distance_matrix)
best_solution = cvrp.tabu_search(max_iter=1000)
print("Best solution:", best_solution)
print("Cost of best solution:", cvrp.calculate_cost(best_solution))