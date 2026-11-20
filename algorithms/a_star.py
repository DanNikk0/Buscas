import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = GOAL_STATE.index(tile)
            total += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        tie = count()
        frontier = [(self.heuristic(initial) + initial.cost, next(tie), initial)]
        best_cost = {initial.tiles: initial.cost}
        closed = set()

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.tiles in closed:
                continue
            if best_cost.get(current.tiles, current.cost) < current.cost:
                continue
            closed.add(current.tiles)
            result.nodes_expanded += 1

            if current.is_goal:
                result.solution = current
                result.depth = current.cost
                return result

            for child in current.neighbors():
                if child.tiles in closed:
                    continue
                known = best_cost.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_cost[child.tiles] = child.cost
                result.nodes_generated += 1
                heapq.heappush(frontier, (child.cost + self.heuristic(child), next(tie), child))

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
