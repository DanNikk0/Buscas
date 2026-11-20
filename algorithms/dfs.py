from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        frontier = [initial]
        best_depth = {initial.tiles: initial.cost}

        while frontier:
            current = frontier.pop()
            if best_depth.get(current.tiles, current.cost) < current.cost:
                continue
            result.nodes_expanded += 1

            if current.is_goal:
                result.solution = current
                result.depth = current.cost
                return result

            if current.cost >= self.depth_limit:
                continue

            for child in reversed(current.neighbors()):
                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                result.nodes_generated += 1
                frontier.append(child)

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
